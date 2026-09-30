# H-M1 — Frozen Research Hypothesis

A causal compression-release breakout may have a different tradeability profile when a confirmed SALMA-B0 slope-state flip occurred 1–3 completed bars before the breakout.

## Frozen base event
At the close of bar t:
1. Close breaks the prior 10-bar high or low.
2. Current bar range >= 1.25 x median range of the prior 10 bars.
3. Mean range of the prior 5 completed bars / rolling-mean True Range(14) <= 1.0.
4. A next same-session bar must exist for the execution benchmark.

## SALMA condition
A direction-aligned confirmed SALMA-B0 flip occurred 1–3 completed bars before the breakout bar.

## Execution benchmark
- Entry: next bar open
- Initial risk: 1 x ATR benchmark (legacy research definition: rolling mean TR14)
- Targets: 1.5R, 2R and 3R
- Vertical barrier: 20 bars or session close
- Same-bar stop/target ambiguity: stop-first

## Exact-formula audit result
TradingView's default ta.stdev uses the population-style estimator. Under that exact SALMA reconstruction, the official Apr-Sep base-event universe remains 513 events, with 73 discovery H-M1 candidates and 66 validation candidates.

## Status
PROMISING, NOT VALIDATED.

H-M1 is frozen. No further in-sample optimization is permitted before unseen/forward testing.
