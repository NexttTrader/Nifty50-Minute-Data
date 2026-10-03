"""Phase 86 prior-extension interaction replication.

This script is descriptive. It does not fit a new execution rule and does not
use holdout outcomes to choose thresholds.
"""
import pandas as pd

old = pd.read_csv("phase36_index_geometry_ml_events_2015_2021.csv")
old_h1 = old[(old.recent_flip3 == 1) & (old.salma_match3 == 1)].copy()
old_h1["priorret5_bin"] = pd.qcut(old_h1["ret5pre"], 3, labels=["low","mid","high"])

print(old_h1.groupby("priorret5_bin", observed=True)[
    ["event_range_atr","ret5pre","ret20pre","range20_atr","vol20_atr","eff20"]
].mean())

print("This phase is a mechanistic replication only. No threshold is selected.")
