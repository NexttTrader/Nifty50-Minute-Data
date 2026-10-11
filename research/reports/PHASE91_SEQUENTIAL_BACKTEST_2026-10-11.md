# Phase 91 — Sequential SALMA Backtest
Date: 2026-10-11

## Verdict
H-M6 remains a research candidate, not a production strategy. On the frozen July–September 2026 validation contracts, a sequential, one-position-at-a-time simulation with a 1R stop and 2R target produced +0.195R/trade across 51 trades, +9.95R in total, PF 1.36 and maximum fixed-risk drawdown 4.0R before costs. A 2-point round-trip cost stress reduces mean expectancy to +0.086R/trade; the 4-point stress turns it negative (-0.022R/trade).

H-M1 alone was essentially flat on validation (+0.015R/trade gross; -0.095R with a 2-point cost stress). All base compression-release events together were negative in validation. Results are not stable enough for deployment; April was negative, June generated most discovery profit, and July/August validation margins were small.

## Frozen rules
- SALMA-B0: Close source, WMA(5) clipping baseline, population SD(5), width 0.30, then WMA(10) and WMA(3), with confirmed close-bar flips.
- Base event: close breaks the prior 10-bar high/low; event range >= 1.25 times the median of prior 10 ranges; mean prior-5-bar range divided by causal ATR14 <= 1.0.
- H-M1: base event and a confirmed SALMA-B0 flip 1–3 completed bars earlier.
- H-M6: H-M1 plus at least 2 of the prior 3 completed candles closing beyond the SALMA volatility band in the breakout direction.
- Entry next bar open; risk = ATR14 calculated from the event bar plus prior 13 true ranges. Test fixed 1.5R, 2R and 3R targets with a 1R stop, max 20 subsequent bars within the same session. Stop-first on same-bar target/stop collisions; otherwise exit at the final available close in the horizon.
- Each simulated strategy holds at most one position. Signals whose next-bar entry overlaps an existing position are skipped. Discovery = April–June; validation = July–September. October remains a separate, incomplete forward holdout.

## Independent outcome-engine audit
All 513 frozen events (258 discovery, 255 validation) were re-run against the raw canonical candles. Maximum absolute numeric difference versus the existing audited benchmark was 1.78e-15 for R1.5, R2, R3, 20-bar signed return, MFE and MAE; R2/R3 outcome status labels also matched exactly. This phase re-audited outcomes/execution from frozen event flags; it did not fit or modify signal thresholds.

## Sequential 2R / 1R results (one position at a time)
All returns are fixed-risk R units, before costs. Drawdown is calculated on the chronological additive R-equity curve; no compounding.

| Group | Split | Available signals | Trades | Mean R/trade | Total R | PF | Win rate | Max DD |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| All base events | Discovery | 258 | 208 | -0.076 | -15.90 | 0.88 | 34.6% | 32.99R |
| All base events | Validation | 255 | 219 | -0.058 | -12.61 | 0.91 | 34.7% | 39.65R |
| H-M1 | Discovery | 73 | 68 | +0.220 | +14.94 | 1.43 | 47.1% | 10.88R |
| H-M1 | Validation | 66 | 63 | +0.015 | +0.95 | 1.02 | 38.1% | 8.70R |
| H-M6 | Discovery | 64 | 59 | +0.373 | +21.99 | 1.81 | 52.5% | 7.83R |
| **H-M6** | **Validation** | **54** | **51** | **+0.195** | **+9.95** | **1.36** | **45.1%** | **4.00R** |
| H-M1 but not H-M6 | Discovery | 9 | 9 | -0.783 | -7.05 | 0.12 | 11.1% | 7.05R |
| H-M1 but not H-M6 | Validation | 12 | 12 | -0.750 | -9.00 | 0.18 | 8.3% | 9.00R |
| Non-H-M1 control | Discovery | 185 | 160 | -0.198 | -31.73 | 0.71 | 29.4% | 39.56R |
| Non-H-M1 control | Validation | 189 | 170 | -0.039 | -6.68 | 0.94 | 35.3% | 30.88R |

## H-M6 validation sensitivity
| Target | Trades | Mean gross R/trade | Total gross R | PF | Mean after 2-point cost stress |
|---|---:|---:|---:|---:|---:|
| 1.5R | 51 | +0.113 | +5.76R | 1.21 | +0.004R |
| 2R | 51 | +0.195 | +9.95R | 1.36 | +0.086R |
| 3R | 50 | +0.167 | +8.34R | 1.27 | +0.058R |

For the validation 2R/1R variant, assumed round-trip costs of 0, 1, 2, 3, 4 and 5 index points produce mean net expectancy of +0.195, +0.141, +0.086, +0.032, -0.022 and -0.076R/trade, respectively. These are fixed-point stress tests, not estimates of actual broker charges, spread or slippage.

## Monthly stability
| Month | Trades | Mean R/trade | Total R | PF | Max DD |
|---|---:|---:|---:|---:|---:|
| April | 18 | -0.171 | -3.08R | 0.72 | 6.42R |
| May | 25 | +0.184 | +4.61R | 1.35 | 6.75R |
| June | 16 | +1.279 | +20.46R | 7.82 | 2.00R |
| July | 12 | +0.110 | +1.31R | 1.19 | 4.00R |
| August | 13 | +0.076 | +0.99R | 1.14 | 2.00R |
| September | 26 | +0.294 | +7.64R | 1.55 | 4.00R |

June is an outsized share of the discovery gain. July and August validation margins are weak before costs. This makes the pooled mean unreliable as a stand-alone claim of robust alpha.

## October forward holdout, kept separate
The supplied October capture includes September 30 warm-up plus only October 1 and 5. The 12 events independently re-run with no numerical outcome mismatch. Sequential 2R/1R results: all base events 11 trades / +1R total; H-M1 2 trades / +1R total (one +2R and one -1R); H-M6 one trade / -1R. This is too small to validate or reject any candidate and is not pooled into July–September results.

## Decision
1. Do not use SALMA green/red as a stand-alone reversal rule.
2. Keep H-M6 as a research tag only; the 2-point cost cushion is small and disappears by 4 points.
3. Do not optimize on the six-month sample. More unseen actual monthly-futures contracts and broker-specific execution costs are required.
4. Keep October rules frozen and append only genuine candles. No synthetic or interpolated candles were used.
