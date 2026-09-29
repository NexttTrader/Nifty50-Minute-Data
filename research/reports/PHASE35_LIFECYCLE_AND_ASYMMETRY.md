# Phase 35 — H-M1 Lifecycle, Directional Asymmetry and Risk Geometry

## Date
2026-09-30

## Scope
H-M1 remained frozen. This phase is descriptive and diagnostic only; it does not change H-M1.

## Lifecycle
Validation H-M1 candidates (n=72) versus controls (n=183):
- 1 bar directional return: +0.078 vs -0.101 ATR
- 3 bars: +0.262 vs -0.037
- 5 bars: +0.537 vs -0.104
- 10 bars: +0.682 vs -0.029
- 20 bars: +1.004 vs -0.024
- 20-bar MFE: 2.843 vs 1.981 ATR
- 20-bar MAE: 1.729 vs 2.013 ATR

H-M1 therefore looks more like a delayed expansion/persistence state than a pure immediate-momentum signal.

## Delayed expansion
Validation:
- delayed 2R (after bar 5 but by bar 20): 25.0% candidates vs 18.0% controls
- +1R within 3 bars: 33.3% vs 35.5%
- MFE <1R in first 5 bars but >=2R by 20 bars: 11.1% vs 8.7%

The separation is stronger at longer horizons than at the first few bars.

## Directional asymmetry
Jul-Sep 2026 validation:
- Downward H-M1 events: n=39, 20-bar directional return +1.817 ATR, MFE 3.384, MAE 1.512, 2R target-first 30.8%.
- Downward controls: n=105, 20-bar directional return -0.135 ATR, MFE ~2.02, MAE ~2.02, 2R target-first 26.7%.
- Upward H-M1 events: n=33, 20-bar directional return +0.044 ATR, 2R benchmark mean approximately +0.072R.
- Upward controls: n=78, 20-bar directional return +0.126 ATR.

Within the validation period, most of the persistence effect is coming from downward breakouts.

## Prior-trend interaction
Using causal prior-20-bar return only for descriptive segmentation:
- Prior downtrend + downward breakout: H-M1 n=25, mean 20-bar return +2.226 ATR, benchmark R2 +0.442, target-first 40.0%, MFE 3.982, MAE 1.320.
- Same subgroup controls n=85: mean return -0.160 ATR, R2 -0.182, target-first 23.5%, MFE 2.027, MAE 2.053.
- Prior uptrend + upward breakout: H-M1 n=25, mean return -0.615 ATR, benchmark R2 -0.305, target-first 16.0%; controls n=60, +0.052 ATR, R2 +0.090, target-first 30.0%.

These are post-hoc descriptive findings with small subgroup counts. They must not be used as a new trading filter before holdout.

## Latent regime
KMeans regimes were fit only on Apr-Jun causal pre-event features and then assigned unchanged to Jul-Sep. One validation regime showed strong H-M1 separation, but the candidate sample there was only 7 events (K=3) or 8 events (K=4). This is evidence for a possible regime interaction, not an inference.

## New test hypothesis
**H-M2:** H-M1 may be regime- and direction-dependent; in 2026 it appears strongest in bearish/negative-direction compression-release events.

Status: **HYPOTHESIS ONLY — NOT VALIDATED.**

## Decision
Do not change frozen H-M1. H-M2 is reserved for unseen/forward testing only.
