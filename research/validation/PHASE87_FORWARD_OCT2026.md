# Phase 87 — Prospective October 2026 NIFTY Futures Capture

## Objective

Convert the current research into a genuinely prospective forward-validation process.

The active October 2026 NIFTY futures contract expires 27-Oct-2026. Current public market sources show that contract is the front NIFTY future in early October 2026. citeturn897861search0turn897861search4

## Capture policy

Every weekday after the market session, GitHub Actions:
1. resolves the current October NIFTY futures symbol through the NSE charting symbol service;
2. refreshes contract-specific 5-minute OHLCV data from 1-Oct-2026 through the current session;
3. records any new H-M1/H-M6/H-M9 signals using only information available at the event close;
4. stores the signal log separately from outcomes;
5. appends an outcome only after the signal has matured to the 20-bar/session-close horizon;
6. commits all generated research files to Git automatically.

The capture is bounded to the October 2026 contract and does not silently roll to November.

## Research tracks

Frozen:
- H-M1
- H-M6
- H-M9

Diagnostic only:
- H-M8 continuous clipping pressure

Future-only:
- H-M13 prior-extension × event-shock interaction

H-M13 is not activated as a trading decision in Phase 87 because its exact functional form was defined after the January external holdout.

## Governance

Signals are immutable.
Outcome rows are separate and appended after maturation.
No threshold is re-estimated on forward observations.
No forward result changes an earlier signal.

## Acceptance gate

Phase 87 is an observation pipeline, not a claim of validation. Strong inference still requires substantially more independent trading days and multiple contracts.
