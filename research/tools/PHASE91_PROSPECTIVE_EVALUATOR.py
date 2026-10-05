
#!/usr/bin/env python3
"""Phase 91: prospective frozen-signal evaluator.

Reads only October 2026 forward artifacts. No thresholds are selected here.
No signal row is regenerated or edited. Immature signals are excluded from
20-bar movement metrics. Fixed 1.5R/2R/3R outcomes use stop-first ambiguity.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("research/data/forward")
REPORT = Path("research/reports/PHASE91_PROSPECTIVE_EVALUATION.md")
RAW = ROOT / "PHASE87_NIFTY26OCTFUT_5m.csv"
SIGNALS = ROOT / "PHASE87_FROZEN_SIGNALS.csv"
OUTCOMES = ROOT / "PHASE87_SIGNAL_OUTCOMES.csv"
MANIFEST = ROOT / "PHASE87_FORWARD_MANIFEST.csv"
SUMMARY = ROOT / "PHASE91_PROSPECTIVE_SUMMARY.csv"
INTEGRITY = ROOT / "PHASE91_DATA_INTEGRITY.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def fixed_barrier_result(path: pd.DataFrame, entry: float, risk: float, direction: int, target_r: float):
    if path.empty:
        return np.nan, None
    target = entry + direction * target_r * risk
    stop = entry - direction * risk
    for j, (_, b) in enumerate(path.iterrows(), start=1):
        fav_hit = b["high"] >= target if direction == 1 else b["low"] <= target
        stop_hit = b["low"] <= stop if direction == 1 else b["high"] >= stop
        if stop_hit:
            return -1.0, None
        if fav_hit:
            return target_r, j
    close = float(path.iloc[-1]["close"])
    return direction * (close - entry) / risk, None


def build_paths(raw: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    if raw.empty or signals.empty:
        return pd.DataFrame()
    x = raw.copy()
    x["datetime"] = pd.to_datetime(x["datetime"], utc=True)
    x = x.sort_values("datetime").reset_index(drop=True)

    s = signals.copy()
    s["signal_timestamp"] = pd.to_datetime(s["signal_timestamp"], utc=True)

    out = []
    for _, row in s.iterrows():
        ts = row["signal_timestamp"]
        day = ts.date()
        future = x[(x["datetime"] > ts) & (x["datetime"].dt.date == day)].head(20)
        if future.empty:
            continue

        entry = float(future.iloc[0]["open"])
        risk = float(row["atr14"])
        direction = int(row["direction"])

        fav = ((future["high"] - entry) if direction == 1 else (entry - future["low"])) / risk
        adv = ((entry - future["low"]) if direction == 1 else (future["high"] - entry)) / risk

        rec = {
            "signal_timestamp": ts.isoformat(),
            "trading_symbol": str(row["trading_symbol"]),
            "direction": direction,
            "h_m1": bool(row["h_m1"]),
            "h_m6": bool(row["h_m6"]),
            "h_m9": bool(row["h_m9"]),
            "h_m14": bool(row["h_m14"]),
            "bars_available": len(future),
            "mature20": len(future) >= 20,
            "entry": entry,
            "atr14": risk,
            "mfe20": float(fav.max()),
            "mae20": float(adv.max()),
            "ret20atr": np.nan,
        }

        if len(future) >= 20:
            rec["ret20atr"] = direction * (float(future.iloc[19]["close"]) - entry) / risk

        for target_r, prefix in [(1.5, "r1_5"), (2.0, "r2"), (3.0, "r3")]:
            value, first_bar = fixed_barrier_result(future, entry, risk, direction, target_r)
            rec[prefix] = value
            rec[prefix + "_first"] = first_bar is not None
            rec[prefix + "_first_bar"] = first_bar

        out.append(rec)

    return pd.DataFrame(out)


def integrity_checks(raw: pd.DataFrame, signals: pd.DataFrame, outcomes: pd.DataFrame) -> pd.DataFrame:
    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    if raw.empty:
        add("raw_present", "FAIL", "Forward raw archive missing or empty.")
        return pd.DataFrame(checks)

    dt = pd.to_datetime(raw["datetime"], utc=True, errors="coerce")
    bad = int(dt.isna().sum())
    add("raw_timestamp_parse", "PASS" if bad == 0 else "FAIL", f"invalid_timestamps={bad}")

    local = dt.dt.tz_convert("Asia/Kolkata")
    regular = (local.dt.time >= pd.Timestamp("09:15:00").time()) & (local.dt.time <= pd.Timestamp("15:29:59").time())
    add("regular_session_only", "PASS" if bool(regular.all()) else "FAIL",
        f"rows_outside_session={int((~regular).sum())}")

    dup = int(dt.duplicated().sum())
    add("raw_duplicate_timestamps", "PASS" if dup == 0 else "FAIL", f"duplicates={dup}")

    bad_ohlc = (
        (raw["high"] < raw[["open", "close", "low"]].max(axis=1))
        | (raw["low"] > raw[["open", "close", "high"]].min(axis=1))
        | (raw["high"] < raw["low"])
    )
    add("ohlc_integrity", "PASS" if not bool(bad_ohlc.any()) else "FAIL",
        f"bad_rows={int(bad_ohlc.sum())}")

    if not dt.dropna().empty:
        now = pd.Timestamp.now(tz="UTC")
        ahead = dt.max() > now + pd.Timedelta(minutes=10)
        add("no_future_bars", "PASS" if not ahead else "FAIL",
            f"max_timestamp={dt.max().isoformat()} now={now.isoformat()}")

    if signals.empty:
        add("frozen_signal_file", "PASS", "No prospective signals recorded.")
    else:
        keys = signals["signal_timestamp"].astype(str) + "|" + signals["trading_symbol"].astype(str)
        dup_sig = int(keys.duplicated().sum())
        add("signal_key_uniqueness", "PASS" if dup_sig == 0 else "FAIL",
            f"duplicate_signal_keys={dup_sig}")

        req = ["signal_timestamp", "trading_symbol", "direction", "atr14",
               "h_m1", "h_m6", "h_m9", "h_m14"]
        missing = [c for c in req if c not in signals.columns]
        add("signal_schema", "PASS" if not missing else "FAIL", f"missing={missing}")

    if outcomes.empty:
        add("outcome_file", "PASS", "No mature outcomes recorded.")
    else:
        keys = outcomes["signal_timestamp"].astype(str) + "|" + outcomes["trading_symbol"].astype(str)
        dup_out = int(keys.duplicated().sum())
        add("outcome_key_uniqueness", "PASS" if dup_out == 0 else "FAIL",
            f"duplicate_outcome_keys={dup_out}")

    return pd.DataFrame(checks)


def fmt(x):
    return "" if pd.isna(x) else f"{float(x):+.3f}"


def pct(x):
    return "" if pd.isna(x) else f"{100.0 * float(x):.1f}%"


def main():
    raw = read_csv(RAW)
    signals = read_csv(SIGNALS)
    outcomes = read_csv(OUTCOMES)
    manifest = read_csv(MANIFEST)

    integrity = integrity_checks(raw, signals, outcomes)
    INTEGRITY.parent.mkdir(parents=True, exist_ok=True)
    integrity.to_csv(INTEGRITY, index=False)

    paths = build_paths(raw, signals)

    rows = []
    for label in ["H-M1", "H-M6", "H-M9", "H-M14"]:
        if paths.empty:
            g = paths
        else:
            mask = paths[label.lower().replace("-", "_")] if False else None
            col = {"H-M1": "h_m1", "H-M6": "h_m6", "H-M9": "h_m9", "H-M14": "h_m14"}[label]
            g = paths[paths[col].astype(bool)]

        rows.append({
            "hypothesis": label,
            "signal_count": int(len(g)),
            "mature_20bar_count": int(g["mature20"].sum()) if not g.empty else 0,
            "mean_ret20_atr": float(g["ret20atr"].mean()) if not g.empty else np.nan,
            "median_ret20_atr": float(g["ret20atr"].median()) if not g.empty else np.nan,
            "positive_ret20_share": float((g["ret20atr"] > 0).mean()) if not g.empty else np.nan,
            "mean_mfe20_atr": float(g["mfe20"].mean()) if not g.empty else np.nan,
            "mean_mae20_atr": float(g["mae20"].mean()) if not g.empty else np.nan,
            "mean_R2_fixed": float(g["r2"].mean()) if not g.empty else np.nan,
            "R2_target_first_share": float(g["r2_first"].mean()) if not g.empty else np.nan,
            "mean_R3_fixed": float(g["r3"].mean()) if not g.empty else np.nan,
            "R3_target_first_share": float(g["r3_first"].mean()) if not g.empty else np.nan,
        })

    summary = pd.DataFrame(rows)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY, index=False)

    raw_sha = sha256(RAW) if RAW.exists() else "MISSING"
    signal_sha = sha256(SIGNALS) if SIGNALS.exists() else "MISSING"
    outcome_sha = sha256(OUTCOMES) if OUTCOMES.exists() else "MISSING"

    manifest_note = "No manifest."
    if not manifest.empty:
        m = manifest.iloc[0]
        manifest_note = (
            f"Rows={m.get('rows', '?')}, last_timestamp={m.get('last_timestamp', '?')}, "
            f"signals={m.get('signal_rows_total', '?')}, outcomes={m.get('outcome_rows_total', '?')}."
        )

    lines = [
        "# Phase 91 — Prospective Frozen-Signal Evaluation",
        f"Date: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Purpose",
        "Evaluate only frozen forward signals using predeclared endpoints. No October outcome is used to modify any signal.",
        "",
        "## Forward state",
        manifest_note,
        f"Raw SHA-256: {raw_sha}",
        f"Signal-file SHA-256: {signal_sha}",
        f"Outcome-file SHA-256: {outcome_sha}",
        "",
        "## Integrity",
        "See research/data/forward/PHASE91_DATA_INTEGRITY.csv.",
        "",
        "## Results",
        "| Hypothesis | Signals | Mature 20-bar | Mean ret20 ATR | Mean R2 | 2R first | Mean R3 | 3R first |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for _, r in summary.iterrows():
        lines.append(
            "| {hyp} | {n} | {m} | {ret} | {r2} | {tf2} | {r3} | {tf3} |".format(
                hyp=r["hypothesis"],
                n=int(r["signal_count"]),
                m=int(r["mature_20bar_count"]),
                ret=fmt(r["mean_ret20_atr"]),
                r2=fmt(r["mean_R2_fixed"]),
                tf2=pct(r["R2_target_first_share"]),
                r3=fmt(r["mean_R3_fixed"]),
                tf3=pct(r["R3_target_first_share"]),
            )
        )

    lines += [
        "",
        "## Governance",
        "- H-M1, H-M6, H-M9 and H-M14 definitions are unchanged.",
        "- Immature signals are excluded from 20-bar movement metrics.",
        "- Fixed-risk target/stop outcomes use stop-first ambiguity.",
        "- H-M14 remains future-only and is not evaluated against the already-seen January external holdout.",
        "- No target, stop, horizon, threshold, or filter is selected from October outcomes.",
        "- A prospective result is not called validated without adequate unseen sample size, clustering adjustment, and cost robustness.",
    ]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
