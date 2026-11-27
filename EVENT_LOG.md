# FIELD TEST 2 — event log

> **Opened 2026-11-26**, nine days after registration (see deviation D-1). The protocol's §6.1 called for baseline values to be "recorded in the event log at v1.0"; they were recorded in §6.1 of the protocol itself, and are not repeated here.
> Protocol: `PROTOCOL.md` (= `BPNRDE-FT2-PROTOCOL-v1.0-registration-17-NOV-2026.md`), SHA-256
> `cf83454158d839ea390250e94f493a60b5de9cb1c88a99f2cadf2e349697b850`.
> **Observation window: from the v1.0 registration commit (registered 2026-11-17, 9:56 AM Toronto) to 2027-12-31; resolved by 2028-03-31.**
> Scored series are monthly (S&P monthly average, BAA−AAA, Census BTOS, UNRATE, NY Fed auto-loan transitions). Daily market events below are context or shocks; none is scored.
> Each entry carries its date of entry, who entered it, and its source with tier (primary · reporting · aggregator · AI summary — not evidence). The FT2 protocol sets no two-source rule; figures from reporting sources are marked "check vs primary" until checked.
> This file is the PI's log; a chair may prepare an entry, the PI enters it.

## A. Scored series — monthly readings in the window

| # | Date entered | Entered by | Series | Reading | Source · tier | Status |
|---|---|---|---|---|---|---|
| A-1 | 2026-11-26 | PI (prepared by Chair 2) | R: S&P monthly average, Nov 2026 | resolves 30 Nov 2026; month to date 7,537.39 at registration (§6.1) | §6.1 · as registered | open — enter at month end |
| A-2 | 2026-11-26 | PI (prepared by Chair 2) | BAA−AAA, Nov 2026 | not yet published (Oct 2026: 0.47 pp, §6.1) | FRED BAA, AAA · primary | open |

## B. Positions (§6.2)

| # | Date entered | Entered by | Statement |
|---|---|---|---|
| B-1 | 2026-11-26 | PI | No change since registration: no position in ANT or NVDA, and no plan to acquire one. |

## C. Deviations from the protocol after registration

| # | Date | Deviation | Reason |
|---|---|---|---|
| D-1 | 2026-11-26 | The event log was opened nine days after registration (protocol line 5: "Event log: to be assigned"; it was not). Entries dated 17–26 Nov in sections D and E were transferred on 26 Nov from contemporaneous notes kept by Chair 2 at the PI's request, each with the date it was originally recorded. No effect on hypotheses H1a–H7, resolution rules or the failure rule. | The log had no file; the gap is stated rather than back-filled silently. Entered on the PI's decision of 26 Nov, prepared by Chair 2. |

## D. Shock log (§6.4 — not scored)

| # | Date of shock | Date entered | Type | Shock | Days to backstop | Source · tier |
|---|---|---|---|---|---|---|
| S-1 | 2026-11-23 | 2026-11-26 (noted 24 Nov) | Single-node (key person) + policy action | Nvidia's board reinstates CEO Jensen Huang, 11 days after his resignation, after "input from senior levels of the United States government"; the President says he spoke to the directors. S&P +4.7%, Nasdaq +6.5%, NVDA +31% that day. | 0 (the act was itself the backstop) | WSJ 23–24 Nov; BBC 24 Nov · reporting |
| S-2 | 2026-11-24 | 2026-11-26 (noted 24 Nov) | Geopolitical / war | US investigates Iran (Russia also suspected) for cyberattacks on up to 50 tankers carrying oil, LPG and chemicals | — | WSJ The 10-Point, 24 Nov · reporting |
| S-3 | 2026-11-24 | 2026-11-26 (noted 24 Nov) | Policy action | Commerce preparing to blacklist Megaspeed (Singapore Nvidia customer) over suspected chip diversion | — | BBC 24 Nov · reporting |
| S-4 | 2026-11-25 | 2026-11-26 | Policy action | Section 301 tariffs proposed on 14 partners (China up to 20% on top of ~25%; EU, Japan, Korea, Taiwan, India and others), "structural overcapacity"; preliminary, no effective dates. Nasdaq fell >4% early, closed −0.6%. | — | Al Jazeera, NBC, 25 Nov · reporting |
| S-5 | 2026-11-25 | 2026-11-26 | Infrastructure outage | Microsoft declares "Code Red" after a large Outlook / Microsoft 365 outage | — | The Verge, 25 Nov · reporting |
| S-6 | 2026-11-26 | 2026-11-26 | Policy action + supply | US closes a loophole giving Chinese firms access to Nvidia chips; Nvidia reported to halt server shipments to Southeast Asia | — | WSJ, Barron's headlines, 26 Nov · reporting (headlines only, not read) |
| S-4a | 2026-11-25 | 2026-11-27 | Policy action (follow-up to S-4) | The Section 301 tariffs "could go into effect in January" — S-4's "no effective dates" is superseded | — | WSJ (G. Bade), 25 Nov · reporting |
| S-7 | 2026-11-27 | 2026-11-27 | Policy action (regulatory) | Monero (XMR) −11.1% intraday after KuCoin delists it ahead of the EU anti-money-laundering rules on privacy coins (second delisting in a row); Zcash (ZEC) +3.5% the same session | — | WSJ crypto screen (PI, 27 Nov); CoinDesk, FinScans, TokenPost 27 Nov · reporting |

## E. Context entries — not scored

