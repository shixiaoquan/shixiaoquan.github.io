#!/usr/bin/env python3
"""荐股归因共享逻辑 — 生产轨与影子轨复用。"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf

HORIZONS = (1, 5, 20)
MAX_NEW_PER_RUN = 40
MIN_AGE_DAYS = 6


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def parse_dt(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def price_on_or_after(hist, start_dt: datetime) -> float | None:
    if hist is None or hist.empty:
        return None
    start = start_dt.date()
    for idx, row in hist.iterrows():
        if idx.date() >= start:
            return float(row["Close"])
    return None


def return_pct(entry: float, exit_price: float | None) -> float | None:
    if not entry or exit_price is None:
        return None
    return round((exit_price - entry) / entry * 100, 2)


def decision_label(pick: dict) -> str | None:
    label = pick.get("decisionLabel")
    if label in ("高", "中", "低"):
        return label
    score = pick.get("decisionScore")
    if score is None:
        return None
    if score >= 70:
        return "高"
    if score >= 50:
        return "中"
    return "低"


def pick_key(record_id: str, symbol: str, *, prefix: str = "") -> str:
    base = f"{record_id}:{symbol}"
    return f"{prefix}{base}" if prefix else base


def run_track_attribution(
    records: list[dict],
    existing_items: dict,
    *,
    key_prefix: str = "",
    max_new: int = MAX_NEW_PER_RUN,
    min_age_days: int = MIN_AGE_DAYS,
    now: datetime | None = None,
) -> tuple[dict, int]:
    """对历史记录做 T+N 归因，返回 (items, new_count)。"""
    now = now or datetime.now(timezone.utc).astimezone()
    items: dict = dict(existing_items or {})
    new_count = 0
    symbol_cache: dict[str, object] = {}

    for record in sorted(records, key=lambda r: r.get("recordedAt") or ""):
        if new_count >= max_new:
            break
        recorded_at = parse_dt(record.get("recordedAt") or "")
        if not recorded_at or (now - recorded_at) < timedelta(days=min_age_days):
            continue
        record_id = record.get("id") or record.get("recordedAt") or ""
        for pick in record.get("picks") or []:
            if new_count >= max_new:
                break
            symbol = pick.get("symbol")
            entry_price = pick.get("price")
            if not symbol or not entry_price:
                continue
            key = pick_key(record_id, symbol, prefix=key_prefix)
            if key in items:
                continue

            if symbol not in symbol_cache:
                try:
                    symbol_cache[symbol] = yf.Ticker(symbol).history(period="6mo", interval="1d")
                except Exception:
                    symbol_cache[symbol] = None
            hist = symbol_cache[symbol]

            horizons: dict[str, float | None] = {}
            for days in HORIZONS:
                target_dt = recorded_at + timedelta(days=days)
                if target_dt > now:
                    horizons[f"t{days}"] = None
                    continue
                exit_px = price_on_or_after(hist, target_dt)
                horizons[f"t{days}"] = return_pct(float(entry_price), exit_px)

            if all(v is None for v in horizons.values()):
                continue

            items[key] = {
                "recordId": record_id,
                "recordedAt": record.get("recordedAt"),
                "symbol": symbol,
                "name": pick.get("name"),
                "market": pick.get("market"),
                "signal": pick.get("signal"),
                "entryPrice": entry_price,
                "score": pick.get("score"),
                "decisionScore": pick.get("decisionScore"),
                "decisionLabel": decision_label(pick),
                "marketRegime": (record.get("marketContext") or {}).get("regime"),
                "marketMood": (record.get("marketContext") or {}).get("mood"),
                "returns": horizons,
            }
            new_count += 1

    return items, new_count


def backfill_decision_labels(
    items: dict,
    records: list[dict],
    *,
    key_prefix: str = "",
    score_missing=None,
) -> None:
    """用历史 picks 回填既有归因项的 decisionScore / decisionLabel。"""
    pick_map: dict[str, dict] = {}
    for record in records:
        record_id = record.get("id") or record.get("recordedAt") or ""
        for pick in record.get("picks") or []:
            symbol = pick.get("symbol")
            if symbol:
                pick_map[pick_key(record_id, symbol)] = pick

    for key, item in items.items():
        if item.get("decisionLabel") and item.get("decisionLabel") != "未知":
            continue
        plain_key = key[len(key_prefix) :] if key_prefix and key.startswith(key_prefix) else key
        pick = pick_map.get(plain_key)
        if not pick:
            continue
        if pick.get("decisionScore") is None and callable(score_missing):
            pick = score_missing(pick)
        item["decisionScore"] = pick.get("decisionScore")
        item["decisionLabel"] = decision_label(pick)


def summarize_items(items: dict) -> dict:
    matured = [v for v in items.values() if v.get("returns", {}).get("t5") is not None]
    by_signal: dict[str, list[float]] = {}
    by_market: dict[str, list[float]] = {}
    by_decision: dict[str, list[float]] = {}
    by_regime: dict[str, list[float]] = {}

    for item in matured:
        ret = item["returns"]["t5"]
        sig = item.get("signal") or "unknown"
        mkt = item.get("market") or "unknown"
        dec = item.get("decisionLabel") or "未知"
        regime = item.get("marketRegime") or "unknown"
        by_signal.setdefault(sig, []).append(ret)
        by_market.setdefault(mkt, []).append(ret)
        by_decision.setdefault(dec, []).append(ret)
        by_regime.setdefault(regime, []).append(ret)

    def _avg(vals: list[float]) -> float | None:
        return round(sum(vals) / len(vals), 2) if vals else None

    def _bucket(vals: list[float]) -> dict:
        if not vals:
            return {"avgT5": None, "count": 0, "winRate": None}
        return {
            "avgT5": _avg(vals),
            "count": len(vals),
            "winRate": round(sum(1 for x in vals if x > 0) / len(vals) * 100, 1),
        }

    return {
        "totalTracked": len(items),
        "maturedT5": len(matured),
        "avgReturnT5": _avg([x["returns"]["t5"] for x in matured]),
        "winRateT5": round(sum(1 for x in matured if x["returns"]["t5"] > 0) / len(matured) * 100, 1)
        if matured
        else None,
        "bySignal": {k: _bucket(v) for k, v in by_signal.items()},
        "byMarket": {k: _bucket(v) for k, v in by_market.items()},
        "byDecisionLabel": {k: _bucket(v) for k, v in by_decision.items()},
        "byRegime": {k: _bucket(v) for k, v in by_regime.items()},
    }
