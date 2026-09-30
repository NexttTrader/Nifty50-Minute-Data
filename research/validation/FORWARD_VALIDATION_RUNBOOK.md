# Forward Validation Runbook

## Purpose
Evaluate frozen hypotheses on newly arriving actual NIFTY futures 5-minute data.

## Frozen tracks
- H-M1
- H-M6
- H-M12 (post-hoc exploratory)
- Generic smoother/envelope control

## At each completed candle
Use only information available at the close. Record any event and its signal state before reading subsequent candles.

## Benchmark execution
- entry: next bar open
- risk: 1 x causal ATR14 benchmark
- targets: 1.5R / 2R / 3R
- horizon: 20 bars or session close
- stop-first ambiguity

## Record
event timestamp, contract, direction, event features, SALMA state/flip, clipping, OI/volume context, entry, stops/targets, outcome, MFE, MAE, time-to-target, 5/10/20-bar signed returns, and day/contract clustering.

## Governance
No threshold retuning after forward outcomes. Any change gets a new hypothesis ID. Treat event-level and day-level uncertainty separately.

## Minimum evidence gate
Do not characterize a forward effect from fewer than 30 independent trading days. Prefer multiple contracts and >=100 eligible events before strong inference.
