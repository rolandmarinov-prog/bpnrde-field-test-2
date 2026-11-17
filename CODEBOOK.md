# Codebook

## data/derived/monthly_panel.csv (monthly, first of month)
| Column | Meaning | Source |
|---|---|---|
| sp_nominal | S&P composite, monthly average, nominal | Shiller |
| cape | Cyclically adjusted P/E (blank where the source reports 0) | Shiller |
| long_rate | 10-year Treasury yield | Shiller |
| fedfunds | Effective Fed funds rate, % | FRED-MD FEDFUNDS |
| baa, aaa | Moody's Baa and Aaa corporate yields, % | FRED-MD |
| credit_spread | baa − aaa, percentage points | derived |
| gs10 | 10-year Treasury, % | FRED-MD |
| unrate | Unemployment rate, % | FRED-MD UNRATE |
| busloans, realln, nonrevsl | Commercial and industrial loans, real estate loans, nonrevolving consumer credit | FRED-MD |
| loans_total | busloans + realln + nonrevsl | derived |
| loans_yoy | 12-month % change in loans_total | derived |
| payems | Nonfarm payrolls | FRED-MD |

## outputs/backtest_results.csv
| Column | Meaning |
|---|---|
| peak, trough | Rule 4.2 |
| drawdown_pct | trough / peak − 1 |
| bp_rate | Rule 4.3, rate channel (descriptive only) |
| bp_credit | Rule 4.3, credit-inflow channel |
| pnr | Rule 4.4, first spread breach |
| pnr_persistent_v1_posthoc | Six-month persistent breach (post-hoc; see PROTOCOL 7) |
| tau_months_bp_rate_to_pnr | Months from bp_rate to pnr |
| peak_to_pnr_months | Months from peak to pnr |
| P2_inflow_before_price | bp_credit ≤ peak |
| unrate_rise_pp, unrate_peak | Rule 4.5 |
| lag_trough_to_unrate_peak_m | Months from price trough to the unemployment peak |
| credit_spread_max_pp | Maximum spread within 36 months of the peak |
| recovery_to_peak, peak_to_recovery_months | Rule 4.6 |

## data/manual
Every row carries `source_to_check` and `verified`. A row counts toward v1.0 only once `verified=yes`.
