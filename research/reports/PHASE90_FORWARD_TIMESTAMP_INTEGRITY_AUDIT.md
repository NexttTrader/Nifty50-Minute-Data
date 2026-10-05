# Phase 90 — Prospective Forward-Capture Timestamp Integrity Audit
Date: 2026-10-05

## Finding

The October 2026 public NSE/OpenChart-compatible feed was inspected before using any prospective signal outcome.

The endpoint's returned millisecond timestamps are represented as NSE wall-clock values. The prior Phase 87 parser interpreted them directly as UTC. This produced a 5h30 timestamp shift and allowed pre-open/after-close reference rows into the archive.

This was detected because the manifest capture time was earlier than the latest stored bar timestamp.

## Correction

The forward parser is now:
1. interprets source timestamps in Asia/Kolkata;
2. converts them to true UTC;
3. retains only the regular NSE futures session, 09:15:00 through 15:29:59 IST;
4. rejects source data that are more than 10 minutes ahead of the runner clock.

The existing 90-row October archive contains 5 rows outside the regular session:
- 2026-10-01 09:08:10
- 2026-10-01 15:34:59
- 2026-10-01 15:39:59
- 2026-10-01 15:40:01
- 2026-10-05 09:09:26

After correction, 85 regular-session bars remain:
- 2026-10-01: 75 bars
- 2026-10-05: 10 bars

## Research impact

No frozen H-M1/H-M6/H-M9/H-M14 signal rows existed and no outcomes existed before this correction. Therefore the timestamp bug did not contaminate any reported forward performance result.

The October forward dataset is now the canonical prospective stream. Previous pre-fix raw SHA: `551fca594a6eea6a202dfa5ab68707bd143bf9cb3f94f519df01d261f8c2085d`.

Corrected raw SHA-256: `823af836e4d0eedf7ccfe2d271bc86e5b05d1b12e0489a07c0ce9b0b43683552`.

## Governance

- H-M1 unchanged.
- H-M6 unchanged.
- H-M9 unchanged.
- H-M14 unchanged.
- No historical validation was rerun or re-tuned.
- The corrected timestamp/session convention will be used for all future October observations.
