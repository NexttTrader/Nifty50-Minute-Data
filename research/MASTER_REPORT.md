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
- Signal-bar expansion, delayed pullback re-entry, breakout exits, price/SALMA cross, simple sweep-to-MSS, and conservative static ML variants did not establish robust profitability.
- Causal features show some information about future movement potential, but much less stable information about risk-adjusted tradeability.
- Discovery/validation feature distributions shift materially, so nonstationarity is a central concern.

### Exact SALMA formula audit
The supplied Pine uses ta.stdev without an explicit biased flag. TradingView documents the default as biased=true, the population-style estimator. Earlier SALMA-specific exploratory artifacts that used sample SD (ddof=1) are superseded. Exact B0 reconstruction on the current futures dataset yields 816 confirmed transitions (410 up, 406 down).

The frozen H-M1 price-event universe is 513 official events after excluding the July contract's June 30 warm-up rows. Exact SALMA produces 73 discovery H-M1 candidates and 66 validation candidates. The main 20-bar movement-persistence direction survives this formula correction, while the executable fixed 1ATR/2R edge remains modest and uncertain.

### H-M6 — SALMA clipping interaction
H-M6 adds a simple SALMA-specific context to H-M1: at least 2 of the previous 3 completed bars have direction-aligned SALMA volatility clipping. Validation n=54, mean R2 +0.240, mean R3 +0.225, 20-bar signed return +1.454 ATR, MFE 2.990 ATR, MAE 1.497 ATR. Relative to non-H-M1 controls, deltas are +0.312R R2, +0.336R R3 and +1.443 ATR at 20 bars. Day-cluster validation intervals remain compatible with zero for the R2/R3 trading metrics, so this is not validated.

Within H-M1 validation candidates, aligned clipping count was strongly stratified: 0 clips n=2 mean R2 -1.000; 1 clip n=10 -0.700; 2 clips n=22 +0.024; 3 clips n=32 +0.388. Discovery shows the same broad ordering. The >=2 threshold remains post-hoc and cannot be promoted before unseen/forward testing.

### Indicator-family interpretation
Under the corrected SALMA formula, generic smoothers can also condition H-M1. Therefore SALMA's short-horizon state change is not proven unique. H-M6 remains more specifically tied to SALMA's volatility clipping.

### Cross-instrument transfer
The same H-M1/H-M6 construction on long 2015-2021 NIFTY index data shows little/no fixed 1ATR/2R improvement and mixed annual movement effects. Therefore H-M6 is not a universal market law and may be instrument/regime specific.

### Current hypothesis status
- H-M1: PROMISING, NOT VALIDATED.
- H-M6: STRONG EXPLORATORY HYPOTHESIS, NOT VALIDATED.

### Next scientific gate
No further in-sample optimization against Apr-Sep. Test frozen H-M1 and H-M6 on genuinely unseen actual futures contracts or forward paper observations. The next research branch should evaluate risk geometry and causal event lifecycle without changing the signal definitions.


## Phase 50-53 — Exact Formula and SALMA Mechanism
The SALMA reconstruction was corrected to population SD (ddof=0) because TradingView documents ta.stdev's default biased=true. Earlier ddof=1 SALMA-specific results are superseded. H-M1 survives the correction. H-M6 remains the strongest thresholded SALMA-specific hypothesis. A new continuous clipping-pressure feature (H-M8) improved a fixed discovery->validation 2R classifier AUC 0.437 -> 0.609 and improved expanding walk-forward AUC in 3/4 monthly tests; this is promising but not conclusive.


## Phase 55-60 — Deeper mechanism research
- Exact B0 clipping is frequent: about 80.6% of usable Apr-Sep futures bars are outside the WMA5 ± 0.30 population-SD band.
- SALMA is highly correlated with an unclipped double-WMA(10,3) (~0.9999); slope-state agrees ~91.2%. Thus SALMA's distinct contribution is mainly nonlinear clipping and small timing differences, not the entire smoothed trend state.
- Exact H-M1 target hazard shows little separation in the first 5 bars, then a clearer 2R separation by 10-20 bars. This reinforces delayed expansion/persistence.
- Within H-M1, aligned clipping count is strongly stratified: validation mean R2 is -0.700 for 1 clip, +0.024 for 2 clips, +0.388 for 3 clips (0-clip n=2). This is exploratory because of small cells and post-hoc discovery.
- H-M8 continuous direction-aligned clipping pressure gives a small incremental improvement in the fixed H-M1 validation classifier (AUC ~0.611 to ~0.623 with the tested causal features), but the gain is modest.
- H-M9, a specific sequence (SALMA flip exactly 2 bars before breakout + all three preceding bars directionally clipped), has futures validation n=10 and mean R2 +0.543. It is exploratory only.
- The same H-M9-style sequence on the 2019-2021 NIFTY index test had n=117, mean R2 +0.385 vs +0.185 controls. This is supportive transfer evidence but not a substitute for futures validation.
- A broad H-M6 risk-surface exploration remained positive in pooled validation across the tested stop/target grid, but contract-level heterogeneity and post-hoc exploration prevent any execution rule from being promoted.

## Current interpretation
The research is converging on a state-transition mechanism: compression/balance -> repeated directional pressure relative to a short volatility envelope -> smoothed-state transition -> range release -> sustained movement. The next decisive experiment is unseen/forward futures testing with H-M1/H-M6/H-M9 frozen and generic smoother controls.
