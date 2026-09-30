# SALMA Exact Formula Audit — 2026-09-30

## Why this audit was required
The supplied Pine code uses ta.stdev(price, sd_len) without explicitly passing the optional biased argument. TradingView documents the biased option as defaulting to true, which uses the population-style estimator. Earlier local exploratory calculations used sample standard deviation in parts of the pipeline. This audit repairs that discrepancy.

## Canonical reconstruction
- Source close
- length 10
- smooth 3
- width 0.30
- SD length 5
- population rolling standard deviation (ddof=0)
- confirmed close-bar state changes only

## Results
On 8,594 actual NIFTY futures 5-minute candles, exact B0 produces 816 confirmed transitions (410 up, 406 down).

Earlier 813-event SALMA-specific artifacts are superseded.

## H-M1 rebaseline
The frozen price-event universe remains 513 official events after excluding July contract warm-up rows.
Exact SALMA gives:
- Discovery Apr-Jun: 73 H-M1 candidates
- Validation Jul-Sep: 66 H-M1 candidates

Validation H-M1 versus non-H-M1 control:
- R2 mean: +0.060 vs -0.072
- R3 mean: +0.063 vs -0.111
- 20-bar signed return: +1.000 vs +0.010 ATR
- MFE: 2.693 vs 2.060 ATR
- MAE: 1.722 vs 2.006 ATR

The movement-persistence direction survives the audit, while the fixed 1ATR/2R executable effect remains small and uncertain.

## H-M6
H-M6 adds at least 2 of the previous 3 direction-aligned SALMA clipping bars.

Validation:
- n=54
- R2 +0.240
- R3 +0.225
- 20-bar signed return +1.454 ATR
- MFE 2.990 ATR
- MAE 1.497 ATR

Compared with non-H-M1 controls:
- R2 delta +0.312R
- R3 delta +0.336R
- 20-bar signed-return delta +1.443 ATR

Day-cluster bootstrap:
- R2 delta 95% CI about [-0.026, +0.714]
- R3 delta 95% CI about [-0.092, +0.808]
- 20-bar signed-return delta 95% CI about [+0.380, +2.888] ATR

## Interpretation
The strongest current SALMA-specific hypothesis is H-M6, but it is still post-hoc and unvalidated. The research should not be optimized further on Apr-Sep.

## Next gate
Use genuinely unseen actual NIFTY futures data or forward paper observations. Test frozen H-M1, H-M6, and generic smoother controls under identical definitions.

Reference: TradingView Pine Script language/reference documentation.