| # | Date of event | Date entered | Entry | Source · tier |
|---|---|---|---|---|
| E-1 | 2026-11-18 | 2026-11-26 (noted 18 Nov) | ANT IPO priced: 980M shares at $83 (range $70–78), $81.3bn, largest on record; 20% retail | CNN Business · reporting |
| E-2 | 2026-11-19/20 | 2026-11-26 (noted 20 Nov) | ANT day 1 close $97.17 (open $111.67); day 2 close $88.91; intraday low $83.05; the $83 IPO price not breached on a close | Refinitiv quote cards (PI) · primary, 15-min delayed |
| E-3 | 2026-11-20 | 2026-11-26 (noted 21–22 Nov) | Closes: Dow 48,147.33; S&P 500 6,910.39 (week −8.61%); Nasdaq Comp 22,617.73 (week −10.02%); Nasdaq-100 19.84% below its 6 Oct record | PI screenshot; WSJ print weekly table · reporting, check vs primary |
| E-4 | 2026-11-13 → 24 | 2026-11-26 | ICE BofA OAS (daily): HY 3.23 → 3.34 → 3.43 → 3.47 → 3.52 → **3.76** (20 Nov) → 3.63 → 3.72 (24 Nov); IG 0.89 → 0.98; CCC 13.16 → 14.05 (24 Nov, highest in the 3-year FRED series) | FRED / ALFRED · primary |
| E-5 | 2026-11-20 | 2026-11-26 (noted 22 Nov) | Chair 2 reading: perception flipped (S&P −8.61% wk; Dow neckline broken 17 Nov); structure not yet (HYG, LQD at premiums to NAV). Marker: HY above 3.94% = stress reaching the middle of credit | [CAM]; threshold from Trefis, 17 Nov · reporting |
| E-6 | 2026-11-25 | 2026-11-26 | Closes: Dow 50,182.95 (+0.33%), S&P 7,182.78 (−0.25%), Nasdaq 23,585.80 (−0.62%); Q3 GDP revised sharply higher; Oct PCE 3.8% | WSJ market table (PI); WSJ, Al Jazeera · reporting |
| E-7 | 2026-11-19 | 2026-11-26 | First Xi–Trump–Putin trilateral summit, Shenzhen (APEC) | SCMP · reporting |
| E-8 | 2026-11-26 | 2026-11-26 | Chair 2 tests (descriptive, not scored, not forecasts): credit-run signal 2 hits of 5 vs 12% base rate, no reliable lead; cash legs, no reliable lead; eve comparison with 2000/2007/2020/2021/2025: broad credit calm, VIX high, Fed reverse repo $0.3bn | [CAM]; FRED · primary data |
| E-9 | 2026-11-25 | 2026-11-27 | "The AI-driven market rout shows how much higher the bar has risen for the central bank to step in" — the Fed is not signalling a backstop | WSJ (N. Timiraos), 25 Nov · reporting |
| E-10 | 2026-11-24 | 2026-11-27 | China to suspend some critical-material export curbs to the US until January — January deadlines now on both sides (see S-4a) | WSJ headline, 24 Nov · reporting (headline only, not read) |
| E-11 | Q3 2026 (reported 2026-11-27) | 2026-11-27 | France in recession in Q3 as exports sag (heat waves slowed Airbus) | WSJ (M. Dalton), 27 Nov · reporting, check vs INSEE |
| E-12 | 2026-11-27, 11:29 Toronto (half-day session) | 2026-11-27 | Intraday vs Wed close: Dow 50,674.69 (+0.98%), S&P 500 7,267.81 (+1.18%), Nasdaq 23,967.53 (+1.62%). Week to date vs 20 Nov close (E-3): Dow +5.2%, S&P +5.2%, Nasdaq +6.0% — about 55% of the 13–20 Nov fall recovered. Intraday, not a close | WSJ market screen (PI); raw in SNAPSHOTS.csv row-date 2026-11-27 · reporting |
| E-13 | 2026-11-27, intraday | 2026-11-27 | Treasuries: bear steepener — 2y +4 bp (4.693%), 10y +6 bp (4.926%), 30y +7 bp (5.322%). Bills rise with maturity (1m 4.175% → 1y 4.592%): no cut priced. Price-change column inconsistent with yields; yields used | WSJ bonds screen (PI) · reporting |
| E-14 | 2026-11-27, intraday | 2026-11-27 | Metals bid, energy down: silver +8.8%, gold +3.2% (3,648.40), copper +3.0%; Brent −1.3%, natural gas −4.2%; Bitcoin −1.2%. [CAM] reading: reflation or pre-tariff buying, not a flight to safety. Half-day thin volume — confirm at Monday's close | WSJ commodities and crypto screens (PI) · reporting; reading [CAM] |
| E-15 | 2026-11-27, intraday | 2026-11-27 | FX: no safe-haven bid (USD/CHF +0.22%, USD/JPY +0.17% to 159.54, near 160); DXY +0.35% led by EUR −0.26%, broad WSJ Dollar Index +0.09%; yuan firmer (USD/CNY 6.6594) despite the tariff plan; USD/CAD flat 1.4249 | WSJ currencies screen (PI) · reporting |

## F. Known future events (§6.4)

| # | Date entered | Event | Note |
|---|---|---|---|
| F-1 | 2026-11-26 (logged in protocol 16 Nov) | ANT lock-up expiry, about 180 days after listing (listing 19 Nov 2026 → about mid-May 2027; date set by the final prospectus) | Scheduled supply event, so it cannot be called a surprise |
