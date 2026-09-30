# Phase 40–44 — Deeper SALMA Research

This report records post-H-M1 exploratory diagnostics. H-M1 itself remains frozen.

## Key findings

1. **SALMA specificity is not yet established.** On the identical compression-release breakout event universe, a recent 1–3 bar direction-aligned flip in an unclipped double-WMA(10,3) also shows a positive validation 3R candidate-vs-control difference (+0.229R) versus SALMA-B0 (+0.312R). WMA20 is +0.171R. This means part of H-M1 may be a generic smoothed-state effect rather than a property unique to SALMA's volatility clipping.

2. **SALMA often changes state earlier than the unclipped double-WMA.** Among H-M1 candidates, SALMA led the direction-aligned double-WMA flip in 41/72 validation events; simultaneous in 30/72; later in 0/72. Mean lead was about 0.76 five-minute bars. The lead itself was not independently stable enough to become a rule.

3. **15-minute alignment is promising but not SALMA-specific.** H-M1 + completed 15m SALMA agreement had validation mean R3 about +0.298R, versus +0.040R when 15m SALMA disagreed. Comparable generic 15m moving-average alignment also showed positive conditioning, so this is better interpreted as a higher-timeframe state feature than proof of a proprietary SALMA effect.

4. **The H-M1 effect appears more pronounced in later movement horizons.** The candidate group has larger 10–20 bar signed returns and larger MFE than controls. This supports a movement-persistence interpretation more than an immediate-momentum interpretation.

5. **Execution remains fragile.** On the independently reconstructed 1ATR/same-session simulation, validation candidate mean R was approximately -0.002 at 1.5R, +0.090 at 2R, and +0.162 at 3R. These are gross diagnostic results and should not be interpreted as deployable strategy performance.

6. **Session-time and expiry effects are exploratory only.** Some early-session bins show better gross 3R behavior, but these cuts are post-hoc and small. No live filter is promoted.

7. **Volume/OI are not yet primary drivers.** Relative volume and short-term OI changes did not show a stable monotonic relationship. OI should remain contextual until source/units are standardized.

8. **Cross-instrument transfer is weak.** On the long 2015–2021 NIFTY index data, the H-M1 sequence showed a small movement-persistence effect but no 1ATR/2R trading improvement. This argues against treating H-M1 as a universal market law.

## New exploratory hypotheses

### H-M3 — Indicator-family hypothesis
The useful component may be a short-horizon smoothed-state transition rather than SALMA's volatility clipping specifically. The holdout should compare SALMA-B0, unclipped double-WMA(10,3), WMA10, EMA10, SMA10 and WMA20 under identical conditions.

### H-M4 — Higher-timeframe alignment
H-M1 may be more informative when the completed 15-minute directional state agrees with the breakout direction. The holdout must compare SALMA 15m alignment with generic 15m moving-average alignment.

### H-M5 — Session timing
H-M1's current 2026 sample shows stronger gross 3R behavior in the first two hours than some later bins. This is unvalidated and may simply reflect regime composition.

## Governance

- H-M1 is frozen.
- H-M3/H-M4/H-M5 are hypotheses only.
- No further in-sample tuning is allowed against Apr–Sep 2026.
- The next decisive evidence must be unseen futures data or forward paper observations.
