"""BPNRDE Field Test 2 — full-episode measures for the US (PROTOCOL section 5C).

For each US episode, measured over the WHOLE episode, from the price peak to the
month the S&P regains that peak (or data end), the same window used for Japan:
  - fall to the final low
  - unemployment rise to its peak
  - residential property prices: own peak to own trough within the episode
Run after backtest.py:  python3 -I code/full_episode.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
d = pd.read_csv(ROOT / "data/derived/monthly_panel.csv", parse_dates=["date"]).set_index("date")
bis = pd.read_csv(ROOT / "data/raw/us_property/QUSN628BIS.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
cs = pd.read_csv(ROOT / "data/raw/us_property/case_shiller_national_monthly.csv", parse_dates=["Date"]).set_index("Date")["National-US"]

PEAKS = {"1929": "1929-09-01", "1961": "1961-12-01", "1968": "1968-12-01", "1973": "1973-01-01",
         "1980": "1980-11-01", "1987": "1987-08-01", "2000": "2000-08-01", "2007": "2007-10-01",
         "2020": "2020-01-01", "2022": "2021-12-01"}
ORIGINAL = {"1929", "2000", "2007", "2020", "2022"}
sp = d["sp_nominal"]


def mo(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


def prop_move(series, start, end):
    s = series[(series.index >= start - pd.DateOffset(months=36)) & (series.index <= end)]
    if s.empty or s.index.min() > start:
        return None
    pk = s.idxmax()
    after = s[s.index >= pk]
    tr = after.idxmin()
    return pk, tr, (after.min() / s.max() - 1) * 100


rows = []
for ep, pk in PEAKS.items():
    pk = pd.Timestamp(pk)
    level = sp[pk]
    later = sp[sp.index > pk]
    rec = later[later >= level]
    end = rec.index[0] if not rec.empty else sp.index[-1]
    win = sp[(sp.index >= pk) & (sp.index <= end)]
    low = win.idxmin()
    row = {"episode": ep, "sample": "original" if ep in ORIGINAL else "out-of-sample",
           "peak": pk.strftime("%Y-%m"), "episode_end": end.strftime("%Y-%m") + ("" if not rec.empty else " (data end)"),
           "final_low": low.strftime("%Y-%m"), "fall_to_final_low_pct": round((win.min() / level - 1) * 100, 1)}
    u = d["unrate"][(d.index >= pk) & (d.index <= end)].dropna()
    if not u.empty and not np.isnan(d["unrate"].get(pk, np.nan)):
        row.update({"unrate_at_peak": d["unrate"][pk], "unrate_max": u.max(),
                    "unrate_max_month": u.idxmax().strftime("%Y-%m"),
                    "unrate_rise_to_max_pp": round(u.max() - d["unrate"][pk], 1)})
    else:
        row["unrate_note"] = "no monthly series: see manual 1929 row (+21.7 pp, 1929-1933 annual)" if ep == "1929" else "no FRED-MD coverage"
    for name, series in (("bis", bis), ("caseshiller", cs)):
        # (a) concurrent: property change from the price peak to the final price low
        if series.index.min() <= pk:
            row[f"prop_{name}_peak_to_low_pct"] = round((series.asof(low) / series.asof(pk) - 1) * 100, 1)
        # (b) worst property drawdown anywhere inside the episode window
        r = prop_move(series, pk, end)
        if r:
            row[f"prop_{name}_peak"], row[f"prop_{name}_trough"] = r[0].strftime("%Y-%m"), r[1].strftime("%Y-%m")
            row[f"prop_{name}_max_drawdown_pct"] = round(r[2], 1)
        else:
            row[f"prop_{name}_max_drawdown_pct"] = None
    rows.append(row)

res = pd.DataFrame(rows)
res.to_csv(OUT / "us_full_episode_measures.csv", index=False)
print(res.to_string(index=False))
