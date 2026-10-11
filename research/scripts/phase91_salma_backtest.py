"""Reproduce the frozen SALMA H-M1/H-M6 outcomes and sequential backtest from repo data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research" / "data"
CAN = DATA / "canonical"
OUT = DATA / "forward"
OUT.mkdir(parents=True, exist_ok=True)

files = sorted(CAN.glob("NIFTY26*_5m_2026.csv"))
if len(files) != 6:
    raise FileNotFoundError(f"Expected six canonical monthly-futures CSVs in {CAN}, found {len(files)}")
raw = pd.concat([pd.read_csv(p) for p in files], ignore_index=True)
raw["datetime"] = pd.to_datetime(raw["datetime"])
raw = raw.sort_values(["tradingsymbol", "datetime"]).reset_index(drop=True)
raw["session_date"] = raw["datetime"].dt.date
raw["bar_idx"] = raw.groupby("tradingsymbol").cumcount()
raw["session_last_idx"] = raw.groupby(["tradingsymbol", "session_date"])["bar_idx"].transform("max")
prev_close = raw.groupby("tradingsymbol")["close"].shift(1)
raw["tr"] = pd.concat([raw["high"]-raw["low"], (raw["high"]-prev_close).abs(),
                       (raw["low"]-prev_close).abs()], axis=1).max(axis=1)
raw["atr14"] = raw.groupby("tradingsymbol")["tr"].transform(lambda x: x.rolling(14, min_periods=14).mean())

event_file = DATA / "SALMA_HM1_EXACT_AUDITED_EVENTS_APR_SEP_2026.csv"
events = pd.read_csv(event_file)
events["datetime"] = pd.to_datetime(events["datetime"])
if len(events) != 513:
    raise AssertionError(f"Frozen event table changed: expected 513 rows; got {len(events)}")
lookup = raw.set_index(["tradingsymbol", "datetime"], drop=False)
out = []
for ev in events.itertuples(index=False):
    key = (ev.tradingsymbol, ev.datetime)
    if key not in lookup.index:
        raise ValueError(f"Event candle missing: {key}")
    bar = lookup.loc[key]
    if isinstance(bar, pd.DataFrame):
        raise ValueError(f"Duplicate candle: {key}")
    ei = int(bar.bar_idx)
    entry_i = ei + 1
    if entry_i > int(bar.session_last_idx):
        raise ValueError(f"No next-bar entry for {key}")
    entry_bar = raw[(raw.tradingsymbol == ev.tradingsymbol) & (raw.bar_idx == entry_i)].iloc[0]
    if entry_bar.session_date != bar.session_date:
        raise ValueError(f"Cross-session entry disallowed: {key}")
    entry, atr, direction = float(entry_bar.open), float(bar.atr14), int(ev.dir)
    path = raw[(raw.tradingsymbol == ev.tradingsymbol) & (raw.bar_idx >= entry_i) &
               (raw.bar_idx <= min(ei + 20, int(bar.session_last_idx)))]
    path = path[path.session_date == bar.session_date]
    if len(path) == 0 or not np.isfinite(atr) or atr <= 0:
        raise ValueError(f"Invalid path or ATR for {key}")
    ret20 = direction * (float(path.iloc[-1].close) - entry) / atr
    mfe = (float(path.high.max()) - entry) / atr if direction == 1 else (entry - float(path.low.min())) / atr
    mae = (entry - float(path.low.min())) / atr if direction == 1 else (float(path.high.max()) - entry) / atr
    row = dict(tradingsymbol=ev.tradingsymbol, datetime=ev.datetime, split=ev.split, dir=direction,
               h_m1=bool(ev.h_m1), h_m6=bool(ev.h_m6), event_bar_idx=ei, entry_datetime=entry_bar.datetime,
               entry_price=entry, atr14_points=atr, ret20atr=ret20, mfe20atr=mfe, mae20atr=mae,
               horizon_bars=len(path))
    for target in (1.5, 2.0, 3.0):
        label = f"{target:g}"
        target_price, stop_price = entry + direction * target * atr, entry - direction * atr
        result, status = ret20, "TIME"
        exit_bar = path.iloc[-1]
        for b in path.itertuples(index=False):
            stop_hit = float(b.low) <= stop_price if direction == 1 else float(b.high) >= stop_price
            target_hit = float(b.high) >= target_price if direction == 1 else float(b.low) <= target_price
            if stop_hit:
                result, status, exit_bar = -1.0, "STOP", b
                break
            if target_hit:
                result, status, exit_bar = target, "TARGET", b
                break
        row[f"R{label}"], row[f"out{label}"] = float(result), status
        row[f"exit_datetime_R{label}"] = exit_bar.datetime
        row[f"exit_bar_end_R{label}"] = pd.Timestamp(exit_bar.datetime) + pd.Timedelta(minutes=5)
    out.append(row)
ledger = pd.DataFrame(out).sort_values(["datetime", "tradingsymbol"]).reset_index(drop=True)

# Audit all numerical outcomes against the frozen audited source table.
canon = events.set_index(["tradingsymbol", "datetime"])
checks = []
for r in ledger.itertuples(index=False):
    c = canon.loc[(r.tradingsymbol, r.datetime)]
    for target, col in [(1.5, "R1.5"), (2.0, "R2.0"), (3.0, "R3.0")]:
        checks.append(abs(getattr(r, f"R{target:g}") - float(c[col])))
    for new, old in [("ret20atr", "ret20atr"), ("mfe20atr", "mfe20atr"), ("mae20atr", "mae20atr")]:
        checks.append(abs(getattr(r, new) - float(c[old])))
    for new, old in [("out2", "out2.0"), ("out3", "out3.0")]:
        if getattr(r, new) != c[old]:
            raise AssertionError(f"Barrier status mismatch: {r.tradingsymbol} {r.datetime} {new}")
if max(checks) > 1e-8:
    raise AssertionError(f"Outcome audit failed; max numeric difference={max(checks)}")
ledger["group"] = np.where(ledger.h_m6, "H-M6",
                    np.where(ledger.h_m1, "H-M1_only", "Control_non_H-M1"))
ledger["month"] = pd.to_datetime(ledger.datetime).dt.strftime("%Y-%m")
ledger["direction_label"] = ledger.dir.map({1: "Long", -1: "Short"})
ledger.to_csv(OUT / "SALMA_BACKTEST_PHASE91_TRADE_LEDGER.csv", index=False)

def group_mask(df, name):
    if name == "Base_all": return np.ones(len(df), dtype=bool)
    if name == "H-M1": return df.h_m1.to_numpy().astype(bool)
    if name == "H-M6": return df.h_m6.to_numpy().astype(bool)
    if name == "H-M1_only": return (df.h_m1.astype(bool) & ~df.h_m6.astype(bool)).to_numpy()
    if name == "Control_non_H-M1": return (~df.h_m1.astype(bool)).to_numpy()
    raise ValueError(name)

def metrics(vals, trades):
    vals = pd.Series(vals, dtype=float)
    pos, neg = float(vals[vals > 0].sum()), float(-vals[vals < 0].sum())
    eq = np.r_[0.0, vals.cumsum().to_numpy()]
    return dict(trades=len(vals), total_R=float(vals.sum()), mean_R=float(vals.mean()) if len(vals) else np.nan,
                profit_factor=pos/neg if neg else (np.inf if pos else np.nan),
                win_rate_pct=float((vals > 0).mean()*100) if len(vals) else np.nan,
                max_drawdown_R=float(np.max(np.maximum.accumulate(eq)-eq)) if len(eq) else 0.0)

summaries, execution = [], []
for split in ("D", "V"):
    for group in ("Base_all", "H-M1", "H-M6", "H-M1_only", "Control_non_H-M1"):
        candidates = ledger[ledger.split.eq(split)].copy()
        candidates = candidates.loc[group_mask(candidates, group)].sort_values(["entry_datetime", "tradingsymbol"])
        for target in (1.5, 2.0, 3.0):
            label = f"{target:g}"
            taken, free = [], None
            for _, trade in candidates.iterrows():
                start = pd.Timestamp(trade.entry_datetime)
                if free is not None and start < free:
                    continue
                taken.append(trade)
                free = pd.Timestamp(trade[f"exit_bar_end_R{label}"])
            selected = pd.DataFrame(taken, columns=candidates.columns) if taken else candidates.iloc[0:0].copy()
            if len(selected):
                selected = selected.copy()
                selected["strategy_group"], selected["target_R"] = group, target
                execution.append(selected)
            row = metrics(selected[f"R{label}"] if len(selected) else [], selected)
            row.update(split=split, strategy_group=group, target_R=target, signals_available=len(candidates),
                       skipped_overlap_signals=len(candidates)-len(selected),
                       barrier_target_pct=float((selected[f"out{label}"] == "TARGET").mean()*100) if len(selected) else np.nan,
                       stop_pct=float((selected[f"out{label}"] == "STOP").mean()*100) if len(selected) else np.nan)
            for cost in (0, 1, 2, 3, 4, 5):
                net = selected[f"R{label}"] - cost / selected.atr14_points if len(selected) else pd.Series(dtype=float)
                row[f"mean_net_R_cost_{cost}pt"] = float(net.mean()) if len(net) else np.nan
                p, n = float(net[net > 0].sum()), float(-net[net < 0].sum())
                row[f"PF_net_cost_{cost}pt"] = p/n if n else (np.inf if p else np.nan)
            summaries.append(row)
pd.DataFrame(summaries).to_csv(OUT / "SALMA_BACKTEST_PHASE91_EXECUTABLE_SUMMARY.csv", index=False)
if execution:
    pd.concat(execution, ignore_index=True).to_csv(OUT / "SALMA_BACKTEST_PHASE91_EXECUTED_TRADES.csv", index=False)
print(f"Audit passed: 513 events; max absolute numeric difference={max(checks):.3g}.")
