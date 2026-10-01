# Autonomous SALMA Deep Analysis — Phase 76
Date: 2026-10-01

## Purpose

This checkpoint continues the frozen NIFTY/SALMA research autonomously. It does **not** modify H-M1, H-M6, H-M8 or H-M9. It focuses on lifecycle, independence, model-family robustness and mechanism decomposition.

## Data actually used

- Exact current NIFTY futures event universe: 513 frozen price-defined events from Apr-Sep 2026.
- Exact SALMA-B0 reconstruction: Close / Length 10 / Smooth 3 / Width 0.30 / SD5, population SD (`ddof=0`).
- H-M1: 139 exact events = 73 discovery + 66 validation.
- H-M6: 118 exact events = 64 discovery + 54 validation.
- H-M9: 25 exact events = 15 discovery + 10 validation.
- Phase55 supplies the independent event-level barrier times at 1R/1.5R/2R/3R.
- The 2015-2021 NIFTY index dataset remains a transfer/mechanism dataset, not a futures holdout.
- The missing independent futures holdout remains Oct 2025-Mar 2026 actual monthly NIFTY futures 5-minute contract data.

## 1. H-M1 competing-hazard result

At the frozen 2R barrier, cumulative target-first incidence in validation separates late rather than immediately:

| Horizon | H-M1 target-first | Control target-first | Difference |
|---|---:|---:|---:|
| 1 bar | 6.1% | 3.7% | +2.4 pp |
| 3 bars | 10.6% | 13.2% | -2.6 pp |
| 5 bars | 16.7% | 18.5% | -1.9 pp |
| 10 bars | 25.8% | 22.2% | +3.5 pp |
| 15 bars | 25.8% | 25.4% | +0.4 pp |
| 20 bars | 28.8% | 27.0% | +1.8 pp |

The stop-first incidence is generally lower for H-M1, but the differences are not large enough to establish a robust fixed-2R trading advantage. The lifecycle evidence continues to point more strongly to **delayed movement persistence** than to immediate breakout momentum.

Across all 513 events, the corresponding final target-first rates at 20 bars are:
- 1.5R: H-M1 39.6% vs control 30.7%
- 2R: H-M1 30.2% vs control 23.3%
- 3R: H-M1 18.0% vs control 12.6%

These are event-level descriptive rates; they do not replace the frozen execution benchmark.

## 2. Independence / non-overlap stress test

Selecting at most one event per 21-bar separation within each contract reduces the usable validation H-M1/H-M6 counts:

| Hypothesis | Validation events | Non-overlap events | Mean 2R R | 95% t CI |
|---|---:|---:|---:|---:|
| H-M1 | 66 | 51 | +0.006R | [-0.378, +0.390] |
| H-M6 | 54 | 41 | +0.178R | [-0.265, +0.621] |
| H-M9 | 10 | 10 | +0.543R | [-0.448, +1.534] |

The important change is that the broad H-M1 executable mean essentially collapses toward zero once overlapping events are removed. H-M6 retains a positive point estimate, but the interval remains wide. H-M9 is too small for inference.

This is consistent with the project governance note that event-level statistics can overstate effective sample size when signals cluster in the same local market episode.

## 3. Direction-matched H-M6 result

In Jul-Sep validation, using controls with the **same breakout direction**:

| Direction | H-M1 delta R2 | H-M6 delta R2 | H-M6 delta 20-bar return |
|---|---:|---:|---:|
| Down | +0.182R | +0.353R | +2.226 ATR |
| Up | +0.069R | +0.255R | +0.316 ATR |

This is a useful mechanistic result. The clipping condition does not merely select the bearish subset: relative to direction-matched non-H-M1 events, H-M6 remains positive in both directions. It therefore looks more like a **pressure-strengthening interaction** than a simple long/short asymmetry filter.

The estimate is still exploratory because the 2026 sample contains only three validation contracts.

## 4. Contract heterogeneity

H-M6 vs non-H-M1 control R2 deltas by contract:

| Contract | Split | H-M6 events | Delta R2 |
|---|---|---:|---:|
| Apr | D | 19 | +0.228 |
| May | D | 28 | +0.377 |
| Jun | D | 17 | +1.154 |
| Jul | V | 12 | +0.174 |
| Aug | V | 14 | -0.016 |
| Sep | V | 28 | +0.559 |

Five of six contract-level point estimates are positive; August is essentially flat. The effect is therefore not literally identical across contracts, but it is not explained by a single contract either.

## 5. Model-family check

For the H-M1 event set, a discovery-trained fixed-specification model predicting 2R target-first on validation gave:

| Model | Feature set | AUC | Brier |
|---|---|---:|---:|
| Logistic | generic causal features | 0.490 | 0.216 |
| Logistic | + SALMA clipping pressure | 0.630 | 0.206 |
| Random forest | generic causal features | 0.611 | 0.201 |
| Random forest | + SALMA clipping pressure | 0.610 | 0.207 |
| HistGradientBoosting | generic causal features | 0.510 | 0.234 |
| HistGradientBoosting | + SALMA clipping pressure | 0.597 | 0.207 |

