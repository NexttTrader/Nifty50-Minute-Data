# Phase 83 — Multiple-Testing Audit of Fixed Validation Hypotheses
Date: 2026-10-03

## Purpose
Audit the existing validation evidence as a family rather than reading each hypothesis in isolation. This is a statistical governance phase, not new signal mining.

H-M1, H-M6 and H-M9 are evaluated exactly as defined. H-M12 is excluded because it was formed after viewing validation outcomes. H-M8 is a continuous diagnostic and is not included in this six-test binary family.

## Six fixed comparisons
Three hypotheses × two endpoints:
- H-M1, H-M6, H-M9
- mean 2R benchmark difference versus non-H-M1 control
- mean 20-bar signed-return difference versus non-H-M1 control

Uncertainty uses day-cluster bootstrap.

## Results
| Hypothesis | Endpoint | n | Difference vs control | 95% cluster interval | Raw P(delta <= 0) | Holm-adjusted |
|---|---|---:|---:|---:|---:|---:|
| H-M1 | 2R | 66 | +0.132R | [-0.215,+0.480] | 0.234 | 0.468 |
| H-M6 | 2R | 54 | +0.312R | [-0.076,+0.680] | 0.058 | 0.230 |
| H-M9 | 2R | 10 | +0.615R | [-0.371,+1.484] | 0.100 | 0.301 |
| H-M1 | ret20 | 66 | +0.990 ATR | [-0.028,+2.225] | 0.028 | 0.142 |
| H-M6 | ret20 | 54 | +1.443 ATR | [+0.329,+2.794] | 0.005 | 0.029 |
| H-M9 | ret20 | 10 | +0.377 ATR | [-1.062,+1.641] | 0.278 | 0.468 |

The Holm correction is applied across all six comparisons. Because the raw probabilities come from a bootstrap sign calculation rather than a classical permutation test, the adjusted values are a governance sensitivity check, not formal frequentist p-values.

## Interpretation
The strongest surviving statement in the current corpus is about delayed movement persistence. H-M6 retains the clearest fixed-hypothesis movement result after accounting for the fact that several related hypotheses/endpoints were examined.

The fixed 2R execution result does not survive the same multiplicity lens. Therefore H-M6 should not be described as a validated executable trading edge.

## Governance
No signal definition changed.
No threshold changed.
No stop/target/holding-period choice changed.
No new hypothesis was promoted.

The research claim remains:
H-M6 is a plausible delayed-expansion/path-persistence marker in the 2026 futures sample, but its monetizable trading advantage remains unvalidated.

The decisive next evidence remains the independent Oct 2025-Mar 2026 actual futures holdout.
