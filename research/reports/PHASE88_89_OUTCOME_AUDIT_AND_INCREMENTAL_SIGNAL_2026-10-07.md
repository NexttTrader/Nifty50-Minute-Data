# NIFTY / SALMA Research — Phase 88/89
## Outcome-engine audit, economic viability, and corrected incremental-signal test
Date: 2026-10-07

## Executive verdict

The benchmark outcome engine is now fully reconciled with the canonical audited event file.

All 513 canonical event outcomes are reproduced exactly (zero mismatches) when the following implementation is used:

- risk = ATR14 calculated from the **current event bar plus the prior 13 true ranges**;
- entry = **next bar open**;
- forward path = up to **20 subsequent 5-minute bars within the same trading session**;
- target/stop levels are anchored to the next-bar entry;
- same-bar target/stop collision = **stop first**;
- if no horizontal barrier is reached, the event is valued at the final available close inside that 20-bar/session window;
- MFE/MAE are measured from the next-bar entry over the same forward window.

This resolves the earlier apparent 31/513 discrepancy. The discrepancy was caused by using an ATR that excluded the event bar. At session opens, the event bar can contain a large overnight gap, so excluding it materially changes the risk denominator.

The important research conclusion is now sharper:

> **H-M1/H-M6 show a delayed-expansion/path-persistence relationship, but the evidence for a stable fixed-2R trading edge is materially weaker than the raw pooled event means suggest.**

## 1. Canonical benchmark reproduction

The canonical audited event table contains 513 events:

- Discovery Apr-Jun: 258
- Validation Jul-Sep: 255

The exact reimplementation matches, for all 513 events:

- R1.5
- R2.0
- R3.0
- out2.0
- out3.0
- ret20atr
- mfe20atr
- mae20atr

with zero mismatches.

This means the existing audited outcome table can be treated as authoritative for subsequent research.

## 2. Exact fixed-R economics

### Discovery Apr-Jun

| Group | n | Mean R2 | PF | 2R target-first |
|---|---:|---:|---:|---:|
| H-M1 | 73 | +0.218 | 1.418 | 31.5% |
| H-M6 | 64 | +0.359 | 1.763 | 35.9% |
| Non-H-M1 control | 185 | -0.166 | 0.750 | 19.5% |

### Validation Jul-Sep

| Group | n | Mean R2 | PF | 2R target-first |
|---|---:|---:|---:|---:|
| H-M1 | 66 | +0.060 | 1.099 | 28.8% |
| H-M6 | 54 | +0.240 | 1.446 | 33.3% |
| Non-H-M1 control | 189 | -0.072 | 0.888 | 27.0% |

The validation H-M1 edge is therefore economically small. H-M6 is more interesting, but +0.240R is still a modest gross margin before friction.

## 3. The most important decomposition: H-M6 versus H-M1-only

H-M6 is nested inside H-M1. The cleanest internal decomposition is therefore:

- H-M6: 54 validation events, mean R2 **+0.240**
- H-M1 but not H-M6: 12 events, mean R2 **-0.750**

The raw difference is about **+0.990R**.

The same direction appears in delayed movement:

- H-M6 mean ret20 = **+1.454 ATR**
- H-M1-only mean ret20 = **-1.041 ATR**

This is an intriguing structural separation, but the H-M1-only validation sample is only 12 events. It remains hypothesis-supporting, not independent proof.

## 4. Fixed-R edge versus movement persistence

The two targets are behaving differently.

### Validation H-M6

- Mean ret20 = **+1.454 ATR**
- Mean MFE20 = **2.990 ATR**
- Mean MAE20 = **1.497 ATR**
- MFE >= 2 ATR: **46.3%**
- MAE <= 1.5 ATR: **57.4%**
- `MFE >= 2 ATR AND MAE <= 1.5 ATR`: **37.0%**
- 2R target-first: **33.3%**
- Stop first: **53.7%**
- Time: **13.0%**

### Validation non-H-M1 control

- Mean ret20 = **+0.010 ATR**
- Mean MFE20 = **2.060 ATR**
- Mean MAE20 = **2.006 ATR**
- MFE >= 2 ATR: **39.2%**
- MAE <= 1.5 ATR: **49.7%**
- `MFE >= 2 ATR AND MAE <= 1.5 ATR`: **31.7%**
- 2R target-first: **27.0%**
- Stop first: **63.0%**
- Time: **10.1%**