The robust qualitative signal here is **not** “all models agree”. Rather:
- the fixed logistic model sees useful incremental information from continuous clipping pressure;
- the tree models do not show the same incremental improvement;
- therefore the evidence supports a simple, approximately monotonic pressure relation more than a highly nonlinear interaction that generalizes automatically.

A paired day-cluster bootstrap of validation AUC for pressure-vs-base logistic gave an observed +0.140 AUC difference with 95% interval approximately [-0.074, +0.343]. Thus the model result is promising but not statistically decisive.

## 6. Time-dependent model test

The same fixed discovery-trained logistic framework was used to predict whether 2R was reached **by** each horizon.

| 2R reached by | Base AUC | + pressure AUC | Approx. 95% CI for AUC gain |
|---|---:|---:|---:|
| 1 bar | 0.423 | 0.504 | [-0.068, +0.537] |
| 3 bars | 0.550 | 0.724 | [-0.127, +0.467] |
| 5 bars | 0.550 | 0.673 | [-0.078, +0.320] |
| 10 bars | 0.505 | 0.618 | [-0.081, +0.291] |
| 15 bars | 0.508 | 0.591 | [-0.104, +0.264] |
| 20 bars | 0.490 | 0.630 | [-0.071, +0.341] |

This is perhaps the most informative model result in the checkpoint: the pressure feature adds its strongest discrimination around the **3–10 bar lifecycle**, while the fixed 2R trading result is still noisy. That matches the broader interpretation that the mechanism is a delayed expansion process.

## 7. Feature ablation inside H-M1

Fixed discovery -> validation logistic:

| Variant | AUC | Brier |
|---|---:|---:|
| Base causal geometry | 0.490 | 0.216 |
| + flip distance | 0.478 | 0.218 |
| + clip count | 0.588 | 0.226 |
| + continuous pressure | 0.630 | 0.206 |
| + count + pressure | 0.629 | 0.217 |
| + all three | 0.614 | 0.225 |

This reinforces a subtle point: **the continuous clipping magnitude carries more transferable information than the binary flip-distance or raw clip-count feature in this small validation sample.**

## 8. H-M9 re-evaluation

H-M9 (exactly two-bar flip lag + all three preceding bars clipped) remains a small sequence:
- discovery n=15
- validation n=10
- validation mean R2 +0.543R
- validation 2R target-first 30%

The factorial decomposition of H-M1 events shows why this should not yet be promoted. In validation, flip distance = 2 with clip count = 3 has n=10 and mean R2 +0.543, but neighboring cells also contain positive outcomes. The evidence is therefore stronger for **persistent clipping pressure** than for an exact two-bar lag as a separately causal parameter.

Under a non-overlap selection, H-M9 still has only 10 validation observations and a wide [-0.448, +1.534] t interval.

## 9. H-M12 OI extension

The post-hoc H-M12 extension (H-M6 + aligned prior-3 price movement + OI build) remains descriptive:
- Discovery n=16 in the exact reconstruction.
- Validation n=12.
- Validation mean R2 +0.337R.
- Validation 20-bar signed return +3.023 ATR.
- Validation MFE 4.542 ATR; MAE 1.135 ATR.

This is not independent evidence because the feature was formed after inspecting the validation period. It should remain frozen only for future observation.

## 10. Overall scientific interpretation

The current evidence increasingly supports the following abstraction:

**compression/balance -> repeated directional pressure outside a narrow robust envelope -> smoothed-state transition -> range release -> delayed directional expansion**

The new model work adds an important distinction:
- continuous clipping pressure appears more informative than a hard clip-count threshold;
- the information is concentrated in the H-M1-conditioned event set;
- the same evidence is much weaker when attempting to predict every base breakout;
- fixed-2R execution remains materially noisier than movement-persistence prediction.

Thus the current research target should remain the **mechanism**, not an optimized trading rule.

## 11. Decision and next gate

No H-M1/H-M6/H-M8/H-M9 parameters are changed.

The Apr-Sep 2026 historical corpus is now exhaustively mined enough for the current research question. Further in-sample search would mainly increase selection bias.

The next decisive evidence must be genuinely unseen actual NIFTY futures 5-minute contract data. The preferred missing window remains **October 2025 through March 2026**, with contract identity and OHLC; OI is strongly preferred for testing the existing H-M12 extension.

Once that dataset exists, the frozen tracks should be run in one pass:
1. H-M1
2. H-M6
3. H-M8 continuous pressure diagnostic
4. H-M9
5. generic smoother/envelope controls
6. non-overlap execution
7. contract/day-clustered uncertainty
8. realistic friction sensitivity

Until then, no current 2026 backtest result should be treated as a validated live edge.
