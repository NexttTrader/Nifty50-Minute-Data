# Phase 30–34 — H-M1 Robustness, Execution Geometry and Modelling Audit

## Date
2026-09-30

## Purpose
H-M1 is frozen. These phases do not change the signal definition. They test whether the apparent relationship survives uncertainty, contract splits, event clustering, execution-friction diagnostics, time-to-target analysis, and independent modelling.

## 1. Canonical H-M1
A causal compression-release breakout is defined by:
- close breaks the prior 10-bar high/low;
- current bar range >= 1.25 x median range of prior 10 bars;
- prior-5 mean range / causal ATR14 <= 1.0;
- entry next bar open;
- initial risk 1 ATR14;
- 20-bar same-session horizon;
- stop-first if stop/target share a bar.

H-M1 adds: a confirmed SALMA-B0 slope flip occurred 1–3 completed bars before the breakout.


## New audit status
Phase 30-34 did not alter H-M1. It found positive candidate-vs-control deltas in every contract and leave-one-contract-out test, but validation cluster intervals still include zero and the gross edge is friction-sensitive. H-M1 remains PROMISING, NOT VALIDATED.

See research/reports/PHASE30_34_HM1_AUDIT.md and research/validation/H-M1_FORWARD_VALIDATION.md.
