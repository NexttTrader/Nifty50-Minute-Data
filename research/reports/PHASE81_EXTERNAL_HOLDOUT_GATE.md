# Phase 81 — Why This Holdout Is the Next Gate

The research corpus has exhausted the useful Apr-Sep 2026 in-sample/first-validation search space. Phases 77-80 therefore stop signal mining and move to an independent historical contract sample.

The preferred holdout is actual NIFTY monthly futures for:
2025-10-28
2025-11-25
2025-12-30
2026-01-27
2026-02-24
2026-03-31

The dates follow NSE's revised Tuesday expiry regime for contracts expiring from September 1, 2025 onward. The acquisition process must still verify the returned contract identity.

Upstox is the current preferred route because its expired-future endpoint resolves expired contracts by expiry date and its expired historical-candle endpoint supports 5-minute candles and documents open interest.

This phase creates only acquisition tooling. It does not consume any holdout outcomes and does not change any hypothesis.
