# Trading Memory

## Exact SALMA audit
The supplied SALMA code uses ta.stdev without an explicit biased argument. TradingView documents the default as biased=true, i.e. the population-style estimator. The canonical reconstruction therefore uses ddof=0. Earlier ddof=1 SALMA-specific artifacts are superseded.

## Current facts
- SALMA-B0: Close, length 10, smooth 3, mult 0.30, sd length 5.
- Current futures dataset: 8,594 five-minute candles across actual Apr-Sep 2026 monthly contracts.
- Exact SALMA-B0: 816 confirmed transitions.
- H-M1 base-event universe: 513 official events.
- Exact H-M1: 73 discovery candidates, 66 validation candidates.

## Negative findings
- Raw green/red reversal is not validated.
- Simple SALMA parameter changes did not establish a stable edge.
- Simple sweep/MSS + SALMA, price/SALMA crossovers, simple breakout + SALMA and static ML variants did not establish a robust trading edge.

## Strongest hypotheses
### H-M1
Compression-release breakout + direction-aligned SALMA flip 1-3 completed bars earlier.
Status: PROMISING, NOT VALIDATED.

### H-M6
H-M1 + at least 2 of previous 3 completed bars direction-aligned SALMA clipping.
Status: STRONG EXPLORATORY HYPOTHESIS, NOT VALIDATED.

## Key conceptual insight
The strongest current evidence is about movement persistence and risk geometry, not immediate directional prediction. H-M6 is currently the most SALMA-specific mechanism because it directly uses the volatility-clipping component.

## Governance
No in-sample optimization of H-M1/H-M6 before unseen or forward validation. Historical predictions are immutable. Discovery, validation, holdout and forward data remain separate.


## Phase 50-53 exact-formula correction
The canonical SALMA reconstruction now uses population SD (ddof=0), matching TradingView's default biased=true semantics. Earlier ddof=1 SALMA-specific artifacts are superseded. Exact B0 = 816 confirmed transitions; exact H-M1 = 73 discovery / 66 validation candidates.

## H-M6 / H-M8
H-M6: H-M1 plus >=2 of prior 3 direction-aligned clipping bars. Validation n=54; R2 +0.240; R3 +0.225; ret20 +1.454 ATR.
H-M8: continuous direction-aligned clipping-pressure sum over the prior 3 bars. Fixed Apr-Jun -> Jul-Sep logistic AUC improved 0.437 -> 0.609; Brier 0.214 -> 0.209. Expanding monthly walk-forward improved AUC in 3/4 months. H-M8 remains exploratory and unvalidated.


## Phase 57-64
Deep research reinforces that the strongest current SALMA mechanism is an interaction: a recent direction-aligned SALMA flip is useful mainly when recent direction-aligned volatility clipping is also present. This is recorded as H-M7. H-M6 is the thresholded operational form and H-M8 is the continuous clipping-pressure form. Multi-timeframe alignment and session context are secondary exploratory conditioning variables. No new live rule is promoted before unseen/forward testing.


## Phase 55-60 discoveries
- SALMA clipping is frequent (~80.6% of usable Apr-Sep futures bars), while SALMA is highly correlated with an unclipped double-WMA(10,3) (~0.9999) and slope-state agrees ~91.2%. This suggests most SALMA behavior is smoothed-state plus a nonlinear clipping deformation.
- Exact H-M1 target-first hazard separates more clearly after 5 bars than immediately, suggesting delayed expansion/persistence rather than pure immediate momentum.
- H-M6 and continuous H-M8 clipping pressure remain the strongest SALMA-specific mechanisms tested, but are unvalidated.
- H-M9 (flip exactly 2 bars before breakout + aligned clipping on all prior 3 bars) is a small but strong exploratory sequence; futures validation n=10, mean R2 +0.543.
- Cross-era NIFTY index 2019-2021 also showed positive H-M9 sequence behavior versus control, but this is not futures validation.
- Risk-surface exploration indicates broad positive pooled H-M6 mean-R regions, but contract-level heterogeneity and post-hoc selection require unseen/forward testing.
