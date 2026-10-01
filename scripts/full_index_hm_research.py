#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "nifty50_candlestick_data.csv"
OUT = ROOT / "artifacts" / "full_index_research"
OUT.mkdir(parents=True, exist_ok=True)

def wma(s, n):
    w = np.arange(1, n + 1, dtype=float)
    return s.rolling(n, min_periods=n).apply(lambda a: np.dot(a, w) / w.sum(), raw=True)

def load_1m():
    d = pd.read_csv(DATA)
    lower = {c.lower(): c for c in d.columns}
    dt = pd.to_datetime(
        d[lower["date"]].astype(str) + " " + d[lower["time"]].astype(str),
        errors="coerce", dayfirst=True
    )
    out = pd.DataFrame({
        "datetime": dt,
        "open": pd.to_numeric(d[lower["open"]], errors="coerce"),
        "high": pd.to_numeric(d[lower["high"]], errors="coerce"),
        "low": pd.to_numeric(d[lower["low"]], errors="coerce"),
        "close": pd.to_numeric(d[lower["close"]], errors="coerce"),
    }).dropna()
    out = out.sort_values("datetime").drop_duplicates("datetime", keep="first")
    if out.datetime.dt.tz is None:
        out.datetime = out.datetime.dt.tz_localize("Asia/Kolkata")
    else:
        out.datetime = out.datetime.dt.tz_convert("Asia/Kolkata")
    return out.reset_index(drop=True)

def make_5m(m):
    x=m[(m.datetime.dt.time >= pd.Timestamp("09:15").time()) &
        (m.datetime.dt.time < pd.Timestamp("15:30").time())].copy()
    x["session"] = x.datetime.dt.date
    x["bucket"] = x.datetime.dt.floor("5min")
    g=x.groupby(["session","bucket"],sort=True)
    y=g.agg(open=("open","first"),high=("high","max"),low=("low","min"),close=("close","last"),src_rows=("close","size")).reset_index()
    y=y.rename(columns={"bucket":"datetime"}).drop(columns="session")
    y["session_date"]=y.datetime.dt.date
    y["bar_in_session"]=y.groupby("session_date").cumcount()
    counts=y.groupby("session_date").size()
    y["session_bars"]=y.session_date.map(counts)
    y["complete_session"]=y.session_bars.eq(75)
    return y.reset_index(drop=True)

def add_features(x):
    x=x.copy()
    c=x.close
    base=wma(c,5)
    stdev=c.rolling(5,min_periods=5).std(ddof=0)
    upper=base+0.30*stdev
    lower=base-0.30*stdev
    cp=c.where(base.notna() & stdev.notna())
    cp=np.where(cp>upper,upper,np.where(cp<lower,lower,cp))
    cp=pd.Series(cp,index=x.index)
    salma=wma(wma(cp,10),3)
    state=(salma>salma.shift(1)).fillna(False)
    su=(state & ~state.shift(1,fill_value=False)).astype(bool)
    sd=(state.shift(1,fill_value=False) & ~state).astype(bool)

    prev=c.shift(1)
    tr=pd.concat([x.high-x.low,(x.high-prev).abs(),(x.low-prev).abs()],axis=1).max(axis=1)
    atr=tr.rolling(14,min_periods=14).mean()
    rng=x.high-x.low
    p_hi=x.high.shift(1).rolling(10,min_periods=10).max()
    p_lo=x.low.shift(1).rolling(10,min_periods=10).min()
    p_med=rng.shift(1).rolling(10,min_periods=10).median()
    p5=rng.shift(1).rolling(5,min_periods=5).mean()
    direction=np.where(c>p_hi,1,np.where(c<p_lo,-1,0))
    base_event=(direction!=0)&(rng/p_med>=1.25)&(p5/atr<=1.0)&x.complete_session

    up_recent=su.shift(1,fill_value=False)|su.shift(2,fill_value=False)|su.shift(3,fill_value=False)
    dn_recent=sd.shift(1,fill_value=False)|sd.shift(2,fill_value=False)|sd.shift(3,fill_value=False)
    hm1=((direction==1)&up_recent)|((direction==-1)&dn_recent)

    clip_up=c>upper
    clip_dn=c<lower
    aligned=np.where(direction==1,clip_up.astype(int),np.where(direction==-1,clip_dn.astype(int),0))
    clip_count=pd.Series(aligned,index=x.index).shift(1).rolling(3,min_periods=3).sum()

    up_ex=np.maximum((c-upper)/atr,0)
    dn_ex=np.maximum((lower-c)/atr,0)
    pressure=np.where(direction==1,up_ex,np.where(direction==-1,dn_ex,0.0))
    pressure3=pd.Series(pressure,index=x.index).shift(1).rolling(3,min_periods=3).sum()

    prior20=(c.shift(1)-c.shift(21))/atr
    prior_abs20=(c.shift(1)-c.shift(21)).abs()/atr
    prior5=(c.shift(1)-c.shift(6))/atr
    x["atr14"]=atr
    x["range"]=rng
    x["salma"]=salma
    x["salma_upper"]=upper
    x["salma_lower"]=lower
    x["swing_up"]=su
    x["swing_down"]=sd
    x["event_dir"]=direction
    x["base_event"]=base_event
    x["hm1"]=hm1
    x["aligned_clip_count_3"]=clip_count
    x["clip_pressure_3"]=pressure3
    x["prior20_ret_atr"]=prior20
    x["prior_abs20_atr"]=prior_abs20
    x["prior5_ret_atr"]=prior5
    return x

