# Phase 82 — Predeclared Delayed-Horizon Movement Test
Date: 2026-10-03

## Purpose

Test whether the frozen H-M6 signal is better characterized as a delayed movement forecast than as an immediate breakout/target-first signal.

This phase does not alter H-M1, H-M6, H-M8 or H-M9. No holding period or trading threshold is selected after looking at outcomes. The horizons 1, 3, 5, 10 and 20 bars were evaluated together as a predeclared lifecycle panel.

## Data

- Exact Apr-Sep 2026 NIFTY futures, 5-minute bars.
- Official frozen event universe: 513 events.
- H-M6: 118 events overall; validation 54.
- Non-H-M1 control: 374 overall; validation 189.
- Returns are direction-adjusted close-to-close returns from the next-bar execution price, normalized by the event ATR14 risk unit.
- Only same-session observations are used. A horizon is measured only when the required number of same-session bars exists.

## Validation horizon results

| Horizon | H-M6 n | H-M6 mean | H-M6 median | H-M6 positive rate | Control n | Control mean | Mean delta |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 54 | +0.110 | -0.037 | 46.3% | 189 | -0.097 | +0.207 ATR |
| 3 | 53 | +0.463 | -0.063 | 45.7% | 187 | -0.026 | +0.377 ATR |
| 5 | 53 | +0.610 | -0.125 | 46.3% | 181 | -0.026 | +0.636 ATR |
| 10 | 51 | +0.992 | +0.218 | 53.7% | 172 | +0.030 | +0.962 ATR |
| 20 | 44 | +1.726 | +0.453 | 65.1% | 158 | +0.014 | +1.712 ATR |

The H-M6 point estimate becomes progressively more positive from 1 through 20 bars, while the control remains near zero or mildly negative.

## Day-cluster uncertainty

| Horizon | Delta | 95% cluster interval | P(delta <= 0) |
|---:|---:|---:|---:|
| 1 | +0.207 ATR | [-0.204, +0.580] | 0.212 |
| 3 | +0.377 ATR | [-0.357, +1.058] | 0.232 |
| 5 | +0.636 ATR | [-0.129, +1.905] | 0.059 |
| 10 | +0.962 ATR | [-0.054, +2.303] | 0.032 |
| 20 | +1.712 ATR | [+0.348, +3.392] | 0.0046 |

## Time-of-day adjustment

A fixed 30-minute time-of-day-bin adjustment was applied together with breakout direction:

- 5 bars: H-M6 coefficient +0.683 ATR, cluster SE 0.533, p=0.200
- 10 bars: +0.982 ATR, SE 0.611, p=0.108
- 20 bars: +1.681 ATR, SE 0.791, p=0.034

Equal-weighting common 30-minute bins retained positive differences:
- 5 bars: +0.490 ATR
- 10 bars: +0.808 ATR
- 20 bars: +1.334 ATR

## Outlier robustness

| Horizon | H-M6 mean | H-M6 median | H-M6 10%-trimmed mean | Control mean | Control 10%-trimmed mean |
|---:|---:|---:|---:|---:|---:|
| 5 | +0.610 | -0.125 | +0.108 | -0.026 | -0.064 |
| 10 | +0.992 | +0.218 | +0.522 | +0.030 | -0.019 |
| 20 | +1.726 | +0.453 | +0.996 | +0.014 | -0.023 |

The 10- and 20-bar H-M6 medians and trimmed means remain positive, so the later effect is not explained solely by a handful of extreme moves.

## Interpretation

The evidence increasingly supports the abstraction:

**H-M6 appears to identify a state with delayed favorable path persistence rather than immediate breakout momentum.**

The result remains exploratory. Later horizons have fewer same-session observations, and the validation sample is small. This is a movement/path finding, not a validated trading rule.

## Scientific consequence

The next unseen-data validation should use movement-persistence forecasting as the primary endpoint and target-first execution as a secondary endpoint. The frozen H-M6 signal should be evaluated prospectively at predeclared horizons rather than repeatedly changing stops or targets.

## Governance

- H-M1 unchanged.
- H-M6 unchanged.
- H-M8 unchanged.
- H-M9 unchanged.
- No target/stop/holding-period optimization.
- 2026 historical corpus remains frozen.
- Unseen actual futures data remains the decisive external validation gate.
