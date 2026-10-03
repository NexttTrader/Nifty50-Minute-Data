# Phase 82 — Independent Public Futures Holdout: NIFTY26JANFUT

Date: 2026-10-03

## Purpose

Run the frozen H-M1/H-M6/H-M9 definitions on a genuinely unseen, contract-specific NIFTY futures dataset that was not part of the Apr-Sep 2026 discovery/validation corpus.

## External source

Source repository:
https://github.com/achauh2723/Quantitative_Trading_Strategy_Development_Task_Aryan_Chauhan

Source file:
data/nifty_futures_5min.csv

Source blob SHA:
3ba0cbf9573d9907940b53a9f6f6148376ccf651

The source file contains 4,125 five-minute observations for NIFTY26JANFUT from 2025-10-29 09:15 IST through 2026-01-16 15:25 IST, covering 55 complete sessions of 75 bars. It includes OHLC, volume, OI, contract symbol and expiry.

The source project's README states that the futures dataset was part of its quantitative pipeline. The file was copied without modification into this repository for provenance.

## Frozen calculation

Canonical SALMA-B0:
- Close
- baseline WMA(5)
- population SD(5)
- width 0.30
- clipped close
- WMA(10)
- final WMA(3)
- state is the sign of consecutive SALMA slope
- confirmed flips only

H-M1/H-M6/H-M9/H-M12 were applied exactly as frozen in the project documentation. No thresholds were re-estimated from this external sample.

Execution:
- next-bar open
- 1 ATR14 risk using causal rolling mean TR14
- 2R / 3R targets
- 20-bar/session-close horizon
- stop-first on same-bar target/stop ambiguity

## Data integrity

- rows: 4125
- sessions: 55
- bars/session: 75 exactly for every session
- intraday gaps larger than 5 minutes: 0
- contract: NIFTY26JANFUT only
- expiry: 2026-01-27

## Results

| Cohort | n | 20-bar return | R2 mean | R3 mean | MFE20 | MAE20 | 2R target-first |
|---|---:|---:|---:|---:|---:|---:|---:|
| H-M1 | 26 | -0.334 | -0.138 | -0.087 | 1.637 | 1.823 | 23.1% |
| H-M6 | 24 | -0.257 | -0.066 | -0.011 | 1.724 | 1.830 | 25.0% |
| H-M9 | 4 | -0.940 | -0.750 | -0.750 | 2.096 | 2.200 | 0.0% |
| H-M12 | 15 | -0.582 | -0.306 | -0.173 | 1.454 | 1.857 | 13.3% |
| Non-H-M1 control | 98 | 0.501 | 0.272 | 0.371 | 2.419 | 1.821 | 35.7% |

### Primary external-holdout observation

H-M1 vs control:
- 20-bar return delta = -0.835 ATR
- R2 delta = -0.410R

H-M6 vs control:
- 20-bar return delta = -0.757 ATR
- R2 delta = -0.338R
- 2R target-first delta = -10.7 percentage points

### Interpretation

The external NIFTY26JANFUT contract does not reproduce the positive H-M1/H-M6 executable behavior seen in Jul-Sep 2026. Both frozen SALMA hypotheses are weaker than the control on this partial unseen contract.

The result is especially important because the event definition and SALMA parameters were not tuned on this sample.

H-M9 is too small for inference (4 events). H-M12 is also post-hoc exploratory and must not be treated as an independent discovery.

## What this means for the research

This is the first independent contract-level holdout that materially challenges the 2026 futures result.

The current evidence now supports:
1. the 2026 H-M6 path pattern is regime/instrument-sensitive rather than universal;
2. the exact SALMA clipping threshold is not a stable edge across unseen data;
3. the delayed-expansion mechanism remains a useful descriptive hypothesis, but it is not yet a validated trading rule;
4. research should stop searching for another Apr-Sep-derived threshold.

## Governance

No signal parameters were changed.
No execution parameters were changed.
No holdout outcome was used to redesign H-M1/H-M6/H-M9.
The Jan contract is retained as an external holdout, and further contracts should be evaluated using the same frozen protocol.

## Reproducibility

- Raw source snapshot: research/data/external_holdout/NIFTY26JANFUT_5m_public_source.csv
- Event-level frozen evaluation: research/data/external_holdout/PHASE82_NIFTY26JANFUT_EVENTS.csv
- Summary metrics: research/data/PHASE82_EXTERNAL_HOLDOUT_SUMMARY.csv

