#!/usr/bin/env python3
"""荐股 T+N 收益归因 — 用已有 reco_history + yfinance，无额外 API。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from attribution_lib import (
    backfill_decision_labels,
    backfill_market_context,
    load_json,
    run_track_attribution,
    summarize_items,
)
from decision_score import load_context_files, score_pick
from evolution_log import append_event

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
HISTORY_FILE = DATA_DIR / "reco_history.json"
OUTPUT_FILE = DATA_DIR / "reco_attribution.json"


def _retro_score_pick(pick: dict) -> dict:
    """历史荐股无 decisionScore 时，用当前宏观上下文近似回填。"""
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


def run_attribution() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    history = load_json(HISTORY_FILE, {"records": []})
    state = load_json(OUTPUT_FILE, {"version": 1, "items": {}, "summary": {}})
    items, new_count = run_track_attribution(
        history.get("records") or [],
        dict(state.get("items") or {}),
        now=now,
    )
    records = history.get("records") or []
    backfill_decision_labels(items, records, score_missing=_retro_score_pick)
    backfill_market_context(items, records)
    summary = summarize_items(items)

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
