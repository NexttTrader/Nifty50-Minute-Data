# Phase 84 — External Holdout Regime-Shift Diagnosis
Date: 2026-10-03

## Question

Why did the frozen H-M1/H-M6 sequence fail on the independent NIFTY26JANFUT archive when it had shown delayed-expansion behavior in Jul-Sep 2026?

This phase is explanatory only. It uses only pre-event features and does not fit or optimize any new trading rule on the external holdout.

## Data

Comparison:
- 2026 validation: exact H-M1 events from the frozen Apr-Sep 2026 futures corpus, n=66.
- External secondary holdout: NIFTY26JANFUT, n=26 H-M1 events.
- The external file covers 55 complete sessions from 2025-10-29 through 2026-01-16.

## Pre-event state comparison

| Feature | 2026 validation H-M1 | Jan-2026 external H-M1 |
|---|---:|---:|
| event range / ATR, mean | 1.740 | 1.452 |
| event range / ATR, median | 1.408 | 1.414 |
| clipping pressure, mean | 0.925 | 0.844 |
| clipping pressure, median | 0.705 | 0.682 |
| aligned clip count, mean | 2.273 | 2.346 |
| flip distance, mean | 1.788 | 1.808 |
| prior 1-bar return, mean | +0.041 ATR | +1.118 ATR |
| prior 3-bar return, mean | +0.335 ATR | +1.704 ATR |
| prior 5-bar return, mean | +0.326 ATR | +2.456 ATR |
| prior 10-bar return, mean | +0.307 ATR | +2.162 ATR |
| prior 20-bar return, mean | +0.071 ATR | +1.684 ATR |
| prior 5-bar return, median | +1.051 ATR | +2.461 ATR |
| prior 20-bar return, median | −0.308 ATR | +1.698 ATR |
| close location in prior 20-bar range, mean | +0.478 | −0.121 |
| close location in prior 20-bar range, median | +0.355 | +0.028 |

The most pronounced shift is not SALMA itself. It is the **state of the price path before the event**.

2026 H-M1 events generally occur after relatively modest prior directional displacement. In the external January sample, H-M1 events occur after substantial same-direction movement has already taken place:
- prior-5-bar movement is about 2.46 ATR on average versus 0.33 ATR in 2026 validation;
- prior-20-bar movement is about 1.68 ATR versus 0.07 ATR;
- the external prior-20 median is +1.70 ATR versus -0.31 ATR.

The January event is therefore often a **late-stage continuation/extension signal**, whereas many 2026 H-M1 events are closer to a transition out of balance/compression.

## Why this matters

This explains several otherwise puzzling Phase 82/83 results.

1. The H-M1 state transition itself can still occur, and clipping can still be high, without producing favorable subsequent movement if the underlying price path is already extended.
2. Continuous clipping pressure remains strongly associated with movement intensity on January data (pressure vs MFE20 Spearman +0.785 and pressure vs MAE20 +0.760), but that intensity is not directional tradeability: pressure can amplify both favorable and adverse excursion.
3. Fixed 1-ATR/2R execution is especially vulnerable when the breakout arrives late in an already extended move.
4. The 2026 H-M6 result may therefore be conditional on **compression-to-expansion geometry**, not simply on clipping count or SALMA transition.

## Important governance point

This does NOT justify adding a prior-return filter now.

The January holdout was observed before this interpretation was formulated, so using the holdout to choose a threshold would contaminate the independent sample.

The correct scientific action is:
- preserve H-M1/H-M6 exactly;
- record the regime-shift diagnosis;
- specify any future extension only before looking at its next unseen test sample;
- test that future extension on a fresh contract/data period.

## Research implication

The next reusable research abstraction is not “more clipping” but:

**state transition + range release + low prior extension**

versus

**state transition + range release after large prior displacement**.

The first may represent genuine expansion from balance; the second may represent a lagged signal after the move has already occurred.

This is a mechanistic hypothesis only. No new threshold is defined in Phase 84.

## Status

Phase 84 is an explanatory regime diagnosis, not a new trading rule and not a validation result.

The next decisive evidence remains another genuinely unseen actual futures contract. A second 5-minute contract with comparable depth is needed before making a multi-contract holdout statement.
