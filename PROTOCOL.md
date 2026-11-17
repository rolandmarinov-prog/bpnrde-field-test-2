# BPNRDE Field Test 2: The Bubble Cycle

**Status:** v1.0 registration candidate. Not registered until the PI publishes it with sections 6 and 6.1 filled in.
**Principal investigator:** Roland Marinov
**Prepared with:** CAM (Claude). Event log: to be assigned.
**Registration:** becomes v1.0 when the PI publishes this file, with section 6.1 filled in, on 369369369.org, commits it to a public repository and archives both. The observation window opens at that commit.

> **Disclosure.** The forward test concerns a market cycle that includes the Anthropic IPO. Anthropic makes Claude, which co-drafted this protocol, so the drafter has an interest in the outcome. For that reason, every decision in section 6 is the PI's alone, and the PI gives no probability forecasts (6.2). Every outcome is resolved from public data by the rules in section 6, not by judgment.

---

## 1. Question

Does the BPNRDE bubble-cycle model describe how speculative booms end? The model's phases are:

1. Boom
2. Breaking Point
3. Point of No Return, after a human delay τ
4. Domino effect
5. Reset, with an adoption ratchet

The question is whether the model **predicts** the current cycle, not just whether it fits the past.

## 2. Model (from the 8 Nov 2026 working session)

- **Adoption:** A(t) is an S-curve. Once A ≥ A\*, it ratchets: dA/dt ≥ 0 regardless of prices.
- **Financing gap:** G = C − R, where R = A·N·p.
- **Capital inflow:** I = I₀·e^(γ·m), where m is valuation momentum.
- **Breaking Point (T_BP):** the first t at which I = G while I − G is falling.
- **Point of No Return:** T_NR = T_BP + τ, when the loop gain γμ ≥ 1.
- **Domino effect:** a node *i* falls when L_i = Σ w_ij·loss_j(t − d_ij) exceeds its buffer b_i. The cascade spreads when R_D > 1.
- **Reset:** recovery begins when A·N·p > C_reset.

The parameters are **not estimated**. This test checks the model's structure and the order of its phases, not its magnitudes.

## 2A. Shocks (proposed 8 Nov 2026, not adopted for the forward test)

A shock is a jump at time t₀:

- **Price:** V(t₀⁺) = V(t₀⁻)·(1 − J), where J is the jump size.
- **Inflow:** I(t) = I₀·e^(γ·m(t))·(1 − s(t)), with a confidence hit s(t) = s₀·e^(−λ(t − t₀)). Fast decay λ looks like 2020; slow decay looks like 1929.
- **Dominoes:** the first loss lands on node k, loss_k(t₀) = J·exposure_k, then spreads through w_ij as in section 2.

**Fragility:** Φ = (c·g)/M
- c is the concentration on the node hit.
- g = γμ is the loop gain.
- M = (I − G)/G is the financing margin before the Breaking Point.

**Rule:** a shock produces a crash when **J·Φ > 1**, and a dip otherwise. The shock is the trigger; fragility sets the size.

**Shock types:** exogenous (a virus); policy (rates, regulation, forced divestiture); single node (a key firm or person); geopolitical (export controls, Taiwan).

**Qualitative fit:**
- 1987: large J, low c, little credit, so no dominoes.
- 2020: very large J, but λ was fast because of policy, so a quick recovery.
- 2008: a moderate J (Lehman) with M near zero, so a crash.

**Not estimated.** Φ needs measured c, g and M. A candidate for Field Test 3.

## 3. Data

| File | Content | Source | Status |
|---|---|---|---|
| `data/raw/shiller_sp500_monthly.csv` | S&P composite monthly averages, 1871–Sep 2026 | Shiller, via github.com/datasets/s-and-p-500 | Pulled 8 Nov 2026; SHA-256 in `outputs/SHA256SUMS_raw.txt` |
| `data/raw/fredmd_2024-09.csv` | FRED-MD 2024-09 vintage, 1959–Aug 2024 | McCracken & Ng / St. Louis Fed, via the github.com/hoanguc3m/MFVART mirror | Pulled 8 Nov 2026. **A mirror, not the official file**: verify against research.stlouisfed.org/econ/mccracken/fred-databases before v1.0 |
| `data/manual/*.csv` | 1929 events, adoption series, IPO counts | Sources named per row | **Unverified (`verified=no`) unless marked otherwise.** Two 1929 rows (the rate rise and the credit peak) were checked against the Federal Reserve Bulletin on 13 Nov 2026 and marked `verified=yes` (section 7, item 11). The rest were entered from standard references and remain unverified. |

## 4. Back-test rules (fixed before running)

**4.1 Episodes and search windows**
- 1929: Jan 1927 – Dec 1932
- 2000: Jan 1998 – Dec 2003
- 2007: Jan 2006 – Dec 2009
- 2020: Jun 2019 – Dec 2020
- 2022: Jan 2021 – Jun 2023

**4.2 Peak and trough.** The trough is the lowest S&P monthly average in the window. The peak is the highest monthly average before the trough.

**4.3 Breaking Point.**
- *Rate channel:* the month of maximum Fed funds rate in the 24 months up to the peak. Because this window ends at the peak, the date is always at or before the peak. It is therefore **descriptive only** and is not used to test P2.
- *Credit-inflow channel:* the month of peak year-on-year growth in BUSLOANS + REALLN + NONREVSL, searched from 36 months before the peak to 12 months after it.

**4.4 Point of No Return (proxy).** The first month after the peak in which the BAA−AAA spread exceeds its trailing 60-month mean plus 2 standard deviations, within 36 months of the peak.

**4.5 Domino proxies.** The rise in unemployment from the peak to its maximum within 36 months, and the maximum BAA−AAA spread.

**4.6 Recovery.** The first month the S&P monthly average regains the peak level (nominal).

**4.7 Ratchet.** The adoption value in the last year before the peak year, compared with the first year after the trough year. The ratchet holds if the later value is at least as high.

## 5. Back-test results (v0, exploratory)

Run with `python3 -I code/backtest.py`. Full output is in `outputs/backtest_results.csv` and `outputs/ratchet_results.csv`.

| Episode | Peak → trough | Fall | P2: credit inflow peaks before price | PNR (proxy) | Peak → PNR | Unemployment rise | Recovery |
|---|---|---|---|---|---|---|---|
| 1929\* | Sep 1929 → Jun 1932 | −84.8% | **Yes, same month, no lead** (Sep 1929; corrected 13 Nov 2026 from Oct 1929, see section 7, item 11) | Dec 1930 | 15 m | +21.7 pp | 300 m |
| 2000 | Aug 2000 → Feb 2003 | −43.7% | Yes (Jul 2000) | Dec 2001 | 16 m | +2.2 pp | 81 m |
| 2007 | Oct 2007 → Mar 2009 | −50.8% | Yes (Aug 2005) | Jan 2008 | 3 m | +5.3 pp | 65 m |
| 2020 | Jan 2020 → Mar 2020 | −19.1% | No (May 2020; PPP lending) | Apr 2020, reversed | 3 m | +11.2 pp | 7 m |
| 2022 | Dec 2021 → Oct 2022 | −20.3% | **Not usable**: the search window reaches back to the May 2020 PPP lending surge, the same spike that makes 2020 fail | not reached | — | +0.4 pp | 24 m |

