# Phase 86 — Prior-Extension Interaction Replication
Date: 2026-10-03

## Purpose

Test whether the January 2026 external failure mode—H-M1 firing after unusually large prior directional displacement—is a recurring mechanism.

The analysis compares:
- the 2015-2021 NIFTY index transfer dataset;
- the Apr-Sep 2026 NIFTY futures validation;
- the NIFTY26JANFUT secondary external holdout.

No new execution rule is fitted.

## 1. Historical 2015-2021 NIFTY index

Exact H-M1 candidates: n=1,184.

Terciles of direction-aligned prior-5-bar displacement:

| Prior-5 displacement tercile | n | Mean R2 | Mean R3 | Mean 20-bar return |
|---|---:|---:|---:|---:|
| Low | 393 | +0.060 | +0.116 | +0.356 ATR |
| Mid | 394 | -0.097 | -0.015 | +0.213 ATR |
| High | 395 | -0.062 | -0.095 | +0.011 ATR |

Low minus high:
- R2: +0.122R
- R3: +0.211R
- 20-bar return: +0.345 ATR

Day-cluster bootstrap over 839 sessions:
- R2 95% interval: [-0.080,+0.324]R
- R3 interval: [-0.038,+0.454]R
- 20-bar return interval: [-0.281,+0.943] ATR

The point estimates support a “late-extension penalty” in this older index transfer sample, but uncertainty is substantial.

## 2. Apr-Sep 2026 NIFTY futures validation

The same diagnostic produces a materially different pattern:

| Prior-5 displacement tercile | n | Mean R2 | Mean R3 | Mean 20-bar return |
|---|---:|---:|---:|---:|
| Low | 22 | +0.062 | -0.029 | +0.271 ATR |
| Mid | 22 | -0.358 | -0.405 | +0.850 ATR |
| High | 22 | +0.476 | +0.622 | +1.880 ATR |

Here the high-extension tercile has the largest positive movement and R2/R3 point estimates.

This directly rules out a universal rule of the form “H-M1 is better only when prior extension is low.”

## 3. NIFTY26JANFUT external holdout

The 26 external H-M1 events had:
- mean prior-5 displacement +2.456 ATR;
- mean prior-20 displacement +1.684 ATR;
- 20-bar return -0.334 ATR;
- R2 mean -0.138R.

Thus the January failure occurred in a population with large pre-event directional extension, but the cross-dataset comparison shows that extension alone cannot explain all regimes.

## 4. Combined interpretation

The evidence now favors a two-dimensional state:

**prior directional extension × event shock / release intensity**

rather than a single prior-return filter.

A large prior move can be:
- continuation fuel in one regime;
- late/chasing behavior in another.

The event shock relative to the preceding local range appears to be a more natural second axis because it measures whether the current breakout is a genuinely new release or simply another move inside an already directional path.

## 5. Governance

This phase is exploratory and post-hoc.

No hard prior-return threshold is adopted.
No event-shock threshold is adopted.
No current holdout is used to fit a new trading rule.

The next new hypothesis is therefore defined as an observational, future-only interaction test.

## Status

Mechanistic replication: useful.
Universal prior-extension filter: not supported.
Future-only H-M13 specification: created separately.
