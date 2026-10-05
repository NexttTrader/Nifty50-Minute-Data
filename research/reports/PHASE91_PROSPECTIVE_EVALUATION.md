# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-05

## Purpose

This is the permanent prospective evaluation gate for the October 2026 NIFTY futures stream.

It evaluates only frozen H-M1, H-M6, H-M9 and future-only H-M14 signals. It does not alter signal definitions, select thresholds from October outcomes, or use immature observations as performance data.

## Current state

The corrected October stream contains 85 regular-session 5-minute bars:
- 75 bars for 2026-10-01;
- 10 bars for 2026-10-05 through 10:03:59 IST.

Frozen prospective signals: 0.
Mature outcomes: 0.

Therefore no forward performance statistic is reported yet.

## Integrity gate

The Phase 90 timestamp correction is applied before this evaluator:
- source timestamps are localized to Asia/Kolkata and converted to UTC;
- only 09:15:00 through 15:29:59 IST is accepted;
- duplicate timestamps and OHLC inconsistencies are rejected;
- future-dated source bars are rejected.

The corrected forward raw SHA-256 is:
823af836e4d0eedf7ccfe2d271bc86e5b05d1b12e0489a07c0ce9b0b43683552

All current integrity checks pass.

## Predeclared endpoints

When mature observations exist, the evaluator will report:
- same-session 20-bar direction-adjusted return in ATR units;
- median and positive-share of 20-bar return;
- 20-bar MFE and MAE;
- fixed 1.5R, 2R and 3R stop-first outcomes;
- target-first rates at those barriers.

H-M14 is future-only and will never be treated as validated using the already-seen January external holdout.

## Governance

No historical result has been retuned.
No October result has been used to modify any signal.
Immature observations remain separate from mature outcomes.
The prospective stream is observational until enough unseen observations accumulate for meaningful clustered and cost-aware evaluation.
