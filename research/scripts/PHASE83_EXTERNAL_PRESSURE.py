"""Phase 83 external pressure diagnostic.

The script reuses the frozen SALMA-B0/H-M1 calculation and computes only
pre-registered descriptive pressure relationships. No threshold is optimized.
"""
# Reuse the exact dataset and formula implementation from Phase 82.
# This script is intentionally descriptive; future risk-geometry hypotheses
# require new IDs and fresh data.
import pandas as pd

events = pd.read_csv("research/data/external_holdout/PHASE82_NIFTY26JANFUT_EVENTS.csv")
hm1 = events[events["hm1"] == True].copy()

print("H-M1 events:", len(hm1))
print("Spearman pressure vs ret20:", hm1["clip_pressure"].corr(hm1["ret20"], method="spearman"))
print("Spearman pressure vs MFE20:", hm1["clip_pressure"].corr(hm1["mfe20"], method="spearman"))
print("Spearman pressure vs MAE20:", hm1["clip_pressure"].corr(hm1["mae20"], method="spearman"))

success = hm1["r2"] == 2
print("Pressure AUC note: binary ranking should be recomputed from the exact frozen event table if the execution columns are extended.")
