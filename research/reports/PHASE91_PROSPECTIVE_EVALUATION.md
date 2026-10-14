# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-14

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=675, last_timestamp=2026-10-14T09:59:59+00:00, signals=3, outcomes=3.
Raw SHA-256: 73e28e1a832ccaf83bc46776e57165bdefa50d0a30092ec69742c4962d045af9
Signal-file SHA-256: 2683f987013140936615f4c02397360af844a6cec641e786bbcd47f11dc1fd12
Outcome-file SHA-256: a886ffc0a9dfa48065a5b4a11b318cea89fcbcac3d4e7b2dc2d8931d110fef11

## Integrity
See research/data/forward/PHASE91_DATA_INTEGRITY.csv.

## Results
| Hypothesis | Signals | Mature 20-bar | Mean ret20 ATR | Mean R2 | 2R first | Mean R3 | 3R first |
|---|---:|---:|---:|---:|---:|---:|---:|
| H-M1 | 3 | 3 | +1.292 | +0.000 | 33.3% | -0.234 | 0.0% |
| H-M6 | 2 | 2 | +1.290 | -1.000 | 0.0% | -1.000 | 0.0% |
| H-M9 | 0 | 0 |  |  |  |  |  |
| H-M14 | 1 | 1 | -1.118 | -1.000 | 0.0% | -1.000 | 0.0% |

## Governance
- H-M1, H-M6, H-M9 and H-M14 definitions are unchanged.
- Immature signals are excluded from 20-bar movement metrics.
- Fixed-risk target/stop outcomes use stop-first ambiguity.
- H-M14 remains future-only and is not evaluated against the already-seen January external holdout.
- No target, stop, horizon, threshold, or filter is selected from October outcomes.
- A prospective result is not called validated without adequate unseen sample size, clustering adjustment, and cost robustness.
