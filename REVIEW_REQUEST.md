# Request for an adversarial review: BPNRDE Field Test 2

**To the reviewer:** this package was built by its proposers, Roland Marinov (the principal investigator) and Claude (an AI model made by Anthropic). Claude has a conflict of interest: the forward test covers a market cycle that includes the Anthropic IPO, reported for the week of 16 Nov 2026, with Nvidia and other chipmakers reported as cornerstone investors. Anthropic is therefore a node in the very network the model describes. Most of the checks Claude ran came out as "supporting" the model, and that is the reason for asking you.

**Your role is to try to break this, not to help it.** Agreement from you is of little use. Specific objections are what we need.

## What to read
1. `PROTOCOL.md`: the model (section 2), the rules (section 4), all back-test results (sections 5 to 5D), and the forward test (section 6).
2. `code/*.py` and `outputs/*.csv`, if you can run or read them.

## Questions, in order of importance

1. **Is the model falsifiable as written?** Name an outcome in 2026–27 that the protocol would count as a clear failure. If you can't find one, say where the escape routes are: conditional predictions, "untested" outcomes, or proposed-but-not-adopted amendments.
2. **Is the back-test circular?** The episodes, windows and rules were chosen by people who already knew the history. Which results would most likely change if a stranger set the rules? Pick the single weakest result in sections 5 to 5D.
3. **Are the proxies valid?**
   - The Point of No Return proxy is the BAA−AAA spread, with a 2-standard-deviation, 6-month rule.
   - The credit-inflow proxy is US bank loans, which cannot see private credit or vendor financing in the AI build.
   - The adoption measures: internet use, e-commerce share, Census BTOS AI use.
   For each, give the strongest reason it could mislead.
4. **What is missing?** Episodes, variables or mechanisms that a sceptical economist would say decide the outcome. Section 5D.7 lists what we already know is missing; go beyond it.
5. **Are the forward predictions (H1a–H7) well-posed?** Check that each can be resolved from public data without judgment. Flag any that could be gamed, or resolved either way after the fact.
6. **Data:** most series are GitHub mirrors, and some rows were hand-entered from memory (marked `verified=no`). Which unverified figures, if wrong, would change a conclusion?
7. **Your own forecasts:** give your probabilities for H1a, H1b, H3, H4 and H5, independent of the PI's, with one line of reasoning each. Do not look at the probabilities recorded in section 7, item 12 before giving yours.
8. **Changes since the earlier reviews (section 7, items 8–12).** Check each one. In particular: (a) the 1929 credit-peak row was corrected from Oct to Sep 1929 using the Federal Reserve Bulletin (Jan 1930), which turned the weakest back-test result from a one-month miss into a tie. That correction favours the model. Is it sound, or is it the end-of-month convention doing convenient work? (b) H8 was dropped and the bubble asset made an interpretation. Is anything still in the test that was chosen after this week's events?
9. **Registration verdict:** register as is, register with named fixes, or do not register. One line of reasoning.
