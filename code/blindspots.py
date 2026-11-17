"""BPNRDE Field Test 2 — blind-spot runs (PROTOCOL section 5D).

1. Real (inflation-adjusted) falls and recoveries for every US episode.
2. Bubble-asset view: residential property in real terms (BIS) for US, Japan, Canada.
3. Canada: TSX episodes by the same >=19% rule; real house-price drawdowns; unemployment.
Run after backtest.py:  python3 -I code/blindspots.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "data/raw", ROOT / "outputs"


def mo(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


# ---------- 1. Real terms, US ----------
sh = pd.read_csv(RAW / "shiller_sp500_monthly.csv", parse_dates=["Date"]).set_index("Date")
nom, real = sh["SP500"], sh["Real Price"].where(sh["Real Price"] > 0).dropna()
PEAKS = {"1929": "1929-09-01", "1961": "1961-12-01", "1968": "1968-12-01", "1973": "1973-01-01",
         "1980": "1980-11-01", "1987": "1987-08-01", "2000": "2000-08-01", "2007": "2007-10-01",
         "2020": "2020-01-01", "2022": "2021-12-01"}


def episode(series, pk):
    lvl = series[pk]
    after = series[series.index > pk]
    rec = after[after >= lvl]
    end = rec.index[0] if not rec.empty else series.index[-1]
    w = series[(series.index >= pk) & (series.index <= end)]
    return (w.min() / lvl - 1) * 100, (mo(pk, rec.index[0]) if not rec.empty else None), w.idxmin()


rows = []
for ep, pk in PEAKS.items():
    pk = pd.Timestamp(pk)
    # real peak: highest real month within +/-6 months of the nominal peak
    rw = real[(real.index >= pk - pd.DateOffset(months=6)) & (real.index <= pk + pd.DateOffset(months=6))]
    rpk = rw.idxmax()
    nf, nm, _ = episode(nom, pk)
    rf, rm, rlow = episode(real, rpk)
    rows.append({"episode": ep, "nominal_peak": pk.strftime("%Y-%m"), "nominal_fall_pct": round(nf, 1),
                 "nominal_months_to_recover": nm, "real_peak": rpk.strftime("%Y-%m"),
                 "real_fall_pct": round(rf, 1), "real_low": rlow.strftime("%Y-%m"),
                 "real_months_to_recover": rm if rm is not None else "not by data end"})
realtab = pd.DataFrame(rows)
realtab.to_csv(OUT / "us_real_terms.csv", index=False)

# ---------- 2/3. BIS property, real, for US / JP / CA ----------
spp = pd.read_csv(RAW / "bis/bis_selected_property_prices_WS_SPP.csv")
qcols = [c for c in spp.columns if c[:4].isdigit() and "-Q" in c]


def bis_series(area, value="R", unit=628):
    r = spp[(spp.REF_AREA == area) & (spp.VALUE == value) & (spp.UNIT_MEASURE == unit)]
    s = pd.to_numeric(r[qcols].iloc[0], errors="coerce").dropna()
    s.index = pd.PeriodIndex(s.index, freq="Q").to_timestamp()
    return s


def drawdowns(s, threshold=-10.0):
    """Every drawdown of at least `threshold` % from a running high, ended by a new high."""
    out, ath, in_dd, pk = [], -np.inf, False, None
    vals = list(s.items())
    for i, (t, v) in enumerate(vals):
        if v >= ath:
            if in_dd:
                seg = s[(s.index >= pk) & (s.index < t)]
                fall = (seg.min() / s[pk] - 1) * 100
                if fall <= threshold:
                    out.append((pk, seg.idxmin(), fall, t))
                in_dd = False
            ath, pk = v, t
        else:
            in_dd = True
    if in_dd:
        seg = s[s.index >= pk]
        fall = (seg.min() / s[pk] - 1) * 100
        if fall <= threshold:
            out.append((pk, seg.idxmin(), fall, None))
    return out


prop_rows = []
for area, name in (("US", "United States"), ("JP", "Japan"), ("CA", "Canada")):
    s = bis_series(area)
    for pk, tr, fall, back in drawdowns(s):
        prop_rows.append({"country": name, "real_peak": pk.strftime("%Y-Q") + str((pk.month - 1) // 3 + 1),
                          "real_trough": tr.strftime("%Y-Q") + str((tr.month - 1) // 3 + 1),
                          "real_fall_pct": round(fall, 1),
                          "back_to_peak": (back.strftime("%Y-Q") + str((back.month - 1) // 3 + 1)) if back is not None else f"not by data end ({s.index[-1].year})",
                          "quarters_to_recover": (len(s[(s.index > pk) & (s.index <= back)]) if back is not None else None)})
proptab = pd.DataFrame(prop_rows)
proptab.to_csv(OUT / "property_real_drawdowns_US_JP_CA.csv", index=False)

# ---------- 3. Canada: TSX episodes and unemployment ----------
tsx = pd.read_csv(RAW / "canada/GSPTSE_monthly.csv", parse_dates=["Date"]).set_index("Date").iloc[:, 0].dropna()
ur = pd.read_csv(RAW / "canada/LRUNTTTTCAM156S_unemployment.csv", parse_dates=["Date"]).set_index("Date").iloc[:, 0]
p = tsx.values
ath = np.maximum.accumulate(p)
dd = p / ath - 1
ca, in_ep = [], False
for i in range(len(p)):
    if dd[i] < 0 and not in_ep:
        in_ep, s0 = True, i
    if in_ep and (dd[i] == 0 or i == len(p) - 1):
        lo = s0 + int(np.argmin(dd[s0:i + 1]))
        if dd[lo] <= -0.19:
            pk, tr = tsx.index[s0 - 1], tsx.index[lo]
            back = tsx.index[i] if dd[i] == 0 else None
            u = ur[(ur.index >= pk) & (ur.index <= (back or ur.index[-1]))]
            ca.append({"tsx_peak": pk.strftime("%Y-%m"), "tsx_trough": tr.strftime("%Y-%m"),
                       "fall_pct": round(dd[lo] * 100, 1),
                       "back_to_peak": back.strftime("%Y-%m") if back is not None else "not by data end",
                       "months_to_recover": mo(pk, back) if back is not None else None,
                       "unrate_at_peak": ur.asof(pk), "unrate_max": u.max() if not u.empty else None,
                       "unrate_rise_pp": round(u.max() - ur.asof(pk), 1) if not u.empty else None})
        in_ep = False
catab = pd.DataFrame(ca)
catab.to_csv(OUT / "canada_tsx_episodes.csv", index=False)

for t, x in (("1. US real terms", realtab), ("2. Real property drawdowns >=10% (BIS)", proptab),
             ("3. Canada TSX episodes >=19%", catab)):
    print("\n" + t); print(x.to_string(index=False))
