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


## Phase 65 — External holdout data-source audit (2026-10-01)
A current data-source audit found a dedicated Upstox expired-derivatives route that is materially suitable for the missing actual-contract holdout: expired NIFTY futures can be resolved by expiry date, then queried at 5-minute candles; the documented expired-candle response includes OHLC, volume and open interest. The feature requires Upstox Plus and authentication. Exact retention of every Oct 2025-Mar 2026 NIFTY monthly contract has not been verified from this environment, so no holdout result has been generated and no hypothesis has been changed.

The preferred next gate remains frozen unseen/forward validation of H-M1/H-M6/H-M9. No further in-sample tuning is permitted before that gate.


## Phase 78 — Geometry-first residual research

A geometry-only discovery->validation logistic model on the frozen Apr-Sep 2026 event universe produced AUC 0.510. Adding the fixed H-M1 state produced 0.511 and adding continuous clipping pressure produced 0.507. Within H-M1 candidates, geometry-only AUC was 0.576 versus 0.601 with pressure, but the day-cluster bootstrap AUC gain was only +0.026 with a 95% interval of approximately [-0.070,+0.134]. The residual pressure effect remains exploratory.

## Phase 79 — Lifecycle and first-passage path analysis

Path-level analysis on the same frozen 2026 futures events shows that H-M6's separation grows with time. In validation, H-M6 versus non-H-M1 control had MFE deltas of +0.453 ATR at 3 bars, +0.609 at 5, +0.717 at 10 and +0.929 at 20. MAE was similar at 3 bars but lower by -0.131, -0.240 and -0.510 ATR at 5, 10 and 20 bars. The 20-bar signed-return delta was +1.443 ATR.

First-passage analysis showed +1R reached before adverse 1R on 57.4% of H-M6 events versus 45.0% of controls (+12.4 percentage points), with +2R first on 37.0% versus 30.2%. Day-cluster uncertainty remains wide and includes zero for these differences.

The lifecycle evidence therefore reinforces the delayed-expansion interpretation but does not establish a validated trading edge. H-M6/H-M1/H-M8/H-M9 remain frozen.


## Phase 80 — Contract stability and leave-one-out lifecycle

The Phase 79 lifecycle effect was checked contract-by-contract and with one validation contract removed at a time. H-M6's 20-bar signed-return delta versus non-H-M1 controls was positive in July (+3.310 ATR), August (+0.426 ATR), and September (+0.979 ATR). The 20-bar MAE delta was negative in all three contracts (-0.501, -0.364, and -0.500 ATR respectively).

Leave-one-contract-out results remained positive for 20-bar return delta (+1.767 ATR without August, +0.724 without July, +1.983 without September) and negative for 20-bar MAE delta (-0.551, -0.438, and -0.502 ATR respectively). This indicates that the lifecycle pattern is not solely a single-contract artifact, although its magnitude is heterogeneous.

The result strengthens the movement/path interpretation but does not validate the executable trading rule. H-M1/H-M6/H-M8/H-M9 remain frozen.


## Phase 81 — External holdout acquisition gate

The next decisive experiment is now operationally defined around six actual NIFTY monthly futures contracts covering October 2025 through March 2026. NSE changed NIFTY index-derivative expiry to Tuesday for contracts expiring from September 1, 2025 onward; the expected monthly expiries are therefore 28-Oct-2025, 25-Nov-2025, 30-Dec-2025, 27-Jan-2026, 24-Feb-2026 and 31-Mar-2026.

The repository now contains a reproducible Upstox expired-futures acquisition tool that resolves the exact contract by expiry, downloads 5-minute contract-specific candles in small windows, preserves OHLCV and OI, and writes a manifest. This phase is acquisition tooling only; no holdout outcome has been viewed or used.


## Phase 82 — Independent secondary futures holdout

A public secondary archive containing 4,125 five-minute NIFTY26JANFUT bars across 55 complete sessions was evaluated with all frozen rules. The base event count was 124, with H-M1 n=26 and H-M6 n=24. H-M1 showed a 20-bar return delta of -0.835 ATR and R2 delta of -0.410R versus the frozen control. H-M6 showed -0.757 ATR and -0.338R respectively, with 2R target-first 25.0% versus 35.7% for control.

This is the first contract-level external challenge to the positive Jul-Sep 2026 H-M1/H-M6 result. It is classified as a credible secondary holdout rather than final broker-independent validation because the originating Zerodha account was not independently authenticated.

## Phase 83 — External pressure diagnostic

On the same 26 external H-M1 events, continuous clipping pressure had Spearman correlations of +0.704 with 20-bar return, +0.785 with MFE20 and +0.760 with MAE20. Pressure-only 2R AUC was 0.392. The distinction is important: pressure can identify larger path intensity without identifying better fixed-risk tradeability.

## Phase 84 — External regime-shift diagnosis

The external January H-M1 events were much more directionally extended before the event than 2026 validation H-M1 events. Mean prior-5-bar return was +2.456 ATR versus +0.326 and mean prior-20-bar return +1.684 versus +0.071. Event range/ATR and clipping pressure were slightly lower on average. This suggests the same SALMA transition can occur at materially different lifecycle stages of the price path.

