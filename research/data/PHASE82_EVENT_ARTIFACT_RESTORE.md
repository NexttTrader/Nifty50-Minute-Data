# Phase 82 Event Artifact Restore

The full event-level table is 85,467 bytes and has SHA-256:
4cef5244ef0dafc6537750cdb6f9f657e0ec5c870fba790283dac351b3b4e441

The lossless gzip copy is 26,969 bytes and has SHA-256:
5461460b781fa09b09924753f6a7930d530d7acea2bcb49c801aa67adbdd80b1

To restore from the compressed artifact:
1. concatenate the encoded Git parts in numeric order;
2. base64-decode to PHASE82_EVENT_HORIZON_RETURNS.csv.gz;
3. gunzip to PHASE82_EVENT_HORIZON_RETURNS.csv;
4. verify the SHA-256 above.

The same table is reproducible from the Phase 82 methodology script using the exact Apr-Sep 2026 futures event/candle inputs.
