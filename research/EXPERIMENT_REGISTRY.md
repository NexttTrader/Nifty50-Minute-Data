# Experiment Registry

## Phases 0-26
Historical exploration of SALMA-B0, market regime, structure, liquidity, MFE/MAE, timing, breakout and model variants.

## Phases 27-28
Event-first meta-labeling and robustness research. H-M1 became the strongest current frozen hypothesis.

## Phase 29
H-M1 frozen. No additional historical parameter/filter mining allowed before unseen validation.

## Data boundary
Current development and first validation universe: Apr-Sep 2026 actual NIFTY monthly futures.
External-holdout backlog: Oct 2025-Mar 2026 actual monthly futures, if legitimately obtainable.

## Phase 65 — External holdout data-source audit (2026-10-01)

A current-source audit identified Upstox's dedicated Expired Instruments API as a viable candidate route for the missing Oct 2025-Mar 2026 actual NIFTY futures holdout. The documented API can retrieve expired futures by expiry date, then retrieve 5-minute expired candles; the candle response documents OHLC, volume and open interest. The feature requires Upstox Plus and authentication. Exact retention of every target contract has not yet been verified from this environment, so no holdout data or hypothesis result has been changed.

DhanHQ's current historical API supports 5-minute intraday data and OI, but its documentation describes the intraday endpoint as applying to active instruments; it is therefore not treated as a confirmed expired-contract route.

Reference: research/data/EXTERNAL_HOLDOUT_BACKFILL.md


## Phase 77 — Autonomous transfer and mechanism study (2026-10-01)

Applied the exact repaired SALMA-B0 definition, frozen H-M1/H-M6 sequence, and H-M8 clipping-pressure diagnostic to the established 2015-2021 NIFTY 50 index 5-minute transfer universe.

Key findings:
- Exact SALMA reconstruction reproduces all 1,184 historical H-M1 candidate timestamps.
- H-M6: n=1,000; mean 20-bar return +0.203 ATR; mean 2R benchmark -0.051R; 2R target-first 30.1%.
- H-M1-not-H-M6: n=184; mean 20-bar return +0.127 ATR; mean 2R +0.038R; 2R target-first 32.6%.
- The H-M6 increment is therefore not a stable cross-instrument 2R edge; day-cluster intervals for the incremental effects include zero.
- H-M8 pressure transfer is negative: pressure-vs-ret20 Spearman ≈ -0.002; fixed 2015-2018 -> 2019-2021 pressure-only 2R AUC ≈ 0.483.
- Generic smoother flip placebos do not establish SALMA uniqueness.

Governance: no 2026 parameters changed; no new threshold promoted. Next decisive gate remains genuinely unseen actual NIFTY futures data.


## Phase 78 — Geometry-first residual research (2026-10-02)

Tested whether generic causal event geometry explains the 2R outcomes and whether the fixed H-M1 state / clipping context adds residual information.

Key findings:
- All-events geometry-only discovery->validation logistic AUC: 0.510.
- Adding fixed H-M1: AUC 0.511.
- Adding continuous clipping pressure: AUC 0.507.
- Within H-M1 events, geometry-only AUC 0.576; geometry + pressure AUC 0.601.
- Day-cluster bootstrap for the H-M1 pressure AUC gain: +0.026 observed, 95% interval approximately [-0.070,+0.134].
- Brier calibration worsened by about +0.010 with pressure.

Interpretation: generic event geometry does not explain the whole H-M1-conditioned effect, but the incremental pressure result is too uncertain to promote.

## Phase 79 — Lifecycle and first-passage path analysis (2026-10-02)

Evaluated the next 20 same-session bars after each frozen event on exact Apr-Sep futures.

Validation H-M6 versus non-H-M1 control:
- MFE3 +0.453 ATR; MFE5 +0.609; MFE10 +0.717; MFE20 +0.929.
- MAE3 +0.043 ATR; MAE5 -0.131; MAE10 -0.240; MAE20 -0.510.
- 20-bar close return +1.443 ATR.
- +1R favorable-first before adverse 1R: 57.4% vs 45.0%, +12.4 pp.
- +2R favorable-first: 37.0% vs 30.2%, +6.9 pp.
- Day-cluster 95% intervals remain compatible with zero.

Interpretation: H-M6's separation is increasingly a path-persistence / adverse-excursion property emerging after roughly 3-5 bars, not an immediate breakout effect.

Governance: no signal or execution parameters changed; no live rule promoted. Next decisive gate remains genuinely unseen actual NIFTY futures data.


## Phase 80 — Contract stability and leave-one-out lifecycle (2026-10-02)

Tested whether the Phase 79 lifecycle effect was concentrated in one 2026 validation contract.

Validation H-M6 vs non-H-M1 control:
- July: MFE20 +2.676 ATR, MAE20 -0.501 ATR, ret20 +3.310 ATR.
- August: MFE20 -0.289 ATR, MAE20 -0.364 ATR, ret20 +0.426 ATR.
- September: MFE20 +0.709 ATR, MAE20 -0.500 ATR, ret20 +0.979 ATR.

