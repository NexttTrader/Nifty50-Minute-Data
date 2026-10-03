# Phase 83 — External Holdout Pressure Diagnostic
Date: 2026-10-03

## Purpose

Evaluate the already-defined H-M8 continuous clipping-pressure feature on the independent NIFTY26JANFUT secondary archive, without changing the threshold or creating a new execution rule.

## Results

Within the 26 frozen H-M1 events:

- Spearman(pressure, 20-bar signed return) = +0.704
- Spearman(pressure, 20-bar MFE) = +0.785
- Spearman(pressure, 20-bar MAE) = +0.760
- Pressure-only AUC for the binary frozen 2R target-first outcome = 0.392
- Six of 26 H-M1 events reached 2R before adverse 1R.
- Mean pressure among 2R successes = 0.744
- Mean pressure among 2R non-successes = 0.874

Within clip-count cells:
- 1 aligned clip: n=2, ret20 -1.261 ATR
- 2 aligned clips: n=13, ret20 -0.849 ATR
- 3 aligned clips: n=11, ret20 +0.444 ATR

## Interpretation

This contract provides an important separation between movement potential and executable tradeability.

Higher continuous clipping pressure is strongly associated with larger favorable excursion and larger adverse excursion. The feature therefore behaves like an **intensity / path-volatility measure**, not a monotonic predictor of whether a fixed 1-ATR stop / 2R target will succeed.

That explains why a movement model can look informative while a fixed 2R strategy remains weak. Increasing pressure appears to increase the size of the subsequent path in both directions.

The external contract therefore does not support promoting a pressure threshold. It does support retaining continuous pressure as a diagnostic feature for future, independently specified risk-geometry research.

## Governance

No H-M8 threshold or H-M6 rule was changed.
No holdout observation was used to fit a new trading rule.
This result is an external diagnostic only.

Future risk-geometry experiments must be given new hypothesis IDs and evaluated on fresh data, not retuned on NIFTY26JANFUT.
