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
