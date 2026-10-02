"""Phase 79 lifecycle path analysis.
Reads exact 2026 futures candles + frozen event artifact and writes path summaries.
No signal parameters are changed.
"""
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(".")
RAW = pd.read_csv(BASE / "NIFTY_FUT_5m_all_contracts_normalized.csv")
EV = pd.read_csv(BASE / "PHASE56_HM8_EXACT_FUTURES.csv")

RAW["datetime"] = pd.to_datetime(RAW["datetime"], errors="coerce", utc=True)
EV["dt"] = pd.to_datetime(EV["dt"], errors="coerce", utc=True)
RAW["datestr"] = RAW["datetime"].astype(str).str[:10]
EV["datestr"] = EV["dt"].astype(str).str[:10]

E = EV[(EV["base_frozen"] == True) & (EV["split"].isin(["D", "V"])) & EV["h_m1"].notna()].copy()
E["hm6"] = E["h_m1"].astype(bool) & (E["aligned_clip_count_3"] >= 2)
E = E.drop_duplicates(["instrument_identifier", "dt"])

records = []
for _, e in E.iterrows():
    future = RAW[
        (RAW["instrument_identifier"] == e["instrument_identifier"])
        & (RAW["datestr"] == e["datestr"])
        & (RAW["datetime"] > e["dt"])
    ].sort_values("datetime").head(20)
    atr = float(e["atr14"])
    if future.empty or not np.isfinite(atr) or atr <= 0:
        continue
    entry = float(future.iloc[0]["open"])
    d = int(e["dir"])
    fav = ((future["high"].to_numpy() - entry) if d == 1 else (entry - future["low"].to_numpy())) / atr
    adv = ((entry - future["low"].to_numpy()) if d == 1 else (future["high"].to_numpy() - entry)) / atr

    row = {
        "dt": str(e["dt"]), "split": e["split"], "h_m1": bool(e["h_m1"]),
        "hm6": bool(e["hm6"]), "mfe20": float(np.max(fav)), "mae20": float(np.max(adv)),
    }
    for h in [1, 3, 5, 10, 20]:
        n = min(h, len(future))
        row[f"mfe{h}"] = float(np.max(fav[:n]))
        row[f"mae{h}"] = float(np.max(adv[:n]))
    for level in [0.5, 1, 1.5, 2, 3]:
        hit = np.where(fav >= level)[0]
        row[f"tf_{level}"] = int(hit[0] + 1) if len(hit) else np.nan
    for level in [0.5, 1]:
        hit = np.where(adv >= level)[0]
        row[f"adverse_{level}"] = int(hit[0] + 1) if len(hit) else np.nan
    records.append(row)

P = pd.DataFrame(records)
P["cohort"] = np.where(P["hm6"], "H-M6", np.where(P["h_m1"], "H-M1-not6", "Control"))

summary = []
for cohort, g in P.groupby("cohort"):
    r = {"cohort": cohort, "n": len(g)}
    for h in [1, 3, 5, 10, 20]:
        r[f"mfe{h}_mean"] = g[f"mfe{h}"].mean()
        r[f"mae{h}_mean"] = g[f"mae{h}"].mean()
    r["tf1_rate"] = g["tf_1"].notna().mean()
    r["tf2_rate"] = g["tf_2"].notna().mean()
    r["tf3_rate"] = g["tf_3"].notna().mean()
    r["adverse1_rate"] = g["adverse_1"].notna().mean()
    summary.append(r)

P.to_csv("PHASE79_EVENT_PATHS.csv", index=False)
pd.DataFrame(summary).to_csv("PHASE79_PATH_SUMMARY_REPRO.csv", index=False)
print(f"events={len(P)}")
