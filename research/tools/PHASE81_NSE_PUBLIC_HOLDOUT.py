#!/usr/bin/env python3
"""Download contract-specific NIFTY futures 5-minute history from NSE's public charting API.

This is the credential-free Phase 81 acquisition path. It uses the same NSE
charting endpoints documented by the open-source OpenChart client:
  POST /v1/exchanges/symbolsDynamic
  POST /v1/charts/symbolHistoricalData

It stores only contract OHLCV. Open interest is not assumed because the public
charting response exposes OHLCV in OpenChart's processing layer.
"""

from __future__ import annotations

import csv
import math
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

BASE = "https://charting.nseindia.com"
SEARCH = f"{BASE}/v1/exchanges/symbolsDynamic"
HIST = f"{BASE}/v1/charts/symbolHistoricalData"

TARGETS = {
    "NIFTY25OCTFUT": "2025-10-28",
    "NIFTY25NOVFUT": "2025-11-25",
    "NIFTY25DECFUT": "2025-12-30",
    "NIFTY26JANFUT": "2026-01-27",
    "NIFTY26FEBFUT": "2026-02-24",
    "NIFTY26MARFUT": "2026-03-30",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://charting.nseindia.com",
    "Referer": "https://charting.nseindia.com/",
}

def search_symbol(session: requests.Session, symbol: str) -> dict:
    r = session.post(SEARCH, json={"symbol": symbol, "segment": "FO"},
                     headers=HEADERS, timeout=30)
    r.raise_for_status()
    obj = r.json()
    if not obj.get("status") or not obj.get("data"):
        raise RuntimeError(f"NSE search returned no data for {symbol}")
    rows = [x for x in obj["data"] if str(x.get("symbol","")).upper() == symbol.upper()]
    if not rows:
        raise RuntimeError(f"Exact symbol not found: {symbol}")
    return rows[0]

def fetch_window(session: requests.Session, info: dict, start: datetime, end: datetime):
    payload = {
        "token": str(info["scripcode"]),
        "fromDate": int(start.timestamp()),
        "toDate": int(end.timestamp()),
        "symbol": info["symbol"],
        "symbolType": info["type"],
        "chartType": "I",
        "timeInterval": 5,
    }
    for attempt in range(6):
        r = session.post(HIST, json=payload, headers=HEADERS, timeout=30)
        if r.status_code in (429, 503):
            time.sleep(min(30, 2 ** attempt))
            continue
        r.raise_for_status()
        obj = r.json()
        if not obj.get("status") or not obj.get("data"):
            return []
        return obj["data"]
    raise RuntimeError(f"Rate-limited fetching {info['symbol']}")

def normalize(data: list[dict], symbol: str, expiry: str):
    out = []
    for row in data:
        if not all(k in row for k in ("time", "open", "high", "low", "close", "volume")):
            continue
        ts = pd.to_datetime(row["time"], unit="ms", utc=True)
        out.append({
            "datetime": ts.isoformat(),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": float(row["volume"]),
            "trading_symbol": symbol,
            "expiry": expiry,
        })
    return out

def main():
    outdir = Path("research/data/external_holdout")
    outdir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=HEADERS, timeout=30)

    combined = []
    manifest = []

    for symbol, expiry_text in TARGETS.items():
        expiry = datetime.fromisoformat(expiry_text).replace(tzinfo=timezone.utc)
        info = search_symbol(session, symbol)

        rows = []
        start = expiry - timedelta(days=120)
        cur = start
        while cur < expiry + timedelta(days=1):
            end = min(cur + timedelta(days=29), expiry + timedelta(days=1))
            rows.extend(normalize(fetch_window(session, info, cur, end), symbol, expiry_text))
            cur = end
            time.sleep(0.35)

        if not rows:
            raise RuntimeError(f"No 5-minute candles returned for {symbol}")

        # Deduplicate and keep only exact contract identity.
        df = pd.DataFrame(rows)
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df = df.drop_duplicates(["datetime"]).sort_values("datetime")

        # Basic OHLC integrity.
        bad = (
            (df["high"] < df[["open","close","low"]].max(axis=1))
            | (df["low"] > df[["open","close","high"]].min(axis=1))
            | (df["high"] < df["low"])
        )
        if bool(bad.any()):
            raise RuntimeError(f"OHLC integrity failure for {symbol}: {int(bad.sum())} rows")

        path = outdir / f"NSE_{symbol}_5m.csv"
        df.to_csv(path, index=False, date_format="%Y-%m-%dT%H:%M:%S%z")

        manifest.append({
            "provider": "NSE charting API",
            "trading_symbol": symbol,
            "expiry": expiry_text,
            "scripcode": info["scripcode"],
            "rows": int(len(df)),
            "first_timestamp": df["datetime"].iloc[0].isoformat(),
            "last_timestamp": df["datetime"].iloc[-1].isoformat(),
            "duplicates_removed": int(len(rows) - len(df)),
        })
        combined.extend(df.to_dict("records"))

    cdf = pd.DataFrame(combined).sort_values(["trading_symbol","datetime"])
    cdf.to_csv(outdir / "NIFTY_FUT_5m_OCT2025_MAR2026_NSE_PUBLIC.csv",
               index=False, date_format="%Y-%m-%dT%H:%M:%S%z")
    pd.DataFrame(manifest).to_csv(outdir / "NSE_CONTRACT_MANIFEST.csv", index=False)

    print(f"Downloaded {len(manifest)} contracts / {len(cdf)} candles")

if __name__ == "__main__":
    main()
