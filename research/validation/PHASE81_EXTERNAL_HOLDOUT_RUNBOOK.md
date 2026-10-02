# Phase 81 — External Futures Holdout Acquisition Runbook

Date: 2026-10-02

## Objective

Acquire genuinely unseen actual NIFTY monthly futures 5-minute candles for the independent Oct 2025-Mar 2026 holdout.

The holdout must remain contract-specific. Continuous rolled futures data is not an acceptable substitute.

## Target contracts

NIFTY monthly futures after the NSE expiry-day change are scheduled on the last Tuesday of the expiry month. NSE's June 25, 2025 circular changed NIFTY monthly/quarterly/half-yearly expiry from the last Thursday to the last Tuesday for contracts expiring from September 1, 2025 onward.

Target monthly expiry dates:
- 2025-10-28
- 2025-11-25
- 2025-12-30
- 2026-01-27
- 2026-02-24
- 2026-03-31

These dates are expected last-Tuesday expiries; the acquisition script verifies the actual expiry returned by the provider before accepting a contract.

## Preferred provider

Upstox currently exposes expired future contracts by underlying instrument and expiry date, plus an expired historical-candle endpoint supporting 5minute candles and fields including OHLC, volume and open interest. The expired-instrument feature requires Upstox Plus and authentication.

## Acquisition protocol

1. Resolve the actual NIFTY futures contract for each target expiry through the expired-future-contract endpoint.
2. Store the returned trading symbol and expired instrument key exactly as supplied.
3. Request 5-minute candles in small date windows from approximately 120 calendar days before expiry through expiry.
4. Preserve timestamp, OHLC, volume and OI.
5. Deduplicate timestamps within contract and sort chronologically.
6. Reject a contract if expiry identity is missing, timestamps duplicate after deduplication, or the candle schema is incomplete.
7. Save one contract-level CSV plus a combined normalized CSV.
8. Run the frozen research tracks only after all contract files pass structural validation.

## Frozen research pass

Once the six contracts exist, run one immutable pass:
- exact SALMA-B0 reconstruction;
- H-M1;
- H-M6;
- H-M8 continuous pressure diagnostic;
- H-M9;
- generic smoother/envelope controls;
- non-overlap execution;
- day/contract clustered uncertainty;
- realistic friction sensitivity.

No threshold changes are permitted after seeing holdout outcomes. Any new rule becomes a new hypothesis ID.

## Acceptance gate

The project runbook requires at least 30 independent trading days before characterizing a forward effect strongly and prefers multiple contracts plus at least 100 eligible events before strong inference.

## Files produced

- research/data/external_holdout/UPSTOX_NIFTY_FUT_<expiry>.csv
- research/data/external_holdout/NIFTY_FUT_5m_OCT2025_MAR2026.csv
- research/data/external_holdout/UPSTOX_CONTRACT_MANIFEST.csv

The manifest must contain provider, expiry, trading symbol, instrument key, row count, first timestamp, last timestamp, duplicate count and pull timestamp.
