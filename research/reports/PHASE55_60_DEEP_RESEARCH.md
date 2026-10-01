# Phase 55-60 — Exact SALMA Anatomy, Sequence Structure and Risk Geometry

## Date
2026-10-01

## Purpose
Deep exploratory research on the current Apr-Sep 2026 NIFTY futures dataset after the exact SALMA formula audit. No historical finding in this phase is promoted to a live rule.

## 1. Exact SALMA anatomy
On 8,594 current-research futures candles, SALMA-B0's close lies outside its WMA5 +/- 0.30*population-SD5 band on about 80.6% of usable bars. This means the clipping mechanism is frequent, not an occasional outlier correction.

SALMA and an unclipped double-WMA(10,3) are highly correlated (~0.9999), with slope-state agreement ~91.2% on usable bars. Most of the line is therefore a generic smoothed state; the distinctive component is the nonlinear clipping and small timing shifts.

## 2. Exact H-M1 target hazard
Across 139 exact H-M1 events (73 discovery, 66 validation), target-first 2R rates by elapsed bars were:

Validation:
- 1 bar: 5.0%
- 3 bars: 12.2%
- 5 bars: 15.1%
- 10 bars: 27.3%
- 15 bars: 28.1%
- 20 bars: 30.2%

This is about the same as controls through 5 bars but separates more strongly after 5 bars. The 3R curve shows the same delayed separation.

Interpretation: H-M1 is better described as a delayed expansion/persistence condition than an immediate momentum trigger.

## 3. Clipping-count gradient inside H-M1
Validation H-M1:
- 0 aligned clips: n=2, mean R2 -1.000
- 1 aligned clip: n=10, -0.700
- 2 aligned clips: n=22, +0.024
- 3 aligned clips: n=32, +0.388

Discovery shows a similar ordering. The small 0/1 buckets prevent strong inference, but the pattern motivates the continuous clipping-pressure model.

## 4. H-M6
H-M1 + >=2 direction-aligned clipping bars:
Validation n=54, mean R2 +0.240, R3 +0.225, 20-bar signed return +1.454 ATR, MFE 2.990 ATR, MAE 1.497 ATR.

Within H-M1, H-M6 versus H-M1-not-H-M6 is especially separated, but the latter group is only n=12 in validation. Therefore H-M6 remains exploratory.

## 5. H-M8 continuous clipping pressure
A fixed Apr-Jun -> Jul-Sep logistic model over H-M1 events:
- base causal features AUC 0.611
- + continuous clipping pressure AUC 0.623
- + clipping count AUC 0.582

A residualized pressure test retained AUC ~0.619.

Thus continuous pressure is more useful than a crude count in the small meta-model, although the incremental gain is modest and not yet validated.

## 6. Sequence anatomy
The most interesting sequence found is H-M9:
- causal compression-release breakout;
- direction-aligned SALMA flip exactly 2 completed bars before breakout;
- all three immediately preceding bars directionally clipped by the SALMA band.

Futures:
- discovery n=15, mean R2 +0.854, R3 +0.526;
- validation n=10, mean R2 +0.543, R3 +0.324.

The sequence improves on the broader H-M1 subset whose flip is exactly 2 bars before the breakout. However, n=10 validation is too small for inference.

A broader sequence observation is that SALMA + unclipped double-WMA agreement is associated with better H-M1 outcomes than SALMA-only events. In validation, the agreement group had mean R2 +0.129 versus -0.250 for SALMA-only events. This suggests the core may be a smoothed-state transition that is strengthened by clipping persistence, not SALMA color alone.

## 7. H-M9 path behavior
For the 10 validation H-M9 events:
- 2R target-first 30%
- 1.5R target-first 50%
- 3R target-first 10%
- mean MFE 1.58 ATR
- mean MAE 1.44 ATR
- mean 20-bar signed return +0.388 ATR

The small validation count makes the mean unstable. H-M9 is therefore not a validated setup.

## 8. Risk surface
For H-M6, pooled validation mean R remained positive over the tested grid of stop widths 0.75-2.0 ATR and target multiples 1.0-4.0R. The positive region was broad, but contract-level means differed materially and only three contracts are in validation. This is evidence of a risk-geometry effect, not proof of a profitable execution strategy.

## 9. Cross-era index sequence
Applying the same H-M9-style sequence to the independent NIFTY index 2015-2021 dataset produced:
- all-period sequence n=313, mean R2 +0.361 vs +0.171 control;
- 2019-2021 sequence n=117, mean R2 +0.385 vs +0.185 control;
- 2019-2021 sequence target-first 34.2% vs 30.4% control.

This transfer result is encouraging for the sequence structure but is not a substitute for futures validation because the instrument and era differ, and the index data lacks usable volume/OI.

## 10. Current interpretation
The project is now converging on a richer causal description:

compression/balance
-> repeated directional pressure relative to a short volatility envelope
-> smoothed-state transition
-> range release
-> multi-bar directional expansion.

SALMA may therefore be valuable because its nonlinear clipping helps expose a short-lived pressure/transition state. The indicator is probably not a complete alpha engine.

## 11. Next scientific gate
Do not alter SALMA-B0 or promote H-M6/H-M8/H-M9 based on these results.

Next priority:
1. Freeze H-M9 as an exploratory sequence.
2. Build an unbiased forward event logger for H-M1/H-M6/H-M9.
3. Obtain any legitimate unseen actual NIFTY futures data when available.
4. Compare H-M1/H-M6/H-M9 against generic smoother controls on the same unseen events.
5. Keep risk/execution optimization locked until the signal mechanism survives unseen data.

Status:
- H-M1: PROMISING, NOT VALIDATED
- H-M6: STRONG EXPLORATORY, NOT VALIDATED
- H-M8: EXPLORATORY, NOT VALIDATED
- H-M9: EXPLORATORY, NOT VALIDATED
