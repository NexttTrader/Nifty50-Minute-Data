# H-M3 — Indicator Family / SALMA Specificity

## Statement
A part of the H-M1 relationship may come from short-horizon smoothed-state transitions generally, rather than SALMA's volatility clipping specifically.

## Current evidence
On the identical compression-release breakout event universe, direction-aligned 1–3 bar flips gave the following validation 3R candidate-vs-control differences:
- SALMA-B0: +0.312R
- unclipped double-WMA(10,3): +0.229R
- WMA10: +0.103R
- EMA10: +0.102R
- SMA10: +0.098R
- WMA20: +0.171R

SALMA also frequently led the unclipped double-WMA state flip by a median ~1 five-minute bar among H-M1 candidates.

## Status
UNVALIDATED.

## Required future test
Freeze the event definition and compare all indicator variants on an unseen futures period with identical execution and no parameter retuning.
