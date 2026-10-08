# Phase 87 — Directional Interaction and Holdout Gate
Date: 2026-10-06

## Purpose
Continue the frozen SALMA/NIFTY research without changing H-M1, H-M6, H-M8 or H-M9.
This phase asks whether the apparent downside H-M6 anomaly remains an incremental effect after controlling for ordinary pre-event price geometry, and whether prior-path interaction provides a stable explanatory mechanism.

No threshold, entry, target, stop, or holding-period parameter was optimized.

## Data
- Exact Apr-Sep 2026 NIFTY futures research corpus: 8,594 five-minute candles.
- Frozen event universe: 513 events.
- Feature-enriched causal event table: 492 rows, because some early events lack the warm-up needed for 20-bar causal features.
- Discovery: Apr-Jun; validation: Jul-Sep.
- Validation feature-complete observations: 158.

## 1. Continuous prior-path interaction test

A fixed discovery-trained OLS model used:
- breakout direction;
- prior direction-adjusted 20-bar return;
- prior direction-adjusted 5-bar return;
- pre-5 range / ATR14;
- event range / ATR14;
- breakout strength;
- H-M6;
- a fixed H-M6 × prior-direction-adjusted-20-bar-return interaction.

Discovery -> validation result:
- interaction coefficient: approximately -0.023 (standardized feature units);
- discovery p-value: 0.944;
- validation rank correlation of predicted vs realized ret20: 0.137;
- validation MSE: 13.127.

The prior-path interaction therefore does not provide evidence of a stable nonlinear H-M6 effect in this small sample.

## 2. Direction interaction after geometry control

A second fixed discovery-trained OLS model added H-M6 × breakout-direction.

- interaction coefficient: approximately +0.173;
- discovery p-value: 0.759;
- validation rank correlation: 0.120;
- validation MSE: 13.238.

The model-implied H-M6 effect after geometry control was about +0.51 ATR for downside events and +0.86 ATR for upside events in the feature-complete validation set. These are model-implied conditional effects, not raw group means.

This is important because the raw validation asymmetry is very different: raw downside H-M6 has a much larger movement separation than upside H-M6. The conditional model does not reproduce that asymmetry reliably.

## 3. Direct 2R test with direction interaction

A discovery-trained logistic classifier using the same geometry features plus H-M6 and H-M6 × direction produced:
- validation AUC ≈ 0.519;
- validation Brier ≈ 0.195;
- validation 2R target-first base rate ≈ 24.1%.

This is weak and does not support a production trading classifier.

## 4. Interpretation correction

The earlier Phase 86 raw result remains descriptively important:
- downside H-M6 n=32, mean ret20 +2.160 ATR;
- same-direction control mean -0.066 ATR;
- raw delta +2.226 ATR.

However, Phase 85 already showed that H-M6 loses most of its incremental explanatory strength after controlling for ordinary causal geometry, especially after excluding July 8. Phase 87 strengthens that warning: neither a continuous H-M6 × prior-path interaction nor H-M6 × direction interaction is stable in a fixed discovery-trained model.

Therefore the research should NOT promote:
- a bearish-only H-M6 filter;
- a prior-trend threshold;
- a H-M6 × direction rule.

## 5. Current best scientific interpretation

The strongest defensible statement remains:

**A subset of 2026 NIFTY futures compression-release events associated with a recent SALMA state transition exhibits delayed directional expansion, but much of the apparent effect overlaps with ordinary event geometry. SALMA-specific incremental causality has not been established.**

The bearish concentration is a useful observation to monitor prospectively, but it is not yet a rule.

## 6. October 2026 data gate

Current public sources confirm that NIFTY26OCTFUT is an active NSE futures contract. GoCharting currently lists the contract with live volume and OI, but the accessible public result does not expose an audited 5-minute OHLCV+OI export. NSE's public historical contract-wise report is daily, with a maximum 90-day window, so it is not a substitute for the required intraday holdout. Accelpix documents a 5-minute OHLCV+OI endpoint, but it requires an API key.

Therefore the October holdout remains pending a legitimate 5-minute futures dataset.

## Governance decision

- SALMA-B0 frozen.
- H-M1 frozen.
- H-M6 frozen as research tag only.
- H-M8 remains diagnostic only.
- No bearish-only rule promoted.
- No prior-path threshold promoted.
- No Apr-Sep optimization continues.
- October remains untouched holdout.

## Next decisive experiment

Process October 2026 NIFTY26OCTFUT 5-minute OHLCV + OI in one frozen pass:
1. exact SALMA-B0;
2. exact H-M1;
3. exact H-M6;
4. continuous clipping pressure diagnostic;
5. frozen 1.5R/2R/3R outcomes;
6. 20-bar same-session movement;
7. 20- and 30-bar de-overlap;
8. direction-specific and prior-path reporting;
9. day/contract clustered uncertainty;
10. no rule changes from October outcomes.