# Phase 85 — Causal Residualization and Holdout Gate
Date: 2026-10-05

## Purpose

Continue the frozen SALMA/NIFTY research without changing H-M1, H-M6, H-M8 or H-M9.
This phase asks a narrower question:

> Is H-M6 adding information beyond ordinary pre-event price geometry, or is it mainly a compact label for unusually strong breakout/compression geometry?

No target, stop, entry, horizon, or SALMA parameter was optimized.

## Frozen research state

- 8,594 actual NIFTY monthly-futures 5-minute candles, Apr-Sep 2026.
- Exact audited event universe: 513 events; validation: 255.
- H-M1 and H-M6 definitions unchanged.
- Validation H-M6 = 54 events.
- Validation non-H-M1 control = 189 events.
- Primary delayed endpoint = frozen same-session 20-bar direction-adjusted return (`ret20atr`).

## 1. Raw H-M6 distribution: real separation, but tail-sensitive

Validation H-M6 vs non-H-M1 control:

| Statistic | H-M6 | Control |
|---|---:|---:|
| n | 54 | 189 |
| Mean ret20 ATR | +1.454 | +0.010 |
| Median ret20 ATR | +0.531 | -0.161 |
| 25th percentile | -0.878 | -1.251 |
| 75th percentile | +2.305 | +1.251 |
| 10%-trimmed mean | +0.676 | -0.074 |
| Wilcoxon vs 0 | p=0.021 | p=0.625 |

The two-sample Mann-Whitney test is significant at about p=0.026 and Cliff's delta is about +0.20.

The mean advantage is therefore not purely one gigantic observation, but the magnitude is clearly tail-sensitive: the median shift is much smaller than the mean shift.

## 2. Single-event and single-day sensitivity

The raw H-M6-minus-control mean ret20 delta is about +1.443 ATR.

Removing any one H-M6 event leaves the delta between about +1.114 and +1.529 ATR.

Removing any one entire validation day leaves the delta between about +0.935 and +1.540 ATR. July 8 is the most weakening day, but removing it does not eliminate the raw movement separation.

Thus the original movement effect is not literally a single-event or single-day artifact.

## 3. Discovery-trained causal-geometry model

To test incremental information rather than in-sample group means, a model was trained only on Apr-Jun discovery and evaluated on Jul-Sep validation.

Base features used only information available by event close:

- breakout direction
- prior direction-adjusted 5-bar return
- prior direction-adjusted 20-bar return
- prior 5-bar compression/range relative to causal ATR14
- event range relative to ATR14
- breakout strength relative to the prior 10-bar range
- time of day

A fixed Ridge model was trained on discovery and then frozen for validation.

### Continuous 20-bar movement prediction

| Validation set | Base model | Base + H-M6 |
|---|---:|---:|
| Full Jul-Sep Spearman | 0.106 | 0.146 |
| Full Jul-Sep MSE | 13.388 | 13.160 |
| Ex-Jul-8 Spearman | 0.106 | 0.135 |
| Ex-Jul-8 MSE | 10.699 | 10.661 |

The full-period improvement is small. After removing July 8, the MSE improvement becomes very small and the H-M6 residual advantage disappears.

A day-level bootstrap over the 24 validation days containing both H-M6 and control observations gives the H-M6 residual advantage:

- mean = +1.118 ATR
- median = +0.925 ATR
- positive-day share = 70.8%
- 95% bootstrap interval = [-0.061, +2.309] ATR
- bootstrap P(delta <= 0) = 0.032

This is supportive but still wide, and the result is based on only 24 common days.

## 4. Conditional OLS audit

A validation-only descriptive regression of ret20 on H-M6 plus the same causal geometry gives:

- H-M6 coefficient = +1.172 ATR
- day-cluster robust p = 0.260
- approximate 95% CI = [-0.866, +3.210] ATR

After excluding July 8:

- H-M6 coefficient = +0.208 ATR
- day-cluster robust p = 0.703
- approximate 95% CI = [-0.864, +1.281] ATR

This is the clearest warning from Phase 85:

**H-M6 does not yet demonstrate a stable incremental effect after ordinary price geometry is accounted for.**

## 5. Direct 2R prediction check

The discovery-trained logistic model predicts frozen 2R target-first outcomes.
Adding H-M6 to the causal-geometry feature set did not improve validation discrimination:

- AUC: 0.546 -> 0.535
- Brier score: 0.188 -> 0.192

This confirms the earlier project distinction:

**H-M6 is more closely associated with delayed movement magnitude than with a stable fixed-2R execution edge.**

## 6. Mechanism interpretation update

The most defensible interpretation is now:

**H-M6 is a state label for a particular compression/release geometry, not yet evidence of an independent SALMA alpha.**

The current evidence supports the existence of a delayed-expansion phenotype in the 2026 futures sample. It does not establish that the exact SALMA clipping threshold itself creates the effect.

This is consistent with the cross-era transfer result, where H-M6 preserved only weak movement persistence and no reliable fixed-R advantage.

## 7. Governance decision

1. H-M1 remains frozen.
2. H-M6 remains frozen as a research tag, not a promoted entry filter.
3. H-M8 continuous pressure remains diagnostic only.
4. No new thresholds or exclusions are promoted.
5. No Apr-Sep optimization continues.
6. The next decisive evidence is unseen actual futures data.

## 8. Forward-holdout gate

The October 2026 monthly contract is now active in current market listings as `NIFTY26OCTFUT`; public market data confirms it is trading, but the accessible public pages found in this phase do not provide an audited export of the required 5-minute OHLCV+OI series.

The next legitimate test is therefore the frozen forward capture of October futures:

- 5-minute OHLCV + OI
- exact SALMA-B0
- exact H-M1
- exact H-M6
- H-M8 pressure diagnostic
- same-session 1.5R/2R/3R and 20-bar outcomes
- non-overlap audit
- contract/day clustered uncertainty
- no rule changes during capture

## Final Phase 85 verdict

**Do not trade H-M6 as a standalone filter.**

The research target has become narrower and stronger:

> We are looking for a reproducible market-state transition in which compressed directional pressure is followed by a range release and delayed expansion. SALMA may measure that state, but the data does not yet prove SALMA is the cause.

October 2026 should now be treated as a genuine holdout/forward experiment, not another optimization sample.