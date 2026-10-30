# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-30

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=1275, last_timestamp=2026-10-27T09:59:58+00:00, signals=5, outcomes=5.
Raw SHA-256: 50fb24924dc6f92d3eb9416636fb1c7eb5ccd8d77ef6a32889eb13f623acd0f4
Signal-file SHA-256: 59432c8a170eb6c7dfd4bd6db91d5ab4f5d3119066270213ec1b75bdf77112f4
Outcome-file SHA-256: 5df2378e37cf6846619743b78a8599b94cee71f02c5be367c16875cc70d4b201

## Integrity
See research/data/forward/PHASE91_DATA_INTEGRITY.csv.

## Results
| Hypothesis | Signals | Mature 20-bar | Mean ret20 ATR | Mean R2 | 2R first | Mean R3 | 3R first |
|---|---:|---:|---:|---:|---:|---:|---:|
| H-M1 | 5 | 5 | +0.839 | -0.400 | 20.0% | -0.541 | 0.0% |
| H-M6 | 4 | 4 | +0.724 | -1.000 | 0.0% | -1.000 | 0.0% |
| H-M9 | 0 | 0 |  |  |  |  |  |
| H-M14 | 2 | 2 | +0.727 | -1.000 | 0.0% | -1.000 | 0.0% |

## Governance
- H-M1, H-M6, H-M9 and H-M14 definitions are unchanged.
- Immature signals are excluded from 20-bar movement metrics.
- Fixed-risk target/stop outcomes use stop-first ambiguity.
- H-M14 remains future-only and is not evaluated against the already-seen January external holdout.
- No target, stop, horizon, threshold, or filter is selected from October outcomes.
- A prospective result is not called validated without adequate unseen sample size, clustering adjustment, and cost robustness.
