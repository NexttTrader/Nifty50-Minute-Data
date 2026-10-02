"""Phase 80 contract stability / leave-one-contract-out lifecycle diagnostics."""
import numpy as np
import pandas as pd

paths = pd.read_csv("PHASE79_EVENT_PATHS.csv")
events = pd.read_csv("PHASE56_HM8_EXACT_FUTURES.csv")
paths["dt"] = pd.to_datetime(paths["dt"], errors="coerce")
events["dt"] = pd.to_datetime(events["dt"], errors="coerce")
mapping = events[["dt", "instrument_identifier"]].drop_duplicates("dt")
paths = paths.merge(mapping, on="dt", how="left")
paths["cohort"] = np.where(paths["hm6"], "H-M6", np.where(paths["h_m1"], "H-M1-not6", "Control"))
V = paths[paths["split"] == "V"]

rows = []
for contract, g in V.groupby("instrument_identifier"):
    a, b = g[g.cohort == "H-M6"], g[g.cohort == "Control"]
    if len(a) == 0 or len(b) == 0:
        continue
    r = {"contract": contract, "hm6_n": len(a), "control_n": len(b)}
    for m in ["mfe5","mfe10","mfe20","mae10","mae20","retclose20"]:
        r[m + "_delta"] = a[m].mean() - b[m].mean()
    for lev in [1, 2]:
        fa, aa = a[f"tf_{lev}"], a["adverse_1"]
        fb, ab = b[f"tf_{lev}"], b["adverse_1"]
        r[f"favfirst_R{lev}_delta"] = (
            (fa.notna() & (~aa.notna() | (fa < aa))).mean()
            - (fb.notna() & (~ab.notna() | (fb < ab))).mean()
        )
    rows.append(r)
pd.DataFrame(rows).to_csv("PHASE80_CONTRACT_LIFECYCLE.csv", index=False)

loo = []
contracts = sorted(V.instrument_identifier.dropna().unique())
for removed in contracts:
    g = V[V.instrument_identifier != removed]
    a, b = g[g.cohort == "H-M6"], g[g.cohort == "Control"]
    r = {"left_out": removed, "hm6_n": len(a), "control_n": len(b)}
    for m in ["mfe5","mfe10","mfe20","mae10","mae20","retclose20"]:
        r[m + "_delta"] = a[m].mean() - b[m].mean()
    for lev in [1, 2]:
        fa, aa = a[f"tf_{lev}"], a["adverse_1"]
        fb, ab = b[f"tf_{lev}"], b["adverse_1"]
        r[f"favfirst_R{lev}_delta"] = (
            (fa.notna() & (~aa.notna() | (fa < aa))).mean()
            - (fb.notna() & (~ab.notna() | (fb < ab))).mean()
        )
    loo.append(r)
pd.DataFrame(loo).to_csv("PHASE80_LEAVE_ONE_OUT.csv", index=False)
