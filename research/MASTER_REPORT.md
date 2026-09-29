# SALMA Deep Research Master Report

## 2026-09-30

### Current dataset
8,594 five-minute candles across six actual NIFTY monthly futures contracts, Apr-Sep 2026.

### Baseline conclusion
SALMA-B0 green/red flips are not a validated standalone entry system.

### Major findings
- SALMA parameter tuning around B0 did not reveal a stable edge.
- SALMA is a lagged state-change descriptor; making it faster did not rescue the baseline.
- Simple reversal, crossover, breakout, sweep/MSS, pullback and exit variants tested so far did not establish robust profitability.
- Causal context models can predict movement potential somewhat better than they predict stop/target tradeability.
- Nonstationarity and event clustering materially affect inference.

### Strongest current hypothesis
H-M1: a causal compression-release breakout with a confirmed SALMA-B0 flip 1-3 completed bars earlier.

### New Phase 30-34 evidence
- Candidate-vs-control mean-R difference remained positive for every Apr-Sep contract.
- Leave-one-contract-out pooled deltas remained positive.
- Validation day-cluster bootstrap still included zero, so uncertainty remains material.
- The gross validation mean is only about +0.096R and is close to flat after a hypothetical 0.10R friction deduction.
- H-M1's relative advantage is stronger over a 10-20 bar movement horizon than within the first 5 bars.
- Movement-potential diagnostics show a large positive 20-bar signed-return difference in validation, but this is not an executable trade result because it ignores interim stops.
- H-M1 candidates have a more favorable MFE/MAE opportunity surface than controls at moderate adverse-excursion limits.
- Conservative sequential ML models show only weak discrimination overall, though simpler models frequently gain a small amount from the SALMA 1-3 bar feature.

### Interpretation
The current evidence supports treating SALMA-B0 as a contextual timing/state variable, not as a standalone directional predictor.

H-M1 may identify a market state in which a compression breakout has a better chance of developing into sustained directional movement.

### Research status
H-M1: **PROMISING, NOT VALIDATED.**

It is now frozen.

No further historical parameter/filter mining is permitted against Apr-Sep before an unseen holdout or forward test.

### Next gate
1. Obtain actual Oct 2025-Mar 2026 monthly NIFTY futures 5-minute data if legitimately obtainable.
2. Otherwise start forward paper validation on the next sessions.
3. Apply the exact frozen H-M1 rule.
4. Evaluate gross and net R, clustering, drawdown and uncertainty.
5. Only after the holdout/forward gate consider a separate risk-geometry research branch.


## Phase 35 — Lifecycle / Asymmetry
H-M1 candidates in Jul-Sep validation show stronger 10-20 bar directional persistence and larger MFE with somewhat lower MAE than controls. The effect is not primarily an immediate first-3-bar momentum effect. A strong directional asymmetry was observed: the largest validation separation was in downward compression-release breakouts, especially following a bearish short-term trend. This is recorded as H-M2, a test hypothesis only.

## Phase 36 — Cross-Instrument Transfer
The frozen H-M1 sequence was applied to the 2015-2021 NIFTY 50 index 5-minute dataset as a transfer test. It showed a small positive 20-bar directional-persistence difference (+0.076 ATR) but no 1ATR/2R trading improvement; the day-cluster interval included zero. Therefore H-M1 should not be described as universal. The evidence currently points toward an instrument/regime-conditional phenomenon.

## Current research interpretation
The project is increasingly separating three questions:
1. Does a market event predict direction/movement potential?
2. Does it create a monetizable MFE/MAE profile?
3. Can a realistic execution rule capture that profile after friction?
H-M1 appears most interesting for question 1 and partly for question 2. Question 3 remains unresolved.