\*1929 events come from manual rows. The rate rise (Aug 1929) and the credit peak (Sep 1929) are verified against the Federal Reserve Bulletin; the PNR date (Dec 1930) is still unverified.

**Ratchet (prediction P1):**
- Held: 2000 (internet use 35.8% → 64.8%), 2020 and 2022 (e-commerce share).
- **Failed:** 2007 (homeownership 68.8% → 66.9%).
- 1929: insufficient data (no pre-1930 radio figure).

**What the back-test shows:**
1. **The ratchet holds for technology bubbles and fails for the credit bubble (2007).** This supports splitting Phase 4 into a technology branch and a credit branch.
2. **"Inflow before price" is weaker than first claimed.** It is clean in 2000 and 2007. In 1929 it holds only as a tie: brokers' borrowings peaked in the same month as prices (Sep 1929), with no lead. The rule is "at or before"; under strict precedence 1929 would fail. The brokers' figure is an end-of-month snapshot, while the price is a monthly average. (Before the 13 Nov 2026 correction this row read "fails by one month"; see section 7, item 11.) It is unusable in 2020 and 2022 because pandemic lending distorts the loan series (2022 is now marked not usable in the table). The working session said "✓ in all four"; that was too strong, and this result supersedes it.
3. **The PNR proxy fired in 2020 and then reversed** after the Fed and fiscal intervention. A spread breach alone is therefore not "no return." This led to a post-hoc rule (section 7).
4. **In the three endogenous episodes, the human delay was about 11–17 months** from the rate peak to the PNR. Measured from the price peak, it ranged from 3 to 16 months.
5. **Five episodes cannot estimate γ, μ, w_ij or b_i.** The back-test checks the order of the phases only.

## 5A. Evidence-hardening runs (rules unchanged)

Run with `python3 -I code/extensions.py` after `backtest.py`. Outputs: `outputs/base_rates_H1b.csv`, `pnr_rule_scan.csv`, `out_of_sample_episodes.csv` and `non_burst_booms.csv`.

**A. Base rates for H1b** (how often the S&P monthly average falls ≥20% below a given month within the next 13 months):

| Sample | Months | Rate |
|---|---|---|
| 1871–2025 | 1,856 | 11.4% |
| 1950–2025 | 908 | 6.9% |
| CAPE in its top decile (≥26.9) | 172 | 15.1% |

**B. False-positive scan of the PNR rule, 1964–2024.**
- The single-month rule (4.4) fired 13 times. A ≥20% fall from the prior 12-month high followed only 4 of them (1974, 2001, 2002, 2008). **The single-month breach is a stress signal, not a bubble signal.**
- The 6-month persistent rule (the H3 rule) fired 4 times: 1970, 1998, 2001 and 2008. It was followed by a bear market, or a near-bear (1970, −19.0%), in 3 of the 4. 1998 (LTCM) is the false positive. The persistent rule therefore has fair precision and low recall: it missed 1974, 1980–82, 1987, 2020 and 2022.

**C. Out-of-sample episodes.** These were selected by rule, not by hand: every monthly-average drawdown of ≥19% from a running all-time high, 1930–2024. The 1937 fall lies inside the 1929 drawdown, because the 1929 high was not regained until 1954, so it is not selected separately.

| Peak → trough | Fall | Credit inflow peaks before price (P2) | PNR (single / persistent) | Unemployment rise |
|---|---|---|---|---|
| Dec 1961 → Jun 1962 | −22.5% | no data | no data | no data |
| Dec 1968 → Jun 1970 | −29.0% | Yes (Dec 1965, 36 m ahead) | Aug 1970 / Aug 1970 | +2.7 pp |
| Jan 1973 → Dec 1974 | −43.4% | **No** (Aug 1973) | Nov 1974 / not reached | +4.1 pp |
| Nov 1980 → Jul 1982 | −19.4% | Yes (Sep 1978, 26 m ahead) | Jan 1981 / not reached | +3.3 pp |
| Aug 1987 → Dec 1987 | −26.8% | Yes (Sep 1984, 35 m ahead) | not reached | 0.0 pp |

**D. Booms that did not burst.** No PNR breach occurred inside 1995–97 (+106.9%), 2013–14 (+38.8%) or 2017 (+17.1%). The worst falls in the following 24 months were +0.1%, −7.3% and −3.6%. **The rule did not raise a false alarm inside a boom.** Its false alarms (1998, 2015) came during shocks.

