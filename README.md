# BPNRDE Field Test 2: The Bubble Cycle

A back-test of the BPNRDE bubble-cycle model on 1929, 2000, 2007, 2020 and 2022, plus a pre-registered forward test running to 31 Dec 2027.

- `PROTOCOL.md`: the pre-registration (DRAFT v0.9 until the PI registers it).
- `CODEBOOK.md`: the variables.
- `code/backtest.py`: rule-based event dating. Run from this folder with `python3 -I code/backtest.py` (needs pandas and numpy).
- `code/extensions.py`: base rates, false-positive scan, out-of-sample episodes and booms that did not burst (PROTOCOL 5A). Run it after backtest.py.
- `code/japan.py`: the Japan 1989 out-of-sample episode (PROTOCOL 5B).
- `code/full_episode.py`: full-episode US measures: fall to the final low, unemployment to its peak, property prices (PROTOCOL 5C).
- `code/blindspots.py`: real terms, real property drawdowns (US, Japan, Canada) and the Canada TSX episodes (PROTOCOL 5D).
- `REVIEW_REQUEST.md`: the brief for an outside, adversarial reviewer.
- `data/raw/`: the source files as pulled (checksums in `outputs/SHA256SUMS_raw.txt`).
- `data/manual/`: hand-entered series. **All are unverified until checked.**
- `data/derived/monthly_panel.csv`: the merged monthly panel.
- `outputs/`: the back-test results.
