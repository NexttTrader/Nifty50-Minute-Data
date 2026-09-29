# Phase 36 — Cross-Instrument Transfer Test

## Dataset
NIFTY 50 index, 5-minute OHLC, 114,830 rows, 1,537 dated sessions; 1,523 full 75-bar sessions used for regular-session testing; 2015-01-09 through 2021-03-25. Volume is zero and OI is unavailable, so the test is price-only.

## Purpose
Apply the frozen H-M1 sequence to a materially different instrument/era as a generalization check, not as final futures validation.

## Result
Direction-matched H-M1:
- candidate n=1,184
- control n=3,409
- 20-bar directional return: +0.191 ATR candidate vs +0.115 ATR control
- incremental difference: +0.076 ATR
- 2R benchmark mean R: -0.037 candidate vs -0.026 control
- 2R target-first: 30.5% vs 31.0%
- day-cluster bootstrap for the 20-bar return difference: 95% CI approximately [-0.190, +0.338] ATR; probability delta <= 0 about 0.289.

## Temporal stability
The movement effect was not stable across all years. It was negative in 2015-2016 and 2021 and positive in 2017-2020.

## Regime test
A K=3 model trained only on 2015-2018 event features and applied to 2019-2021 showed regime-dependent H-M1 effects. Some regimes had positive candidate-vs-control movement and 2R differences, others were negative. This reinforces conditionality rather than universality.

## Conclusion
H-M1 does not transfer as a robust fixed-1ATR/2R trading edge to long-history NIFTY index data. It shows a small directional-persistence effect, but the monetizable edge is not stable.

This does not invalidate H-M1 for NIFTY futures. It means the effect may be instrument- and regime-specific.
