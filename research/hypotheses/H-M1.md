# H-M1 — Frozen Research Hypothesis

## Statement
A causal compression-release breakout may have a different tradeability profile when a confirmed SALMA-B0 slope-state flip occurred 1-3 completed bars before the breakout.

## Frozen base event
At the close of bar t:
1. Close breaks the prior 10-bar high or low.
2. Current bar range >= 1.25 x median range of the prior 10 bars.
3. Mean range of the prior 5 bars / causal ATR14 <= 1.0.

## Frozen SALMA condition
A confirmed SALMA-B0 flip occurred 1-3 completed bars before bar t.

## Execution benchmark
- Entry: next bar open
- Initial risk: 1 x ATR14 measured at event-bar close
- Targets: 1.5R, 2R and 3R
- Vertical barrier: 20 bars or session close
- Same-bar stop/target ambiguity: stop-first

## Evidence so far
Discovery Apr-Jun 2026: 76 candidate events; mean R +0.163 at the 2R benchmark; no-recent-flip control mean R -0.149.
Validation Jul-Sep 2026: 72 candidate events; mean R +0.096; no-recent-flip control mean R -0.091; candidate MFE about 2.84 ATR; candidate MAE about 1.73 ATR.
A nearby-definition robustness grid over 27 combinations preserved a positive candidate-vs-control delta in discovery and validation.

## Status
PROMISING, NOT VALIDATED.
No further historical optimization is permitted before an unseen holdout or forward paper test.