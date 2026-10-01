# Phase 57-58 — SALMA Sequence Anatomy and Cross-Era Test

## Date
2026-10-01

## Scope
These are exploratory analyses after H-M1/H-M6 freezing. No rule is promoted to live use.

## 1. SALMA clipping is frequent
On the exact Apr-Sep 2026 futures reconstruction, close was outside the SALMA WMA5 +/- 0.30*population-SD5 band on about 80.6% of usable bars. Up-clipping was about 40.0%; down-clipping about 40.6%.

Interpretation: SALMA's clipping is not an occasional outlier operation in this configuration. It is a frequent nonlinear deformation of the source price before smoothing.

## 2. SALMA is very close to a generic smoothed state
The exact SALMA and an unclipped double-WMA(10,3) are correlated about 0.9999 in the current futures sample. Their slope-state direction agrees on about 91.2% of usable bars.

Therefore a large part of the SALMA color behavior is a generic smoothed-state effect. SALMA's distinctive contribution is in the nonlinear clipping/deformation and small timing differences.

## 3. H-M1 lifecycle
Exact H-M1 validation target-first hazard for 2R:
- by 1 bar: 5.0% candidate vs 2.4% control
- by 3 bars: 12.2% vs 10.7%
- by 5 bars: 15.1% vs 15.2%
- by 10 bars: 27.3% vs 19.8%
- by 15 bars: 28.1% vs 21.9%
- by 20 bars: 30.2% vs 23.3%

This reinforces that H-M1 is not primarily an immediate-momentum signal. Its incremental value appears later in the post-breakout lifecycle.

For 3R:
- by 5 bars: 9.4% vs 4.3%
- by 10 bars: 13.7% vs 8.6%
- by 20 bars: 18.0% vs 12.6%

## 4. H-M6 within H-M1
Within exact H-M1 candidates:
- Validation clip count 0: n=2, R2=-1.000
- clip count 1: n=10, R2=-0.700
- clip count 2: n=22, R2=+0.024
- clip count 3: n=32, R2=+0.388

Discovery shows the same ordering with a stronger top bucket.

This supports an intensity/sequence hypothesis but is not sufficient for validation because the low-count buckets are tiny and the threshold is post-hoc.

## 5. A particularly interesting sequence
A specific sequence found during exploratory decomposition is:
- compression-release breakout
- direction-aligned SALMA flip exactly 2 completed bars before the breakout
- direction-aligned SALMA clipping on each of the 3 bars immediately before the breakout

Discovery Apr-Jun:
- n=15
- mean R2 +0.854
- mean R3 +0.526
- 2R target-first 53.3%
- 3R target-first 26.7%

Validation Jul-Sep:
- n=10
- mean R2 +0.543
- mean R3 +0.324
- 2R target-first 30.0%
- 3R target-first 20.0%

Compared with all H-M1 events whose flip was exactly 2 bars before the breakout, the sequence improves mean R2 from +0.695 to +0.854 in discovery and from +0.221 to +0.543 in validation.

This sequence is small and post-hoc. It is a candidate for forward/holdout testing, not a strategy.

## 6. Cross-era index transfer
The same exact sequence was tested on the long 2015-2021 NIFTY index dataset as a separate generalization test.

2019-2021 test:
- sequence n=117
- mean R2 +0.385
- 2R target-first 34.2%
- 20-bar directional return +0.412 ATR
- MFE 2.794 ATR
- MAE 0.303 ATR
- non-sequence control n=2,792
- control mean R2 +0.185
- control 2R target-first 30.4%

This is encouraging but not decisive. The index is not futures, the dataset has no usable volume/OI, and year-level behaviour is heterogeneous (2017-2018 had weaker terminal-direction effects). Therefore this is transfer evidence, not futures validation.

## 7. New interpretation
The strongest current causal story is:

compression/balance
-> repeated directional pressure outside a narrow robust band
-> smoothed-state transition
-> range release
-> sustained movement

The exact sequence may therefore be more fundamental than the green/red color itself.

## Research governance
- H-M1 remains frozen.
- H-M6 remains exploratory.
- H-M8 remains exploratory.
- The exact 2-bar + 3-clipping sequence is exploratory (call it H-M9).
- No in-sample tuning against Apr-Sep is authorized before unseen/forward testing.
