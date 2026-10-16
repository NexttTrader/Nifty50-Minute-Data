# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-16

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=825, last_timestamp=2026-10-16T09:59:59+00:00, signals=4, outcomes=4.
Raw SHA-256: c890f374b79f7ae02ffe45d9343aafc8db22d09b2eef1ce376449b97db1ff496
Signal-file SHA-256: 4868d8cae90ba86b6cf7dfd9c19538fc84f793bf5e261147bd473ef7b91ca647
Outcome-file SHA-256: 485626d2f1b2d26ba92520d581601d1e7e55ef0cbdab4a711e34a8394cc8c986

## Integrity
See research/data/forward/PHASE91_DATA_INTEGRITY.csv.

## Results
| Hypothesis | Signals | Mature 20-bar | Mean ret20 ATR | Mean R2 | 2R first | Mean R3 | 3R first |
|---|---:|---:|---:|---:|---:|---:|---:|
| H-M1 | 4 | 4 | +0.406 | -0.250 | 25.0% | -0.426 | 0.0% |
| H-M6 | 3 | 3 | +0.108 | -1.000 | 0.0% | -1.000 | 0.0% |
| H-M9 | 0 | 0 |  |  |  |  |  |
| H-M14 | 1 | 1 | -1.118 | -1.000 | 0.0% | -1.000 | 0.0% |

## Governance
- H-M1, H-M6, H-M9 and H-M14 definitions are unchanged.
- Immature signals are excluded from 20-bar movement metrics.
- Fixed-risk target/stop outcomes use stop-first ambiguity.
- H-M14 remains future-only and is not evaluated against the already-seen January external holdout.
- No target, stop, horizon, threshold, or filter is selected from October outcomes.
- A prospective result is not called validated without adequate unseen sample size, clustering adjustment, and cost robustness.
