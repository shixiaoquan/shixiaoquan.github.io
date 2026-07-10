#!/usr/bin/env python3
"""影子荐股轨 — 用 strategy_candidates 候选参数并行记账，周度与生产对比。"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import strategy_scoring as sc
from decision_score import enrich_picks, load_context_files
from fetch_data import (
    CANDIDATES,
    MARKETS,
    RECO_PICK_STICKY_HOURS,
    WATCH_SCORE,
    analyze_candidate,
    compact_pick,
    fetch_benchmark_closes,
    picks_fingerprint,
)
from strategy_config import BREAKOUT_SCORE_MIN, BUY_SCORE, STRATEGY_VERSION

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "shadow_reco.json"
CANDIDATES_FILE = DATA_DIR / "strategy_candidates.json"
PROD_HISTORY = DATA_DIR / "reco_history.json"
MAX_SHADOW_RECORDS = 80

SHADOW_RELAX = {
    "REQUIRE_BREAKOUT_FOR_BUY": False,
    "REQUIRE_BULL_MARKET": False,
    "REQUIRE_BENCH_ABOVE_MA200": False,
    "REQUIRE_MACD_POSITIVE": False,
    "MIN_RELATIVE_STRENGTH": 0.0,
}


def _load(path: Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _candidate_params() -> dict:
    data = _load(CANDIDATES_FILE, {}) or {}
    best = data.get("bestCandidate") or {}
    if best.get("buyScore") is not None:
        return {
            "buyScore": int(best["buyScore"]),
            "breakoutScoreMin": int(best.get("breakoutScoreMin") or BREAKOUT_SCORE_MIN),
            "source": "strategy_candidates.bestCandidate",
        }
    return {
        "buyScore": max(BUY_SCORE - 6, 68),
        "breakoutScoreMin": max(BREAKOUT_SCORE_MIN - 6, 62),
        "source": "default_shadow_offset",
    }


def build_shadow_picks(now: datetime, params: dict) -> list[dict]:
    patches = {
        "BUY_SCORE": params["buyScore"],
        "BREAKOUT_SCORE_MIN": params["breakoutScoreMin"],
        **SHADOW_RELAX,
    }
    benchmarks = fetch_benchmark_closes()
    analyzed = []
    with patch.multiple(sc, **patches):
        for symbol, meta in CANDIDATES.items():
            result = analyze_candidate(symbol, meta, benchmarks)
            if result:
                analyzed.append(result)

    picks: list[dict] = []
    for market in MARKETS:
        pool = [a for a in analyzed if a["market"] == market and a["signal"] in ("buy", "watch")]
        pool.sort(key=lambda x: x["score"], reverse=True)
        if pool:
            picks.append(pool[0])
        else:
            fallback = sorted([a for a in analyzed if a["market"] == market], key=lambda x: -x["score"])
            if fallback and fallback[0]["score"] >= 40:
                top = fallback[0].copy()
                top["signal"] = "watch"
                top["signalLabel"] = "影子弱信号"
                picks.append(top)
    picks.sort(key=lambda x: (0 if x["signal"] == "buy" else 1, -x["score"]))
    return picks[: len(MARKETS)]


def _append_shadow_history(state: dict, picks: list[dict], recorded_at: datetime) -> None:
    records = state.setdefault("history", {}).get("records", [])
    if not isinstance(state.get("history"), dict):
        state["history"] = {"records": []}
        records = state["history"]["records"]

    fp = picks_fingerprint(picks)
    if records and picks_fingerprint(records[-1].get("picks", [])) == fp:
        return
    records.append(
        {
            "id": recorded_at.isoformat(timespec="seconds"),
            "recordedAt": recorded_at.isoformat(timespec="seconds"),
            "picks": [compact_pick(p) for p in picks],
        }
    )
    state["history"]["records"] = records[-MAX_SHADOW_RECORDS:]


def compare_tracks() -> dict:
    """对比生产 vs 影子历史记录数量与近期重叠度。"""
    prod = _load(PROD_HISTORY, {"records": []}) or {"records": []}
    shadow = _load(OUTPUT, {}) or {}
    shadow_records = (shadow.get("history") or {}).get("records") or []
    prod_records = prod.get("records") or []

    overlap = 0
    pairs = min(len(prod_records), len(shadow_records), 20)
    for i in range(1, pairs + 1):
        pr = prod_records[-i]
        sr = shadow_records[-i]
        ps = {p.get("symbol") for p in pr.get("picks") or []}
        ss = {p.get("symbol") for p in sr.get("picks") or []}
        if ps & ss:
            overlap += 1

    attr = _load(DATA_DIR / "reco_attribution.json", {}) or {}
    summary = attr.get("summary") or {}
    shadow_weeks = len(shadow_records) // max(1, len(MARKETS))
    prod_matured = summary.get("maturedT5") or 0
    shadow_wins = False
    reason = "影子轨积累中"
    if shadow_weeks >= 4 and prod_matured >= 10:
        # 待 shadow_attribution 成熟后细化；暂用探索回测期望作参考
        cand = _load(CANDIDATES_FILE, {}) or {}
        explore = (cand.get("current") or {}).get("exploration") or {}
        prod_exp = explore.get("expectancy", 0)  # placeholder until dual attribution
        best_exp = (cand.get("bestCandidate") or {}).get("expectancy", 0)
        if best_exp > prod_exp + 0.5:
            shadow_wins = True
            reason = f"影子候选期望 {best_exp}% 优于探索基准 {prod_exp}%（满 4 周可提 PR）"

    return {
        "prodRecords": len(prod_records),
        "shadowRecords": len(shadow_records),
        "shadowWeeks": shadow_weeks,
        "symbolOverlapRecent": overlap,
        "shadowWins": shadow_wins,
        "reason": reason,
        "readyForUpgradePR": shadow_wins and shadow_weeks >= 4,
    }


def run_shadow_update() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    params = _candidate_params()
    picks = build_shadow_picks(now, params)
    ctx = load_context_files()
    market = _load(DATA_DIR / "market_core.json") or _load(DATA_DIR / "market.json") or {}
    masters = _load(DATA_DIR / "market_reco.json") or market
    master_reco = masters.get("masterRecommendations")
    picks = enrich_picks(picks, market.get("summary"), master_reco, ctx)

    state = _load(OUTPUT, {}) or {}
    state["updatedAt"] = now.isoformat(timespec="seconds")
    state["track"] = "shadow"
    state["productionVersion"] = STRATEGY_VERSION
    state["candidateParams"] = params
    state["recommendations"] = {
        "strategy": f"影子轨 buy≥{params['buyScore']} breakout≥{params['breakoutScoreMin']}（候选参数，非生产）",
        "picks": picks,
        "disclaimer": "影子荐股仅供 forward 验证，不可直接跟单。",
    }
    _append_shadow_history(state, picks, now)
    state["comparison"] = compare_tracks()
    OUTPUT.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Shadow reco: {len(picks)} picks · records {len(state['history']['records'])} · {state['comparison']['reason']}")
    return state


if __name__ == "__main__":
    run_shadow_update()
