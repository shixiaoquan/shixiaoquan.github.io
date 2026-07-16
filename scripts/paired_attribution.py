#!/usr/bin/env python3
"""同期配对归因 — 生产 vs 影子轨：同标的 + 同市场日级 T+5 对比。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from attribution_lib import load_json

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "paired_attribution.json"


def _day_key(text: str | None) -> str | None:
    if not text:
        return None
    return text[:10]


def _index_records_by_day(records: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for record in records:
        day = _day_key(record.get("recordedAt"))
        if day:
            out[day] = record
    return out


def _lookup_t5(items: dict, record_id: str, symbol: str, *, prefix: str = "") -> float | None:
    key = f"{prefix}{record_id}:{symbol}"
    item = items.get(key)
    if not item:
        return None
    return (item.get("returns") or {}).get("t5")


def _summarize_pairs(pairs: list[dict], *, win_key: str = "shadowWins") -> dict:
    if not pairs:
        return {
            "pairedCount": 0,
            "shadowWinRate": None,
            "avgEdgeT5": None,
            "prodAvgT5": None,
            "shadowAvgT5": None,
        }
    wins = sum(1 for p in pairs if p.get(win_key))
    edges = [p["edgeT5"] for p in pairs]
    return {
        "pairedCount": len(pairs),
        "shadowWinRate": round(wins / len(pairs) * 100, 1),
        "avgEdgeT5": round(sum(edges) / len(edges), 2),
        "prodAvgT5": round(sum(p["prodReturnT5"] for p in pairs) / len(pairs), 2),
        "shadowAvgT5": round(sum(p["shadowReturnT5"] for p in pairs) / len(pairs), 2),
    }


def build_paired_attribution() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    prod_history = load_json(DATA_DIR / "reco_history.json", {"records": []})
    shadow_state = load_json(DATA_DIR / "shadow_reco.json", {})
    prod_attr = load_json(DATA_DIR / "reco_attribution.json", {"items": {}})
    shadow_attr = load_json(DATA_DIR / "shadow_attribution.json", {"items": {}})

    prod_items = prod_attr.get("items") or {}
    shadow_items = shadow_attr.get("items") or {}
    prod_records = prod_history.get("records") or []
    shadow_records = (shadow_state.get("history") or {}).get("records") or []
    shadow_by_day = _index_records_by_day(shadow_records)

    symbol_pairs: list[dict] = []
    market_pairs: list[dict] = []

    for prod_record in prod_records:
        day = _day_key(prod_record.get("recordedAt"))
        if not day:
            continue
        shadow_record = shadow_by_day.get(day)
        if not shadow_record:
            continue

        record_id = prod_record.get("id") or prod_record.get("recordedAt") or ""
        shadow_id = shadow_record.get("id") or shadow_record.get("recordedAt") or ""
        prod_picks = {p.get("symbol"): p for p in prod_record.get("picks") or [] if p.get("symbol")}
        shadow_picks = {p.get("symbol"): p for p in shadow_record.get("picks") or [] if p.get("symbol")}

        for symbol in sorted(set(prod_picks) & set(shadow_picks)):
            prod_t5 = _lookup_t5(prod_items, record_id, symbol)
            shadow_t5 = _lookup_t5(shadow_items, shadow_id, symbol, prefix="shadow:")
            if prod_t5 is None or shadow_t5 is None:
                continue
            edge = round(shadow_t5 - prod_t5, 2)
            symbol_pairs.append(
                {
                    "type": "symbol",
                    "recordedAt": prod_record.get("recordedAt"),
                    "symbol": symbol,
                    "name": prod_picks[symbol].get("name"),
                    "market": prod_picks[symbol].get("market"),
                    "prodReturnT5": prod_t5,
                    "shadowReturnT5": shadow_t5,
                    "edgeT5": edge,
                    "shadowWins": shadow_t5 > prod_t5,
                }
            )

        # 同日同市场：各取最高分 pick 对比（样本更稠密）
        for market in ("A股", "港股", "美股"):
            prod_m = [p for p in prod_picks.values() if p.get("market") == market]
            shadow_m = [p for p in shadow_picks.values() if p.get("market") == market]
            if not prod_m or not shadow_m:
                continue
            prod_top = max(prod_m, key=lambda p: p.get("score") or 0)
            shadow_top = max(shadow_m, key=lambda p: p.get("score") or 0)
            prod_t5 = _lookup_t5(prod_items, record_id, prod_top["symbol"])
            shadow_t5 = _lookup_t5(shadow_items, shadow_id, shadow_top["symbol"], prefix="shadow:")
            if prod_t5 is None or shadow_t5 is None:
                continue
            edge = round(shadow_t5 - prod_t5, 2)
            market_pairs.append(
                {
                    "type": "market",
                    "recordedAt": prod_record.get("recordedAt"),
                    "market": market,
                    "prodSymbol": prod_top["symbol"],
                    "shadowSymbol": shadow_top["symbol"],
                    "prodName": prod_top.get("name"),
                    "shadowName": shadow_top.get("name"),
                    "prodReturnT5": prod_t5,
                    "shadowReturnT5": shadow_t5,
                    "edgeT5": edge,
                    "shadowWins": shadow_t5 > prod_t5,
                }
            )

    symbol_summary = _summarize_pairs(symbol_pairs)
    market_summary = _summarize_pairs(market_pairs)

    # 升级判断优先用同标的；不足时用市场日配对作补充信号
    primary = symbol_summary if symbol_summary["pairedCount"] >= 4 else market_summary
    summary = {
        **symbol_summary,
        "marketPairedCount": market_summary["pairedCount"],
        "marketShadowWinRate": market_summary["shadowWinRate"],
        "marketAvgEdgeT5": market_summary["avgEdgeT5"],
        "effectivePairedCount": primary["pairedCount"],
        "effectiveShadowWinRate": primary["shadowWinRate"],
        "effectiveAvgEdgeT5": primary["avgEdgeT5"],
        "pairMode": "symbol" if symbol_summary["pairedCount"] >= 4 else "market",
    }

    payload = {
        "version": 2,
        "updatedAt": now.isoformat(timespec="seconds"),
        "pairs": symbol_pairs[-80:],
        "marketPairs": market_pairs[-80:],
        "summary": summary,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Paired attribution: symbol={summary['pairedCount']} "
        f"market={summary['marketPairedCount']} · "
        f"mode={summary['pairMode']} win={summary.get('effectiveShadowWinRate')}% "
        f"edge={summary.get('effectiveAvgEdgeT5')}%"
    )
    return payload


if __name__ == "__main__":
    build_paired_attribution()
