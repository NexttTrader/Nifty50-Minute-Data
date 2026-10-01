# Phase 77 — Autonomous Transfer and Mechanism Research
Date: 2026-10-01

## Purpose
Continue the SALMA research without changing any frozen 2026 definitions. This phase uses the materially older NIFTY 50 index 5-minute dataset (2015-01-09 through 2021-03-25) as a cross-instrument / cross-era transfer test.

This is **not** a substitute for unseen actual NIFTY futures validation. It is an independent mechanism/generalization test designed to answer whether the 2026 H-M6/H-M8 behavior is structural enough to survive a different instrument and regime history.

## Data and protocol

Source dataset:
- NIFTY 50 index 5-minute OHLC
- 114,830 rows
- 1,537 dated sessions
- 2015-01-09 to 2021-03-25
- volume is zero; no OI

Fixed event universe:
- 4,593 price-defined breakout/compression events from the existing cross-instrument transfer artifact.
- Exact SALMA-B0 was reconstructed independently on the full index series using the canonical formula: WMA(5) baseline, population SD(5), width 0.30, clipped close, WMA(10), then WMA(3).
- The exact SALMA aligned-flip condition reproduces all 1,184 historical H-M1 candidate timestamps in the fixed event universe.

Frozen sequence definitions applied unchanged:
- H-M1: fixed recent direction-aligned confirmed SALMA flip 1–3 completed bars before the event.
- H-M6: H-M1 + at least 2 of the previous 3 direction-aligned closes beyond the SALMA volatility band.
- H-M8 diagnostic: continuous direction-aligned clipping excess over the previous 3 completed bars.

Historical outcomes are taken from the established cross-instrument benchmark artifact, whose `r2` field is the 2R execution benchmark and whose `ret20` field is the 20-bar directional return normalized by the event risk unit.

## 1. Exact H-M1 transfer check

The existing cross-instrument H-M1 universe contains 1,184 candidate events. Reconstructing SALMA-B0 with the exact population-standard-deviation specification reproduces the same 1,184 timestamps.

This confirms that the historical transfer result is compatible with the repaired canonical SALMA formula; the earlier transfer result does not depend on the now-superseded sample-SD reconstruction.

## 2. H-M6 transfer result

On the fixed 1,184-event H-M1 set:

| Cohort | n | Mean 20-bar return | Mean 2R benchmark | 2R target-first |
|---|---:|---:|---:|---:|
| H-M6 | 1,000 | +0.203 ATR | -0.051R | 30.1% |
| H-M1 but not H-M6 | 184 | +0.127 ATR | +0.038R | 32.6% |
| Non-H-M1 control | 3,409 | +0.115 ATR | -0.026R | 31.0% |
| H-M1 total | 1,184 | +0.191 ATR | -0.037R | 30.5% |

The key result is the mismatch between the 2026 futures behavior and the older index behavior:

- H-M6 retains a small positive movement-persistence point estimate.
- H-M6 does **not** improve the 2R benchmark over the non-H-M1 control.
- Within H-M1, adding the >=2 clipping requirement increases mean ret20 by about +0.076 ATR versus H-M1-not-H-M6, but lowers mean 2R outcome by about 0.089R and lowers 2R target-first rate.

Thus the 2026 H-M6 effect is not a stable cross-instrument property.

## 3. Direction-matched H-M6 transfer

Using same-direction non-H-M1 events as controls:

| Direction | H-M6 n | Ret20 delta vs control | 2R delta vs control |
|---|---:|---:|---:|
| Up | 418 | +0.042 ATR | -0.046R |
| Down | 582 | +0.103 ATR | -0.016R |

Both directions retain a small positive movement point estimate, but neither produces a positive 2R effect.

Day-cluster bootstrap uncertainty remains wide:

- Up ret20 delta 95% CI: [-0.395, +0.484] ATR; 2R delta CI: [-0.192, +0.104]R.
- Down ret20 delta 95% CI: [-0.286, +0.490] ATR; 2R delta CI: [-0.151, +0.119]R.