The holdout result therefore strengthens the hypothesis that the useful 2026 behavior was conditional on a compression-to-expansion state, rather than being a universal property of SALMA flips or clipping.

No new prior-return filter is adopted because that interpretation was derived after observing the external holdout.

## Phase 85 — External price provenance

Five complete NIFTY26JANFUT sessions were cross-checked against an independent NSE daily futures archive. Daily open/high/low and the final five-minute price matched exactly on all five sampled dates; daily futures volume was consistent after converting lots by the 65-unit NIFTY lot size. Intraday OI differed from daily end-of-day OI and is therefore not used as a provenance anchor.

## Current research status

The research has now passed the useful in-sample signal-mining boundary. The external evidence currently says:
- 2026 H-M6 shows a delayed path-persistence pattern;
- the first secondary out-of-sample contract fails the frozen H-M1/H-M6 trading benchmark;
- clipping pressure remains related to path intensity but not fixed-2R success;
- the external contract's H-M1 events occur after substantially greater prior directional movement.

This is a regime-sensitive research result, not a validated universal strategy.

The next decisive evidence remains another genuinely unseen contract-level 5-minute futures dataset. No parameter changes are permitted until such data is available.


## Phase 87 — Prospective October 2026 forward capture

A scheduled, credential-free forward-validation pipeline has been added for the active October 2026 NIFTY futures contract. Current public market sources identify the October contract as expiring 27-Oct-2026. citeturn897861search0turn897861search4

The pipeline refreshes contract-specific 5-minute OHLCV after each weekday session, records frozen H-M1/H-M6/H-M9 signals using only event-time information, and stores mature outcomes separately. It is bounded to the October contract and does not silently roll to November.

The forward phase is observational and does not change any frozen research rule. H-M13 remains future-only and is not used for decisions.


## Phase 86 — Prior-extension interaction replication

Prior directional extension was replicated as a diagnostic across the older NIFTY index and 2026 futures validation. The relationship changes sign across datasets, so prior extension alone is not a stable filter. The future-only H-M13 hypothesis therefore requires interaction with current event shock/release intensity.

## Phase 87 — Prospective October 2026 forward capture

A scheduled GitHub Actions pipeline now captures the active October 2026 NIFTY futures contract using the public NSE/OpenChart-compatible charting endpoint. It records frozen H-M1/H-M6/H-M9 signals without using future outcomes, and stores outcomes separately only after they mature. H-M13 is deliberately excluded from trading decisions until its functional form is formally frozen.


## Phase 87 — First prospective observation

The first automated prospective capture of NIFTY26OCTFUT (scripcode 48704, expiry 27-Oct-2026) produced 79 five-minute bars for the first captured session and zero frozen H-M1 signals. No outcome inference is made from this checkpoint.

The forward pipeline is now operational and preserves raw bars, immutable signal records, separate mature outcomes, and a reproducible manifest. No parameter is changed from the frozen research definitions.


## Phase 82 — Predeclared delayed-horizon movement test (2026-10-03)

A fixed-horizon, same-session analysis evaluated the frozen H-M6 signal at 1, 3, 5, 10 and 20 bars from next-bar execution, without selecting a holding period after seeing outcomes.

Validation H-M6 minus non-H-M1 control mean return deltas were +0.207, +0.377, +0.636, +0.962 and +1.712 ATR at 1, 3, 5, 10 and 20 bars respectively. At 20 bars, the H-M6 median return was +0.453 ATR and the 10%-trimmed mean was +0.996 ATR versus -0.023 ATR for the control.

Day-cluster bootstrap intervals were wide early and more favorable late; the 20-bar difference was +1.712 ATR with a 95% cluster interval of [+0.348,+3.392]. A fixed time-of-day-bin plus breakout-direction regression remained positive at 5, 10 and 20 bars, with H-M6 coefficients +0.683, +0.982 and +1.681 ATR.

Interpretation: the strongest recurring property of H-M6 is delayed favorable path persistence rather than immediate breakout momentum. This remains exploratory; later-horizon sample sizes are smaller because the analysis requires complete same-session horizons.


## Phase 83 — Multiple-testing audit

The fixed validation family H-M1/H-M6/H-M9 was evaluated across two endpoints: mean 2R benchmark difference and mean 20-bar signed-return difference. Day-cluster bootstrap probabilities were Holm-adjusted across the six comparisons.

Only H-M6's 20-bar movement result remained below 0.05 after adjustment (adjusted bootstrap probability approximately 0.029). H-M6's 2R result adjusted to approximately 0.230, and H-M1's 20-bar result adjusted to approximately 0.142. H-M9 remains too small and uncertain.

This strengthens the distinction between a delayed movement/persistence signal and a validated executable trading edge. No signal definition or execution rule changed.


## Phase 88 — Event independence and clustering robustness (2026-10-03)

A dependence audit tested whether the frozen H-M6 20-bar movement result is materially created by overlapping event windows or by unequal event frequency across days. The audit used the exact Apr-Sep 2026 futures event universe and the Phase 82 non-H-M1 control.

