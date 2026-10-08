# Phase 86 — Directional Asymmetry and Lifecycle Audit
Date: 2026-10-06

## Purpose
Continue the frozen SALMA/NIFTY research without changing H-M1, H-M6, H-M8 or H-M9.
This phase tests whether the residual H-M6 movement association is symmetric across breakout direction and whether it appears only after a delayed lifecycle has developed.

No threshold, entry, target, stop, or holding-period parameter was optimized.

## Data
- Exact Apr-Sep 2026 NIFTY futures dataset: 8,594 five-minute candles.
- Frozen event universe: 513 events.
- Validation: 255 events.
- H-M6 validation events: 54.
- Outcomes: frozen `ret20atr` from the audited event table.

## 1. Directional asymmetry

Validation H-M6 versus same-direction non-H-M1 controls:

| Breakout direction | H-M6 n | Control n | H-M6 mean ret20 | Control mean ret20 | Delta |
|---|---:|---:|---:|---:|---:|
| Down | 32 | 107 | +2.160 ATR | -0.066 ATR | **+2.226 ATR** |
| Up | 22 | 82 | +0.426 ATR | +0.110 ATR | +0.316 ATR |

The movement association is therefore overwhelmingly concentrated in **downside H-M6 events** during the 2026 validation sample.

Day-cluster bootstrap for the downside delta across 21 common days:
- mean day-level delta: +1.764 ATR
- median day-level delta: +0.805 ATR
- 95% bootstrap interval: approximately [+0.06, +3.77] ATR
- bootstrap P(delta <= 0): approximately 0.021

The corresponding upside day-cluster interval spans zero:
- +0.313 ATR point estimate
- 95% interval approximately [-0.96, +1.59] ATR
- P(delta <= 0) approximately 0.31

### July 8 sensitivity
Removing the entire July 8 session from the downside H-M6 comparison leaves:
- H-M6 n = 30
- control n = 105
- H-M6 mean ret20 = +1.326 ATR
- control mean = -0.049 ATR
- delta = **+1.375 ATR**

Thus the downside association is not solely a July 8 artifact.

## 2. Contract stability of the downside effect

Downside H-M6 versus downside non-H-M1 control by validation contract:

| Contract | H-M6 n | Control n | Delta ret20 |
|---|---:|---:|---:|
| July 2026 | 7 | 41 | +5.483 ATR |
| August 2026 | 9 | 23 | +0.423 ATR |
| September 2026 | 16 | 43 | +1.476 ATR |

All three validation contracts have positive point estimates, although July is much larger and contains the major tail observation.

This is stronger than the all-direction result for one reason: the asymmetry is visible across all three contracts, not just in a pooled sample.

## 3. Non-overlap stress test for downside H-M6

Chronology-preserving same-session thinning was applied so that events had to be at least N bars apart.

| Cooldown | H-M6 n | Control n | Delta ret20 |
|---:|---:|---:|---:|
| 0 | 32 | 107 | +2.226 ATR |
| 10 | 21 | 84 | +2.095 ATR |
| 20 | 17 | 61 | +1.895 ATR |
| 30 | 13 | 50 | +1.507 ATR |

The point estimate remains strongly positive even after the 20-bar de-overlap condition. At 30 bars the confidence becomes wide, as expected from the small number of independent episodes.

For the 20-bar cooldown:
- 13 common days remain.
- day-level mean delta ≈ +2.241 ATR.
- day-level median delta ≈ +0.805 ATR.
- 95% day bootstrap interval ≈ [-0.69, +5.98] ATR.
- bootstrap P(delta <= 0) ≈ 0.084.

This means the downside effect survives de-overlap in point-estimate terms, but strict episode-level uncertainty is still substantial.

## 4. Lifecycle from the raw candles

An independent raw-candle reconstruction measured direction-adjusted return from the next-bar open to future same-session closes using the event-bar ATR14 as the scale. This is an ancillary lifecycle diagnostic; the audited event-table `ret20atr` remains the primary endpoint.

| Horizon | H-M6 mean | Control mean | Delta |
|---:|---:|---:|---:|
| 1 bar | +0.110 | -0.097 | +0.207 ATR |
| 3 bars | +0.345 | -0.031 | +0.377 ATR |
| 5 bars | +0.610 | -0.026 | +0.636 ATR |
| 10 bars | +0.992 | +0.030 | +0.962 ATR |
| 15 bars | +1.482 | +0.053 | +1.428 ATR |
| 20 bars | +1.726 | +0.014 | +1.712 ATR |

The median effect is small at short horizons and becomes more positive by 10–20 bars. This is consistent with the earlier competing-hazard and pressure-model results: H-M6 is better interpreted as a **delayed expansion state** than as immediate breakout momentum.

At 20 bars, the H-M6 positive-return share was about 61% versus 51% for control; the share exceeding +1 ATR was about 43% versus 30%.

## 5. What this changes

The most interesting remaining anomaly is no longer “H-M6 works in general.”

It is:

**downside breakout + prior directional pressure + compressed release + recent SALMA state transition + repeated downside clipping -> delayed downside expansion**

The evidence is still insufficient to claim a tradable edge because:
- the exact effect is based on only 32 validation downside H-M6 events;
- July 8 contributes a large tail, even though the result survives its removal;
- strict episode-level independence leaves wide uncertainty;
- older index transfer did not preserve a comparable fixed-R advantage;
- generic smoother tests indicate SALMA-specific causality is not established.

## 6. Research decision

No new trading filter is promoted.

The downside asymmetry is now registered as a **mechanism hypothesis**, not a rule:

> H-M6 may be detecting a bearish pressure-release regime in which prior downside displacement is still structurally unresolved and a subsequent compression break produces delayed continuation/acceleration.

This hypothesis is frozen for forward observation. It must not be refined using October outcomes.

## 7. October 2026 holdout status

Current market data confirms `NIFTY26OCTFUT` is an active NSE futures contract. Public sources show current price, volume and OI and GoCharting advertises historical/tick history and chart-data export for NSE derivatives, but no audited 5-minute OHLCV+OI file was accessible directly in this research environment.

The October holdout therefore remains pending legitimate 5-minute data capture.

Once obtained, October will be processed in one pass with:
1. exact SALMA-B0;
2. exact H-M1;
3. exact H-M6;
4. H-M8 pressure diagnostic;
5. frozen 1.5R / 2R / 3R outcomes;
6. 20-bar same-session endpoint;
7. 20- and 30-bar event de-overlap;
8. direction-specific reporting;
9. day/contract clustered uncertainty;
10. no rule changes.

## Final verdict

The research has narrowed from “find a SALMA strategy” to a much more specific scientific question:

**Can a frozen state-transition / compression-release detector identify delayed bearish expansion in unseen NIFTY futures?**

The answer remains unknown.

The historical evidence is strong enough to justify the holdout, but not strong enough to trade it live.