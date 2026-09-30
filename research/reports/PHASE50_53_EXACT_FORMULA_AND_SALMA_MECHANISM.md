# Phase 50-53 — Exact Formula Repair and SALMA Mechanism Research

## Critical integrity repair
TradingView's Pine reference documents ta.stdev's optional biased argument as defaulting to true, i.e. a population-style estimator. Earlier research used sample SD in parts of the SALMA reconstruction. The canonical SALMA-B0 has been rebaselined to population SD (ddof=0). Earlier SALMA-specific artifacts are superseded.

## Exact B0
8,594 Apr-Sep futures candles; 816 confirmed transitions (410 up, 406 down).

## Exact H-M1
The price-defined base event universe remains 513 official events.
Exact SALMA:
- Discovery: 73 candidates
- Validation: 66 candidates

Validation H-M1:
- mean R2 +0.060 vs -0.072 control
- mean R3 +0.063 vs -0.111
- 20-bar signed return +1.000 vs +0.010 ATR
- MFE 2.693 vs 2.060 ATR
- MAE 1.722 vs 2.006 ATR

## H-M6
H-M1 + at least 2 of prior 3 direction-aligned clipping bars:
- Discovery n=64, R2 +0.359, R3 +0.384, ret20 +0.883 ATR
- Validation n=54, R2 +0.240, R3 +0.225, ret20 +1.454 ATR, MFE 2.990 ATR, MAE 1.497 ATR
- Validation vs non-H-M1 control deltas: R2 +0.312R, R3 +0.336R, ret20 +1.443 ATR
- Day-cluster bootstrap R2 CI about [-0.026,+0.714]; ret20 CI about [+0.380,+2.888] ATR.

## New H-M8
A continuous direction-aligned clipping-pressure feature adds information inside H-M1 events. A fixed discovery->validation logistic model improved validation AUC from 0.437 to 0.609 and slightly improved Brier score from 0.214 to 0.209. Expanding monthly walk-forward improved AUC in 3 of 4 months and mean AUC from 0.458 to 0.619. The effect is exploratory and uncertainty is still substantial.

## Mechanistic interpretation
The current evidence is more compatible with:
market compression-release event
+ recent SALMA state transition
+ persistence of price beyond SALMA's narrow volatility band
than with simple green/red reversal.

## Research governance
H-M1 and H-M6 remain frozen. H-M8 is exploratory. No further in-sample threshold tuning is permitted before unseen/forward testing.
