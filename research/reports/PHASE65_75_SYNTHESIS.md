# Phase 65–75 — Deep Research Synthesis

The project now separates the SALMA question into:
1. movement-potential prediction,
2. risk geometry,
3. executable trading profitability.

## Main conclusions

- Raw SALMA color/swing reversal is not a trading system.
- H-M1 is the strongest event-sequence hypothesis: compression-release breakout + recent direction-aligned SALMA flip.
- H-M6 is the strongest current SALMA-specific thresholded hypothesis: H-M1 + >=2 prior-3 direction-aligned SALMA clipping bars.
- H-M8 uses continuous clipping pressure and can improve meta-model discrimination, but remains exploratory.
- Exact ablation shows generic smoothers and generic short volatility envelopes also condition the same breakout universe. Therefore the mechanism is not proven uniquely SALMA-specific.
- Exact flip-direction placebo shows any recent flip is associated with some improvement; direction alignment is not independently proven essential because opposite-only samples are small.
- H-M6's strongest effect is on 10–20 bar movement persistence and favorable excursion, not necessarily immediate target-first execution.
- Fixed 1ATR/2R profitability is economically fragile and becomes uncertain under day clustering and friction.
- H-M12 (H-M6 + direction-aligned prior-3 price movement + rising OI) is a promising post-hoc extension with validation R2 +0.374 and R3 +0.479, but it is not an independent validation because it was discovered after viewing Jul-Sep.
- MTF alignment improves conditioning, but generic 15m moving-average alignment produces similar results; this is not uniquely SALMA-specific.
- Non-overlap execution greatly reduces effective sample size and can erase apparent event-level profitability.
- Long 2015–2021 NIFTY index transfer does not reproduce a robust fixed 1ATR/2R edge, reinforcing regime/instrument dependence.

## Current research interpretation

The best current abstraction is:

compression
-> directional pressure
-> short-horizon smoothed-state transition
-> range release
-> persistent expansion

SALMA may be a useful detector inside this sequence. Its volatility-clipping component may add information, but the evidence does not yet prove uniqueness versus generic smoothers/envelopes.

## Scientific gate

The historical Apr-Sep universe is now frozen for discovery/first validation. Further mining is prohibited until new data arrives.

The next evidence must come from:
- genuinely unseen actual futures contracts, or
- forward paper observations.

Do not promote H-M6/H-M12 to a live rule from the current dataset.
