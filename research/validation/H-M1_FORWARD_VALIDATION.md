# H-M1 — Forward Validation Protocol

## Objective
Test the frozen H-M1 hypothesis on genuinely unseen data without modifying the rule.

## Rule
Do not optimize:
- SALMA parameters
- 1–3 bar window
- breakout thresholds
- compression thresholds
- risk
- target
- filters

## Required input
Actual NIFTY futures 5-minute OHLC data with contract identity.

## Procedure
At the close of every completed event bar:
1. Determine whether the frozen compression-release breakout occurred.
2. Determine whether a confirmed SALMA-B0 flip occurred 1–3 completed bars earlier.
3. If yes, record the signal before subsequent candles are available.
4. Entry is the next bar open.
5. Risk is 1 ATR14 from event-bar close.
6. Record 1.5R, 2R and 3R outcomes.
7. Record MFE, MAE and time-to-target.
8. Allow at most one H-M1 trade to be active at a time unless a later policy is explicitly pre-registered.
9. Preserve all raw events, including losing and rejected/no-trade cases.

## Daily output
- event timestamp
- contract
- direction
- signal state
- entry
- stop
- targets
- outcome
- MFE
- MAE
- time-to-target
- market/session metadata

## Governance
Predictions are immutable.
Outcomes are appended later.
No future chart information may alter an earlier signal record.

## Evaluation
Report:
- gross R
- net R after stated costs
- profit factor
- max drawdown
- target-first rates
- MFE/MAE
- contract and day clustering
- uncertainty intervals
- number of trades
- no-trade rate

The frozen hypothesis is not considered validated until forward/holdout evidence is sufficiently large and reproducible.
