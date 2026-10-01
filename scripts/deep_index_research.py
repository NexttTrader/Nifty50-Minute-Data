#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "nifty50_candlestick_data.csv"
OUT = ROOT / "artifacts" / "deep_index_research"
OUT.mkdir(parents=True, exist_ok=True)


def wma(s: pd.Series, n: int) -> pd.Series:
    w = np.arange(1, n + 1, dtype=float)
    return s.rolling(n, min_periods=n).apply(lambda x: float(np.dot(x, w) / w.sum()), raw=True)


def parse_source(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    cols = {c.lower().strip(): c for c in df.columns}
    if "datetime" in cols:
        dt = pd.to_datetime(df[cols["datetime"]], errors="coerce", dayfirst=True)
    elif "timestamp" in cols:
        dt = pd.to_datetime(df[cols["timestamp"]], errors="coerce", dayfirst=True)
    elif "date" in cols and "time" in cols:
        dt = pd.to_datetime(
            df[cols["date"]].astype(str) + " " + df[cols["time"]].astype(str),
            errors="coerce",
            dayfirst=True,
        )
    else:
        raise ValueError(f"Could not identify timestamp columns: {df.columns.tolist()}")

    rename = {}
    for wanted in ["open", "high", "low", "close", "volume"]:
        if wanted in cols:
            rename[cols[wanted]] = wanted
    df = df.rename(columns=rename)
    required = ["open", "high", "low", "close"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing OHLC columns: {missing}")

    out = pd.DataFrame({
        "datetime": dt,
        "open": pd.to_numeric(df["open"], errors="coerce"),
        "high": pd.to_numeric(df["high"], errors="coerce"),
        "low": pd.to_numeric(df["low"], errors="coerce"),
        "close": pd.to_numeric(df["close"], errors="coerce"),
    })
    if "volume" in df.columns:
        out["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    out = out.dropna(subset=["datetime", "open", "high", "low", "close"])
    out = out.sort_values("datetime").drop_duplicates("datetime", keep="first").reset_index(drop=True)
    if out["datetime"].dt.tz is None:
        out["datetime"] = out["datetime"].dt.tz_localize("Asia/Kolkata")
    else:
        out["datetime"] = out["datetime"].dt.tz_convert("Asia/Kolkata")
    return out


def aggregate_to_5m(minute: pd.DataFrame) -> pd.DataFrame:
    x = minute.copy()
    # Historical NIFTY index session used here: 09:15-15:30 IST.
    x = x[(x.datetime.dt.time >= pd.Timestamp("09:15").time()) &
          (x.datetime.dt.time < pd.Timestamp("15:30").time())].copy()
    x["date"] = x.datetime.dt.date
    x["bucket"] = x.datetime.dt.floor("5min")
    agg = x.groupby(["date", "bucket"], sort=True).agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum") if "volume" in x.columns else ("close", "size"),
        n_src=("close", "size"),
    ).reset_index()
    agg = agg.rename(columns={"bucket": "datetime"})
    return agg.drop(columns=["date"])


def add_session_metadata(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["session_date"] = x.datetime.dt.date
    counts = x.groupby("session_date").size()
    x["session_bars"] = x.session_date.map(counts)
    x["complete_session"] = x["session_bars"].eq(75)
    return x


def add_salma(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    close = x["close"]
    baseline = wma(close, 5)
    stdev = close.rolling(5, min_periods=5).std(ddof=0)
    upper = baseline + 0.30 * stdev
    lower = baseline - 0.30 * stdev
    # The original SALMA calculation is intended to use the available price
    # only after its volatility-band inputs are defined; this also avoids
    # contaminating the WMA warm-up with undefined band values.
    cprice = close.where(close.between(lower, upper), np.nan)
    cprice = cprice.fillna(np.where(close > upper, upper, np.where(close < lower, lower, close)))
    # Explicitly require the band window before allowing cprice to initialize.
    cprice = cprice.where(upper.notna() & lower.notna())
    w10 = wma(cprice, 10)
    salma = wma(w10, 3)
    up = salma > salma.shift(1)
    # Pine bool comparisons involving na do not create a confirmed swing.
    su = (up & ~up.shift(1, fill_value=False)).fillna(False)
    sd = (up.shift(1, fill_value=False) & ~up).fillna(False)

    x["salma_baseline"] = baseline
    x["salma_sd"] = stdev
    x["salma_upper"] = upper
    x["salma_lower"] = lower
    x["salma_clipped_price"] = cprice
    x["salma"] = salma
    x["salma_up"] = up.fillna(False)
    x["swing_up"] = su.astype(bool)
    x["swing_down"] = sd.astype(bool)
    return x


def add_causal_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    prev_close = x["close"].shift(1)
    tr = pd.concat([
        x["high"] - x["low"],
        (x["high"] - prev_close).abs(),
        (x["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    atr14 = tr.rolling(14, min_periods=14).mean()
    rng = x["high"] - x["low"]
    prior10_hi = x["high"].shift(1).rolling(10, min_periods=10).max()
    prior10_lo = x["low"].shift(1).rolling(10, min_periods=10).min()
    prior10_med_rng = rng.shift(1).rolling(10, min_periods=10).median()
    prev5_mean_rng = rng.shift(1).rolling(5, min_periods=5).mean()

    x["tr"] = tr
    x["atr14"] = atr14
    x["range"] = rng
    x["prior10_hi"] = prior10_hi
    x["prior10_lo"] = prior10_lo
    x["expansion_ratio"] = rng / prior10_med_rng
    x["compression_ratio"] = prev5_mean_rng / atr14

    up_break = x["close"] > prior10_hi
    dn_break = x["close"] < prior10_lo
    x["event_dir"] = np.where(up_break, 1, np.where(dn_break, -1, 0))
    x["base_event"] = (
        x["event_dir"].ne(0)
        & x["expansion_ratio"].ge(1.25)
        & x["compression_ratio"].le(1.0)
        & x["complete_session"]
    )

    # Recent direction-aligned SALMA state changes, only using completed bars.
    flip_up = x["swing_up"]
    flip_dn = x["swing_down"]
    prior_up = flip_up.shift(1).fillna(False) | flip_up.shift(2).fillna(False) | flip_up.shift(3).fillna(False)
    prior_dn = flip_dn.shift(1).fillna(False) | flip_dn.shift(2).fillna(False) | flip_dn.shift(3).fillna(False)
    x["hm1"] = ((x["event_dir"] == 1) & prior_up) | ((x["event_dir"] == -1) & prior_dn)

    clip_up = x["close"] > x["salma_upper"]
    clip_dn = x["close"] < x["salma_lower"]
    x["clip_up"] = clip_up.fillna(False)
    x["clip_dn"] = clip_dn.fillna(False)
    clip_count = (
        np.where(x["event_dir"].eq(1), clip_up.astype(int), np.where(x["event_dir"].eq(-1), clip_dn.astype(int), 0))
    )
    # Only previous 3 bars.
    aligned_prev3 = pd.Series(clip_count, index=x.index).shift(1).rolling(3, min_periods=3).sum()
    x["aligned_clip_count_3"] = aligned_prev3
    x["hm6"] = x["hm1"] & x["aligned_clip_count_3"].ge(2)

    # Continuous directional clipping pressure: signed excess over the band,
    # normalized by ATR. This is causal at event time.
    up_excess = ((x["close"] - x["salma_upper"]) / x["atr14"]).clip(lower=0)
    dn_excess = ((x["salma_lower"] - x["close"]) / x["atr14"]).clip(lower=0)
    signed_clip = np.where(
        x["event_dir"].eq(1), up_excess,
        np.where(x["event_dir"].eq(-1), dn_excess, 0.0)
    )
    x["clip_pressure_3"] = pd.Series(signed_clip, index=x.index).shift(1).rolling(3, min_periods=3).sum()

    # Prior trend for descriptive regime interaction.
    x["prior20_ret_atr"] = (x["close"].shift(1) - x["close"].shift(21)) / atr14
    x["loc20"] = (
        (x["close"] - x["close"].shift(1).rolling(20, min_periods=20).min()) /
        (x["close"].shift(1).rolling(20, min_periods=20).max() -
         x["close"].shift(1).rolling(20, min_periods=20).min())
    )
    x["valid_event"] = x["base_event"] & x["atr14"].notna()
    return x


def outcome_for_event(x: pd.DataFrame, i: int, direction: int, atr: float, horizon: int = 20) -> dict:
    session = x.loc[i, "session_date"]
    sub = x[(x.index > i) & (x.session_date == session)].head(horizon)
    if sub.empty or not np.isfinite(atr) or atr <= 0:
        return {"valid": False}
    entry = float(sub.iloc[0]["open"])
    stop = entry - direction * atr
    target2 = entry + direction * 2 * atr
    target3 = entry + direction * 3 * atr
    target15 = entry + direction * 1.5 * atr

    r2 = 0.0
    r3 = 0.0
    r15 = 0.0
    out2 = "TIME"
    out3 = "TIME"
    out15 = "TIME"
    t2 = t3 = t15 = 999
    mfe = 0.0
    mae = 0.0
    path = []

    for k, (_, row) in enumerate(sub.iterrows(), start=1):
        hi = float(row["high"]); lo = float(row["low"]); cl = float(row["close"])
        fav = direction * (hi - entry) if direction == 1 else direction * (lo - entry)
        adv = direction * (lo - entry) if direction == 1 else direction * (hi - entry)
        mfe = max(mfe, fav / atr)
        mae = max(mae, -adv / atr)

        if out15 == "TIME":
            hit_stop = (lo <= stop) if direction == 1 else (hi >= stop)
            hit_target = (hi >= target15) if direction == 1 else (lo <= target15)
            if hit_stop and hit_target:
                out15 = "STOP"
                r15 = -1.0
                t15 = k
            elif hit_stop:
                out15 = "STOP"; r15 = -1.0; t15 = k
            elif hit_target:
                out15 = "TARGET"; r15 = 1.5; t15 = k

        if out2 == "TIME":
            hit_stop = (lo <= stop) if direction == 1 else (hi >= stop)
            hit_target = (hi >= target2) if direction == 1 else (lo <= target2)
            if hit_stop and hit_target:
                out2 = "STOP"; r2 = -1.0; t2 = k
            elif hit_stop:
                out2 = "STOP"; r2 = -1.0; t2 = k
            elif hit_target:
                out2 = "TARGET"; r2 = 2.0; t2 = k

        if out3 == "TIME":
            hit_stop = (lo <= stop) if direction == 1 else (hi >= stop)
            hit_target = (hi >= target3) if direction == 1 else (lo <= target3)
            if hit_stop and hit_target:
                out3 = "STOP"; r3 = -1.0; t3 = k
            elif hit_stop:
                out3 = "STOP"; r3 = -1.0; t3 = k
            elif hit_target:
                out3 = "TARGET"; r3 = 3.0; t3 = k

        path.append(cl)

    if out15 == "TIME": r15 = direction * (float(sub.iloc[-1]["close"]) - entry) / atr
    if out2 == "TIME": r2 = direction * (float(sub.iloc[-1]["close"]) - entry) / atr
    if out3 == "TIME": r3 = direction * (float(sub.iloc[-1]["close"]) - entry) / atr

    return {
        "valid": True,
        "entry": entry,
        "r15": r15, "r2": r2, "r3": r3,
        "out15": out15, "out2": out2, "out3": out3,
        "t15": t15, "t2": t2, "t3": t3,
        "mfe20": mfe, "mae20": mae,
        "ret20atr": direction * (float(sub.iloc[-1]["close"]) - entry) / atr,
    }


def build_event_table(x: pd.DataFrame) -> pd.DataFrame:
    events = x[x["valid_event"]].copy()
    recs = []
    for i, row in events.iterrows():
        o = outcome_for_event(x, i, int(row["event_dir"]), float(row["atr14"]))
        if not o["valid"]:
            continue
        rec = {
            "datetime": row["datetime"],
            "year": int(row["datetime"].year),
            "direction": int(row["event_dir"]),
            "hm1": bool(row["hm1"]),
            "hm6": bool(row["hm6"]),
            "aligned_clip_count_3": float(row["aligned_clip_count_3"]) if pd.notna(row["aligned_clip_count_3"]) else np.nan,
            "clip_pressure_3": float(row["clip_pressure_3"]) if pd.notna(row["clip_pressure_3"]) else np.nan,
            "prior20_ret_atr": float(row["prior20_ret_atr"]) if pd.notna(row["prior20_ret_atr"]) else np.nan,
            "loc20": float(row["loc20"]) if pd.notna(row["loc20"]) else np.nan,
            "r2": o["r2"], "r3": o["r3"], "r15": o["r15"],
            "out2": o["out2"], "out3": o["out3"],
            "t2": o["t2"], "t3": o["t3"],
            "mfe20": o["mfe20"], "mae20": o["mae20"], "ret20atr": o["ret20atr"],
        }
        recs.append(rec)
    return pd.DataFrame(recs)


def auc_rank(y, score):
    y = np.asarray(y, dtype=int); score = np.asarray(score, dtype=float)
    keep = np.isfinite(score)
    y=y[keep]; score=score[keep]
    pos=score[y==1]; neg=score[y==0]
    if len(pos)==0 or len(neg)==0: return np.nan
    ranks=pd.Series(np.r_[pos,neg]).rank(method="average").to_numpy()
    n1=len(pos); n0=len(neg)
    return float((ranks[:n1].sum() - n1*(n1+1)/2)/(n1*n0))


def cluster_bootstrap_delta(events: pd.DataFrame, n_boot=3000, seed=7):
    rng=np.random.default_rng(seed)
    d=events.copy()
    day=d["datetime"].dt.date.astype(str)
    days=np.array(sorted(day.unique()))
    observed=d.loc[d.hm1,"r2"].mean()-d.loc[~d.hm1,"r2"].mean()
    vals=[]
    for _ in range(n_boot):
        samp=rng.choice(days,size=len(days),replace=True)
        parts=[d[day==s] for s in samp]
        b=pd.concat(parts,ignore_index=True)
        if b.hm1.any() and (~b.hm1).any():
            vals.append(b.loc[b.hm1,"r2"].mean()-b.loc[~b.hm1,"r2"].mean())
    vals=np.array(vals)
    return observed, float(np.quantile(vals,0.025)), float(np.quantile(vals,0.975))


def hazard_table(events: pd.DataFrame, flag_col="hm1", R=2):
    out=[]
    target=f"out{R:g}"
    tcol=f"t{R:g}"
    if R==1.5:
        target="out15"; tcol="t15"
    for flag in [False, True]:
        g=events[events[flag_col]==flag]
        for k in range(1,21):
            at=(g[tcol]>=k).sum()
            te=((g[tcol]==k)&(g[target]=="TARGET")).sum()
            se=((g[tcol]==k)&(g[target]=="STOP")).sum()
            out.append([flag,k,at,te,se,te/at if at else np.nan,se/at if at else np.nan])
    return pd.DataFrame(out,columns=["flag","t","at_risk","target_events","stop_events","target_hazard","stop_hazard"])


def main():
    minute=parse_source(DATA)
    bars=aggregate_to_5m(minute)
    bars=add_session_metadata(bars)
    bars=bars.sort_values("datetime").reset_index(drop=True)
    bars=add_salma(bars)
    bars=add_causal_features(bars)

    # Restrict event evaluations to complete sessions and require a next bar.
    event_tbl=build_event_table(bars)

    # Exact B0 audit: formula and state changes.
    salma_summary={
        "minute_rows": int(len(minute)),
        "five_minute_rows": int(len(bars)),
        "first_datetime": str(bars.datetime.min()),
        "last_datetime": str(bars.datetime.max()),
        "sessions": int(bars.session_date.nunique()),
        "complete_sessions": int(bars.groupby("session_date")["complete_session"].first().sum()),
        "incomplete_sessions": int(bars.groupby("session_date")["complete_session"].first().eq(False).sum()),
        "swing_up": int(bars.swing_up.sum()),
        "swing_down": int(bars.swing_down.sum()),
        "base_events": int(len(event_tbl)),
        "hm1_events": int(event_tbl.hm1.sum()),
        "hm6_events": int(event_tbl.hm6.sum()),
    }

    # Yearly comparison.
    yearly=[]
    for y,g in event_tbl.groupby("year"):
        cand=g[g.hm1]; ctrl=g[~g.hm1]
        if len(cand)==0 or len(ctrl)==0: continue
        yearly.append({
            "year":int(y),
            "base_events":len(g),
            "hm1_events":len(cand),
            "control_events":len(ctrl),
            "hm1_mean_r2":cand.r2.mean(),
            "control_mean_r2":ctrl.r2.mean(),
            "delta_r2":cand.r2.mean()-ctrl.r2.mean(),
            "hm1_mean_r3":cand.r3.mean(),
            "control_mean_r3":ctrl.r3.mean(),
            "delta_r3":cand.r3.mean()-ctrl.r3.mean(),
            "hm1_ret20atr":cand.ret20atr.mean(),
            "control_ret20atr":ctrl.ret20atr.mean(),
            "delta_ret20atr":cand.ret20atr.mean()-ctrl.ret20atr.mean(),
            "hm1_mfe20":cand.mfe20.mean(),
            "control_mfe20":ctrl.mfe20.mean(),
            "hm1_mae20":cand.mae20.mean(),
            "control_mae20":ctrl.mae20.mean(),
            "hm1_2r_target_rate":(cand.out2=="TARGET").mean(),
            "control_2r_target_rate":(ctrl.out2=="TARGET").mean(),
        })
    yearly_df=pd.DataFrame(yearly)

    # Hazard and conditional survival diagnostics.
    h2=hazard_table(event_tbl,R=2)
    h3=hazard_table(event_tbl,R=3)

    # Continuous clipping pressure: information coefficient and binned event rates.
    ep=event_tbl.dropna(subset=["clip_pressure_3"]).copy()
    spearman=ep[["clip_pressure_3","ret20atr","r2"]].corr(method="spearman")
    bins=pd.qcut(ep.clip_pressure_3.rank(method="first"),5,labels=False)+1
    clip_bins=ep.assign(pressure_q=bins).groupby("pressure_q").agg(
        n=("r2","size"), mean_r2=("r2","mean"), mean_r3=("r3","mean"),
        ret20atr=("ret20atr","mean"), mfe20=("mfe20","mean"), mae20=("mae20","mean"),
        target2=("out2",lambda s:(s=="TARGET").mean())
    ).reset_index()

    # Directional asymmetry.
    dir_rows=[]
    for d,g in event_tbl.groupby("direction"):
        cand=g[g.hm1]; ctrl=g[~g.hm1]
        if len(cand) and len(ctrl):
            dir_rows.append({
                "direction":int(d),"hm1_n":len(cand),"control_n":len(ctrl),
                "delta_r2":cand.r2.mean()-ctrl.r2.mean(),
                "delta_r3":cand.r3.mean()-ctrl.r3.mean(),
                "delta_ret20atr":cand.ret20atr.mean()-ctrl.ret20atr.mean(),
                "delta_mfe":cand.mfe20.mean()-ctrl.mfe20.mean(),
                "delta_mae":cand.mae20.mean()-ctrl.mae20.mean(),
            })
    dir_df=pd.DataFrame(dir_rows)

    # H-M6 and H-M8 incremental view within the exact base-event universe.
    incremental=[]
    for name,mask in [
        ("H-M1", event_tbl.hm1),
        ("H-M6", event_tbl.hm6),
    ]:
        a=event_tbl[mask]; b=event_tbl[~mask]
        incremental.append({
            "group":name,"n":len(a),"control_n":len(b),
            "mean_r2":a.r2.mean(),"control_mean_r2":b.r2.mean(),
            "delta_r2":a.r2.mean()-b.r2.mean(),
            "mean_r3":a.r3.mean(),"delta_r3":a.r3.mean()-b.r3.mean(),
            "ret20atr":a.ret20atr.mean(),"delta_ret20atr":a.ret20atr.mean()-b.ret20atr.mean(),
            "mfe20":a.mfe20.mean(),"mae20":a.mae20.mean()
        })
    inc_df=pd.DataFrame(incremental)

    # H-M8: monotone pressure diagnostic among all base events.
    ep["pressure_rank"] = ep.clip_pressure_3.rank(pct=True)
    y=(ep.out2=="TARGET").astype(int)
    auc=auc_rank(y,ep.clip_pressure_3)
    m8_summary=pd.DataFrame([{
        "events":len(ep),"pressure_auc_for_2r_target":auc,
        "spearman_pressure_ret20":spearman.loc["clip_pressure_3","ret20atr"],
        "spearman_pressure_r2":spearman.loc["clip_pressure_3","r2"],
    }])

    # Cluster bootstrap on H-M1 vs control R2.
    boot=dict(zip(["observed_delta","ci_low","ci_high"],cluster_bootstrap_delta(event_tbl)))

    # Save outputs.
    bars[["datetime","open","high","low","close","salma","salma_upper","salma_lower",
          "swing_up","swing_down","event_dir","base_event","hm1","hm6","aligned_clip_count_3",
          "clip_pressure_3","atr14","expansion_ratio","compression_ratio","prior20_ret_atr","loc20"]].to_csv(
        OUT/"INDEX_5M_SALMA_EXACT_FEATURES_2015_2024.csv",index=False)
    event_tbl.to_csv(OUT/"INDEX_HM1_FULL_EVENT_LOG_2015_2024.csv",index=False)
    yearly_df.to_csv(OUT/"INDEX_HM1_YEARLY_RESULTS_2015_2024.csv",index=False)
    h2.to_csv(OUT/"INDEX_HM1_HAZARD_R2.csv",index=False)
    h3.to_csv(OUT/"INDEX_HM1_HAZARD_R3.csv",index=False)
    clip_bins.to_csv(OUT/"INDEX_CLIPPING_PRESSURE_QUINTILES_2015_2024.csv",index=False)
    dir_df.to_csv(OUT/"INDEX_HM1_DIRECTION_RESULTS_2015_2024.csv",index=False)
    inc_df.to_csv(OUT/"INDEX_HM1_HM6_INCREMENTAL.csv",index=False)
    m8_summary.to_csv(OUT/"INDEX_HM8_SUMMARY_2015_2024.csv",index=False)

    report_lines=[]
    report_lines += ["# Deep Index Research — 2015-2024", "", "## Data audit", pd.Series(salma_summary).to_string(), ""]
    report_lines += ["## H-M1 / H-M6 year-by-year", yearly_df.to_string(index=False), ""]
    report_lines += ["## H-M1 vs H-M6 incremental", inc_df.to_string(index=False), ""]
    report_lines += ["## Directional asymmetry", dir_df.to_string(index=False), ""]
    report_lines += ["## Clipping pressure", m8_summary.to_string(index=False), clip_bins.to_string(index=False), ""]
    report_lines += ["## Day-cluster bootstrap for H-M1 R2 delta", str(boot), ""]
    report_lines += ["## Interpretation", 
                     "This is a cross-instrument transfer and mechanism study, not the final NIFTY-futures validation.",
                     "H-M1/H-M6 were defined before this 2015-2024 test and are not re-optimized here.",
                     "Any apparent year/regime concentration is descriptive and must not be promoted to a trading filter without unseen validation.",
                     ""]
    (OUT/"PHASE37_DEEP_INDEX_RESEARCH.md").write_text("\n".join(report_lines),encoding="utf-8")
    print((OUT/"PHASE37_DEEP_INDEX_RESEARCH.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
