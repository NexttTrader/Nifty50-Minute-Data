# SALMA Deep Research Master Report

## 2026-09-30

### Current dataset
8,594 five-minute candles across six actual NIFTY monthly futures contracts, Apr-Sep 2026.

### Baseline conclusion
SALMA-B0 green/red flips are not a validated standalone entry system.

### Major findings
- Parameter tuning around B0 did not reveal a stable edge.
- SALMA flips add little independent 2R information after matching on causal price context.
- SALMA is measurably lagged; making it faster did not improve baseline trade results.
- Immediate post-flip returns show a small, unstable contrarian drift.
- Signal-bar expansion, delayed pullback re-entry, breakout exits, price/SALMA crossovers, and simple sweep-to-MSS definitions did not establish robust profitability.
- Causal features show some information about future movement potential, but much less stable information about risk-adjusted tradeability.
- Discovery/validation feature distributions shift materially, so nonstationarity is a central concern.

### Current hypothesis
H-M1: a compression-release breakout with a recent 1-3 bar confirmed SALMA flip appears to have a better MFE/MAE and mean-R profile than comparable breakouts without that recent flip.

### Next scientific gate
Freeze H-M1. Test on genuinely unseen actual futures contracts and in forward observations. Do not optimize H-M1 against Apr-Sep again before the holdout is completed.