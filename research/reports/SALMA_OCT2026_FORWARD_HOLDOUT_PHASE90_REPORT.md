# SALMA Research — Phase 90 October 2026 Forward Holdout

Date captured: 2026-10-05 data endpoint supplied in conversation

## Status
This is the first forward/holdout evaluation using the frozen SALMA-B0 / H-M1 / H-M6 definitions. No thresholds, windows, stops, targets, or event rules were changed for these sessions.

The supplied capture contains 3 unique sessions in chronological context: 2026-09-30 (warm-up), 2026-10-01, and 2026-10-05. The duplicate Sep-30 payloads were de-duplicated. The October holdout results below use only 2026-10-01 and 2026-10-05; Sep-30 is warm-up context only.

## Data integrity
- 231 unique 5-minute candles across the supplied three sessions.
- Each session contains 77 bars from 09:15 through 15:35.
- No duplicate timestamps after de-duplication.
- No OHLC integrity violations.
- October sessions are fully captured for their respective days.

The uploaded Oct-1 series begins at 09:15 and ends at 15:35; the uploaded Oct-5 series likewise runs 09:15 to 15:35.

## Frozen definitions used
SALMA-B0: Close source, WMA(5) volatility baseline, population SD(5), width 0.30, clip close to the volatility band, WMA(10), then WMA(3), with confirmed close-bar slope transitions.

H-M1: base compression-release event + a confirmed SALMA-B0 state/slope flip 1–3 completed bars earlier.

Base event:
1. Close breaks the prior 10-bar high or low.
2. Event range >= 1.25 x median range of the prior 10 bars.
3. Mean range of prior 5 bars / causal ATR14 <= 1.0.
4. Entry = next-bar open.
5. Risk = ATR14 at event bar.
6. Same-session horizon = 20 bars or session close.
7. Stop-first on same-bar stop/target collision.

H-M6: H-M1 + at least 2 of the previous 3 completed bars with direction-aligned closes beyond the SALMA volatility band.

## October forward results so far

| Date | Base events | H-M1 | H-M6 | Key observation |
|---|---:|---:|---:|---|
| 2026-10-01 | 5 | 0 | 0 | Seven SALMA flips occurred, but none preceded a qualifying compression-release event by 1–3 bars. |
| 2026-10-05 | 7 | 2 | 1 | One H-M1 event reached 2R, but only at the end of the 20-bar horizon; the H-M6 event stopped out. |
| **Total** | **12** | **2** | **1** | Too small for validation. |

### H-M1 cohort (n=2)
- Mean 20-bar signed return: **+0.289 ATR**.
- Mean R at 1.5R benchmark: **+0.250R**.
- Mean R at 2R benchmark: **+0.500R**.
- Mean R at 3R benchmark: **+0.136R**.
- 2R target-first: **50.0%**.
- Mean MFE: **1.108 ATR**.
- Mean MAE: **0.913 ATR**.

### H-M6 cohort (n=1)
- Mean 20-bar signed return: **-0.692 ATR**.
- Mean R at 2R benchmark: **-1.000R**.
- 2R target-first: **0.0%**.
- MFE: **0.081 ATR**.
- MAE: **1.030 ATR**.

### Direction-matched control snapshot
Both H-M1 events were bearish. The four non-H-M1 bearish base events on Oct-1 had:
- mean 20-bar signed return = **+1.584 ATR**;
- mean 2R benchmark = **-0.250R**;
- 2R target-first = **25.0%**.

The two H-M1 events therefore show **+0.750R** in the fixed 2R benchmark versus that tiny direction-matched control snapshot, but **-1.295 ATR** in 20-bar movement. Both comparisons are dominated by very small n and are descriptive only.

## Event-level interpretation

### 2026-10-05 10:20 — H-M1, not H-M6
- Bearish breakout.
- SALMA flip lag = 2 bars.
- Only 1 of the prior 3 bars was direction-aligned clipped, so it does not qualify for H-M6.
- Next-bar entry = 22625.0; ATR14 = 43.264 points.
- 1.5R target hit on bar 18; 2R target hit on bar 20; 3R not reached.
- Final 20-bar close return = +1.271 ATR.
- MFE = 2.136 ATR; MAE = 0.795 ATR.

This is a **moderate H-M1 success**, but it does not exhibit the fast 3–10 bar expansion pattern highlighted in prior diagnostic work: the 2R path was only completed at the final bar of the allowed horizon.

### 2026-10-05 15:00 — H-M1 and H-M6
- Bearish breakout.
- SALMA flip lag = 3 bars.
- 2 of the prior 3 bars were direction-aligned clipped, so H-M6 qualifies.
- Next-bar entry = 22596.0; ATR14 = 34.657 points.
- Stop was hit 6 bars later at 15:30 for all three target levels.
- MFE = only 0.081 ATR; MAE = 1.030 ATR.

This is a **clean H-M6 false positive** in the forward holdout: strong-looking pre-event clipping state did not lead to continuation and the move reversed before session close. It is only one observation, so it cannot reject H-M6 statistically, but it is exactly the kind of failure the holdout is supposed to expose.

## Important control counterexample
On 2026-10-01 12:40, a bearish base compression-release event with **no H-M1 flag** reached 3R. Its 20-bar MFE was about 6.03 ATR and MAE was effectively 0 ATR in the benchmark window.

That is useful because it prevents a false conclusion that “SALMA timing is required” for a strong breakout. The forward evidence so far says the broader event geometry can succeed without H-M1.

## SALMA state activity
The October sessions had 7 confirmed slope-state flips on Oct-1 and 4 on Oct-5. The H-M1 filter therefore remained selective: most SALMA flips were not immediately followed by the frozen compression-release event.

## OI / volume diagnostics — not filters
The two H-M1 events on Oct-5 were accompanied by materially different OI/volume behaviour:
- 10:20: volume about 1.41x the prior-5-bar median; OI increased about 33,215 from five bars earlier.
- 15:00: volume about 5.33x the prior-5-bar median; OI decreased about 29,380 from five bars earlier.

These are mechanism observations only. **No OI or volume rule is being promoted from them.**

## Holdout verdict at this checkpoint
**H-M1: still open, not validated.** The first two qualifying October events are mixed; one reached 2R and one stopped. The direction-matched control comparison is unstable because n=2.

**H-M6: first forward observation is a failure, not a rejection.** The sample is n=1, but the failure is highly relevant because the event satisfies the exact frozen >=2-of-3 clipping condition and then immediately loses continuation.

**Mechanism hypothesis: still alive but under pressure.** The October data already shows a successful base breakout without H-M1 and an H-M6 false positive. That pushes the research interpretation further toward the broader compression -> transition -> release family rather than SALMA clipping as a standalone causal edge.

## Governance decision
No rule changes are allowed from these observations. October remains a genuine holdout. Additional October sessions should be appended mechanically and then re-evaluated with the same definitions.