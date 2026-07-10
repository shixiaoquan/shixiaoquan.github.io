#!/usr/bin/env python3
"""同期配对归因 — 生产 vs 影子轨在同一时点、同一标的上的 T+5 对比。"""

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

    pairs: list[dict] = []
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
            prod_key = f"{record_id}:{symbol}"
            shadow_key = f"shadow:{shadow_id}:{symbol}"
            prod_item = prod_items.get(prod_key)
            shadow_item = shadow_items.get(shadow_key)
            if not prod_item or not shadow_item:
                continue
            prod_t5 = (prod_item.get("returns") or {}).get("t5")
            shadow_t5 = (shadow_item.get("returns") or {}).get("t5")
            if prod_t5 is None or shadow_t5 is None:
                continue
            edge = round(shadow_t5 - prod_t5, 2)
            pairs.append(
                {
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

    matured = pairs
    shadow_wins = sum(1 for p in matured if p["shadowWins"])
    edges = [p["edgeT5"] for p in matured]
    summary = {
        "pairedCount": len(matured),
        "shadowWinRate": round(shadow_wins / len(matured) * 100, 1) if matured else None,
        "avgEdgeT5": round(sum(edges) / len(edges), 2) if edges else None,
        "prodAvgT5": round(sum(p["prodReturnT5"] for p in matured) / len(matured), 2) if matured else None,
        "shadowAvgT5": round(sum(p["shadowReturnT5"] for p in matured) / len(matured), 2) if matured else None,
    }

    payload = {
        "version": 1,
        "updatedAt": now.isoformat(timespec="seconds"),
        "pairs": pairs[-120:],
        "summary": summary,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Paired attribution: {summary['pairedCount']} pairs · "
        f"shadow win={summary.get('shadowWinRate')}% edge={summary.get('avgEdgeT5')}%"
    )
    return payload


if __name__ == "__main__":
    build_paired_attribution()