Interpretation:

H-M6 clearly shifts the path distribution in a favorable direction. It produces more favorable excursion, less adverse excursion, more target-first outcomes, and fewer stop-first outcomes.

However, the magnitude of delayed movement is much larger than the fixed-R monetization edge. That is the key distinction for the next research stage.

## 5. Clustered evidence changes the interpretation of pooled R2

The pooled validation R2 mean for H-M6 is +0.240R, but a day-level comparison against non-H-M1 controls is much weaker.

Across 33 validation days containing both groups:

- mean daily H-M6-minus-control R2 difference: **+0.070R**
- bootstrap 95% interval: approximately **[-0.354, +0.523]R**
- positive-day share: about **33%**

For H-M1:

- 37 common days
- mean daily H-M1-minus-control R2 difference: **-0.088R**
- bootstrap 95% interval: approximately **[-0.511, +0.337]R**
- positive-day share: about **30%**

This is a major governance finding:

> The pooled positive R2 means should **not** be interpreted as strong independent daily alpha.

Part of the pooled separation comes from which types of days generated the events.

The same clustering test behaves very differently for delayed movement:

### H-M6 delayed movement

- common validation days: 33
- mean daily delta: **+1.463 ATR**
- median daily delta: **+0.805 ATR**
- positive-day share: **66.7%**
- 10% trimmed mean: **+0.849 ATR**
- day-resampled 95% interval: approximately **[+0.251, +2.870] ATR**

This is the strongest surviving statistical distinction in the project.

## 6. Contract-by-contract validation

For H-M6 versus non-H-M1 controls:

| Contract | H-M6 R2 delta | H-M6 ret20 delta |
|---|---:|---:|
| July 2026 | +0.174R | +3.310 ATR |
| August 2026 | -0.016R | +0.426 ATR |
| September 2026 | +0.559R | +0.979 ATR |

The movement effect is positive in all three validation contracts.

The fixed-R effect is positive in July and September but effectively zero in August.

That asymmetry is exactly why H-M6 is still a research label rather than a trading filter.

## 7. Non-overlap audit

Using event spacing equal to the 20-bar outcome horizon:

- H-M6 validation: 45 non-overlapping events, mean R2 **+0.174R**, PF **1.31**
- H-M1 validation: 55 non-overlapping events, mean R2 **+0.015R**, PF **1.02**
- Control validation: 114 non-overlapping events, mean R2 **+0.005R**, PF **1.01**

Using a stricter 30-bar spacing:

- H-M6 validation: 42 events, mean R2 **+0.222R**, PF **1.41**
- H-M1 validation: 50 events, mean R2 **+0.026R**, PF **1.04**
- Control validation: 99 events, mean R2 **+0.248R**, PF **1.46**

The 30-bar control result is an additional warning that fixed-R performance is highly dependent on event selection and clustering.

## 8. Friction hurdle

The validation mean event ATR is about 20.2 points for both H-M1 and H-M6.

Approximate net-R sensitivity for a fixed cost of `C` NIFTY points per trade is:

`net R = gross R - C / event_ATR`

For H-M1 validation:

- 0 points: +0.060R
- 1 point: +0.005R
- 2 points: -0.049R
- 3 points: -0.104R

For H-M6 validation:

- 0 points: +0.240R
- 1 point: +0.186R
- 2 points: +0.133R
- 3 points: +0.080R
- 4 points: +0.026R
- 5 points: -0.027R

These are not broker cost estimates. They are a stress test in price points, showing how much room the gross result has before friction erases it.

## 9. Corrected out-of-sample feature test

A fresh causal feature matrix was rebuilt directly from the raw 8,594-candle futures file and joined to the exact H-M1/H-M6 flags. The prior corrupted H-M1 field in `SALMA_DEEP_CAUSAL_EVENT_FEATURES_APR_SEP_2026.csv` was **not** used for the flags.

Complete-case rows: 510 events.

A fixed discovery-trained Ridge model predicting 20-bar direction-adjusted return produced:

| Feature set | Validation Spearman | MSE |
|---|---:|---:|
| Base causal geometry | 0.031 | 9.637 |
| + H-M1 | 0.091 | 9.483 |
| + H-M6 | 0.131 | 9.374 |
| + H-M1 + H-M6 | 0.139 | 9.365 |

