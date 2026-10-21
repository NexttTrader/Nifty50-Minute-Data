# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-21

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=975, last_timestamp=2026-10-21T09:59:58+00:00, signals=5, outcomes=5.
Raw SHA-256: ba41bb82665bf0278a9333daed90bd7973d0a55dfca92e89055a744ac3cc23fd
Signal-file SHA-256: ebfc066bf29c60416ec35781ef4a00dd707e347ced253c3b0def01c7907acc61
Outcome-file SHA-256: e86a855bf2cdb6a21fe030885a808e3af292a7b91ecb45b93c1f3c98fdf16c5d

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
