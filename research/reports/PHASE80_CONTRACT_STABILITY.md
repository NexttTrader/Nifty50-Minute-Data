# Phase 80 — Contract Stability and Leave-One-Contract-Out Lifecycle Test
Date: 2026-10-02

## Purpose

Test whether the Phase 79 lifecycle effect is concentrated in a single 2026 validation contract. No signal, threshold, stop, target, or holding period is changed.

## Validation contract results

H-M6 versus non-H-M1 control:

| Contract | H-M6 n | Control n | MFE20 delta | MAE20 delta | 20-bar return delta | +1R first delta | +2R first delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| July 2026 | 12 | 79 | +2.676 ATR | -0.501 ATR | +3.310 ATR | +9.5 pp | +3.0 pp |
| August 2026 | 14 | 45 | -0.289 | -0.364 | +0.426 | +13.2 pp | -7.5 pp |
| September 2026 | 28 | 65 | +0.709 | -0.500 | +0.979 | +11.0 pp | +15.7 pp |

Three observations matter:
1. The 20-bar signed-return difference is positive in all three validation contracts.
2. The 20-bar MAE difference is negative in all three contracts.
3. The largest MFE/return effect occurs in July, but August still retains positive 20-bar return and first-passage +1R separation despite weaker MFE.

## Leave-one-contract-out

The validation sample was recomputed after removing each contract in turn.

| Contract removed | H-M6 n | Control n | MFE20 delta | MAE20 delta | 20-bar return delta | +1R first delta | +2R first delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| August | 40 | 144 | +1.331 ATR | -0.551 ATR | +1.767 ATR | +11.9 pp | +11.9 pp |
| July | 42 | 110 | +0.317 | -0.438 | +0.724 | +11.3 pp | +8.1 pp |
| September | 26 | 124 | +1.239 | -0.502 | +1.983 | +13.3 pp | -2.9 pp |

The path-level result therefore survives removal of any single validation contract:
- MFE20 delta remains positive in all three leave-one-out samples.
- MAE20 delta remains negative in all three.
- 20-bar return delta remains positive in all three.
- +1R favorable-first remains positive in all three.
- +2R favorable-first is positive in two of three and slightly negative when September is removed.

## Interpretation

This is a more useful robustness result than simply observing a pooled average. The lifecycle pattern is not dependent on one contract alone, although its magnitude is heterogeneous.

The strongest stable component is:

**H-M6 events tend to accumulate more favorable excursion while accumulating less adverse excursion over the later 5–20 bar window.**

The 2R trading metric remains noisier than this path geometry, so the mechanism should continue to be evaluated as a movement/path hypothesis rather than treated as a validated trading system.

## Governance

No hypothesis definition was modified.
No execution rule was optimized.
No new filter was created.

The next decisive gate remains genuinely unseen actual NIFTY futures data, preferably the October 2025–March 2026 expired-contract window with OI.