A fixed logistic model for 2R target-first produced:

| Feature set | Validation AUC | Brier |
|---|---:|---:|
| Base causal geometry | 0.531 | 0.204 |
| + H-M1 | 0.518 | 0.207 |
| + H-M6 | 0.540 | 0.208 |
| + H-M1 + H-M6 | 0.558 | 0.207 |

The continuous-return signal is more encouraging than the direct 2R classifier, but neither result is remotely strong enough for production.

### Monthly walk-forward 2R AUC

Using the same fixed logistic specification, trained on all earlier contracts and tested on the next contract:

| Test contract | Base | +H-M1 | +H-M6 | +H-M1+H-M6 |
|---|---:|---:|---:|---:|
| May | 0.492 | 0.496 | 0.499 | 0.499 |
| Jun | 0.617 | 0.629 | 0.665 | 0.689 |
| Jul | 0.466 | 0.455 | 0.477 | 0.501 |
| Aug | 0.548 | 0.491 | 0.507 | 0.523 |
| Sep | 0.599 | 0.610 | 0.637 | 0.650 |

H-M6 and the combined representation improve several sequential tests, but the pattern is not stable enough to call predictive alpha. August remains a clear warning.

## 10. What this means scientifically

The research now has a much narrower hypothesis:

**compressed local range -> directional state transition -> short delay -> range release -> stronger-than-normal continuation/movement**

The exact SALMA clipping mechanics may be a useful state measurement, but the evidence does not establish that SALMA itself is the cause.

Supporting evidence:

- H-M6 produces a strong delayed-movement separation from controls.
- The effect survives contract splitting in movement space.
- Day-clustered movement remains positive.
- MFE rises and MAE falls.
- Stop-first frequency falls.
- Generic smoother ablations have shown similar families of behaviour, weakening a claim of SALMA uniqueness.

Counter-evidence:

- fixed-R edge is much smaller;
- daily clustered R2 separation is weak;
- cross-era transfer of the exact H-M6 rule failed;
- ordinary causal geometry explains a meaningful share of the separation;
- direct 2R classification remains near chance-to-weak;
- the hypothesis was discovered after inspecting the 2026 sample.

## 11. Research decisions

### H-M1
**Status: PROMISING, NOT VALIDATED.**

Do not trade it by itself.

### H-M6
**Status: STRONG RESEARCH TAG, NOT VALIDATED AS ALPHA.**

The cleanest interpretation is a phenotype label for a delayed-expansion regime.

### H-M8 pressure
**Status: DIAGNOSTIC ONLY.**

No parameter change or threshold promotion.

### Bearish-only H-M6
**Status: REJECTED AS AN INDEPENDENT RULE.**

The apparent downside asymmetry weakened materially after causal control.

### Further Apr-Sep threshold mining
**STOP.**

The discovery/validation sample has already been mined heavily. Additional tuning would increase selection bias without creating new evidence.

## 12. Next decisive experiment

The project should now move to genuinely unseen data.

The active October 2026 futures contract is `NIFTY26OCTFUT`. Current public market data confirms that this contract is active and reports live volume/OI, but the public page is not an auditable 5-minute OHLCV+OI export. citeturn753535search12

FYERS currently documents historical data access through its History API, with candle completeness after the specified interval closes and timestamps representing the beginning of each candle. FYERS also exposes Futures OI at 5-minute resolution through its analytics tooling. citeturn753535search5turn753535search6turn753535search0

The October holdout therefore remains:

1. exact SALMA-B0;
2. exact H-M1;
3. exact H-M6;
4. H-M8 pressure as a diagnostic;
5. frozen 1.5R/2R/3R benchmark;
6. same-session 20-bar path;
7. 20/30-bar non-overlap checks;
8. direction and contract/day clustering;
9. no rule changes after the first October observations are seen.

## Final Phase 88/89 verdict

The project has crossed an important methodological checkpoint: **the benchmark outcome engine is now exact and auditable.**

The evidence does **not** justify calling SALMA a profitable standalone system.

The most credible remaining research object is a **delayed expansion / state-transition phenotype**, with H-M6 as one candidate measurement. The strongest evidence is the persistence in movement distribution, not a demonstrated fixed-R trading edge.

The next major improvement in evidence will come from October 2026 forward holdout data, not from another round of Apr-Sep optimization.