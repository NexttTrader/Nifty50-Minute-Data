# Trading Memory

## Facts
- SALMA-B0 uses Close, Length 10, Smooth 3, Mult 0.30, SD Length 5.
- Research uses close-confirmed SALMA state changes.
- Current research data is Apr-Sep 2026 actual NIFTY monthly futures.

## Negative findings
- Raw green/red reversal is not validated.
- Simple parameter tweaks did not establish a stable edge.
- Simple sweep-to-MSS plus SALMA did not establish an edge.
- Price/SALMA crossover did not establish an edge.
- Static 2R outcome models did not show strong stable discrimination.

## Working model
SALMA is treated primarily as a lagged state/transition descriptor.

## Current hypothesis
H-M1: recent SALMA transition plus causal compression-release breakout.
Status: frozen, awaiting unseen/forward validation.

## Research discipline
Do not turn a hypothesis into a rule because it looks good on a completed chart. Do not edit historical predictions after outcomes are known. Keep discovery, validation and holdout data separate.