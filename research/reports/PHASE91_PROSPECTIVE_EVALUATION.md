# Phase 91 — Prospective Frozen-Signal Evaluation
Date: 2026-10-19

## Purpose
Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.

## Forward state
Rows=900, last_timestamp=2026-10-19T09:59:59+00:00, signals=4, outcomes=4.
Raw SHA-256: 8b8e22a38d754f8f65e28532b59f0a4b33959d3fcd3bbead859fb8b396d0eaec
Signal-file SHA-256: d17a762add83b1db49542d0ad777283931a644efb1963697deb11227e8d4d11f
Outcome-file SHA-256: 3e2fc3ffb071d8c5ca4911026dcf4770a0618c3ac93f9fb9df22d46e12cc7eca

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
