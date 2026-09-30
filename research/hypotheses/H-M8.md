# H-M8 — Continuous SALMA Clipping Pressure

## Statement
Within H-M1 events, the continuous magnitude of recent direction-aligned SALMA clipping may contain more information about executable tradeability than a binary SALMA flip alone.

## Feature
For an event at bar t, compute the signed clipping excess for each of t-1, t-2, t-3:
- upper-band exceedance for an upward event
- lower-band exceedance for a downward event
Normalize each excess by the causal ATR14 benchmark and sum the three values.

## Discovery -> validation experiment
A logistic model was trained on Apr-Jun H-M1 events and tested on Jul-Sep without retuning.

Base features:
- prior 3-bar absolute return / ATR
- event range / ATR

Base validation AUC: 0.437
Base Brier score: 0.214

Adding continuous aligned clipping pressure:
Validation AUC: 0.609
Validation Brier score: 0.209

Expanding-month walk-forward:
- June: AUC 0.394 -> 0.606
- July: 0.732 -> 0.518
- August: 0.462 -> 0.821
- September: 0.246 -> 0.533

The clipping feature improved AUC in 3 of 4 sequential tests and improved mean AUC from about 0.458 to 0.619.

A bootstrap interval for the fixed Apr-Jun -> Jul-Sep test AUC was approximately [0.451, 0.758]. A 10,000-permutation diagnostic gave p about 0.086, so this is not statistically conclusive.

## Relation to H-M6
Within validation H-M1 candidates, aligned clipping count and R2 outcome had Spearman rho about +0.288 (p about 0.019), while clipping count and MAE had rho about -0.286 (p about 0.020). The continuous clipping-pressure feature showed a similar directional relationship.

## Interpretation
This is the strongest current evidence that SALMA's volatility-clipping component may add incremental information beyond a generic smoothed-state flip. It also suggests that the mechanism may be continuous rather than a hard >=2-bars threshold.

## Status
STRONG EXPLORATORY HYPOTHESIS — NOT VALIDATED.

Do not tune the feature or deploy it before unseen futures/forward testing.
