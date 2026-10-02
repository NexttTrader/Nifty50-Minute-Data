# Phase 78 — Geometry-First Residual Research
Date: 2026-10-02

## Question
Does the apparent SALMA/H-M1/H-M6 behavior contain information beyond the underlying compression-release event geometry?

This phase does not alter any frozen trading hypothesis. It evaluates a predetermined causal geometry feature family and asks whether adding the fixed H-M1 state and clipping-pressure variables adds out-of-sample information on the existing Apr-Jun -> Jul-Sep 2026 split.

## Data
- Existing exact Apr-Sep 2026 futures event artifact.
- Official events with frozen discovery/validation split: n=513.
- Discovery: n=258; validation: n=255.
- Validation 2R base rate: 0.275.

## Geometry-only model
Feature family: event range / ATR, close location, prior returns (1/3/5/10/20), and prior directional context. No SALMA state, band or clipping variables are used.

## Discovery -> validation model results
| Model | AUC | Brier |
|---|---:|---:|
| geometry_only | 0.510 | 0.204 |
| geometry_plus_HM1 | 0.511 | 0.205 |
| geometry_plus_HM1_pressure | 0.507 | 0.208 |
| geometry_plus_HM1_clipcount | 0.520 | 0.210 |
| geometry_plus_HM1_all_SALMA_context | 0.518 | 0.211 |
| HM1_geometry_only | 0.576 | 0.207 |
| HM1_geometry_plus_pressure | 0.601 | 0.217 |
| HM1_geometry_plus_clipcount | 0.543 | 0.248 |
| HM1_geometry_plus_pressure_count | 0.586 | 0.240 |

The full-event comparison asks whether adding H-M1 and its clipping context improves discrimination over event geometry alone. The result is descriptive and uses one fixed chronological split; it is not a new optimized trading rule. On all events, geometry-only AUC is 0.510; adding H-M1 moves it to 0.511, while adding continuous pressure moves it to 0.507. This does not show a robust global incremental signal.

## H-M1-conditioned residual test

Within H-M1 events only, the same geometry baseline is compared against continuous clipping pressure and clip count. This is the cleanest residual test of whether the SALMA clipping mechanism contributes after the compression-release event and H-M1 state are already known.

- H-M1 discovery n=73, validation n=66.
- Results are in PHASE78_GEOMETRY_MODEL_RESULTS.csv.

## Geometry stratification

Prior 5-bar displacement and event-shock terciles were defined on discovery only, then applied unchanged to validation. The full cells are preserved in PHASE78_GEOMETRY_BUCKETS.csv. This is a diagnostic of whether the delayed-expansion effect is concentrated in generic event geometry rather than SALMA state.

## Interpretation

The scientific objective is to separate three possibilities:
1. geometry itself predicts the later expansion;
2. H-M1 adds residual information to geometry;
3. clipping pressure adds residual information after geometry + H-M1.

Only (2) or (3), if stable on truly unseen futures data, would justify further SALMA-specific investigation. A result on Apr-Sep 2026 alone is not sufficient for validation.

## Clustered uncertainty for the H-M1 residual pressure effect

A 10,000-resample day-cluster bootstrap was run on the 66-event validation H-M1 subset, keeping the discovery-trained models fixed.

- Pressure added to geometry: AUC gain = +0.026. 95% cluster-bootstrap interval = [-0.070, +0.134]; bootstrap probability of gain <= 0 was 27.8%.
- Brier change from adding pressure = +0.010 (worse calibration). 95% interval = [-0.019, +0.046].

This makes the H-M1-conditioned pressure result a useful research lead, not evidence of a validated predictive advantage.

## Governance
No H-M1/H-M6/H-M8/H-M9 definition changed. No execution threshold was tuned. The next decisive gate remains unseen actual futures data, while these residual diagnostics define exactly what should be tested there.
