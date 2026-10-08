# GitHub Data Archive Manifest — NIFTY / SALMA Research
Date: 2026-10-09
Repository: NexttTrader/Nifty50-Minute-Data

## Canonical NIFTY futures data
The original normalized file was:
NIFTY_FUT_5m_all_contracts_normalized.csv
Rows: 8,594
SHA-256: 096ae30767652caff0fd1efdfc30cabaa8df586462d7c2e40fe7c2c3df7561e8
Because the GitHub connector cannot stream the local binary file directly, it is rebuilt in GitHub as six exact contract CSVs. The per-contract files below preserve the original normalized CSV fields and row counts.

| Contract | Rows | SHA-256 of reconstructed CSV |
|---|---:|---|
| NIFTY26APRFUT | 1,350 | fe29cbd554bca45a66c1743f87411d4f79d16274cea79920791722a681594103 |
| NIFTY26MAYFUT | 1,275 | ded3ff611c11658abd1c1216c68a4d8cf882fd2bf3ef5939f8766d01d9321dfd |
| NIFTY26JUNFUT | 1,575 | 730bed2a1204e51b3e02a9758de60e817ac68fcf07499020e70a7e9bb525d796 |
| NIFTY26JULFUT | 1,545 | a2f9e36866f9418a9d3f00f1de3fc45447078714e0431623613bfb67037569d4 |
| NIFTY26AUGFUT | 1,309 | 5d3695043ab77d1806ac0635c7a2ac037049059bf232d880c38b483b0931029b |
| NIFTY26SEPFUT | 1,540 | c69727604ddb1e4e5dc87cda06d50a225cb3c8c2cf79d97a05cbd473f7e3b6f4 |

## SALMA research artifacts
- SALMA_B0_event_log_APR_SEP_2026.csv — canonical SALMA transition event log.
- SALMA_HM1_EXACT_AUDITED_EVENTS_APR_SEP_2026.csv — 513 audited base-event outcomes.
- SALMA_DEEP_CAUSAL_EVENT_FEATURES_APR_SEP_2026.csv — legacy feature artifact; archived under research/data/legacy because its historical H-M1 flag must not be used for current flags.
- PHASE88_89_OUTCOME_AUDIT_AND_INCREMENTAL_SIGNAL_2026-10-07.md — corrected outcome-engine and incremental-signal audit.
- SALMA_OCT2026_FORWARD_HOLDOUT_PHASE90_REPORT.md — October forward-holdout report.
- SALMA_OCT2026_FORWARD_HOLDOUT_EVENTS_PHASE90.csv — October event-level holdout outcomes.
- NIFTY26OCTFUT_5m_OHLCV_OI_2026-09-30_to_2026-10-05.csv — 231 supplied candles, including Sep-30 warm-up plus Oct-1 and Oct-5, with OI.

No thresholds or holdout rules were changed based on October observations.
