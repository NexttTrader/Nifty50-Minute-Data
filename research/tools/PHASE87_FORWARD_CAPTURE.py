#!/usr/bin/env python3
"""Phase 87 prospective NIFTY front-month 5-minute capture.

Runs after market close. It:
1) resolves the current October-2026 NIFTY futures contract through NSE/OpenChart;
2) refreshes the October 5m OHLCV archive;
3) appends only new frozen signal rows;
4) appends mature outcomes separately.

No outcome data is ever used to alter a signal row.
"""

from __future__ import annotations

import csv
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from curl_cffi import requests

SEARCH_URL = "https://charting.nseindia.com/v1/exchanges/symbolsDynamic"
HIST_URL = "https://charting.nseindia.com/v1/charts/symbolHistoricalData"

EXPECTED_EXPIRY = "2026-10-27"
MAX_DATE = pd.Timestamp("2026-10-27 23:59:59", tz="UTC")
START_DATE = pd.Timestamp("2026-10-01 00:00:00", tz="UTC")

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://charting.nseindia.com",
    "Referer": "https://charting.nseindia.com/",
}

ROOT = Path("research/data/forward")
ROOT.mkdir(parents=True, exist_ok=True)

RAW_PATH = ROOT / "PHASE87_NIFTY26OCTFUT_5m.csv"
SIGNAL_PATH = ROOT / "PHASE87_FROZEN_SIGNALS.csv"
OUTCOME_PATH = ROOT / "PHASE87_SIGNAL_OUTCOMES.csv"
MANIFEST_PATH = ROOT / "PHASE87_FORWARD_MANIFEST.csv"

def wma(s: pd.Series, n: int) -> pd.Series:
    weights = pd.Series(range(1, n + 1), dtype=float)
    den = weights.sum()
    return s.rolling(n, min_periods=n).apply(lambda x: float((x * weights.to_numpy()).sum() / den), raw=True)

def popstd(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).std(ddof=0)

def resolve_symbol(session: requests.Session) -> dict:
    candidates = ["NIFTY26OCTFUT", "NIFTY27OCT26FUT", "NIFTYOCT"]
    all_rows = []
    for q in candidates:
        r = session.get(SEARCH_URL, params={"symbol": q, "segment": "FO"}, headers=HEADERS, timeout=30)
        r.raise_for_status()
        obj = r.json()
        all_rows.extend(obj.get("data") or [])
    seen = {}
    for row in all_rows:
        sym = str(row.get("symbol", "")).upper()
        typ = str(row.get("type", "")).lower()
        if "FUT" not in sym or "NIFTY" not in sym or "future" not in typ:
            continue
        seen[sym] = row
    preferred = [s for s in ["NIFTY26OCTFUT", "NIFTY27OCT26FUT"] if s in seen]
    if preferred:
        return seen[preferred[0]]
    if not seen:
        raise RuntimeError("No active NIFTY October futures contract returned by NSE symbol search")
    # Restrict to October-labelled symbols and choose the most likely exact month contract.
    october = {k:v for k,v in seen.items() if "OCT" in k}
    if not october:
        raise RuntimeError(f"No October NIFTY FUT in search results: {sorted(seen)[:30]}")
    return sorted(october.items())[0][1]

def fetch_history(session: requests.Session, info: dict) -> pd.DataFrame:
    payload = {
        "token": str(info["scripcode"]),
        "fromDate": int(START_DATE.timestamp()),
        "toDate": int(MAX_DATE.timestamp()),
        "symbol": info["symbol"],
        "symbolType": info["type"],
        "chartType": "I",
        "timeInterval": 5,
    }
    r = session.get(HIST_URL, params=payload, headers=HEADERS, timeout=60)
    r.raise_for_status()
    obj = r.json()
    data = (obj.get("data") or [])
    if not data:
        raise RuntimeError(f"No historical candles returned for {info['symbol']}")
    df = pd.DataFrame(data)
    rename = {"time":"datetime","open":"open","high":"high","low":"low","close":"close","volume":"volume"}
    df = df.rename(columns=rename)
    required = ["datetime","open","high","low","close","volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Historical schema missing {missing}; columns={list(df.columns)}")
    df = df[required].copy()
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms", utc=True)
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["datetime","open","high","low","close"]).drop_duplicates("datetime")
    df = df.sort_values("datetime")
    df["trading_symbol"] = info["symbol"]
    df["scripcode"] = info["scripcode"]
    df["expiry"] = EXPECTED_EXPIRY
    bad = (
        (df["high"] < df[["open","close","low"]].max(axis=1))
        | (df["low"] > df[["open","close","high"]].min(axis=1))
        | (df["high"] < df["low"])
    )
    if bool(bad.any()):
        raise RuntimeError(f"OHLC integrity failure in {int(bad.sum())} rows")
    return df