Within-H-M1 H-M6 versus H-M1-not-H-M6:

- ret20 delta +0.076 ATR; day-cluster 95% CI [-0.472, +0.623] ATR.
- 2R delta -0.089R; day-cluster 95% CI [-0.310, +0.125]R.

The historical evidence therefore does not establish an incremental clipping-threshold effect once event direction and clustering are respected.

## 4. Continuous clipping pressure transfer (H-M8 mechanism)

Within exact H-M1 events, the continuous direction-aligned pressure feature is essentially unrelated to 20-bar return on this historical transfer sample:

- Spearman correlation pressure vs ret20: -0.002.
- 2015–2018 discovery -> 2019–2021 validation:
  - pressure-only logistic 2R AUC = 0.483, Brier = 0.220.
  - clip-count-only logistic AUC = 0.492, Brier = 0.220.
  - count + pressure AUC = 0.489, Brier = 0.220.
- 2019–2021 H-M1 test-set 2R base rate = 32.4%.

This is a strong negative transfer result for H-M8: the continuous pressure feature that looked useful inside the 2026 futures sample does not retain comparable discrimination in the older index history.

## 5. Smoother placebo / SALMA uniqueness check

Using the same fixed 4,593-event price universe, the recent direction-aligned flip condition was recomputed with several predetermined generic smoothers.

| State smoother | Candidate n | Ret20 delta | 2R delta |
|---|---:|---:|---:|
| SALMA-B0 | 1,184 | +0.076 ATR | -0.012R |
| WMA10 | 1,774 | -0.130 ATR | +0.001R |
| EMA10 | 1,808 | -0.047 ATR | +0.013R |
| SMA10 | 1,782 | -0.003 ATR | +0.033R |
| Double-WMA(10,3) | 1,398 | -0.100 ATR | +0.014R |
| WMA20 | 1,219 | -0.057 ATR | +0.069R |

These are descriptive placebo results, not optimized comparisons. They do not establish that SALMA is uniquely predictive. The SALMA state flip has a small positive movement delta, but no corresponding 2R advantage.

## 6. What changed in the research interpretation

The transfer tests sharpen the mechanism diagnosis:

1. H-M1 can carry a small movement-persistence effect across instrument/era, but that effect is not a stable monetizable 1ATR/2R edge.
2. H-M6's >=2 clipping threshold does not transfer reliably; the older index sample does not show the positive 2R separation seen in 2026 futures.
3. H-M8's continuous clipping-pressure feature is not invariant across eras/instruments.
4. Generic smoothers can generate similar-scale state-transition effects, so SALMA-specific causality remains unproven.
5. The recurring transferable component appears to be the **event geometry / delayed expansion family**, not the exact SALMA clipping threshold itself.

This is consistent with the broader project interpretation that SALMA may be a detector embedded in a compression -> transition -> release sequence, rather than the source of a universal standalone alpha.

## 7. Research governance decision

No 2026 frozen definition is changed.

No new threshold is promoted from this transfer study.

The 2026 Apr-Sep futures corpus remains frozen for discovery/validation. The next decisive evidence remains genuinely unseen actual NIFTY futures contracts.

The preferred missing holdout remains October 2025 through March 2026 actual monthly NIFTY futures 5-minute contract data, with OI preferred for testing the already-defined post-hoc H-M12 extension.

Current external-data route identified from Upstox documentation:
- expired futures contracts can be enumerated by underlying and expiry;
- expired historical candles support 5-minute intervals;
- the dedicated expired-instrument APIs are part of Upstox Plus and require authenticated API access.

No connected Upstox/Dhan plugin is currently available in this environment, so this phase does not fabricate or substitute broker data.

## Bottom line

The research has moved one step away from “SALMA clipping is the edge.”

The evidence now points more cautiously to:

**compression -> short-horizon state transition -> breakout/range release -> delayed expansion**

with SALMA/clipping potentially serving as one measurement of that state, but without evidence yet that the exact SALMA clipping rule is itself a universal causal advantage.
