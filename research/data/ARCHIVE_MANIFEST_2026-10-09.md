# Canonical NIFTY Futures / SALMA Research Archive

Date: 2026-10-09
Repository: NexttTrader/Nifty50-Minute-Data
Branch: main

## Canonical NIFTY futures corpus

The canonical research corpus contains 8,594 actual 5-minute candles from six contract-specific NIFTY monthly futures contracts covering April-September 2026.

| Contract | Rows | SHA-256 |
|---|---:|---|
| NIFTY26APRFUT | 1,350 | fe29cbd554bca45a66c1743f87411d4f79d16274cea79920791722a681594103 |
| NIFTY26MAYFUT | 1,275 | ded3ff611c11658abd1c1216c68a4d8cf882fd2bf3ef5939f8766d01d9321dfd |
| NIFTY26JUNFUT | 1,575 | 730bed2a1204e51b3e02a9758de60e817ac68fcf07499020e70a7e9bb525d796 |
| NIFTY26JULFUT | 1,545 | a2f9e36866f9418a9d3f00f1de3fc45447078714e0431623613bfb67037569d4 |
| NIFTY26AUGFUT | 1,309 | 5d3695043ab77d1806ac0635c7a2ac037049059bf232d880c38b483b0931029b |
| NIFTY26SEPFUT | 1,540 | c69727604ddb1e4e5dc87cda06d50a225cb3c8c2cf79d97a05cbd473f7e3b6f4 |

Each contract file is stored independently under `research/data/canonical/`. No continuous-contract stitching is used.

## SALMA research data

- `research/data/SALMA_B0_event_log_APR_SEP_2026.csv`
- `research/data/SALMA_HM1_EXACT_AUDITED_EVENTS_APR_SEP_2026.csv`
- `research/data/legacy/SALMA_DEEP_CAUSAL_EVENT_FEATURES_APR_SEP_2026.csv` — retained as legacy because its historical H-M1 field is not authoritative for current flag reconstruction.
- `research/data/forward/NIFTY26OCTFUT_5m_OHLCV_OI_2026-09-30_to_2026-10-05.csv` — 231 supplied 5-minute candles for Sep-30 warm-up plus Oct-1 and Oct-5, including volume and OI.
- `research/data/forward/SALMA_OCT2026_FORWARD_HOLDOUT_EVENTS_PHASE90.csv`
- `research/data/forward/PHASE90_TIMESTAMP_AUDIT.csv`
- `research/data/forward/PHASE91_DATA_INTEGRITY.csv`
- `research/data/forward/PHASE91_PROSPECTIVE_SUMMARY.csv`
- `research/data/forward/PHASE87_NIFTY26OCTFUT_5m.csv`

## Research reports

This archive includes the Phase 85, 86, 87 and 88/89 reports plus the Phase 90 October holdout report and the earlier phase history already present in the repository.

## Data-governance rules

- No fabricated or interpolated candles.
- No silent contract stitching.
- No future leakage.
- Frozen holdout definitions are not changed from October outcomes.
- Contract identity is preserved.
- H-M6 remains a research tag, not a promoted live-trading rule.
