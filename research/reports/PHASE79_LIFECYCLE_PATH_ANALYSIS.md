# Phase 79 — Lifecycle and First-Passage Path Analysis
Date: 2026-10-02

## Purpose

Determine where the H-M6 separation actually appears in the path after the frozen event, without changing H-M1/H-M6 definitions or optimizing execution.

This phase tests the existing interpretation that H-M6 is a delayed-expansion condition rather than an immediate breakout-momentum signal.

## Data

- Actual NIFTY monthly futures, 5-minute bars, Apr-Sep 2026.
- Official frozen event universe: 513 events.
- Discovery: 258; validation: 255.
- Exact H-M1: 139 events.
- Exact H-M6: 118 events.
- Validation H-M6: 54 events.
- Validation non-H-M1 control: 189 events.
- H-M1-but-not-H-M6 validation: 12 events.

For each event, the next same-session bars were evaluated using the frozen 1-ATR risk unit and direction-adjusted high/low excursions.

## 1. Validation lifecycle separation

| Metric | H-M6 | Non-H-M1 control | Difference |
|---|---:|---:|---:|
| MFE, 3 bars | 1.351 ATR | 0.898 ATR | +0.453 |
| MFE, 5 bars | 1.785 | 1.175 | +0.609 |
| MFE, 10 bars | 2.244 | 1.527 | +0.717 |
| MFE, 20 bars | 2.990 | 2.060 | +0.929 |
| MAE, 3 bars | 0.988 ATR | 0.945 ATR | +0.043 |
| MAE, 5 bars | 1.077 | 1.208 | −0.131 |
| MAE, 10 bars | 1.274 | 1.514 | −0.240 |
| MAE, 20 bars | 1.497 | 2.006 | −0.510 |
| 20-bar close return | +1.454 ATR | +0.010 ATR | +1.443 |

The important shape is temporal. At 3 bars H-M6 already has higher favorable excursion, but the larger separation appears at 5–20 bars. Adverse excursion is similar at 3 bars, then becomes lower for H-M6 from 5 bars onward.

This is stronger evidence for **path persistence / asymmetric continuation** than for immediate breakout follow-through.

## 2. First-passage competition

The frozen event path was treated as a competition between reaching a favorable level and reaching adverse 1R first.

Validation results:

| Favorable level | H-M6 favorable-first | Control favorable-first | Difference |
|---|---:|---:|---:|
| +1R | 57.4% | 45.0% | +12.4 pp |
| +1.5R | 42.6% | 35.4% | +7.1 pp |
| +2R | 37.0% | 30.2% | +6.9 pp |
| +3R | 27.8% | 21.7% | +6.1 pp |

At +1R, the point estimate is the clearest separation. At larger favorable levels the advantage remains positive but narrows.

The H-M6 adverse-1R hit rate was 72.2% versus 75.7% for controls, a −3.4 pp point difference. The uncertainty is large.

## 3. Clustered uncertainty

A day-cluster bootstrap over the 57 validation trading days was used for the first-passage comparisons.

| Metric | Observed H-M6 minus control | 95% cluster interval |
|---|---:|---:|
| +1R favorable-first rate | +12.4 pp | −1.7 to +26.1 pp |
| +1.5R favorable-first | +7.1 pp | −7.4 to +21.5 pp |
| +2R favorable-first | +6.9 pp | −7.0 to +20.2 pp |
| +3R favorable-first | +6.1 pp | −6.7 to +18.3 pp |
| Adverse 1R hit rate | −3.4 pp | −18.1 to +10.6 pp |

Therefore the path result is **directionally informative but not statistically decisive** at the available sample size.

## 4. H-M6 versus the H-M1 remainder

The within-H-M1 comparison is even more visually separated, but the validation remainder is only 12 events.

H-M6 minus H-M1-not-H-M6:

- MFE3: +0.650 ATR
- MFE5: +0.930 ATR
- MFE10: +1.147 ATR
- MFE20: +1.631 ATR
- MAE5: −0.223 ATR
- MAE10: −0.895 ATR
- MAE20: −1.241 ATR
- 20-bar close return: +2.495 ATR

Because only 12 validation events are in the H-M1-not-H-M6 remainder, this comparison is descriptive and not suitable for promotion.

## 5. Interpretation

Phase 79 changes the mechanistic emphasis:

**repeated directional clipping + recent state transition does not mainly predict the first few bars; it appears to identify events whose favorable path keeps extending while adverse excursion does not grow proportionally.**

This matches the earlier hazard work showing late 2R separation and the Phase 78 residual-model result showing that generic event geometry alone does not explain the full H-M1-conditioned behavior.

The evidence still does not establish that SALMA clipping is the unique causal mechanism. Cross-instrument transfer remains negative for H-M6/H-M8, and generic smoothers can condition similar state transitions.

## 6. Governance

No frozen H-M1/H-M6/H-M8/H-M9 definition changed.
No stop, target, holding-period, or threshold was optimized.
No live rule is promoted.

The next decisive gate remains genuinely unseen actual NIFTY futures data, preferably Oct 2025-Mar 2026 contract history with OI.

## Files

- PHASE79_PATH_SUMMARY.csv
- PHASE79_HM6_LIFECYCLE_COMPARISON.csv
- PHASE79_FIRST_PASSAGE.csv
- PHASE79_FIRST_PASSAGE_BOOTSTRAP.csv
- PHASE79_CONTRACT_COHORT_SUMMARY.csv
- phase_analysis.py
- bootstrap_first_fast.py

The event-level path table used during computation is treated as an intermediate reconstruction artifact; summary tables preserve the research outputs used for conclusions.
