# Daily market snapshots — Field Test 2 (context, not scored)

Opened 2026-11-27 at the PI's decision. Purpose: a same-method daily series, so patterns are read from the series rather than from one screen.

Rules:
1. **Same time each day** — about 11:30 AM Toronto. A different time is logged as such in `time`.
2. **Raw first, readings apart.** `SNAPSHOTS.csv` holds the figures exactly as shown on the source screen, nothing derived or corrected. Readings ([CAM] or [R]) go in EVENT_LOG.md, never in the CSV.
3. **Same screens each day** — indexes, bonds, currencies, crypto, commodities (WSJ Markets). A missing screen is noted as missing, not filled in.
4. One row per instrument per day. Corrections are new rows with a note, never edits to old rows.

Tier: reporting (WSJ market data, delayed). Not scored under the protocol; no hypothesis depends on it.