Validation event spacing was similar across groups: H-M6 median same-day gap 13 bars versus 12 for control; 70.2% of H-M6 events and 78.0% of control events had a prior same-day event within 20 bars. Thus H-M6 is clustered, but not uniquely more clustered than the control.

A chronology-preserving same-session de-overlap test retained only the first event and then required a cooldown of N bars before retaining another event. The H-M6 minus control 20-bar return delta remained positive at every tested cooldown:
- 0 bars: +1.443 ATR;
- 5 bars: +1.407 ATR;
- 10 bars: +1.445 ATR;
- 20 bars: +1.350 ATR;
- 30 bars: +1.016 ATR.

The 20-bar cooldown is the key independence stress test because it prevents retained events from sharing the primary 20-bar outcome window within a session. Its day-block 95% interval was approximately [-0.154,+3.125] ATR with bootstrap P(delta<=0) approximately 0.043. At 30 bars the interval widened to approximately [-0.635,+3.102] ATR.

An equal-day-weighted comparison without thinning, restricted to the 33 validation days containing both H-M6 and control events, produced mean daily delta +1.463 ATR, median +0.805 ATR, 66.7% positive days and a 10%-trimmed mean +0.849 ATR. A day-resampled interval was approximately [+0.245,+2.849] ATR.

The audit therefore supports the narrower claim that H-M6's delayed movement association is not explained simply by ordinary event overlap or event frequency. However, aggressive episode collapse materially widens uncertainty, and strict matched-day de-overlap is not an independent confirmation.

No signal, target, stop, horizon, or threshold was changed. H-M6 remains an exploratory movement-persistence hypothesis, not a validated trading rule. The next decisive evidence remains genuinely unseen contract-level futures data and the independent October 2026 forward capture.


## Phase 89 — Cross-dataset H-M7 selectivity and future-only H-M14 freeze (2026-10-05)

The January external NIFTY26JANFUT holdout was decomposed using the already-defined H-M7 clipping-count interaction.

H-M6 (>=2 aligned clips) qualified 24 of 26 H-M1 events (92.3%) on the external contract, versus 54 of 66 (81.8%) in the frozen Jul-Sep 2026 validation set. Its external 20-bar return remained negative (-0.257 ATR versus +0.501 ATR for control). The failure was present in both directions.

Within external H-M6, 2-clip events had mean R2 -0.372R and 15.4% 2R target-first, while 3-clip events had mean R2 +0.295R and 36.4% target-first. The 3-clip > 2-clip ordering was already present in discovery and validation and is reproduced externally, but the external 3-clip mean R2 is only marginally above the external control (+0.272R).

Conclusion: >=2 clipping is not a stable external selector. The exact-3 branch is a more coherent state candidate, but it is not a validated edge.

A future-only H-M14 hypothesis was therefore frozen as H-M1 + exactly 3 direction-aligned clipped bars among the previous 3 completed bars. H-M14 is recorded prospectively on the October 2026 stream only and does not modify H-M6.


## Phase 90 — Prospective forward timestamp integrity audit (2026-10-05)

An audit of the October 2026 forward capture found that the public NSE/OpenChart-compatible endpoint's returned millisecond timestamps were being interpreted directly as UTC even though the values correspond to NSE wall-clock timestamps. The first archive also contained reference/partial rows outside the regular session.

The parser was corrected to interpret source timestamps in Asia/Kolkata, convert them to true UTC, enforce the regular 09:15-15:29:59 IST session, and reject source bars more than 10 minutes ahead of the runner clock.

The existing 90-row raw archive contained 5 non-session rows (2 pre-open and 3 post-close/reference), leaving 85 valid regular-session bars: 75 on 2026-10-01 and 10 on 2026-10-05. No H-M1/H-M6/H-M9/H-M14 signals or outcomes had been recorded before the correction, so no reported forward performance result was contaminated.

Corrected October raw SHA-256: `823af836e4d0eedf7ccfe2d271bc86e5b05d1b12e0489a07c0ce9b0b43683552`.

Governance: no historical hypothesis was retuned; H-M1/H-M6/H-M9/H-M14 remain frozen.

## Phase 91 — Prospective frozen-signal evaluation gate (2026-10-05)

Added a dedicated evaluator for the October 2026 forward stream. It reports only predeclared endpoints for frozen H-M1/H-M6/H-M9 and future-only H-M14, reconstructs fixed 1.5R/2R/3R stop-first outcomes, excludes immature 20-bar observations, and performs data-integrity checks before reporting any forward result.

Current corrected October stream state at the Phase 91 checkpoint: 85 regular-session 5-minute bars (75 on Oct 1 and 10 on Oct 5 through 10:03:59 IST), zero prospective frozen signals, zero mature outcomes. Therefore no forward performance inference is made.

The evaluator is wired into the Phase 87 forward workflow and a fresh workflow-trigger commit was recorded. The repository will continue to treat October observations as prospective and immutable; no historical parameter may be changed from this stream. A local bytecode syntax test could not be completed in this environment because the container cannot resolve raw.githubusercontent.com; no claim of that test is made.
