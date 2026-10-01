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
