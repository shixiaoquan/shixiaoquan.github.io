#!/usr/bin/env python3
"""影子荐股轨 T+N 归因 — 独立于生产轨的 forward 验证。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from attribution_lib import backfill_decision_labels, load_json, run_track_attribution, summarize_items
from decision_score import load_context_files, score_pick
from evolution_log import append_event

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SHADOW_FILE = DATA_DIR / "shadow_reco.json"
OUTPUT_FILE = DATA_DIR / "shadow_attribution.json"
KEY_PREFIX = "shadow:"


def _retro_score_pick(pick: dict) -> dict:
    ctx = load_context_files()
    market = load_json(DATA_DIR / "market_core.json", {}) or load_json(DATA_DIR / "market.json", {}) or {}
    masters = load_json(DATA_DIR / "market_reco.json", {}) or market
    scored = score_pick(
        pick,
        market_summary=market.get("summary"),
        macro=ctx.get("macro"),
        wencai=ctx.get("wencai"),
        master_reco=masters.get("masterRecommendations"),
        truth=ctx.get("truth"),
    )
    return {**pick, **scored}


def run_shadow_attribution() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    shadow = load_json(SHADOW_FILE, {})
    state = load_json(OUTPUT_FILE, {"version": 1, "items": {}, "summary": {}})
    records = (shadow.get("history") or {}).get("records") or []

    items, new_count = run_track_attribution(
        records,
        dict(state.get("items") or {}),
        key_prefix=KEY_PREFIX,
        now=now,
    )
    backfill_decision_labels(items, records, key_prefix=KEY_PREFIX, score_missing=_retro_score_pick)
    summary = summarize_items(items)

    payload = {
        "version": 1,
        "track": "shadow",
        "updatedAt": now.isoformat(timespec="seconds"),
        "candidateParams": shadow.get("candidateParams"),
        "items": items,
        "summary": summary,
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if new_count:
        append_event(
            "shadow_attribution",
            {
                "newItems": new_count,
                "avgReturnT5": summary.get("avgReturnT5"),
                "winRateT5": summary.get("winRateT5"),
            },
        )
        print(
            f"Shadow attribution: +{new_count} items, "
            f"T+5 win={summary.get('winRateT5')}% avg={summary.get('avgReturnT5')}%"
        )
    else:
        print(f"Shadow attribution: no new items ({len(items)} tracked)")
    return payload


if __name__ == "__main__":
    run_shadow_attribution()
