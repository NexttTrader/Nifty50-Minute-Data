# Phase 89 — Cross-Dataset H-M7 Selectivity and Future-Only Exact-3 Freeze
Date: 2026-10-05

## Purpose

Use the already-defined H-M7 clipping-count interaction to determine whether the frozen H-M6 threshold (>=2 aligned clips) is itself a stable selector, and whether the pre-existing 3-clip branch is sufficiently coherent to be frozen for future-only observation.

This phase is a diagnostic. The January 2025-26 external holdout was already used to challenge H-M6, so no new rule is validated on that holdout. The exact-3 branch is frozen prospectively only for the October 2026 forward stream.

## External selectivity result

On the NIFTY26JANFUT secondary external holdout:

- Base events: 124
- H-M1 events: 26
- H-M6 events: 24
- H-M1-not-H-M6: 2
- H-M6 share of H-M1: 92.3%

For comparison, in the frozen Jul-Sep 2026 validation set, H-M6 was 54/66 H-M1 events = 81.8%.

Thus H-M6's >=2 threshold loses selectivity in the external contract.

## External direction robustness

The H-M6 failure is not caused by one breakout direction:

| Direction | H-M6 n | H-M6 ret20 | Control n | Control ret20 | Delta |
|---|---:|---:|---:|---:|---:|
| Up | 15 | -0.248 ATR | 53 | +0.470 ATR | -0.718 ATR |
| Down | 9 | -0.272 ATR | 45 | +0.536 ATR | -0.808 ATR |

Both directions show a negative H-M6-minus-control movement result.

## External clipping-count decomposition

Within external H-M6:

| Aligned clip count | n | Mean ret20 | Mean R2 | 2R target-first |
|---:|---:|---:|---:|---:|
| 2 | 13 | -0.849 ATR | -0.372R | 15.4% |
| 3 | 11 | +0.444 ATR | +0.295R | 36.4% |

The original frozen H-M6 therefore mixes two materially different states in the external contract.

## Cross-dataset ordering of the H-M7 branch

The 3-clip state has been part of H-M7's pre-existing interaction analysis since before this phase.

Discovery Apr-Jun 2026:
- 2 clips: n=30, mean R2 -0.146R, 2R target-first 23.3%
- 3 clips: n=34, mean R2 +0.805R, 2R target-first 47.1%

Validation Jul-Sep 2026:
- 2 clips: n=22, mean R2 +0.024R, 2R target-first 31.8%
- 3 clips: n=32, mean R2 +0.388R, 2R target-first 34.4%

External NIFTY26JANFUT:
- 2 clips: n=13, mean R2 -0.372R, 2R target-first 15.4%
- 3 clips: n=11, mean R2 +0.295R, 2R target-first 36.4%

The ordinal relationship (3 clips better than 2 clips on fixed-2R outcome) is reproduced in all three datasets. However, in the external holdout the 3-clip state only barely exceeds the external control's mean R2 (+0.295R versus +0.272R), so this is not evidence of a validated edge.

## Interpretation

The most defensible conclusion is not “3 clips is profitable.”

The better conclusion is:

**The >=2 clipping threshold is not a stable external selector, but the already-known 3-clip state is a more coherent candidate state than the 2-clip state, and its fixed-risk ordering relative to the 2-clip state replicates across discovery, 2026 validation, and the January external contract.**

Because the external holdout has already been viewed, no threshold is tuned from it and no October outcomes are used to support this conclusion.

## Future-only hypothesis freeze

A new future-only hypothesis is registered:

**H-M14 — H-M1 + exactly 3 direction-aligned clipped bars among the prior 3 completed bars.**

H-M14 inherits the frozen H-M1 event/execution specification:
- prior 10-bar breakout;
- event range >=1.25x prior-10 median range;
- prior-5 mean range / causal ATR14 <=1;
- confirmed direction-aligned SALMA-B0 flip 1-3 completed bars earlier;
- next-bar-open execution;
- 1 ATR risk;
- 1.5R/2R/3R benchmark targets;
- 20-bar/session barrier;
- stop-first ambiguity convention.

H-M14 is recorded prospectively but is NOT a trading recommendation, is NOT backtested further on the already-seen January holdout, and is NOT allowed to modify H-M6.

## Governance

- H-M1 frozen.
- H-M6 frozen.
- H-M7 remains exploratory.
- H-M14 is future-only and not validated.
- No parameter optimization was performed on the external holdout.
- October 2026 outcomes remain untouched and prospective.
- The decisive test is whether H-M14 shows reproducible behavior on future unseen observations without degrading after costs and clustering adjustment.
