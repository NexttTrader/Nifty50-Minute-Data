# Phase 82 — Source provenance correction

The NIFTY26JANFUT archive is a **secondary public-data holdout**, not a broker-verification feed directly accessed by this research environment.

Source:
https://github.com/achauh2723/Quantitative_Trading_Strategy_Development_Task_Aryan_Chauhan

Source commit:
13d8384db17d400d8acc2ef18fe1e220367dd46b

The source acquisition notebook explicitly shows Zerodha `kite.historical_data(..., interval="5minute", oi=True)` and a chunked 90-day retrieval that produced 4,125 rows for NIFTY26JANFUT, with 5-minute OHLC and OI.

The source repository's README contains a contradictory note about futures access restrictions, so provenance should be described conservatively: the file is a public secondary archive whose acquisition notebook documents a Zerodha historical-data pull. The research environment has not independently authenticated the broker account or regenerated the source data from Zerodha.

The file is still useful because:
- it is contract-specific;
- it has 55 complete 75-bar sessions;
- it has no observed intraday gaps >5 minutes;
- its dates do not overlap the Apr-Sep 2026 canonical research corpus;
- the frozen research rules were defined before this archive was evaluated.

Therefore Phase 82 is classified as an **external secondary holdout challenge**, not final broker-independent validation.