Leave-one-contract-out:
- Remove August: ret20 delta +1.767 ATR, MAE20 delta -0.551.
- Remove July: ret20 delta +0.724 ATR, MAE20 delta -0.438.
- Remove September: ret20 delta +1.983 ATR, MAE20 delta -0.502.

Thus the later-path effect is not driven by a single validation contract, although magnitude is heterogeneous and July contributes the largest point estimate.

Governance: no signal or execution parameters changed. Next decisive gate remains unseen actual futures data.


## Phase 81 — External holdout acquisition gate (2026-10-02)

The research gate is now operationally specified for actual NIFTY monthly futures contracts expiring:
- 2025-10-28
- 2025-11-25
- 2025-12-30
- 2026-01-27
- 2026-02-24
- 2026-03-31

NSE changed the NIFTY index-derivative expiry day to Tuesday for contracts expiring from September 1, 2025 onward. The Phase 81 target dates follow that rule.

Upstox expired-instrument APIs were selected as the primary acquisition route because they resolve expired futures by expiry date and provide 5-minute expired historical candles with OHLC, volume and OI. The associated fetcher stores exact contract identity and validates the returned expiry before accepting data.

No holdout data has been consumed and no hypothesis has changed.


## Phase 82 — Independent secondary futures holdout challenge (2026-10-03)

A public secondary archive for NIFTY26JANFUT was evaluated using the frozen H-M1/H-M6/H-M9/H-M12 definitions.

Data:
- 4,125 five-minute bars
- 55 complete 75-bar sessions
- 2025-10-29 through 2026-01-16
- 124 frozen base events
- H-M1 n=26
- H-M6 n=24
- H-M9 n=4
- H-M12 n=15

Results versus the frozen base-event control:
- H-M1 20-bar return -0.835 ATR delta; R2 delta -0.410R.
- H-M6 20-bar return -0.757 ATR delta; R2 delta -0.338R.
- H-M6 2R target-first 25.0% vs control 35.7%.
- Day-cluster intervals include zero but point estimates are materially negative.

This is classified as a credible secondary external holdout challenge after a Phase 85 daily cross-source price audit. It is not final broker-independent validation because the original source's Zerodha account/pull was not independently authenticated.

## Phase 83 — External pressure diagnostic (2026-10-03)

Within the 26 external H-M1 events:
- clipping pressure vs ret20 Spearman +0.704;
- pressure vs MFE20 +0.785;
- pressure vs MAE20 +0.760;
- pressure-only 2R AUC 0.392.

Interpretation: pressure behaves like movement-intensity information, increasing both favorable and adverse excursion, rather than monotonic fixed-2R tradeability.

## Phase 84 — External regime-shift diagnosis (2026-10-03)

Compared with 2026 validation H-M1 events, the external January H-M1 events show much larger pre-event directional displacement:
- mean prior-5-bar return +2.456 ATR vs +0.326;
- mean prior-20-bar return +1.684 ATR vs +0.071;
- event range/ATR mean 1.452 vs 1.741;
- mean clipping pressure 0.844 vs 0.925.

The January sequence therefore often fires after a more extended prior move and a smaller event shock. This is an explanatory regime diagnosis, not a new filter.

## Phase 85 — External price provenance audit (2026-10-03)

Five January NIFTY26JANFUT sessions were independently cross-checked against the AvilPage NSE daily futures archive. Open, high, low and the final 5-minute price matched exactly on all five sampled dates. Intraday volume was directionally consistent after converting the daily lot volume by the 65-unit NIFTY lot size. Intraday OI does not exactly match daily end-of-day OI and remains advisory.

The Jan archive is therefore retained as a credible secondary external price holdout, not as a fully broker-authenticated source.


## Phase 87 — Prospective October 2026 forward capture (2026-10-03)

A scheduled GitHub Actions pipeline is now operational for the active October 2026 NIFTY futures contract. It captures contract-specific 5-minute OHLCV after each weekday session, records frozen H-M1/H-M6/H-M9 signals immutably, and stores later outcomes separately after maturation.

The pipeline is bounded to the October contract expiring 2026-10-27 and does not roll silently to another contract. H-M13 is recorded only as a future-only research hypothesis and is not used as a trading decision.

No forward outcome is used to alter any prior signal.


## Phase 86 — Prior-extension interaction replication (2026-10-03)

Replicated the January external failure mode in the older 2015-2021 NIFTY index and compared it with the 2026 futures validation sample.

- 2015-2021 H-M1 prior-5 displacement terciles: low R2 +0.060 / ret20 +0.356; mid -0.097 / +0.213; high -0.062 / +0.011.
- 2026 validation H-M1: low +0.062 / +0.271; mid -0.358 / +0.850; high +0.476 / +1.880.
- January external H-M1 had mean prior-5 displacement +2.456 ATR and negative subsequent outcomes.

Conclusion: prior extension alone is not a universal filter. Any future-only interaction must include event-shock/release context.

## H-M13 — Future-only prior-extension × event-shock interaction

