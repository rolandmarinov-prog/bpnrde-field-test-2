"""BPNRDE Field Test 2 — evidence-hardening runs (PROTOCOL section 5A).

Uses the panel built by backtest.py and the SAME rules (4.2–4.6), unchanged.
Run after backtest.py:  python3 -I code/extensions.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
d = pd.read_csv(ROOT / "data/derived/monthly_panel.csv", parse_dates=["date"])
p = d.sp_nominal.values
H = 13  # forward-test window length in months

# ---------- A. Base rates for H1b ----------
n = len(p) - H
hit = pd.Series([p[i + 1:i + 1 + H].min() / p[i] <= 0.8 for i in range(n)], index=d.date[:n])
cape = d.cape.iloc[:n].values
top = np.nanpercentile(cape, 90)
base = pd.DataFrame([
    {"sample": "1871-2025, all months", "months": len(hit), "rate_pct": hit.mean() * 100},
    {"sample": "1950-2025, all months", "months": int((hit.index >= "1950").sum()),
     "rate_pct": hit[hit.index >= "1950"].mean() * 100},
    {"sample": f"CAPE in top decile (>= {top:.1f})", "months": int((cape >= top).sum()),
     "rate_pct": hit[cape >= top].mean() * 100},
]).round(1)
base.to_csv(OUT / "base_rates_H1b.csv", index=False)

# ---------- B. PNR-rule false-positive scan, 1964-2024 ----------
f = d.dropna(subset=["credit_spread"]).copy()
f["mu"] = f.credit_spread.rolling(60).mean().shift(1)
f["sd"] = f.credit_spread.rolling(60).std().shift(1)
f["br"] = f.credit_spread > f.mu + 2 * f.sd
f = f.dropna(subset=["mu"])
run_id = (f.br != f.br.shift()).cumsum()
fp = []
for _, g in f[f.br].groupby(run_id[f.br]):
    start = g.date.iloc[0]
    # outcome: worst S&P fall from the start month over the next 24 months
    w = d[(d.date >= start) & (d.date <= start + pd.DateOffset(months=24))]
    fall = w.sp_nominal.min() / w.sp_nominal.iloc[0] - 1
    # outcome 2: worst fall measured from the prior 12-month high
    w0 = d[(d.date >= start - pd.DateOffset(months=12)) & (d.date <= start)]
    fall_from_high = w.sp_nominal.min() / w0.sp_nominal.max() - 1
    fp.append({"breach_start": start.strftime("%Y-%m"), "months_in_breach": len(g),
               "persistent_6m": len(g) >= 6,
               "fall_next_24m_pct": round(fall * 100, 1),
               "fall_from_prior_12m_high_pct": round(fall_from_high * 100, 1),
               "bear_20pct_from_high": fall_from_high <= -0.2})
fp = pd.DataFrame(fp)
fp.to_csv(OUT / "pnr_rule_scan.csv", index=False)

# ---------- C. Out-of-sample: every episode the rule selects, 1964-2024 ----------
# Selection rule (fixed): a monthly-average drawdown of >= 19% from the running all-time
# high, separated from the next by a new all-time high. 19% matches the smallest
# drawdown in the original sample (2020, -19.1%).
ath = np.maximum.accumulate(p)
dd = p / ath - 1
eps, in_ep = [], False
for i in range(len(p)):
    if dd[i] < 0 and not in_ep:
        in_ep, s = True, i
    if in_ep and dd[i] == 0:
        seg = slice(s, i)
        lo = s + int(np.argmin(dd[seg]))
        if dd[lo] <= -0.19:
            eps.append((s - 1, lo))
        in_ep = False
seen = {"2000-08", "2007-10", "2020-01", "2021-12", "1929-09"}


def episode(pk, tr):
    peak, trough = d.iloc[pk], d.iloc[tr]
    row = {"peak": peak.date.strftime("%Y-%m"), "trough": trough.date.strftime("%Y-%m"),
           "drawdown_pct": round((trough.sp_nominal / peak.sp_nominal - 1) * 100, 1)}
    row["in_original_sample"] = row["peak"] in seen
    pre = d[(d.date >= peak.date - pd.DateOffset(months=36)) & (d.date <= peak.date + pd.DateOffset(months=12))]
    if pre.loans_yoy.notna().sum() < 12 or f[f.date <= peak.date].empty:
        row["note"] = "no FRED-MD coverage: price only"
        return row
    bpc = pre.loc[pre.loans_yoy.idxmax(), "date"]
    row["bp_credit"] = bpc.strftime("%Y-%m")
    row["P2_inflow_before_price"] = bool(bpc <= peak.date)
    win = f[(f.date > peak.date) & (f.date <= peak.date + pd.DateOffset(months=36))]
    first = win.loc[win.br, "date"]
    row["pnr"] = first.iloc[0].strftime("%Y-%m") if not first.empty else "not reached"
    brk = win.br.astype(int)
    run = brk.groupby((brk != brk.shift()).cumsum()).cumsum() * brk
    pers = win.loc[run.values >= 6, "date"]
    row["pnr_persistent_6m"] = (pers.iloc[0] - pd.DateOffset(months=5)).strftime("%Y-%m") if not pers.empty else "not reached"
    dom = d[(d.date >= peak.date) & (d.date <= peak.date + pd.DateOffset(months=36))]
    row["unrate_rise_pp"] = round(dom.unrate.max() - peak.unrate, 1)
    return row


oos = pd.DataFrame([episode(a, b) for a, b in eps if d.iloc[a].date.year >= 1930])
oos.to_csv(OUT / "out_of_sample_episodes.csv", index=False)

# ---------- D. Booms that did not burst ----------
quiet = []
for name, a, b in [("1995-97 run-up", "1995-01-01", "1997-12-01"),
                   ("2013-14 run-up", "2013-01-01", "2014-12-01"),
                   ("2017 run-up", "2017-01-01", "2017-12-01")]:
    w = f[(f.date >= a) & (f.date <= b)]
    nxt = d[(d.date > b) & (d.date <= pd.Timestamp(b) + pd.DateOffset(months=24))]
    quiet.append({"period": name,
                  "price_gain_pct": round((d[d.date == b].sp_nominal.iloc[0] / d[d.date == a].sp_nominal.iloc[0] - 1) * 100, 1),
                  "pnr_breach_inside_period": bool(w.br.any()),
                  "worst_fall_next_24m_pct": round((nxt.sp_nominal.min() / d[d.date == b].sp_nominal.iloc[0] - 1) * 100, 1)})
quiet = pd.DataFrame(quiet)
quiet.to_csv(OUT / "non_burst_booms.csv", index=False)

for t, x in [("A. H1b base rates", base), ("B. PNR rule scan", fp),
             ("C. Out-of-sample episodes", oos), ("D. Booms that did not burst", quiet)]:
    print("\n" + t); print(x.to_string(index=False))
