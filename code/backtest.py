"""BPNRDE Field Test 2 — back-test of the bubble-cycle model.

Every event date below is produced by a rule fixed in PROTOCOL.md section 4.
No date is chosen by hand, except where a series does not exist for an
episode (1929); those rows are taken from data/manual/ and flagged.

Run:  python3 -I code/backtest.py   (from the package root)
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW, MAN, DER, OUT = (ROOT / p for p in ("data/raw", "data/manual", "data/derived", "outputs"))

# ---------- 1. Build the monthly panel ----------
sh = pd.read_csv(RAW / "shiller_sp500_monthly.csv", parse_dates=["Date"])
sh = sh.rename(columns={"Date": "date", "SP500": "sp_nominal", "PE10": "cape",
                        "Long Interest Rate": "long_rate"})
sh = sh[["date", "sp_nominal", "cape", "long_rate"]]
sh.loc[sh["cape"] == 0, "cape"] = np.nan
sh.loc[sh["long_rate"] == 0, "long_rate"] = np.nan

fm = pd.read_csv(RAW / "fredmd_2024-09.csv")
fm = fm.iloc[1:].copy()                      # row 0 holds transformation codes
fm["date"] = pd.to_datetime(fm["sasdate"], format="%m/%d/%Y")
keep = {"FEDFUNDS": "fedfunds", "BAA": "baa", "AAA": "aaa", "GS10": "gs10",
        "UNRATE": "unrate", "BUSLOANS": "busloans", "REALLN": "realln",
        "NONREVSL": "nonrevsl", "PAYEMS": "payems"}
fm = fm[["date", *keep]].rename(columns=keep)
for c in keep.values():
    fm[c] = pd.to_numeric(fm[c], errors="coerce")
fm["credit_spread"] = fm["baa"] - fm["aaa"]
fm["loans_total"] = fm["busloans"] + fm["realln"] + fm["nonrevsl"]
fm["loans_yoy"] = fm["loans_total"].pct_change(12, fill_method=None) * 100

panel = sh.merge(fm, on="date", how="left").sort_values("date").reset_index(drop=True)
panel.to_csv(DER / "monthly_panel.csv", index=False)

# ---------- 2. Episodes (search windows fixed in PROTOCOL 4.1) ----------
EPISODES = {
    "1929": ("1927-01-01", "1932-12-01"),
    "2000": ("1998-01-01", "2003-12-01"),
    "2007": ("2006-01-01", "2009-12-01"),
    "2020": ("2019-06-01", "2020-12-01"),
    "2022": ("2021-01-01", "2023-06-01"),
}
manual = pd.read_csv(MAN / "episode_events_manual.csv", dtype={"episode": str})


def months(a, b):
    return None if a is None or b is None else (b.year - a.year) * 12 + (b.month - a.month)


def first_where(df, mask):
    hit = df.loc[mask, "date"]
    return None if hit.empty else hit.iloc[0]


rows = []
for ep, (w0, w1) in EPISODES.items():
    w = panel[(panel.date >= w0) & (panel.date <= w1)]
    # 4.2 peak and trough (nominal monthly average)
    # trough = lowest month in the window; peak = highest month before that trough
    trough = w.loc[w.sp_nominal.idxmin()]
    before = w[w.date < trough.date]
    peak = before.loc[before.sp_nominal.idxmax()]
    drawdown = trough.sp_nominal / peak.sp_nominal - 1
    # 4.6 recovery: first month nominal price >= peak again
    later = panel[panel.date > trough.date]
    rec = first_where(later, later.sp_nominal >= peak.sp_nominal)

    pre = panel[(panel.date >= peak.date - pd.DateOffset(months=36)) &
                (panel.date <= peak.date + pd.DateOffset(months=12))]
    has_fred = pre["fedfunds"].notna().any()
    m = manual[manual.episode == ep].set_index("event")["date"].to_dict() if not has_fred else {}

    if has_fred:
        # 4.3 Breaking Point, rate channel: max Fed funds in the 24 months up to the peak
        r = panel[(panel.date >= peak.date - pd.DateOffset(months=24)) & (panel.date <= peak.date)]
        bp_rate = r.loc[r.fedfunds.idxmax(), "date"]
        # 4.3 Breaking Point, credit-inflow channel: peak YoY loan growth in [peak-36, peak+12]
        bp_credit = pre.loc[pre.loans_yoy.idxmax(), "date"]
        # 4.4 Point of No Return: spread > trailing-60m mean + 2 SD, first month after peak
        s = panel[["date", "credit_spread"]].copy()
        s["mu"] = s.credit_spread.rolling(60).mean().shift(1)
        s["sd"] = s.credit_spread.rolling(60).std().shift(1)
        win = s[(s.date > peak.date) & (s.date <= peak.date + pd.DateOffset(months=36))]
        pnr = first_where(win, win.credit_spread > win.mu + 2 * win.sd)
        # POST-HOC variant (logged in PROTOCOL 7): breach must persist 6 consecutive months
        brk = (win.credit_spread > win.mu + 2 * win.sd).astype(int)
        run = brk.groupby((brk != brk.shift()).cumsum()).cumsum() * brk
        hit = win.loc[run.values >= 6, "date"]
        pnr_persist = None if hit.empty else hit.iloc[0] - pd.DateOffset(months=5)
        # 4.5 Domino proxies
        dom = panel[(panel.date >= peak.date) & (panel.date <= peak.date + pd.DateOffset(months=36))]
        u0 = panel.loc[panel.date == peak.date, "unrate"].iloc[0]
        u_peak_row = dom.loc[dom.unrate.idxmax()]
        du = u_peak_row.unrate - u0
        u_peak = u_peak_row.date
        spread_max = dom.credit_spread.max()
        src = "rule (FRED-MD 2024-09 vintage)"
    else:
        to_ts = lambda k: pd.Timestamp(m[k]) if isinstance(m.get(k), str) and m[k] else None
        bp_rate, bp_credit, pnr, u_peak = (to_ts(k) for k in ("bp_rate", "bp_credit", "pnr", "unrate_peak"))
        du = float(manual[(manual.episode == ep) & (manual.event == "unrate_rise_pp")]["value"].iloc[0])
        spread_max = np.nan
        src = "manual - data/manual - VERIFY"
        pnr_persist = pnr

    rows.append({
        "episode": ep, "source": src,
        "peak": peak.date.date(), "trough": trough.date.date(),
        "drawdown_pct": round(drawdown * 100, 1),
        "bp_rate": bp_rate.date() if bp_rate is not None else None,
        "bp_credit": bp_credit.date() if bp_credit is not None else None,
        "pnr": pnr.date() if pnr is not None else "not reached",
        "tau_months_bp_rate_to_pnr": months(bp_rate, pnr),
        "peak_to_pnr_months": months(peak.date, pnr),
        # P2 uses the credit channel only: bp_rate is <= peak by construction (4.3)
        "P2_inflow_before_price": None if bp_credit is None else bool(bp_credit <= peak.date),
        "pnr_persistent_v1_posthoc": pnr_persist.date() if pnr_persist is not None else "not reached",
        "unrate_rise_pp": round(du, 1) if du == du else None,
        "unrate_peak": u_peak.date() if u_peak is not None else None,
        "lag_trough_to_unrate_peak_m": months(trough.date, u_peak),
        "credit_spread_max_pp": round(spread_max, 2) if spread_max == spread_max else None,
        "recovery_to_peak": rec.date() if rec is not None else "not by data end",
        "peak_to_recovery_months": months(peak.date, rec),
    })

res = pd.DataFrame(rows)
res.to_csv(OUT / "backtest_results.csv", index=False)

# ---------- 3. Ratchet test (PROTOCOL 4.7) ----------
ad = pd.read_csv(MAN / "adoption_annual.csv", dtype={"episode": str})
rat = []
for ep, g in ad.groupby("episode"):
    r = res[res.episode == ep].iloc[0]
    py, ty = pd.Timestamp(r.peak).year, pd.Timestamp(r.trough).year
    for series, h in g.groupby("series"):
        a0 = h[h.year < py].sort_values("year").tail(1)     # last year strictly before the peak year
        a1 = h[h.year > ty].sort_values("year").head(1)     # first year strictly after the trough year
        if a0.empty or a1.empty:
            continue
        rat.append({"episode": ep, "series": series,
                    "year_before_peak": int(a0.year.iloc[0]), "value_0": float(a0.value.iloc[0]),
                    "year_after_trough": int(a1.year.iloc[0]), "value_1": float(a1.value.iloc[0]),
                    "ratchet_held": bool(a1.value.iloc[0] >= a0.value.iloc[0]),
                    "verified": h.verified.iloc[0]})
pd.DataFrame(rat).to_csv(OUT / "ratchet_results.csv", index=False)

print(res.to_string(index=False))
print()
print(pd.DataFrame(rat).to_string(index=False))