def load_existing(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

def build_signals(df: pd.DataFrame) -> pd.DataFrame:
    x = df.sort_values("datetime").reset_index(drop=True).copy()
    c = x["close"]
    rng = x["high"] - x["low"]
    prev_c = c.shift(1)
    tr = pd.concat([
        x["high"] - x["low"],
        (x["high"] - prev_c).abs(),
        (x["low"] - prev_c).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean()
    med10 = rng.rolling(10, min_periods=10).median()
    mean5 = rng.rolling(5, min_periods=5).mean()
    b = wma(c, 5)
    sd = popstd(c, 5)
    upper = b + 0.30 * sd
    lower = b - 0.30 * sd
    clipped = c.clip(lower, upper)
    salma = wma(wma(clipped, 10), 3)
    slope = salma.diff()
    state = slope > 0
    flip_dir = pd.Series(0, index=x.index, dtype=int)
    upflip = state & (~state.shift(1).fillna(False))
    dnflip = (~state) & state.shift(1).fillna(False)
    flip_dir.loc[upflip] = 1
    flip_dir.loc[dnflip] = -1
    last_i = -1
    last_d = 0
    flip_i = []
    flip_d = []
    for i, d in enumerate(flip_dir.to_numpy()):
        if d:
            last_i, last_d = i, int(d)
        flip_i.append(last_i)
        flip_d.append(last_d)
    x["atr14"] = atr
    x["event_range_atr"] = rng / atr
    x["median10_range"] = med10
    x["mean5_range"] = mean5
    x["salma"] = salma
    x["upper"] = upper
    x["lower"] = lower
    x["_flip_i"] = flip_i
    x["_flip_d"] = flip_d
    out = []
    for i in range(14, len(x) - 1):
        dt = x.loc[i, "datetime"]
        if x.loc[i + 1, "datetime"].date() != dt.date():
            continue
        prev_hi = x.loc[i-10:i-1, "high"].max()
        prev_lo = x.loc[i-10:i-1, "low"].min()
        up_break = c.iloc[i] > prev_hi
        dn_break = c.iloc[i] < prev_lo
        if not (up_break or dn_break):
            continue
        if not (rng.iloc[i] >= 1.25 * med10.iloc[i]):
            continue
        if not (mean5.iloc[i] / atr.iloc[i] <= 1.0):
            continue
        direction = 1 if up_break else -1
        dist = i - int(x.loc[i, "_flip_i"])
        if not (1 <= dist <= 3 and int(x.loc[i, "_flip_d"]) == direction):
            continue
        cc = 0
        pressure = 0.0
        for z in range(1, 4):
            j = i - z
            aligned = c.iloc[j] > upper.iloc[j] if direction == 1 else c.iloc[j] < lower.iloc[j]
            cc += int(aligned)
            excess = max(0.0, c.iloc[j] - upper.iloc[j]) if direction == 1 else max(0.0, lower.iloc[j] - c.iloc[j])
            pressure += excess / atr.iloc[i]
        prior = {f"priorret{n}": direction * (c.iloc[i] - c.iloc[i-n]) / atr.iloc[i] for n in [1,3,5,10,20]}
        out.append({
            "signal_timestamp": dt.isoformat(),
            "trading_symbol": x.loc[i, "trading_symbol"],
            "expiry": EXPECTED_EXPIRY,
            "direction": direction,
            "flip_dist": dist,
            "clip_count_3": cc,
            "clip_pressure_3": pressure,
            "h_m1": True,
            "h_m6": cc >= 2,
            "h_m9": (cc == 3 and dist == 2),
            "event_range_atr": rng.iloc[i] / atr.iloc[i],
            "atr14": atr.iloc[i],
            **prior,
        })
    return pd.DataFrame(out)

def build_outcomes(df: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return signals
    x = df.sort_values("datetime").reset_index(drop=True)
    rows = []
    for _, s in signals.iterrows():
        event_ts = pd.to_datetime(s["signal_timestamp"], utc=True)
        g = x[(x["datetime"] > event_ts) & (x["datetime"].dt.date == event_ts.date())].head(20)
        if len(g) == 0:
            continue
        # The next bar must exist; at most 20 bars are evaluated.
        if len(g) < 20:
            max_horizon = len(g)
        else:
            max_horizon = 20
        entry = float(g.iloc[0]["open"])
        R = float(s["atr14"])
        d = int(s["direction"])
        fav = ((g["high"] - entry) if d == 1 else (entry - g["low"])) / R
        adv = ((entry - g["low"]) if d == 1 else (g["high"] - entry)) / R
        mfe = float(fav.max())
        mae = float(adv.max())
        def first(level):
            z = fav.to_numpy()
            idx = (z >= level).nonzero()[0]
            return int(idx[0] + 1) if len(idx) else None
        rows.append({
            "signal_timestamp": s["signal_timestamp"],
            "trading_symbol": s["trading_symbol"],
            "bars_available": max_horizon,
            "mfe20": mfe,
            "mae20": mae,
            "r1_first_bars": first(1.0),
            "r1_5_first_bars": first(1.5),
            "r2_first_bars": first(2.0),
            "r3_first_bars": first(3.0),
            "mature": max_horizon >= 20,
        })
    return pd.DataFrame(rows)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    today = pd.Timestamp.now(tz="UTC")
    if today > MAX_DATE:
        print("Phase 87 October capture window is closed.")
        return
    session = requests.Session(impersonate="chrome120")
    session.headers.update(HEADERS)
    session.get("https://www.nseindia.com", timeout=20)
    info = resolve_symbol(session)
    df = fetch_history(session, info)
    df.to_csv(RAW_PATH, index=False, date_format="%Y-%m-%dT%H:%M:%S%z")

    signals_new = build_signals(df)
    existing = load_existing(SIGNAL_PATH)
    if not existing.empty:
        existing_keys = set(existing["signal_timestamp"].astype(str) + "|" + existing["trading_symbol"].astype(str))
        signals_new["_key"] = signals_new["signal_timestamp"].astype(str) + "|" + signals_new["trading_symbol"].astype(str)
        signals_new = signals_new[~signals_new["_key"].isin(existing_keys)].drop(columns=["_key"])
    if not signals_new.empty:
        combined = pd.concat([existing, signals_new], ignore_index=True) if not existing.empty else signals_new
    else:
        combined = existing
    if combined.empty:
        pd.DataFrame(columns=[
            "signal_timestamp","trading_symbol","expiry","direction","flip_dist",
            "clip_count_3","clip_pressure_3","h_m1","h_m6","h_m9",
            "event_range_atr","atr14","priorret1","priorret3","priorret5",
            "priorret10","priorret20"
        ]).to_csv(SIGNAL_PATH, index=False)
    else:
        combined.sort_values(["signal_timestamp","trading_symbol"]).to_csv(SIGNAL_PATH, index=False)

    all_signals = load_existing(SIGNAL_PATH)
    mature = build_outcomes(df, all_signals)
    old_out = load_existing(OUTCOME_PATH)
    if not mature.empty:
        mature = mature[mature["mature"] == True]
        if not old_out.empty:
            keys = set(old_out["signal_timestamp"].astype(str) + "|" + old_out["trading_symbol"].astype(str))
            mature["_key"] = mature["signal_timestamp"].astype(str) + "|" + mature["trading_symbol"].astype(str)
            mature = mature[~mature["_key"].isin(keys)].drop(columns=["_key"])
        if not mature.empty:
            out = pd.concat([old_out, mature], ignore_index=True) if not old_out.empty else mature
            out.sort_values(["signal_timestamp","trading_symbol"]).to_csv(OUTCOME_PATH, index=False)

    manifest = pd.DataFrame([{
        "provider":"NSE charting API via OpenChart-compatible endpoint",
        "trading_symbol":info["symbol"],
        "scripcode":info["scripcode"],
        "expected_expiry":EXPECTED_EXPIRY,
        "rows":len(df),
        "first_timestamp":df["datetime"].min().isoformat(),
        "last_timestamp":df["datetime"].max().isoformat(),
        "signal_rows_total":len(load_existing(SIGNAL_PATH)),
        "outcome_rows_total":len(load_existing(OUTCOME_PATH)),
        "captured_at_utc":datetime.now(timezone.utc).isoformat(),
        "raw_sha256":sha256(RAW_PATH),
    }])
    manifest.to_csv(MANIFEST_PATH, index=False)
    print(manifest.to_string(index=False))

if __name__ == "__main__":
    main()
