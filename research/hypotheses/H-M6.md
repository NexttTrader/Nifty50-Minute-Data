# H-M6 — SALMA Clipping Interaction Hypothesis

## Statement
H-M1 may be materially stronger when at least 2 of the previous 3 completed bars contain a SALMA direction-aligned volatility-clipping event.

For an upward breakout, aligned clipping means close above the SALMA upper band. For a downward breakout, aligned clipping means close below the lower band.

## Exact audit evidence
Discovery Apr-Jun:
- n=64
- mean R2 +0.359
- mean R3 +0.384
- 20-bar signed return +0.883 ATR

Validation Jul-Sep:
- n=54
- mean R2 +0.240
- mean R3 +0.225
- 20-bar signed return +1.454 ATR
- MFE 2.990 ATR
- MAE 1.497 ATR
- 2R target-first 33.3%

Validation non-H-M1 control n=189:
- mean R2 -0.072
- mean R3 -0.111
- 20-bar signed return +0.010 ATR

Candidate-control deltas:
- R2 +0.312R
- R3 +0.336R
- 20-bar signed return +1.443 ATR

## Cluster uncertainty
Validation day-cluster bootstrap, 10,000 resamples:
- R2 delta 95% CI approximately [-0.026, +0.714]
- R3 delta 95% CI approximately [-0.092, +0.808]
- 20-bar signed-return delta 95% CI approximately [+0.380, +2.888] ATR

## Sensitivity
Within validation H-M1 candidates, mean R2 increases across aligned clipping counts. Thresholds >=1, >=2, and =3 yield candidate-control R2 deltas of approximately +0.165, +0.312 and +0.460 respectively. These are post-hoc diagnostics, not fitted rules.

## Interpretation
The potential mechanism is that repeated directional closes outside SALMA's narrow volatility band indicate persistent directional pressure, while the SALMA state flip provides a short-horizon transition marker before the compression-release event.

This is an exploratory interpretation only.

## Status
STRONG EXPLORATORY HYPOTHESIS, NOT VALIDATED.
No optimization or live deployment before unseen/forward testing.
