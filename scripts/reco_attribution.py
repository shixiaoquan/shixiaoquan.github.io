#!/usr/bin/env python3
"""荐股 T+N 收益归因 — 用已有 reco_history + yfinance，无额外 API。"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf

from evolution_log import append_event

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
HISTORY_FILE = DATA_DIR / "reco_history.json"
OUTPUT_FILE = DATA_DIR / "reco_attribution.json"

HORIZONS = (1, 5, 20)
MAX_NEW_PER_RUN = 40
MIN_AGE_DAYS = 6


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _parse_dt(text: str) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _price_on_or_after(hist, start_dt: datetime) -> float | None:
    if hist is None or hist.empty:
        return None
    start = start_dt.date()
    for idx, row in hist.iterrows():
        if idx.date() >= start:
            return float(row["Close"])
    return None


def _return_pct(entry: float, exit_price: float | None) -> float | None:
    if not entry or exit_price is None:
        return None
    return round((exit_price - entry) / entry * 100, 2)


def _pick_key(record_id: str, symbol: str) -> str:
    return f"{record_id}:{symbol}"


def run_attribution() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    history = _load_json(HISTORY_FILE, {"records": []})
    state = _load_json(OUTPUT_FILE, {"version": 1, "items": {}, "summary": {}})
    items: dict = dict(state.get("items") or {})
    new_count = 0

    records = sorted(history.get("records") or [], key=lambda r: r.get("recordedAt") or "")
    symbol_cache: dict[str, object] = {}

    for record in records:
        if new_count >= MAX_NEW_PER_RUN:
            break
        recorded_at = _parse_dt(record.get("recordedAt") or "")
        if not recorded_at or (now - recorded_at) < timedelta(days=MIN_AGE_DAYS):
            continue
        record_id = record.get("id") or record.get("recordedAt") or ""
        for pick in record.get("picks") or []:
            if new_count >= MAX_NEW_PER_RUN:
                break
            symbol = pick.get("symbol")
            entry_price = pick.get("price")
            if not symbol or not entry_price:
                continue
            key = _pick_key(record_id, symbol)
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
                exit_px = _price_on_or_after(hist, target_dt)
                horizons[f"t{days}"] = _return_pct(float(entry_price), exit_px)

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
                "returns": horizons,
            }
            new_count += 1

    # 汇总
    matured = [v for v in items.values() if v.get("returns", {}).get("t5") is not None]
    by_signal: dict[str, list[float]] = {}
    by_market: dict[str, list[float]] = {}
    for item in matured:
        ret = item["returns"]["t5"]
        sig = item.get("signal") or "unknown"
        mkt = item.get("market") or "unknown"
        by_signal.setdefault(sig, []).append(ret)
        by_market.setdefault(mkt, []).append(ret)

    def _avg(vals: list[float]) -> float | None:
        return round(sum(vals) / len(vals), 2) if vals else None

    summary = {
        "totalTracked": len(items),
        "maturedT5": len(matured),
        "avgReturnT5": _avg([x["returns"]["t5"] for x in matured]),
        "winRateT5": round(sum(1 for x in matured if x["returns"]["t5"] > 0) / len(matured) * 100, 1)
        if matured
        else None,
        "bySignal": {k: {"avgT5": _avg(v), "count": len(v)} for k, v in by_signal.items()},
        "byMarket": {k: {"avgT5": _avg(v), "count": len(v)} for k, v in by_market.items()},
    }

    payload = {
        "version": 1,
        "updatedAt": now.isoformat(timespec="seconds"),
        "items": items,
        "summary": summary,
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if new_count:
        append_event(
            "reco_attribution",
            {
                "newItems": new_count,
                "avgReturnT5": summary.get("avgReturnT5"),
                "winRateT5": summary.get("winRateT5"),
            },
        )
        print(f"Attribution: +{new_count} items, T+5 avg={summary.get('avgReturnT5')}%")
    else:
        print(f"Attribution: no new items ({len(items)} tracked)")
    return payload


if __name__ == "__main__":
    run_attribution()