def event_outcomes(x):
    idx=np.flatnonzero(x.base_event.to_numpy())
    o=x.open.to_numpy(); hi=x.high.to_numpy(); lo=x.low.to_numpy(); cl=x.close.to_numpy(); atr=x.atr14.to_numpy()
    sess=x.session_date.to_numpy(); direction=x.event_dir.to_numpy()
    rows=[]
    for i in idx:
        if not np.isfinite(atr[i]) or i+1>=len(x): continue
        # same-session future indices, capped at 20 bars
        end=min(len(x),i+21)
        inds=np.arange(i+1,end)
        inds=inds[sess[inds]==sess[i]]
        if len(inds)==0: continue
        a=atr[i]; d=int(direction[i]); entry=o[inds[0]]
        stop=entry-d*a
        out2="TIME";out3="TIME";t2=999;t3=999
        mfe=0;mae=0
        for k,j in enumerate(inds,1):
            hs=(lo[j]<=stop) if d==1 else (hi[j]>=stop)
            ht2=(hi[j]>=entry+2*a) if d==1 else (lo[j]<=entry-2*a)
            ht3=(hi[j]>=entry+3*a) if d==1 else (lo[j]<=entry-3*a)
            mfe=max(mfe, ((hi[j]-entry) if d==1 else (entry-lo[j]))/a)
            mae=max(mae, ((entry-lo[j]) if d==1 else (hi[j]-entry))/a)
            if out2=="TIME":
                if hs: out2="STOP";t2=k
                elif ht2: out2="TARGET";t2=k
            if out3=="TIME":
                if hs: out3="STOP";t3=k
                elif ht3: out3="TARGET";t3=k
        r2=2.0 if out2=="TARGET" else -1.0 if out2=="STOP" else d*(cl[inds[-1]]-entry)/a
        r3=3.0 if out3=="TARGET" else -1.0 if out3=="STOP" else d*(cl[inds[-1]]-entry)/a
        ret20=d*(cl[inds[-1]]-entry)/a
        rows.append({
            "datetime":x.datetime.iloc[i],
            "year":int(x.datetime.iloc[i].year),
            "session_date":x.session_date.iloc[i],
            "direction":d,
            "hm1":bool(x.hm1.iloc[i]),
            "hm6":bool(x.hm1.iloc[i] and x.aligned_clip_count_3.iloc[i]>=2),
            "clip_count":x.aligned_clip_count_3.iloc[i],
            "clip_pressure":x.clip_pressure_3.iloc[i],
            "prior20_ret_atr":x.prior20_ret_atr.iloc[i],
            "prior_abs20_atr":x.prior_abs20_atr.iloc[i],
            "prior5_ret_atr":x.prior5_ret_atr.iloc[i],
            "r2":r2,"r3":r3,"out2":out2,"out3":out3,"t2":t2,"t3":t3,
            "mfe20":mfe,"mae20":mae,"ret20atr":ret20
        })
    return pd.DataFrame(rows)

def bootstrap_day_delta(e, flag="hm1", n=3000, seed=42):
    rng=np.random.default_rng(seed)
    e=e.copy()
    days=np.array(sorted(e.session_date.astype(str).unique()))
    obs=e.loc[e[flag],"r2"].mean()-e.loc[~e[flag],"r2"].mean()
    vals=[]
    for _ in range(n):
        samp=rng.choice(days,len(days),replace=True)
        b=pd.concat([e[e.session_date.astype(str)==d] for d in samp],ignore_index=True)
        if b[flag].any() and (~b[flag]).any():
            vals.append(b.loc[b[flag],"r2"].mean()-b.loc[~b[flag],"r2"].mean())
    v=np.asarray(vals)
    return obs,float(np.quantile(v,.025)),float(np.quantile(v,.975))

