#!/usr/bin/env python3
"""Fetch contract-specific NIFTY expired futures 5-minute OHLCV+OI from Upstox.

Usage:
  export UPSTOX_ACCESS_TOKEN='...'
  python UPSTOX_EXPIRED_NIFTY_FUTURES_HOLDOUT.py --out research/data/external_holdout

The access token is read only from the environment and is never written to disk.
The script resolves each target expired future, downloads 5-minute candles in
30-day windows, validates the response, and writes normalized contract files.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

import requests

BASE_URL = "https://api.upstox.com/v2"
UNDERLYING = "NSE_INDEX|Nifty 50"
TARGET_EXPIRIES = [
    "2025-10-28", "2025-11-25", "2025-12-30",
    "2026-01-27", "2026-02-24", "2026-03-31",
]

def get_json(session: requests.Session, token: str, url: str, params=None):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    for attempt in range(6):
        response = session.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 429:
            time.sleep(min(30, 2 ** attempt))
            continue
        response.raise_for_status()
        return response.json()
    raise RuntimeError("rate limited after retries")

def resolve_future(session: requests.Session, token: str, expiry: str):
    payload = get_json(
        session,
        token,
        f"{BASE_URL}/expired-instruments/future/contract",
        {"instrument_key": UNDERLYING, "expiry_date": expiry},
    )
    contracts = [
        x for x in payload.get("data", [])
        if x.get("instrument_type") == "FUT"
        and x.get("underlying_symbol") == "NIFTY"
    ]
    if len(contracts) != 1:
        raise RuntimeError(f"expected exactly one NIFTY FUT for {expiry}, got {len(contracts)}")
    return contracts[0]

def fetch_window(session: requests.Session, token: str, expired_key: str, start: date, end: date):
    encoded = quote(expired_key, safe="")
    url = (
        f"{BASE_URL}/expired-instruments/historical-candle/"
        f"{encoded}/5minute/{end.isoformat()}/{start.isoformat()}"
    )
    payload = get_json(session, token, url)
    return (payload.get("data") or {}).get("candles", [])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="research/data/external_holdout")
    parser.add_argument("--days-before-expiry", type=int, default=120)
    args = parser.parse_args()

    token = os.environ.get("UPSTOX_ACCESS_TOKEN")
    if not token:
        raise SystemExit("UPSTOX_ACCESS_TOKEN is required")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    combined = []
    session = requests.Session()

    for expiry_text in TARGET_EXPIRIES:
        expiry = date.fromisoformat(expiry_text)
        contract = resolve_future(session, token, expiry_text)

        if contract.get("expiry") != expiry_text:
            raise RuntimeError(
                f"expiry mismatch: requested {expiry_text}, returned {contract.get('expiry')}"
            )

        expired_key = contract.get("instrument_key")
        trading_symbol = contract.get("trading_symbol")
        if not expired_key or not trading_symbol:
            raise RuntimeError(f"missing contract identity for {expiry_text}")

        start = expiry - timedelta(days=args.days_before_expiry)
        cur = start
        raw_candles = []

        while cur <= expiry:
            window_end = min(cur + timedelta(days=29), expiry)
            raw_candles.extend(fetch_window(session, token, expired_key, cur, window_end))
            cur = window_end + timedelta(days=1)

        normalized = []
        for candle in raw_candles:
            if len(candle) < 7:
                raise RuntimeError(f"bad candle schema for {trading_symbol}: {candle}")
            normalized.append({
                "datetime": candle[0],
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5],
                "open_interest": candle[6],
                "trading_symbol": trading_symbol,
                "instrument_key": expired_key,
                "expiry": expiry_text,
            })

        before = len(normalized)
        dedup_map = {row["datetime"]: row for row in normalized}
        dedup = sorted(dedup_map.values(), key=lambda x: x["datetime"])
        duplicate_count = before - len(dedup)

        if not dedup:
            raise RuntimeError(f"no candles returned for {trading_symbol}")

        contract_path = out / f"UPSTOX_NIFTY_FUT_{expiry.strftime('%Y%m%d')}.csv"
        fields = [
            "datetime", "open", "high", "low", "close", "volume",
            "open_interest", "trading_symbol", "instrument_key", "expiry",
        ]
        with contract_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(dedup)

        manifest.append({
            "provider": "upstox",
            "expiry": expiry_text,
            "trading_symbol": trading_symbol,
            "instrument_key": expired_key,
            "rows": len(dedup),
            "first_timestamp": dedup[0]["datetime"],
            "last_timestamp": dedup[-1]["datetime"],
            "duplicate_count": duplicate_count,
            "pulled_at_utc": datetime.now(timezone.utc).isoformat(),
        })
        combined.extend(dedup)

    combined.sort(key=lambda x: (x["trading_symbol"], x["datetime"]))
    fields = [
        "datetime", "open", "high", "low", "close", "volume",
        "open_interest", "trading_symbol", "instrument_key", "expiry",
    ]
    combined_path = out / "NIFTY_FUT_5m_OCT2025_MAR2026.csv"
    with combined_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(combined)

    manifest_path = out / "UPSTOX_CONTRACT_MANIFEST.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "provider", "expiry", "trading_symbol", "instrument_key", "rows",
            "first_timestamp", "last_timestamp", "duplicate_count", "pulled_at_utc",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(manifest)

    (out / "UPSTOX_CONTRACT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print(f"downloaded {len(manifest)} contracts / {len(combined)} candles")

if __name__ == "__main__":
    main()
