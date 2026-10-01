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
