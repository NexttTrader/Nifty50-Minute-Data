"""Phase 79 day-cluster bootstrap for first-passage comparisons."""
import numpy as np
import pandas as pd

P = pd.read_csv("PHASE79_EVENT_PATHS.csv")
V = P[P["split"] == "V"].copy()
V["day"] = V["dt"].astype(str).str[:10]
V["cohort"] = np.where(V["hm6"], "H-M6", np.where(V["h_m1"], "H-M1-not6", "Control"))

days = np.array(sorted(V["day"].unique()))
rng = np.random.default_rng(7902)
out = []

for level in [1, 1.5, 2, 3]:
    fav = V[f"tf_{level}"].notna()
    adv = V["adverse_1"].notna()
    first = fav & (~adv | (V[f"tf_{level}"] < V["adverse_1"]))

    def cohort_rate(frame, cohort):
        x = first[frame.index]
        return x[frame["cohort"] == cohort].mean()

    observed = cohort_rate(V[V["cohort"] == "H-M6"], "H-M6") - cohort_rate(V[V["cohort"] == "Control"], "Control")

    daily = []
    for day in days:
        z = V["day"] == day
        daily.append([
            int(first[z & (V["cohort"] == "H-M6")].sum()),
            int((z & (V["cohort"] == "H-M6")).sum()),
            int(first[z & (V["cohort"] == "Control")].sum()),
            int((z & (V["cohort"] == "Control")).sum()),
        ])
    daily = np.asarray(daily, float)
    samples = rng.integers(0, len(days), size=(50000, len(days)))
    totals = daily[samples].sum(axis=1)
    boot = totals[:, 0] / totals[:, 1] - totals[:, 2] / totals[:, 3]

    out.append({
        "metric": f"fav_first_before_adverse1_R{level}",
        "observed": observed,
        "ci_low_95": np.quantile(boot, .025),
        "ci_high_95": np.quantile(boot, .975),
        "p_le_zero": np.mean(boot <= 0),
        "n_days": len(days),
    })

pd.DataFrame(out).to_csv("PHASE79_FIRST_PASSAGE_BOOTSTRAP_REPRO.csv", index=False)
