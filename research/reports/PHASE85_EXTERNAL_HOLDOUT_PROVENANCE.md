# Phase 85 — External Holdout Provenance Cross-Check
Date: 2026-10-03

## Purpose

Independently cross-check the NIFTY26JANFUT 5-minute public archive used in Phase 82 against a separate NSE daily futures archive.

## Sources

Primary 5-minute archive:
- Repository: achauh2723/Quantitative_Trading_Strategy_Development_Task_Aryan_Chauhan
- File: data/nifty_futures_5min.csv
- Contract: NIFTY26JANFUT
- Source blob SHA: 3ba0cbf9573d9907940b53a9f6f6148376ccf651

Independent daily archive:
- Repository: AvilPage/historical-option-chain-data
- Daily files: NIFTY.csv
- Contract token: 49229 / NIFTY26JANFUT
- Daily records use the NSE contract master format with OHLC, last price, open interest and traded volume.

## Exact OHLC cross-check

For five sampled complete sessions, the primary 5-minute archive was aggregated to daily OHLC and compared with the independent daily archive.

| Date | Open match | High match | Low match | Final 5m close = daily LastPric |
|---|---|---|---|---|
| 2026-01-09 | yes | yes | yes | yes |
| 2026-01-12 | yes | yes | yes | yes |
| 2026-01-13 | yes | yes | yes | yes |
| 2026-01-14 | yes | yes | yes | yes |
| 2026-01-16 | yes | yes | yes | yes |

Thus the five-minute archive reproduces the independent NSE daily OHLC/last-price records exactly on all sampled days.

## Volume cross-check

The independent NSE daily file reports traded volume in contract lots. Using the NIFTY lot size of 65 units:

- 2026-01-09: 5,601,180 vs 5,830,435 equivalent units (96.1%)
- 2026-01-12: 6,726,200 vs 7,919,145 (84.9%)
- 2026-01-13: 5,527,405 vs 5,686,330 (97.2%)
- 2026-01-14: 4,450,875 vs 4,592,965 (96.9%)
- 2026-01-16: 5,836,025 vs 6,014, - equivalent units (97.0%)

The difference is not treated as a data-integrity failure because daily and intraday providers can apply different volume accounting conventions; OHLC is an exact match.

## OI note

Intraday OI values do not exactly equal the daily archive's end-of-day OI values on the sampled dates. This is recorded as a provider-field difference and is why Phase 82 conclusions do not depend on OI.

## Conclusion

The external NIFTY26JANFUT 5-minute archive has strong cross-source provenance for price data. Its daily OHLC/last-price aggregates exactly match the independent NSE contract archive on five sampled sessions.

Therefore Phase 82 can be classified as a credible secondary external price holdout, while retaining the original caveat that the underlying Zerodha account/pull was not independently authenticated by this research environment.

The OI field is treated as advisory until independently cross-checked at intraday resolution.

## Governance

No hypothesis definition changed.
No outcome was re-fitted.
This is a provenance audit only.