Created as a post-hoc future-only hypothesis. H-M13 is not evaluated on the January holdout and is not used as a trading decision in Phase 87.

## Phase 87 — Prospective October 2026 forward capture

A scheduled capture pipeline is active for NIFTY26OCTFUT through its 2026-10-27 expiry. It saves raw 5-minute OHLCV, immutable H-M1/H-M6/H-M9 signal rows, and mature outcomes as separate Git artifacts.


## Phase 87 — First prospective observation (2026-10-03)

The automated forward pipeline captured the active NIFTY26OCTFUT contract:
- scripcode 48704
- expiry 2026-10-27
- 79 five-minute bars from the first captured session
- 0 frozen H-M1 signals
- 0 mature outcomes

This is a data-pipeline checkpoint only; no performance inference is made.

## Phase 87 governance

The forward workflow now persists:
- raw contract-specific 5-minute OHLCV;
- immutable frozen H-M1/H-M6/H-M9 signal rows;
- mature outcome rows stored separately;
- a capture manifest and SHA-256 of the raw file.

The workflow runs on weekdays after the market session through the October contract expiry and automatically commits its artifacts to main.


## Phase 82 — Predeclared delayed-horizon movement test (2026-10-03)

Frozen H-M6 was evaluated at fixed 1/3/5/10/20-bar same-session horizons. Validation mean-return deltas versus non-H-M1 control were +0.207, +0.377, +0.636, +0.962 and +1.712 ATR. The 20-bar day-cluster bootstrap 95% interval was [+0.348,+3.392] ATR.

Time-of-day and direction adjustment preserved positive H-M6 coefficients at 5/10/20 bars (+0.683/+0.982/+1.681 ATR). Ten-percent trimming and medians also remained positive at 10/20 bars.

Governance: no signal, threshold, stop, target or holding-period rule changed. The result is a movement-persistence diagnostic, not a validated trading rule.


## Phase 83 — Multiple-testing audit (2026-10-03)

Audited H-M1/H-M6/H-M9 across 2R and 20-bar movement endpoints as one six-comparison family using day-cluster bootstrap probabilities and Holm adjustment.

Key governance result:
- H-M6 ret20 raw probability ~0.005; Holm-adjusted ~0.029.
- H-M6 2R raw ~0.058; adjusted ~0.230.
- H-M1 ret20 raw ~0.028; adjusted ~0.142.
- H-M9 endpoints remain uncertain because n=10.

No hypothesis or execution parameter changed. The surviving evidence is movement persistence, not a validated fixed-2R trading edge.


## Phase 88 — Event independence and clustering robustness (2026-10-03)

Audited dependence in the frozen 2026 validation event sample.

- H-M6 and control event spacing is similar; H-M6 is clustered but not uniquely denser.
- Same-session cooldown de-overlap retained positive H-M6 minus control 20-bar return deltas of +1.407 ATR at 5 bars, +1.445 ATR at 10, +1.350 ATR at 20, and +1.016 ATR at 30.
- At the key 20-bar cooldown, day-block bootstrap CI was approximately [-0.154,+3.125] ATR, P(delta<=0) ≈ 0.043.
- Equal-day weighting without thinning gave +1.463 ATR mean daily delta across 33 common days, with 66.7% positive days.

Conclusion: the 2026 movement-persistence point estimate survives moderate event de-overlapping, but strict episode-level independence produces substantially wider uncertainty. No hypothesis or execution parameter changed.



## Phase 89 — Cross-dataset H-M7 selectivity and future-only H-M14 freeze (2026-10-05)

The external January contract shows H-M6 qualifying 92.3% of H-M1 events, compared with 81.8% in 2026 validation, so the >=2 threshold loses selectivity out of sample.

Within the external H-M6 sample:
- 2 clips: n=13, mean R2 -0.372R, 2R target-first 15.4%.
- 3 clips: n=11, mean R2 +0.295R, 2R target-first 36.4%.

The 3-clip > 2-clip fixed-risk ordering is reproduced in discovery, validation and the external January contract. It is still not a validated edge because external 3-clip R2 is only slightly above the external control.

H-M14 is now frozen as a future-only hypothesis: H-M1 plus exactly 3 direction-aligned clipped bars among the prior 3 completed bars. It is recorded prospectively on October 2026 and cannot be evaluated using the already-seen January holdout.


## Phase 90 — Prospective forward timestamp integrity audit (2026-10-05)

Found and corrected a timestamp/session-integrity problem in the October forward capture. NSE/OpenChart-compatible returned timestamps were interpreted as UTC although they represent NSE wall-clock values. Five of 90 archived rows were outside the regular 09:15-15:29:59 IST session.

The parser now localizes source values to Asia/Kolkata, converts to UTC, filters the regular session, and rejects source bars more than 10 minutes ahead of the runner clock. The corrected archive contains 85 valid bars (75 on Oct 1, 10 on Oct 5) and zero frozen signals/outcomes existed before correction.

Corrected raw SHA-256: `823af836e4d0eedf7ccfe2d271bc86e5b05d1b12e0489a07c0ce9b0b43683552`. No hypothesis or execution rule changed.