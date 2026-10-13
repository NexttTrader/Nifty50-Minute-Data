# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-13

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=600, last_timestamp=2026-10-13T09:59:58+00:00, signals=2, outcomes=2.
Raw SHA-256: 46868287510aab8f9d8d0a58a95e8c7876cea85d326970db8635375fea39a51d
Signal-file SHA-256: 4adba4203898a16477d1bb100646d659e4e61ed5e9731947fea1c5e88519785d
Outcome-file SHA-256: b56ad68587742f3617a437c4527e885cb9ef2202c383b652329311f6a495f3d2

## Integrity
See research/data/forward/PHASE91_DATA_INTEGRITY.csv.

## Results
| Hypothesis | Signals | Mature 20-bar | Mean ret20 ATR | Mean R2 | 2R first | Mean R3 | 3R first |
|---|---:|---:|---:|---:|---:|---:|---:|
| H-M1 | 2 | 2 | +0.089 | +0.500 | 50.0% | +0.148 | 0.0% |
| H-M6 | 1 | 1 | -1.118 | -1.000 | 0.0% | -1.000 | 0.0% |
| H-M9 | 0 | 0 |  |  |  |  |  |
| H-M14 | 1 | 1 | -1.118 | -1.000 | 0.0% | -1.000 | 0.0% |

## Governance
- H-M1, H-M6, H-M9 and H-M14 definitions are unchanged.
- Immature signals are excluded from 20-bar movement metrics.
- Fixed-risk target/stop outcomes use stop-first ambiguity.
- H-M14 remains future-only and is not evaluated against the already-seen January external holdout.
- No target, stop, horizon, threshold, or filter is selected from October outcomes.
- A prospective result is not called validated without adequate unseen sample size, clustering adjustment, and cost robustness.
