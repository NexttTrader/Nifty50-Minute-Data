# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-15

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=750, last_timestamp=2026-10-15T09:59:59+00:00, signals=3, outcomes=3.
Raw SHA-256: 8e184b00e373b5ae370d09e0b5ba3eb794b80172251e41b8d683d07dd67bb67a
Signal-file SHA-256: 71abf377c2d253e97899d5214d676dcdd096bb91ff062d8acd30b9bf8264e813
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
