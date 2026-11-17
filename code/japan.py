"""BPNRDE Field Test 2 — Japan 1989 out-of-sample episode (PROTOCOL section 5B).

Same rules as backtest.py / extensions.py, adapted only where a US series has no
Japanese equivalent in the files (stated in the output and in PROTOCOL 5B).
Run:  python3 -I code/japan.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
J = ROOT / "data/raw/japan"
OUT = ROOT / "outputs"

m = pd.read_csv(J / "jp_macro_monthly_dissrepl.csv", parse_dates=["date"]).set_index("date")
credit = pd.read_csv(J / "QJPPAM770A.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
prop = pd.read_csv(J / "QJPN628BIS.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
daily = pd.read_csv(J / "nikkei225_daily_1970_2015.csv")
daily["Date"] = pd.to_datetime(daily["Date"])

nk = m["n225"].dropna()

# Cross-check the two Nikkei sources (monthly mean of daily file vs monthly file)
dm = daily.set_index("Date")["Price"].resample("MS").mean()
both = pd.concat([nk, dm], axis=1, join="inner").dropna()
xdiff = ((both.iloc[:, 0] / both.iloc[:, 1] - 1).abs() * 100)

# Episode selection (as extensions.py C): drawdown >= 19% from running all-time high
p = nk.values
ath = np.maximum.accumulate(p)
dd = p / ath - 1
i_trough = int(np.argmin(dd))
i_peak = int(np.argmax(p[:i_trough + 1]))
peak, trough = nk.index[i_peak], nk.index[i_trough]
later = nk[nk.index > trough]
rec = later[later >= p[i_peak]]
recovery = rec.index[0] if not rec.empty else None
# first trough within 36 months (comparable with US rule 4.2 windows)
w36 = nk[(nk.index >= peak) & (nk.index <= peak + pd.DateOffset(months=36))]

# Breaking Point, rate channel (descriptive): first hike and max policy rate up to peak+12
pol = m["policy"].dropna()
pre = pol[(pol.index >= peak - pd.DateOffset(months=24)) & (pol.index <= peak + pd.DateOffset(months=12))]
first_hike = pre[pre.diff() > 0].index.min()
rate_peak = pre.idxmax()

# Breaking Point, credit-inflow channel: peak 4-quarter change in credit/GDP, [peak-36, peak+12]
cg = credit.diff(4)
cw = cg[(cg.index >= peak - pd.DateOffset(months=36)) & (cg.index <= peak + pd.DateOffset(months=12))]
bp_credit = cw.idxmax()

# Property: peak and fall (the "credit branch" asset; no technology ratchet expected)
prop_peak = prop.idxmax()
prop_trough = prop[prop.index > prop_peak].idxmin()

# Dominoes: unemployment
ur = m["ur"].dropna()
u0 = ur.asof(peak)
u36 = ur[(ur.index >= peak) & (ur.index <= peak + pd.DateOffset(months=36))].max()
u_max = ur[(ur.index >= peak) & (ur.index <= trough)]

man = pd.read_csv(ROOT / "data/manual/episode_events_manual.csv", dtype={"episode": str})
pnr = pd.Timestamp(man[(man.episode == "japan1989") & (man.event == "pnr")]["date"].iloc[0])


def mo(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


res = {
    "nikkei_cross_check_max_abs_diff_pct": round(xdiff.max(), 2),
    "peak": peak.strftime("%Y-%m"), "peak_level": round(p[i_peak], 0),
    "trough_36m": w36.idxmin().strftime("%Y-%m"),
    "drawdown_36m_pct": round((w36.min() / p[i_peak] - 1) * 100, 1),
    "trough_full": trough.strftime("%Y-%m"),
    "drawdown_full_pct": round(dd[i_trough] * 100, 1),
    "recovery_to_peak": recovery.strftime("%Y-%m") if recovery is not None else "not by data end",
    "peak_to_recovery_months": mo(peak, recovery) if recovery is not None else None,
    "first_rate_hike": first_hike.strftime("%Y-%m"),
    "rate_peak_month": rate_peak.strftime("%Y-%m"), "rate_peak_pct": pre.max(),
    "bp_credit_quarter": bp_credit.strftime("%Y-%m"),
    "P2_inflow_before_price": bool(bp_credit <= peak),
    "property_peak": prop_peak.strftime("%Y-%m"), "property_trough": prop_trough.strftime("%Y-%m"),
    "property_fall_pct": round((prop[prop_trough] / prop[prop_peak] - 1) * 100, 1),
    "pnr_manual_VERIFY": pnr.strftime("%Y-%m"),
    "peak_to_pnr_months": mo(peak, pnr),
    "tau_rate_peak_to_pnr_months": mo(rate_peak, pnr),
    "unrate_at_peak": u0, "unrate_rise_36m_pp": round(u36 - u0, 1),
    "unrate_max_to_full_trough": u_max.max(), "unrate_max_month": u_max.idxmax().strftime("%Y-%m"),
    "unrate_rise_to_max_pp": round(u_max.max() - u0, 1),
}
pd.Series(res).to_csv(OUT / "japan_1989_results.csv", header=["value"])
for k, v in res.items():
    print(f"{k:38s} {v}")
