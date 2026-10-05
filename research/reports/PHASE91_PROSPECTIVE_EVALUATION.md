# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-05

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=150, last_timestamp=2026-10-05T09:59:58+00:00, signals=1, outcomes=1.
Raw SHA-256: ef29eeea7bd407bd2790f5c866a36b70b7e0ae50f914cfdb69d72a592fa044ee
Signal-file SHA-256: e18e9823624212c714928b3687ed946be1de97eacf8d46fe4d59940390534594
Outcome-file SHA-256: 2a60d94ba23ebdcc4e61899f985ebab355aad40556b63b8080aa5fc25d1848d4

## Integrity
See research/data/forward/PHASE91_DATA_INTEGRITY.csv.

## Results
| Hypothesis | Signals | Mature 20-bar | Mean ret20 ATR | Mean R2 | 2R first | Mean R3 | 3R first |
|---|---:|---:|---:|---:|---:|---:|---:|
| H-M1 | 1 | 1 | +1.297 | +2.000 | 100.0% | +1.297 | 0.0% |
| H-M6 | 0 | 0 |  |  |  |  |  |
| H-M9 | 0 | 0 |  |  |  |  |  |
| H-M14 | 0 | 0 |  |  |  |  |  |

## Governance
- H-M1, H-M6, H-M9 and H-M14 definitions are unchanged.
- Immature signals are excluded from 20-bar movement metrics.
- Fixed-risk target/stop outcomes use stop-first ambiguity.
- H-M14 remains future-only and is not evaluated against the already-seen January external holdout.
- No target, stop, horizon, threshold, or filter is selected from October outcomes.
- A prospective result is not called validated without adequate unseen sample size, clustering adjustment, and cost robustness.