**What this changes:**
1. **P2 is true in 6 of the 8 episodes that have data, but the lead time is long and irregular** (1 to 36 months), and it fails in 1973 and 2020. "Inflow before price" holds as an ordering, not as a timing tool.
2. **No dominoes without credit stress.** 1987 and 2022 had no spread breach and almost no rise in unemployment. 1974 and 2008 had both. This is consistent with the R_D condition (debt-financed losses spread, equity losses mostly don't). It is the strongest out-of-sample support in the file.
3. **H3 is a hard test.** The persistent rule has fired only 4 times in 60 years, so a "yes" on H3 in the window would be informative.
4. **Scoring benchmark (added to section 6):** H1b forecasts are compared with the 15.1% top-decile-CAPE base rate.

**Not done here, and why.** Japan 1990 is covered separately in section 5B. The robustness grid, rival-model registration and independent re-dating are listed in section 8.

## 5B. Japan 1989 (out of sample)

Run with `python3 -I code/japan.py`. Output: `outputs/japan_1989_results.csv`.

**Data** (in `data/raw/japan/`, SHA-256 in `outputs/SHA256SUMS_raw.txt`). All are GitHub mirrors, not official files: verify them before v1.0 as for FRED-MD.

| File | Content | Origin (as labelled by the mirror) |
|---|---|---|
| `jp_macro_monthly_dissrepl.csv` | Monthly Nikkei 225, BOJ policy rate, unemployment, M2, JGB yields | github.com/sebvellu/dissrepl (replication data) |
| `nikkei225_daily_1970_2015.csv` | Daily Nikkei 225 closes, used only as a cross-check | github.com/ksnt/Global-Terrorism-Data-Analysis |
| `QJPPAM770A.csv` | Credit to the private non-financial sector, % of GDP, quarterly | BIS, via a FRED cache in github.com/wilsoniumite/labor |
| `QJPN628BIS.csv` | Residential property prices, nominal, quarterly | BIS, via the same cache |

The two Nikkei sources agree to within 0.52% in every month, which is a first check on the mirrors.

**Rule adaptations** (Japan has no series in these files for a corporate credit spread):
- The credit-inflow channel uses the 4-quarter change in credit/GDP instead of US bank loans.
- The PNR is taken from a **manual, unverified** row: the November 1997 failures of Hokkaido Takushoku and Yamaichi. The spread rule cannot be run.

**Results:**

| Measure | Japan 1989 | US range (sections 5, 5A, 5C) |
|---|---|---|
| Peak | Dec 1989 (38,115, monthly average) | — |
| Fall within 36 months | −58.6% (Aug 1992) | −19% to −51% |
| Fall to the full trough | −79.8% (Feb 2009) | −19.1% to −84.8% (1929) |
| Months to regain the peak | **411** (Mar 2024) | 7 to 300 (1929) |
| Rate channel | First hike May 1989; peak 6.0% Aug 1990 | — |
| P2: credit inflow before price | **Yes** (credit growth peaked Jul 1987, 29 months ahead) | 6 of 8 |
| Property prices, worst fall inside the episode (nominal) | Peak Jan 1991, −46.5% to Apr 2009 | 0% in 5 of 7 with data; −5.3% in 2000 (start of the next bubble's turn); −31.1% (2007); 1929–1968 no data |
| Peak → PNR (manual) | **95 months** | 2–22 |
| Unemployment rise in 36 months | +0.2 pp | 0.0–11.2 pp |
| Unemployment rise to its peak, inside the episode | +3.4 pp (2.1% → 5.5%, 2002) | 0.0 to +11.2 pp (2020); 1929 +21.7 pp (annual, manual) |

**What Japan adds:**
1. **P2 holds**, with a long lead, as in the US cases.
2. **No ratchet:** the bubble asset (property) fell by half and stayed down for 18 years. This matches the credit branch, as in 2007.
3. **The human delay was more than four times the longest US case** (95 months against 22). The dominoes came slowly (+0.2 pp in 3 years, +3.4 pp over 12) because the losses were carried, not recognised. **If the current cycle followed this path, H7 (3–18 months) would come out false, and that would be informative, not a failure of the test.**
4. **Proposed amendment to Phase 4, not adopted for the forward test:** recovery starts only after losses are written down, and postponing the write-down lengthens τ and delays recovery. It is supported by the contrast between Japan (no forced write-down; 411 months) and the US in 2009 (stress tests and TARP; 65 months). It is post-hoc and rests on two cases, so it is recorded here as a hypothesis for a later field test.

## 5C. Full-episode measures for the US

Run with `python3 -I code/full_episode.py`. Output: `outputs/us_full_episode_measures.csv`. Each episode runs from the price peak to the month the S&P regains that peak, the same window used for Japan.

**Property data** (in `data/raw/us_property/`; GitHub mirrors, to be verified):
- BIS nominal residential property prices for the US (QUSN628BIS, quarterly from 1970), via github.com/terrypacker/fin-sim-framework.
- S&P/Case-Shiller US National Home Price Index (monthly from 1975), via github.com/datasets/house-prices-us.

| Episode | Peak → back to peak | Final low | Fall to final low | Unemployment rise to its peak | Property, peak to final low (BIS) | Property, worst fall inside episode (BIS / Case-Shiller) |
|---|---|---|---|---|---|---|
| 1929 | Sep 1929 → Sep 1954 | Jun 1932 | −84.8% | +21.7 pp (annual, manual) | no data | no data |
| 1961 | Dec 1961 → Sep 1963 | Jun 1962 | −22.5% | 0.0 pp | no data | no data |
| 1968 | Dec 1968 → Mar 1972 | Jun 1970 | −29.0% | +2.7 pp (Dec 1970) | no data | no data |
| 1973 | Jan 1973 → Jul 1980 | Dec 1974 | −43.4% | +4.1 pp (May 1975) | +15.7% | 0.0% / n.a. |
| 1980 | Nov 1980 → Nov 1982 | Jul 1982 | −19.4% | +3.3 pp (Nov 1982) | +6.0% | 0.0% / −0.6% |
| 1987 | Aug 1987 → Jul 1989 | Dec 1987 | −26.8% | 0.0 pp | +2.0% | 0.0% / 0.0% |
| 2000 | Aug 2000 → May 2007 | Feb 2003 | −43.7% | +2.2 pp (Jun 2003) | **+23.1%** | −5.3% / −1.6%\* |
| 2007 | Oct 2007 → Mar 2013 | Mar 2009 | −50.8% | +5.3 pp (Oct 2009) | **−19.2%** | **−31.1% / −26.0%** |
| 2020 | Jan 2020 → Aug 2020 | Mar 2020 | −19.1% | +11.2 pp (Apr 2020) | 0.0% | 0.0% / 0.0% |
| 2022 | Dec 2021 → Dec 2023 | Oct 2022 | −20.3% | +0.1 pp | +6.9% | 0.0% / 0.0% |

\*The 2000 episode window runs to May 2007, so its "worst fall" picks up the start of the 2006–07 housing turn. This is the next bubble, not the 2000 one. Measured concurrently, property rose 23.1% through the 2000–03 stock crash.

**What it shows:**
1. **Property only fell in the credit bubbles: 2007 in the US (−31%) and Japan (−46.5%).** In the technology crash of 2000, property rose 23% while stocks fell 44%. That is the clearest separation of the two branches in the file.
2. **The 1970s readings are nominal.** In high inflation, nominal house prices didn't fall even when real ones did. A real-price version (BIS QUSR628BIS) is a possible addition.
3. **The full-episode unemployment rise is close to the 36-month figure in every US case.** Japan is the exception: +0.2 pp in 36 months against +3.4 pp in the full episode. In the US the dominoes fell within three years; in Japan they kept falling for a decade.

## 5D. Blind-spot runs (9 Nov 2026)

Run with `python3 -I code/blindspots.py`. Outputs: `outputs/us_real_terms.csv`, `property_real_drawdowns_US_JP_CA.csv` and `canada_tsx_episodes.csv`. Concentration rows: `data/manual/concentration.csv` (unverified). New raw data: the BIS selected property prices for all countries (`data/raw/bis/`), and Canada's TSX and unemployment (`data/raw/canada/`), all GitHub mirrors to be verified.

### 5D.1 Real terms (inflation-adjusted, Shiller real price)

| Episode | Nominal fall / months to recover | Real fall / months to recover |
|---|---|---|
| 1929 | −84.8% / 300 | −80.6% / 350 |
| 1961 | −22.5% / 21 | −23.0% / 24 |
| 1968 | −29.0% / 39 | **−62.6% / 277** (real low Jul 1982) |
| 1973 | −43.4% / 90 | **−59.6% / 175** |
| 1980 | −19.4% / 24 | −29.3% / 29 |
| 1987 | −26.8% / 23 | −27.5% / 53 |
| 2000 | −43.7% / 81 | **−58.6% / 171** (real low Mar 2009) |
| 2007 | −50.8% / 65 | −51.7% / 73 |
| 2020 | −19.1% / 7 | −19.1% / 7 |
| 2022 | −20.3% / 24 | −25.5% / not measurable (the real series in the file ends Sep 2023) |

**Finding:** in real terms, 1968–82 is the second-worst episode on record after 1929, by both the size of the fall and the time to recover. (The 1973 episode lies inside it, since the real 1968 peak was not regained until 1992.) Nominal measurement hid it. This points to **a third ending, inflation erosion:** the bubble asset's price stalls while inflation removes its real value over a decade or more. The model has no branch for it. **Proposed (not adopted):** add an erosion branch, and judge recovery in real terms.

### 5D.2 Following the bubble asset: real residential property (BIS)

| Country | Real peak → trough | Real fall | Back to peak |
|---|---|---|---|
| United States | 1979 Q4 → 1982 Q3 | −10.1% | 1986 Q3 |
| United States | 1989 Q4 → 1995 Q2 | −12.6% | 2000 Q1 |
| United States | **2006 Q1 → 2011 Q2** | **−39.0%** | **2021 Q4 (63 quarters)** |
| Japan | 1973 Q3 → 1977 Q2 | −31.1% | 1987 Q3 |
| Japan | **1991 Q1 → 2009 Q2** | **−48.9%** | not by 2023 |
| Canada | 1976 Q4 → 1984 Q3 | −21.9% | 1987 Q1 |
| Canada | 1989 Q1 → 1998 Q3 | −21.1% | 2003 Q4 (59 quarters) |
| Canada | **2022 Q1 → 2023 Q1 (data end)** | **−18.9%** | **open** |

### 5D.3 Canada

- **Stocks (TSX, ≥19% rule, from 1985):** 1987 (−26.1%), 1998 (−27.8%), 2000–02 (−45.1%), 2008–09 (−44.8%), 2020 (−22.7%). Unemployment rose most in 2020 (+8.6 pp) and 1987 (+3.4 pp, mostly in the 1990–92 recession).
- **Property, the bubble asset:** Canada has had two earlier real-terms housing busts, each about −21% and each taking 10 to 15 years to recover. Unemployment rose **+5.7 pp** in the 1976–84 bust (to 13.1%) and **+4.6 pp** in the 1989–98 bust (to 12.1%). Both were bigger than the stock-market episodes. **On the asset that actually inflated, Canada's credit-branch dominoes have historically been large.**
- **The current episode is open.** Real house prices fell 18.9% from their 2022 Q1 peak to 2023 Q1, almost the size of the two earlier busts. The BIS file and the unemployment file in this package both end in 2023, so the outcome since then is not measured. **This is the most relevant live case for RLS, and current data is needed before drawing anything from it.**

### 5D.4 Concentration (manual, unverified)

| Measure | Value |
|---|---|
| Top-10 share of the S&P 500 | 1963 ~30% · 1980 ~26% · 2000 ~26% · 2015 ~17.8% · 2020 ~27% · 2024 ~35% · **2025 40.7% (record)** · **5 Nov 2026 39.1%** (top 5: 29.9%) |
| US share of world market value | 1989 29.3% · 2007 33.0% · **2024 54.0%** (World Bank) |
| Japan's share of world market value, 1989 | commonly cited at 40–45%; **not found in a checkable source**; to be computed from World Bank data |
| Nifty Fifty peak, 1972 | not found |

**Two kinds of concentration exist now at once.** Within the index, the top 10 hold a record share. Across countries, the US is 54% of world market value. That is a larger share than the commonly cited figure for Japan in 1989, though the Japan figure is unverified. Neither has a tested place in the model yet. **Proposed (not adopted):** concentration as a multiplier on R_D, because a handful of firms (or one country) carry the domino links for everyone.

### 5D.5 Bubbles or crashes? (PI decision needed before v1.0)

The back-test selected every ≥19% drawdown, so it is a test of **crashes**, not of bubbles. Some of these crashes had no inflated asset at all: the 1980–82 Fed-induced recession, and the 2020 virus. A bubble test needs the bubble asset identified *before* the crash. **Proposed classification, for the PI to accept or change:**

| Type | Episodes | Bubble asset |
|---|---|---|
| Bubble crash: technology | 2000; Railway Mania (not in the dataset) | Nasdaq / internet stocks |
| Bubble crash: credit | 1929, 2007, Japan 1989, Canada 1989 | margin loans and shares; housing; land and shares; housing |
| Bubble crash: concentration | 1972–74 (Nifty Fifty); possibly 1968 | a small group of "one-decision" growth stocks |
| Crash without a bubble asset | 1962, 1980–82, 1987(?), 2020, 2022(?) | none (policy, a shock or a rates move) |

**PI decision (13 Nov 2026): the classification above is accepted as proposed.**

**PI's interpretation (outside the test).** The PI takes the current bubble asset to be the **AI build-out**: AI chips, neoclouds (GPU-cloud lenders and operators) and data-centre power, with two features: **concentration** (5D.4) and **vendor financing** (5D.7). This is an interpretation, not a prediction, and it is not part of the decision above or of the forward test: nothing in section 6 is scored on it. It is recorded so that readers can judge the forward results against it.

**Caveat, recorded with the interpretation:** the chip layer was already falling when it was named. The PHLX Semiconductor index peaked on 22 June 2026 and stood about 38% below that peak on 5 Nov 2026. So the asset is named before the **index** breaks, not before the **asset** began to fall. Readers should weigh the forward test with that in mind.

### 5D.6 The conversion signal (hypothesis, from the PI, 9 Nov 2026)

The PI's point: in the tulip story, the red flag was not the price of tulips. It was **people selling or mortgaging their houses, the essential and safe asset, to buy the bubble asset.** That pattern repeats: margin loans on savings in 1929, home-equity loans spent on shares and houses in 2005–07, Japanese firms borrowing against land to buy shares in 1989.
- **Proposed variable:** a conversion ratio, the share of new money flowing into the bubble asset that is borrowed against essential assets (homes, retirement savings) rather than paid from income. Candidate measures today: margin debt, home-equity borrowing, leveraged ETF flows, and the AI-stock share of retirement accounts.
- **Caution:** historians (Goldgar, *Tulipmania*, 2007) argue the tulip episode itself was small and its damage exaggerated. The pattern is better documented in 1929 and 2007 than in 1637.
- Not in the forward test. It is a candidate for Field Test 3.

### 5D.7 Still open

- Credit for the AI build that bank-loan data cannot see (private credit, off-balance-sheet vehicles, vendor financing) has no series in this package. H2 may therefore miss the turn.
- Policy actions (rate cuts, bailouts) are not coded as data.
- Cross-border dominoes are not modelled.
- Outside review: see `REVIEW_REQUEST.md`.

## 6. Forward test (pre-registered)

**Window:** from the v1.0 registration commit to **31 December 2027**, resolved by **31 March 2028** using the latest published data.

**Baseline values:** each series' latest published value at the registration date, recorded in the event log at v1.0.

| ID | Prediction | Resolution rule and source | PI forecast |
|---|---|---|---|
| H1a | **Breaking Point, cycle measure.** The US market falls into bear territory from the cycle high. | Some S&P composite monthly average in the window is ≥20% below the highest monthly average from Jan 2026 to that month (Robert Shiller's online data, Yale, in the version published at resolution; if that series ends before December 2027, S&P Dow Jones Indices' official monthly averages of S&P 500 daily closes). *Partly informed:* the cycle high (Oct 2026) predates registration, so the baseline drawdown B (section 6.1) is already in hand. | declined (6.2) |
| H1b | **Breaking Point, clean measure.** The market falls 20% from where it stands at registration. | Some S&P composite monthly average in the window is ≥20% below the **registration-month** monthly average R (section 6.1), same source as H1a. Nothing in the outcome is known at registration, though R itself includes the part of the registration month before registration (disclosed in section 7, item 13). | declined (6.2) |
| H2 | **Inflow before price.** *Conditional on H1a:* new-issue money peaks before prices. | The peak month of trailing-3-month US IPO proceeds falls at or before the S&P peak month used in H1a (the cycle high). **Search window: the same as the back-test's rule 4.3, from 36 months before that S&P peak month to 12 months after it, cut off at December 2027.** **Series:** monthly US IPO proceeds as published by Renaissance Capital (IPO Center statistics, its standard US universe: IPOs of at least $50 million market value, SPACs excluded); if Renaissance's monthly proceeds are not publicly available for the whole search window, Jay Ritter's monthly IPO statistics; if neither publishes monthly proceeds, H2 resolves as **not applicable**. *Disclosure: the back-test measured credit inflow with bank loans, not IPO proceeds; this IPO measure has not been back-tested (section 7, item 13).* | declined (6.2) |
| H3 | **Point of No Return.** | BAA−AAA (FRED: BAA, AAA) exceeds its trailing-60-month mean + 2 SD for **6 consecutive months**, as in the back-test code: the mean and the sample standard deviation are taken over the 60 months ending the month **before** each month (lagged one month). The run must **begin** within the window; its later months may fall after December 2027 if they are published by 31 March 2028. *Caveat: the New York Fed has noted that the scarcity of AAA-rated issuers weakens this spread as a credit-risk gauge; it may miss stress in high-yield, private or vendor credit.* | declined (6.2) |
| H4 | **Ratchet.** AI adoption keeps rising even if prices fall. | The latest US Census BTOS national reading of the share of firms using AI (now labelled "Super Intelligence or SI" by the Census Bureau) **in any of their business functions**, under the instrument wording in force at registration (the wording introduced with the 19 Oct 2026 collection), is higher at window end than at the baseline. The baseline is the latest national release under that wording at registration or, if none has yet been published, the first such release. "Window end" is the latest BTOS release published on or before 31 December 2027. Both readings must use the same question wording; if the Census Bureau changes the wording within the window, H4 resolves as **not applicable**. *Also scored conditionally on H1b.* | declined (6.2) |
| H5 | **Dominoes.** | US unemployment (BLS UNRATE) reaches ≥1.0 pp above baseline in some month of the window. Both the baseline month and the window months are read from the **same data vintage**, the one published at resolution (including BLS's annual revisions). | declined (6.2) |
| H6 | **Delinquency lag.** *Conditional on H5:* delinquencies follow jobs. | The NY Fed auto-loan 90+ day transition rate in the last published quarter of the window is above its baseline quarter. | declined (6.2) |
| H7 | **Human delay.** *Conditional on H1a and H3:* τ falls in the back-test range. | The months from the H1a peak month (the cycle high) to the first month of the **first** H3 run in the window are between 3 and 18 inclusive. | declined (6.2) |

**6.1 Baseline, recorded at registration (fill in on the registration date)**

| Item | Value | Source and date read |
|---|---|---|
| Registration timestamp (Toronto) | **17 November 2026, 9:56 AM (EST, UTC−5)** | PI, at publication on 369369369.org |
| Cycle high: highest S&P monthly average since Jan 2026, and its month | **7,726.69, Oct 2026** (Aug 2026: 7,711.32, 0.2% lower) | Oct: mean of the 22 daily closes, 1–30 Oct 2026, from Yahoo Finance (^SPX, 1–22 Oct) and Investing.com (16–30 Oct; the overlapping days agree), read 16 Nov 2026. Jan–Sep: Shiller series via the datasets/s-and-p-500 mirror, read 16 Nov 2026, which ends at Sep 2026. Resolution uses Shiller's published value (H1a), which may differ slightly. |
| R: S&P monthly average for the registration month (resolved at month end) | resolved at 30 Nov 2026; month to date **7,537.39** (10 closes, 2–13 Nov) | Investing.com, read 16 Nov 2026 |
| B: baseline drawdown = latest S&P monthly average ÷ cycle high − 1 | **0.0%** (the latest complete month, Oct, is the cycle high); November to date is **−2.4%** | as above |
| BAA−AAA spread, latest month | **0.47 pp** (Oct 2026: BAA 6.59%, AAA 6.12%) | FRED BAA, AAA, read 16 Nov 2026 |
| Census BTOS share of firms using AI in any business function (latest release; record the question wording) | **24.2%** (standard error 0.61), national, answer "Yes", period 112: 19 Oct – 1 Nov 2026, the first release under the new wording. Wording (BTOS question ID 6, "AI current"): "In the last two weeks, did this business use Super Intelligence or SI (formerly referred to as Artificial Intelligence or AI) in any of its business functions? (Examples of SI use include: SI-powered data analysis; generative SI for marketing, product design, or coding; virtual SI agents for customer service; SI-powered forecasting or pricing; SI-driven computer vision for quality control, etc.)" Source: Census BTOS API, /hfp/btos/api/periods/112/questions and /periods/112/data, read by the PI 16 Nov 2026 (national row = all strata empty; the separate "XX" state code is not the national figure). The Census Bureau's About page (read 16 Nov 2026) states that from the 19 Oct 2026 collection "instrument wording was updated due to Executive Order 14434", and the series is now titled "Super Intelligence or SI (formerly referred to as Artificial Intelligence or AI) Use". Earlier wording (17 Nov 2025 to 19 Oct 2026): "...use Artificial Intelligence (AI) in any of its business functions?" Last official national figure seen under that earlier wording: 19.8%, period ending 3 May 2026. | Census BTOS (census.gov/hfp/btos); Census Bureau story "Large Firms With at Least 20 Employees Biggest AI Users", 26 May 2026. A 23.8% figure entered earlier from a secondary site was withdrawn: it matches the 20–49-employee size class (six-survey average, period ending 4 Oct 2026), not the national rate. |
| UNRATE, latest month | **4.1%** (Oct 2026) | BLS Employment Situation, released 6 Nov 2026 |
| NY Fed auto-loan 90+ transition rate, latest quarter | **3.02%** (2026 Q3; annualized share of balances; Q3 2025: 2.99%) | NY Fed Household Debt and Credit press release, 10 Nov 2026 |

Report B next to H1a so readers can judge how much of H1a was already known at registration. At registration, the cycle-high month is complete and November is 2.4% below it, so H1a starts about 2.4 points into its 20-point fall.

**6.2 PI forecasts, positions and authorship**

- **No probability forecasts.** The PI declines to give probabilities for H1a–H7, to keep intuition-led numbers out of the test. The PI states a bearish view of AI-linked equities, and the co-drafter (CAM, an Anthropic model) is conflicted (below). The PI's Brier scoring is therefore **not applicable**. For reference only: the H1b base rate is 15.1% (section 5A), and the three outside reviewers' probabilities are recorded in section 7, items 12–13.
- **Positions.** At registration the PI holds no position in ANT (Anthropic) or NVDA (Nvidia) and has no plan to acquire one during the window. Any change is to be logged in the event log with its date.
- **Authorship and conflict.** This protocol was drafted with CAM, an AI model made by Anthropic, during the week of Anthropic's IPO, and ratified by the PI. Anthropic is a node in the network the model describes.

**6.3 Scenario map, fixed before the outcome.** Each path and what it means for the model, decided now so that no result can be reinterpreted afterwards:

| Path | What happens by 31 Dec 2027 | Verdict |
|---|---|---|
| 1. No bear market | Neither H1a nor H1b occurs | **Untested, not confirmed.** A boom that doesn't break is not evidence for the model. |
| 2. Soft landing | H1a or H1b occurs; H3 does not (no Point of No Return); H2, H4 and H7 true where they apply | **Structural pass, fast-recovery branch.** Consistent with the model; says nothing about the domino stage. |
| 3. Full cycle | H1a or H1b occurs; H3 occurs; H5 and possibly H6 follow; H2, H4 and H7 true | **Structural pass, full cycle.** The strongest support the test can give. |
| 4. Money arrived late | A bear market occurs, and IPO money peaks after the price peak (H2 false) | **Model fails.** Inflow did not precede price. |
| 5. Adoption fell | A bear market occurs, and BTOS AI use is not higher at window end than at baseline (H4 false) | **Model fails.** The ratchet did not hold. |
| 6. Delay outside range | A bear market and a Point of No Return occur, but the delay is under 3 or over 18 months (H7 false) | **Model fails** on the human-delay term. |
| 7. Data path | A rule resolves not applicable (wording change, no public IPO series) | Reported as such; it neither passes nor fails the model. |

**6.4 Known future events and the shock log**

- **Known in advance:** the ANT lock-up expiry, expected about 180 days after listing (the date is set by the final prospectus), falls inside the window. It is a scheduled supply event, logged now so it cannot be called a surprise.
- **Shock log.** Exogenous shocks are logged as they happen, with date and type, and are **not scored**: supply or single-node (a key firm or person), geopolitical or war, infrastructure outage (power, grid, cloud or email systems), natural events, and policy actions (with the days from shock to backstop). The log is raw material for Field Test 3, where the shock term of section 2A may be adopted.

**Scoring.**
- Each prediction is resolved as **true**, **false** or **not applicable** (when its condition is not met).
- The PI's forecasts would be scored with the Brier score, (p − outcome)²; the PI has declined to forecast (6.2), so this is not applicable. Reviewers' probabilities may be scored the same way for reference.
- **Benchmark (reference only):** the H1b base rate of 15.1% (section 5A).
- **Structural test, triggered by a bear market on either measure (H1a or H1b).** If H1a or H1b occurs: the model **fails** if any of H2, H4 or H7 is false; it **passes** if H4 holds and H2 and H7 are true whenever they apply. "Not applicable" is neither true nor false.
- **What the failure rule leaves out, and why.** H3, H5 and H6 are scored as forecasts (Brier) but are not part of the failure rule, because the model allows a bear market that never reaches the Point of No Return: the fast-recovery branch of section 2 (a quick decay of the confidence hit, as in 2020). A bear market without H3 is therefore not a contradiction of the model; a bear market in which money arrived after the price peak (H2 false), adoption fell (H4 false) or the human delay fell outside 3–18 months (H7 false) is.
- H1a and H1b are scored separately. The model's headline result uses **H1b**, the measure not known at registration.
- If neither H1a nor H1b occurs in the window, the model is **untested, not confirmed**. A boom that doesn't break is not evidence for the model.

## 7. Deviations log (changes made after seeing data)

Items 1–3 were made after the back-test had been run. Item 4 was made after the cycle high and the 5 Nov 2026 drop were already known.

1. **Peak rule (4.2).** The first rule took the peak as the window maximum. In 2020 that picked December 2020, after the recovery. It was changed to "the highest month before the window's lowest month." The change applies to all episodes.
2. **P2 test.** The first version allowed the rate channel to count toward P2. The rate peak precedes the price peak by construction, so P2 would have been true automatically. P2 now uses the credit channel only.
3. **PNR persistence.** After the 2020 reversal, a variant requires the spread breach to persist for 6 consecutive months (column `pnr_persistent_v1_posthoc`). **It is post-hoc in the back-test.** It is used as the H3 rule in the forward test, where it is not post-hoc.
4. **H1 split (8 Nov 2026, before registration).** The original H1 measured the fall from a cycle high that predates registration, so part of the outcome was already known. It was split into H1a (cycle measure, kept, flagged partly informed) and H1b (from the registration-month level, clean). The baseline drawdown B is recorded in section 6.1.
5. **Write-down amendment (8 Nov 2026), proposed only.** Suggested by Japan (section 5B). It does not change any forward-test rule.
6. **Shock terms and fragility Φ (section 2A) and Appendix A, proposed only (8–9 Nov 2026).** None changes a forward-test rule.
7. **Blind-spot additions (9 Nov 2026), proposed only:** the erosion branch, real-terms recovery, concentration as an R_D multiplier, the bubble/crash classification and the conversion signal (section 5D). None changes a forward-test rule. The classification (5D.5) was accepted by the PI on 13 Nov 2026 (item 9).
8. **Events known before registration (logged 13 Nov 2026).** The forecasts in section 6 were made knowing all of these. Figures are from press reports and must be checked against exchange data before v1.0:
   - **5 Nov 2026:** the PHLX Semiconductor index fell 12.2% in one day, its largest one-day fall since March 2020, and stood about 38% below its 22 June 2026 peak. The Nasdaq Composite closed about 12% below its 6 Oct 2026 record. CoreWeave's five-year CDS spread reached a record high.
   - **8–12 Nov 2026:** Nvidia CEO Jensen Huang admitted an affair (8 Nov); press reports followed (10–11 Nov); he resigned on 12 Nov, and CFO Colette Kress became interim CEO. NVDA closed at $166.19 on 12 Nov (−4.3% that day, −13% intraday), about 31% below its October 2026 high, after six consecutive weekly declines.
   - **13 Nov 2026:** David Rosenberg (Rosenberg Research) wrote that "Nvidia's stakes, guarantees and backstops are what tie the AI trade together, so the weakest links are the borrowers who depend on Nvidia's support."
   - **Pending at the time of writing:** Anthropic's IPO, reported for the week of 16 Nov 2026, with cornerstone investors reported to include Nvidia, AMD, Broadcom, Micron, Microsoft, TSMC and Google.
   - **Logged 16 Nov 2026, at registration:** the IPO is set on Nasdaq under the ticker ANT, at a range of $70–78 a share (825 million shares, up to $64.4bn), with seven strategic partners including Google and Nvidia buying $26bn of non-voting stock at the IPO price; trading is expected as early as 18–19 Nov. In Washington, the Huang affair has opened a race among technology firms for policy influence and revived pressure for tighter limits on AI-chip exports to China. Context only; no prediction or rule changes.
   - **Logged 16 Nov 2026:** Gary Gensler (former SEC chair) publicly places a reversal of the AI investment boom 18–30 months out (about Apr 2028 – May 2029), citing roughly $500–600bn of AI-related debt, off-balance-sheet guarantees and special-purpose vehicles, and the 4–7-year useful life of chips bought with that debt; CNN (16 Nov 2026) reports him expecting a recession by the 2028 election. Most of that window falls after this test's end date (31 Dec 2027). Context only; no prediction or rule changes.
9. **Changes made on 13 Nov 2026, after the item-8 events were known:**
   - **H8 added.** It tests the ordering in section 2 (dominoes start where buffers are thinnest) and was prompted by the events in item 8. It is labelled in section 6 as added after the Huang event. H1–H7 are unchanged.
   - **Baseline rows added** for NVDA and CRWV (section 6.1).
   - **5D.5 classification accepted**, and the current bubble asset named (the AI build-out), with the caveat that the chip layer was already falling.
   - **Not changed:** H1–H7, section 2A (still proposed only), and H3's proxy (BAA−AAA). A high-yield or vendor-financing credit measure is noted for Field Test 3 rather than swapped in now.
10. **Changes made on 13 Nov 2026 after a first outside review** (ChatGPT, given a summary only, not the files):
   - **H4 resolution rule corrected.** The BTOS question H4 named (AI use "in producing goods or services") was replaced from the 17 Nov 2025 collection by AI use "in any of its business functions"; the level roughly doubled on the wording change alone. H4 now resolves on the current wording at both ends, and as not applicable if the wording changes again. This was an error in the original H4, found by the reviewer.
   - **H8 demoted to exploratory**, outside the confirmatory test, on the reviewer's objection that it was chosen after the events made it look likely.
   - **The current bubble asset (5D.5) reworded** as an interpretation, not a prediction; nothing is scored on it.
   - **Caveat added to H3** on the limits of the BAA−AAA spread.
   - **Explicit failure rule added** to the scoring.
11. **1929 credit-peak row corrected against a primary source (13 Nov 2026)**, after the second review named 1929 P2 as the weakest result. The PI decided to verify the row and to report whatever the source showed, before it was checked. The Federal Reserve Bulletin (Jan 1930) table "Brokers' borrowings on collateral in New York City reported by the New York Stock Exchange" gives **end-of-month** figures: Sep 1929 $8,549m (the peak), Oct 1929 $6,109m. The largest monthly increase was also in September (+$667m). The row had read Oct 1929, from the widely cited "$8.5 billion on 1 October" figure, which is the end-September value. **Effect: 1929 P2 changes from "fails by one month" to "holds as a tie, no lead."** The rate-rise row (FRBNY discount rate 5% to 6%, established 9 Aug 1929; Federal Reserve Bulletin, Sep 1929) was confirmed unchanged. Both rows are now `verified=yes`. The PNR row (Dec 1930) was not checked and stays unverified. Only `outputs/backtest_results.csv` changed when all scripts were rerun.
12. **Second outside review (ChatGPT, 13 Nov 2026), given the full package as one PDF; it quoted section 6 and H4 to confirm it had read it.** Verdict: no fatal objections. Serious: falsifiability (the "untested" exit if H1b does not occur; the conditional and not-applicable exits for H2, H4 and H7; the Brier scoring and the base-rate benchmark did not change its verdict), back-test circularity (it named 1929 P2 as the weakest result, which section 5 already did; that row was then verified, item 11), proxy validity, and missing variables (private credit, policy timing, cross-border spillovers, a rival model). Changes made in response, on 13 Nov 2026:
   - **H8 dropped** from Field Test 2 altogether, together with the NVDA and CoreWeave baseline rows. All three reviews recommended it: a prediction chosen after the events that made it look likely does not belong in the test, even when labelled exploratory. It is carried to Field Test 3, to be defined there from the start. The events themselves stay in item 8.
   - **The bubble asset (5D.5) retitled** as the PI's interpretation, outside the decision and outside the test.
   - **H2's source order fixed in advance:** Renaissance Capital first; Ritter only if Renaissance's monthly figures are unavailable for the whole window. The reviewer had flagged the choice between two sources as a gaming risk.
   - **Not changed:** H1–H7 otherwise; the failure rule; the 1929 P2 result, which is reported as the verified source gave it.
   - **The reviewer's own probabilities, recorded for comparison:** H1a 72%, H1b 58%, H3 44%, H4 66%, H5 41% (and 27% for the now-dropped H8). **The PI read these before setting his own forecasts in section 6;** readers should allow for anchoring.
   - The reviewer's file names in its answer on unverified data were wrong (it named files that do not exist), but the rows it pointed to were the right ones: the 1929 events and the adoption series.
13. **Third outside review (Gemini, 13 Nov 2026), given the full PDF; it quoted section 6 and the corrected 1929 row to confirm it had read it.** Verdict: do not register. The PI and CAM checked its two factual claims about the data and found both wrong: the "duplicate and contradictory rows" in `adoption_annual.csv` are context years repeated by design with identical values, and `concentration.csv` gives 1963 as 30%, matching section 5D.4. Its other objections were accepted as follows. This was declared the last review before registration; the fixes below were made in response and not sent for review again.
   - **Fatal, fixed: H2 had no search window.** H2 now uses the back-test's own rule 4.3 window (36 months before the S&P peak to 12 months after), names the series and its exclusions, and resolves as not applicable if no public monthly proceeds exist. The window was taken from the existing rule, not chosen fresh. Known consequence: if the Anthropic IPO (reported for the week of 16 Nov 2026) makes Nov 2026 the IPO peak, after the Oct 2026 S&P peak, H2 resolves false.
   - **Fatal, fixed: the failure rule triggered only on H1b.** It now triggers on H1a or H1b, so a bear market measured from the cycle high also tests the structure. The reason H3, H5 and H6 stay outside the failure rule is now stated in section 6.
   - **Resolution details fixed:** one named index source for H1a and H1b; H3's lagged 60-month mean and sample SD, and runs that begin in the window; H4's "window end"; H5 read from one data vintage; H7 uses the cycle high and the first H3 run.
   - **Back-test: 2022 P2 changed from "Yes, contaminated" to "Not usable"**, because its search window reuses the 2020 lending surge. The 1929 tie is now reported with its strict-precedence result (it would fail) and the snapshot-versus-average caveat.
   - **Disclosed, not changed:** (a) **selective verification**: only the two 1929 rows were checked, because they were the weakest result, and the correction helped the model; every back-test claim that rests on an unverified row (the 1929 PNR date and human delay, Japan's PNR and its 95-month delay, the ratchet results from `adoption_annual.csv`, and the concentration figures) is unproven until checked. (b) H2's IPO measure was never back-tested. (c) R includes the part of the registration month before registration. (d) The PI saw two reviewers' probabilities before setting his own (item 12; this reviewer's: H1a 38%, H1b 26%, H3 18%, H4 82%, H5 24%).
   - **Carried to Field Test 3:** the model's own mechanism, the financing gap G = C − R (AI capital spending against outside AI revenue), which Field Test 2 does not measure; the IPO's pricing against target as the outside-money verdict on the build-out; a vendor-financing credit measure; a rival model; the omitted episodes (1937–38, China 2007 and 2015, the euro crisis, crypto 2021–22); and the weakest-link ordering dropped as H8.
14. **PI decisions, 13 Nov 2026, after the third review:** (a) the PI declines to give probability forecasts (section 6.2), so the PI's Brier scoring is not applicable; (b) a scenario map ties each possible outcome to its verdict in advance (6.3); (c) the PI's position is declared: no holding in ANT or NVDA, and no plan to acquire one; (d) the drafting conflict is declared (CAM, an Anthropic model, during Anthropic's IPO); (e) the ANT lock-up expiry is logged as a known future event, and an unscored shock log is set up (6.4). None of these changes a prediction or a resolution rule.
15. **Registration-day corrections (16 Nov 2026).** The header still said the PI's forecasts would be in section 6 and that outcomes resolve by the rules in "section 5"; both are corrected (no forecasts, per 6.2; the rules are in section 6). The baseline table in 6.1 was filled in from the sources named there. No prediction or resolution rule changed.
16. **BTOS wording changed before registration (found 16 Nov 2026).** The Census Bureau's About page states that from the 19 Oct 2026 collection the AI questions' instrument wording was updated under Executive Order 14434, and the series was relabelled "Super Intelligence or SI". H4 named the 17 Nov 2025 wording, which was therefore no longer in use at registration. H4's baseline is moved to the wording in force at registration; the rule itself (same wording at both ends, not applicable if it changes within the window) is unchanged. Disclosure: the measure H4 relies on has now been redefined twice in a year, the second time by executive order, so H4 carries a higher risk of resolving as not applicable. Also corrected: a 23.8% baseline taken from a secondary site was a firm-size figure, not the national rate, and was withdrawn.

## 8. Before v1.0, the PI's checklist

- [ ] Verify every `data/manual` row against its cited source, and set `verified=yes` or correct it.
- [ ] Verify the FRED-MD mirror against the official file, and update its SHA-256.
- [ ] Verify the two US property mirrors (section 5C) against BIS and S&P.
- [ ] Verify the BIS global property file, the Canada files and the concentration rows (section 5D).
- [x] Decide the bubble/crash classification (5D.5). Done 13 Nov 2026.
- [x] Send `REVIEW_REQUEST.md` with the package to an outside reviewer, and log the reply and any changes before v1.0. Done 13 Nov 2026: three reviews (ChatGPT twice, Gemini once), logged in section 7, items 10, 12 and 13. The third was declared the last before registration.
- [ ] Verify the four Japan mirrors (section 5B) against the BOJ, BIS and Nikkei originals, and the manual Nov 1997 PNR row.
- [x] PI forecasts: declined, with reasons (6.2). Scenario map fixed (6.3). Decided 13 Nov 2026.
- [x] Fill in the baseline table in section 6.1 on the registration date. Done 16 Nov 2026, except the timestamp (PI, at publication). BTOS read from the Census API by the PI.
- [ ] Publish on 369369369.org; also commit and tag v1.0 on GitHub, and archive both (Internet Archive), as for Field Test 1.
- [ ] Optional, stronger: register on OSF as well, and anchor the SHA-256 of PROTOCOL.md with OpenTimestamps.
- [ ] Optional, stronger: a robustness grid (1.5 / 2.5 SD; 36 / 84-month windows), Smith's −44% formula registered as a rival forecast, and independent blind re-dating of events from section 4 alone.
- [ ] Any manual row still unverified at registration stays marked `verified=no`, and the back-test (section 5) is cited as exploratory only.

---

## Appendix A. Worked scenario: forced break-up and sale of Nvidia (illustrative, not a forecast)

*Stress test from the 8–9 Nov 2026 session. There is no current legal path for this to happen overnight: forcing a US company to divest would need legislation, as with TikTok. The scenario assumes someone with the power to do it does it.*

**A.1 Shock path** (Nvidia ≈ 8% of the S&P and ≈ $5T; top 10 ≈ 39%):

| Stage | Mechanism | Cumulative index effect |
|---|---|---|
| Day 0 | Forced-sale repricing of Nvidia (J = −30% to −50%) | −2% to −4% |
| Week 1 | The buyers (other top-10 firms) must issue shares or debt on a historic scale: congestion inside the most concentrated group | −8% to −12% |
| Weeks 1–4 | Policy risk repriced across US equities: +0.5 pp on required returns at an earnings yield of ≈3.5% gives ≈ −12% to −14% by P = E/(r − g); foreign holders pull out (US ≈ 54% of world market value) | −15% to −25% |
| Months 1–6 | AI capex pauses; GPU-backed loans face collateral calls (private credit, unseen by H2); China retaliates | crash if J·Φ > 1 and policy does not act within τ |

**A.2 Recovery paths.** All four assume the ratchet holds: AI use keeps rising, as internet use did in 2000–02. Which path occurs is set by three dials:
1. Does policy act within τ?
2. How fast are the losses written down?
3. Does inflation rise?

| Path | Dials | Precedent | Nominal recovery | Real recovery |
|---|---|---|---|---|
| **V: backstop** | Fed and Treasury backstop the sale financing and GPU-backed lending within weeks | 2020 | 6–18 months | similar |
| **Reset: write-down** | No full backstop; losses written down fast (GPU collateral marked to market, data centres sold cheaply) | 2000–07, US 2009 | 5–7 years | 6–14 years |
| **Erosion** | Backstop funded by money creation, plus tariffs and retaliation: inflation rises | 1968–82, 1973 | 7–8 years | 15–23 years |
| **Japan** | Losses carried, not recognised; failing borrowers kept alive | Japan 1989 | decades | decades |

**A.3 What leads the next bull.** In the reset path, the post-2002 pattern applies: the bust leaves cheap infrastructure behind, as dark fibre did. A break-up adds competition in chips and software, so the cost of computing (C) falls. The next bull would most likely be led by **companies that use AI** and buy cheaper compute (the Amazons and Googles of the cycle), not by the builders of the build-out (the telecom carriers of 2000).

**A.4 Signals that the turn has come**, in the order the model predicts:
1. Credit spreads peak and start to narrow.
2. New issues get bought again: the IPO window reopens (I recovers).
3. Capex guidance stops falling.
4. Prices make a low.
5. Unemployment peaks, typically months after the price low.