def pressure_auc(e):
    z=e.dropna(subset=["clip_pressure"]).copy()
    y=(z.out2=="TARGET").astype(int).to_numpy()
    s=z.clip_pressure.to_numpy()
    pos=s[y==1]; neg=s[y==0]
    if len(pos)==0 or len(neg)==0:return np.nan
    ranks=pd.Series(np.r_[pos,neg]).rank(method="average").to_numpy()
    n1=len(pos);n0=len(neg)
    return float((ranks[:n1].sum()-n1*(n1+1)/2)/(n1*n0))

def hazard(e, flag="hm1"):
    rows=[]
    for val in [False,True]:
        g=e[e[flag]==val]
        for k in range(1,21):
            at=(g.t2>=k).sum()
            te=((g.t2==k)&(g.out2=="TARGET")).sum()
            se=((g.t2==k)&(g.out2=="STOP")).sum()
            rows.append({"group":str(val),"t":k,"at_risk":int(at),"target_events":int(te),"stop_events":int(se),
                         "target_hazard":te/at if at else np.nan,"stop_hazard":se/at if at else np.nan})
    return pd.DataFrame(rows)

def main():
    minute=load_1m()
    bars=add_features(make_5m(minute))
    events=event_outcomes(bars)

    audit={
        "source_rows_1m":len(minute),
        "bars_5m":len(bars),
        "first":str(bars.datetime.min()),
        "last":str(bars.datetime.max()),
        "sessions":int(bars.session_date.nunique()),
        "complete_sessions":int(bars.groupby("session_date").complete_session.first().sum()),
        "swing_up":int(bars.swing_up.sum()),
        "swing_down":int(bars.swing_down.sum()),
        "base_events":len(events),
        "hm1":int(events.hm1.sum()),
        "hm6":int(events.hm6.sum())
    }

    yearly=[]
    for y,g in events.groupby("year"):
        a=g[g.hm1];b=g[~g.hm1]
        if len(a)==0 or len(b)==0: continue
        yearly.append({
            "year":y,"n":len(g),"hm1_n":len(a),"control_n":len(b),
            "delta_r2":a.r2.mean()-b.r2.mean(),
            "delta_r3":a.r3.mean()-b.r3.mean(),
            "delta_ret20atr":a.ret20atr.mean()-b.ret20atr.mean(),
            "delta_mfe":a.mfe20.mean()-b.mfe20.mean(),
            "delta_mae":a.mae20.mean()-b.mae20.mean(),
            "hm1_target2":(a.out2=="TARGET").mean(),
            "control_target2":(b.out2=="TARGET").mean()
        })
    yearly_df=pd.DataFrame(yearly)

    # H-M6 and H-M8 across the long history.
    groups=[]
    for name,col in [("H-M1","hm1"),("H-M6","hm6")]:
        a=events[events[col]];b=events[~events[col]]
        groups.append({
            "group":name,"n":len(a),"control_n":len(b),
            "mean_r2":a.r2.mean(),"control_r2":b.r2.mean(),"delta_r2":a.r2.mean()-b.r2.mean(),
            "mean_r3":a.r3.mean(),"delta_r3":a.r3.mean()-b.r3.mean(),
            "mean_ret20atr":a.ret20atr.mean(),"delta_ret20atr":a.ret20atr.mean()-b.ret20atr.mean(),
            "mean_mfe":a.mfe20.mean(),"mean_mae":a.mae20.mean(),
            "target2_rate":(a.out2=="TARGET").mean(),"control_target2_rate":(b.out2=="TARGET").mean()
        })
    group_df=pd.DataFrame(groups)

    pressure_bins=events.dropna(subset=["clip_pressure"]).copy()
    pressure_bins["q"]=pd.qcut(pressure_bins.clip_pressure.rank(method="first"),5,labels=False)+1
    qdf=pressure_bins.groupby("q").agg(
        n=("r2","size"),mean_r2=("r2","mean"),mean_r3=("r3","mean"),
        ret20atr=("ret20atr","mean"),mfe=("mfe20","mean"),mae=("mae20","mean"),
        target2=("out2",lambda s:(s=="TARGET").mean()),
        hm1_rate=("hm1","mean")
    ).reset_index()
    auc=pressure_auc(events)

    direction=[]
    for d,g in events.groupby("direction"):
        a=g[g.hm1];b=g[~g.hm1]
        if len(a) and len(b):
            direction.append({"direction":d,"hm1_n":len(a),"control_n":len(b),
                              "delta_r2":a.r2.mean()-b.r2.mean(),
                              "delta_r3":a.r3.mean()-b.r3.mean(),
                              "delta_ret20atr":a.ret20atr.mean()-b.ret20atr.mean(),
                              "delta_mfe":a.mfe20.mean()-b.mfe20.mean(),
                              "delta_mae":a.mae20.mean()-b.mae20.mean()})
    direction_df=pd.DataFrame(direction)

    # Prior-trend interaction, kept descriptive.
    trend=[]
    for bucket,g in events.assign(prior_trend=np.select(
        [events.prior20_ret_atr<=-1,events.prior20_ret_atr>=1],["bearish","bullish"],default="neutral"
    )).groupby(["prior_trend","direction"]):
        a=g[g.hm1];b=g[~g.hm1]
        if len(a)>=20 and len(b)>=20:
            trend.append({"prior_trend":bucket[0],"direction":bucket[1],"hm1_n":len(a),"control_n":len(b),
                           "delta_r2":a.r2.mean()-b.r2.mean(),"delta_ret20atr":a.ret20atr.mean()-b.ret20atr.mean()})
    trend_df=pd.DataFrame(trend)

    h2=hazard(events)
    boot=bootstrap_day_delta(events)

    # Cross-era blocks (fixed, not optimized): 2015-17, 2018-20, 2021-24.
    era_specs=[("2015-2017",2015,2017),("2018-2020",2018,2020),("2021-2024",2021,2024)]
    eras=[]
    for name,y0,y1 in era_specs:
        g=events[(events.year>=y0)&(events.year<=y1)]
        if len(g)==0:continue
        a=g[g.hm1];b=g[~g.hm1]
        eras.append({"era":name,"n":len(g),"hm1_n":len(a),"control_n":len(b),
                     "delta_r2":a.r2.mean()-b.r2.mean(),"delta_r3":a.r3.mean()-b.r3.mean(),
                     "delta_ret20atr":a.ret20atr.mean()-b.ret20atr.mean()})
    era_df=pd.DataFrame(eras)

    # Save
    events.to_csv(OUT/"INDEX_HM1_FULL_EVENT_LOG_2015_2024.csv",index=False)
    yearly_df.to_csv(OUT/"INDEX_HM1_YEARLY_RESULTS.csv",index=False)
    group_df.to_csv(OUT/"INDEX_HM1_HM6_RESULTS.csv",index=False)
    qdf.to_csv(OUT/"INDEX_CLIPPING_PRESSURE_QUINTILES.csv",index=False)
    direction_df.to_csv(OUT/"INDEX_DIRECTIONAL_RESULTS.csv",index=False)
    trend_df.to_csv(OUT/"INDEX_PRIOR_TREND_INTERACTION.csv",index=False)
    era_df.to_csv(OUT/"INDEX_ERA_RESULTS.csv",index=False)
    h2.to_csv(OUT/"INDEX_HM1_HAZARD_R2.csv",index=False)

    report=[
        "# Full 2015-2024 NIFTY Index Deep Research","","## Audit",pd.Series(audit).to_string(),"",
        "## H-M1/H-M6 overall",group_df.to_string(index=False),"",
        "## Yearly H-M1 deltas",yearly_df.to_string(index=False),"",
        "## Era results",era_df.to_string(index=False),"",
        "## Directional asymmetry",direction_df.to_string(index=False),"",
        "## Prior-trend interaction",trend_df.to_string(index=False),"",
        "## Continuous clipping pressure",f"2R target AUC from clipping pressure: {auc:.4f}" if np.isfinite(auc) else "AUC unavailable",qdf.to_string(index=False),"",
        "## H-M1 R2 day-cluster bootstrap",f"observed delta={boot[0]:.4f}, 95% CI=[{boot[1]:.4f}, {boot[2]:.4f}]","",
        "## Hazard R2",h2.to_string(index=False),"",
        "## Interpretation",
        "This is a fixed transfer test of hypotheses discovered on Apr-Sep 2026 NIFTY futures. No thresholds were fitted to 2015-2024. Index data is not a substitute for futures execution validation.",
        "The analysis is designed to distinguish movement-persistence from executable 1ATR/2R tradeability and to reveal whether the phenomenon is stable across eras, directions, and pressure levels."
    ]
    (OUT/"PHASE_FULL_INDEX_DEEP_RESEARCH.md").write_text("\n".join(report),encoding="utf-8")
    print("\n".join(report))

if __name__=="__main__":
    main()
