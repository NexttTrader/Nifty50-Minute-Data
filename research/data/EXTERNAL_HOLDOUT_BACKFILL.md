# External Holdout Backfill — Data Source Audit

## Date
2026-10-01

## Research need

The current canonical futures universe is Apr-Sep 2026. The preferred additional holdout is actual NIFTY monthly futures for Oct 2025-Mar 2026.

## Newly confirmed route: Upstox Expired Instruments API

Current Upstox developer documentation exposes dedicated expired-derivative endpoints:

1. **Get Expired Future Contracts**
   - Endpoint: `GET /v2/expired-instruments/future/contract`
   - Inputs include the NIFTY 50 underlying instrument key and a specified expiry date.
   - The response provides the expired contract metadata, including an instrument key that can be used with the historical-candle endpoint.

2. **Get Expired Historical Candle Data**
   - Endpoint: `GET /v2/expired-instruments/historical-candle/{expired_instrument_key}/{interval}/{to_date}/{from_date}`
   - Supported intervals include **5minute**.
   - The documented candle response contains timestamp, OHLC, volume and **open interest**.

3. The expired-instrument endpoints require an **Upstox Plus** subscription and an authenticated access token.

## Why this matters

This route is materially closer to the exact research requirement than generic continuous futures history because it exposes data for the actual expired contracts rather than a rolled continuous series. It also potentially restores the missing OI field for the same 5-minute contract-level candles.

## What is and is not verified

Verified from current Upstox documentation:
- expired futures can be looked up by expiry date;
- expired historical candles support 5-minute candles;
- expired candle responses document OI;
- the feature is restricted to Upstox Plus.

Not yet verified from this environment:
- whether Upstox currently retains every NIFTY monthly contract in the target **Oct 2025-Mar 2026** window;
- the exact expired instrument keys returned for those six monthly expiries;
- whether the user's account has the required Upstox Plus access/token.

Therefore no holdout data has been added and no research result has been changed.

## Secondary route: DhanHQ

Current DhanHQ v2 documentation says intraday historical data is available at 1/5/15/25/60-minute intervals for up to five years and can include OI for futures/options. However, the documentation describes the intraday endpoint as applying to **active instruments**. It is therefore not treated as a confirmed expired-contract backfill route.

## Governance

The missing Oct 2025-Mar 2026 data remains an independent holdout opportunity. If obtained, it must be ingested without changing H-M1/H-M6/H-M9 definitions, and all predictions must be generated only from information available at each historical timestamp.

No strategy conclusion is changed by this source audit alone.
