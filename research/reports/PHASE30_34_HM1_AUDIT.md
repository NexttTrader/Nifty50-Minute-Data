# Phase 30–34 — H-M1 Robustness, Execution Geometry and Modelling Audit

## Date
2026-09-30

## Purpose
H-M1 is frozen. These phases do not change the signal definition. They test whether the apparent relationship survives uncertainty, contract splits, event clustering, execution-friction diagnostics, time-to-target analysis, and independent modelling.

## 1. Canonical H-M1
A causal compression-release breakout is defined by:
- close breaks the prior 10-bar high/low;
- current bar range >= 1.25 x median range of prior 10 bars;
- prior-5 mean range / causal ATR14 <= 1.0;
- entry next bar open;
- initial risk 1 ATR14;
- 20-bar same-session horizon;
- stop-first if stop/target share a bar.

H-M1 adds: a confirmed SALMA-B0 slope flip occurred 1–3 completed bars before the breakout.

## 2. Contract robustness
The candidate-vs-control mean-R difference at the canonical 2R benchmark was positive for every individual contract in the Apr-Sep sample:
- Apr: +0.146R
- May: +0.115R
- Jun: +0.834R
- Jul: +0.169R
- Aug: +0.030R
- Sep: +0.282R

Leave-one-contract-out pooled deltas also remained positive in all six omission tests. This reduces concern that a single pooled contract completely creates the sign of the effect.

However, candidate mean R itself was negative for Apr and approximately flat for Aug. The June candidate result is unusually strong and therefore remains an important concentration risk.

## 3. Cluster uncertainty
Candidate events cluster within days:
- Discovery: 76 events on 46 days; mean 1.65 events/day among candidate days; max 4.
- Validation: 72 events on 39 days; mean 1.85 events/day; max 5.

Day-cluster bootstrap for candidate-minus-control mean R2:
- Discovery: 95% interval approximately [-0.013, +0.637], probability delta <= 0 about 0.03.
- Validation: 95% interval approximately [-0.135, +0.513], probability delta <= 0 about 0.128.

Therefore validation uncertainty remains material.

A strict non-overlap filter (20-bar exclusion) leaves very few events and produces unstable results. This means event dependence/cluster structure is a real implementation issue and should not be ignored.

## 4. Friction sensitivity
Validation candidate mean R2 is about +0.096R before costs.

Subtracting hypothetical all-in friction per trade:
- 0.02R -> +0.076R
- 0.05R -> +0.046R
- 0.10R -> -0.004R
- 0.15R -> -0.054R
- 0.20R -> -0.104R

Mean validation ATR at candidate events is about 20.23 points, so 0.10R is roughly 2.02 NIFTY points. This is a diagnostic break-even scale, not a claim about any particular broker's actual costs.

The current gross edge is therefore economically fragile.

## 5. Time-to-target / expansion timing
For the canonical 2R benchmark:

Validation candidate vs control:
- 2R reached within 5 bars: 16.7% vs 18.6%
- within 10 bars: 26.4% vs 21.9%
- within 20 bars: 30.6% vs 26.2%
- 3R reached within 20 bars: 19.4% vs 14.2%

So H-M1 does not look like a pure immediate-momentum signal. Its relative advantage appears more clearly over a longer post-breakout horizon.

## 6. Unbounded movement-potential diagnostic
Using directional close-to-entry returns over future bars, not executable stop-and-target returns:

Validation mean signed return at:
- 1 bar: candidate +0.078 ATR vs control -0.101
- 3 bars: +0.246 vs -0.035
- 5 bars: +0.547 vs -0.088
- 10 bars: +0.712 vs -0.002
- 20 bars: +1.209 vs -0.024

This is not a tradable backtest because it allows the path to continue even after a hypothetical stop would have been hit. It is evidence that H-M1 may identify subsequent directional movement potential rather than an immediately monetizable stop/target trade.

## 7. Risk-geometry insight
Validation candidate events show a higher probability of achieving large MFE while keeping MAE under a moderate threshold. For example:
- MFE >= 2.0 ATR and MAE <= 1.5 ATR: 37.5% candidate vs 30.6% control.
- MFE >= 2.5 ATR and MAE <= 1.5 ATR: 34.7% candidate vs 21.9% control.
- MFE >= 3.0 ATR and MAE <= 1.5 ATR: 25.0% candidate vs 15.8% control.

Among validation events that actually hit 2R before the 1R stop, the median adverse excursion before reaching 2R was about 0.48 ATR for H-M1 candidates. This indicates the winners themselves generally did not require extreme adverse movement; the main problem is that some non-winning paths reverse before the expected expansion materializes.

## 8. Walk-forward ML audit
Fixed, conservative walk-forward classifiers were tested on sequential monthly contracts. Models:
- logistic regression
- random forest
- histogram gradient boosting
- LightGBM

Across May-Sep tests, adding the SALMA 1–3 bar feature to causal base-event features improved AUC in:
- logistic: 4/5
- LightGBM: 4/5
- random forest: 3/5
- histogram gradient boosting: 0/5

Mean AUC remained close to 0.50–0.53 overall. This is weak predictive discrimination, but the repeated positive incremental sign for SALMA timing in simpler models is consistent with H-M1 being a small meta-feature rather than a standalone classifier.

## 9. Core interpretation
The strongest current interpretation is:

SALMA-B0 is not a direct directional alpha engine.

H-M1 may instead be detecting a short-horizon transition state before a later volatility/range release. The useful information may be:
- event sequencing,
- movement persistence,
- and improved MFE/MAE geometry.

The 1 ATR stop / 2R benchmark is therefore not necessarily the correct monetization mechanism, but we are not changing it before the frozen holdout.

## 10. Research status
H-M1 remains:
**PROMISING, NOT VALIDATED.**

No parameter changes, additional filters, or execution optimizations are promoted from this phase.

## 11. Next scientific gate
The next research gate is an unseen holdout or forward paper test.

Priority:
1. Actual Oct 2025-Mar 2026 monthly NIFTY futures 5-minute data, if legitimately obtainable.
2. Otherwise forward observations starting with the next available sessions.

The frozen H-M1 definition must be applied without modification.

---
