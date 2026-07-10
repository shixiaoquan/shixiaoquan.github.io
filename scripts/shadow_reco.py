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
from market_regime import detect_market_regime
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


def _append_shadow_history(state: dict, picks: list[dict], recorded_at: datetime, *, market_context: dict | None = None) -> None:
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
            "marketContext": market_context or {},
            "picks": [compact_pick(p) for p in picks],
        }
    )
    state["history"]["records"] = records[-MAX_SHADOW_RECORDS:]


def compare_tracks() -> dict:
    """对比生产 vs 影子历史记录与 T+5 归因。"""
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

    prod_attr = _load(DATA_DIR / "reco_attribution.json", {}) or {}
    shadow_attr = _load(DATA_DIR / "shadow_attribution.json", {}) or {}
    prod_summary = prod_attr.get("summary") or {}
    shadow_summary = shadow_attr.get("summary") or {}

    shadow_weeks = len(shadow_records) // max(1, len(MARKETS))
    prod_matured = prod_summary.get("maturedT5") or 0
    shadow_matured = shadow_summary.get("maturedT5") or 0
    prod_win = prod_summary.get("winRateT5")
    prod_avg = prod_summary.get("avgReturnT5")
    shadow_win = shadow_summary.get("winRateT5")
    shadow_avg = shadow_summary.get("avgReturnT5")

    shadow_wins = False
    reason = "影子轨积累中"
    if shadow_matured > 0 and shadow_win is not None:
        reason = (
            f"影子 T+5 {shadow_win}%/{shadow_avg}% "
            f"vs 生产 {prod_win}%/{prod_avg}% · {shadow_matured} 笔成熟"
        )
    elif shadow_weeks >= 1:
        reason = f"影子轨第 {shadow_weeks} 周 · 归因样本积累中"

    min_shadow_samples = 8
    paired = _load(DATA_DIR / "paired_attribution.json", {}) or {}
    paired_summary = paired.get("summary") or {}
    paired_count = paired_summary.get("pairedCount") or 0
    paired_win = paired_summary.get("shadowWinRate")
    paired_edge = paired_summary.get("avgEdgeT5")

    if paired_count >= 6 and paired_win is not None:
        reason = (
            f"配对归因 {paired_count} 对 · 影子胜率 {paired_win}% · "
            f"均边际 {paired_edge}%"
        )

    if (
        shadow_weeks >= 4
        and paired_count >= 6
        and paired_win is not None
        and paired_edge is not None
    ):
        if paired_win >= 55 and paired_edge >= 0.5:
            shadow_wins = True
            reason = (
                f"配对归因 {paired_count} 对：影子胜率 {paired_win}%，"
                f"均边际 +{paired_edge}% — 可申请升级 PR"
            )
    elif (
        shadow_weeks >= 4
        and shadow_matured >= min_shadow_samples
        and prod_matured >= min_shadow_samples
        and shadow_win is not None
        and prod_win is not None
        and shadow_avg is not None
        and prod_avg is not None
    ):
        win_edge = shadow_win - prod_win
        avg_edge = shadow_avg - prod_avg
        if win_edge >= 3 and avg_edge >= -0.3:
            shadow_wins = True
            reason = (
                f"影子 T+5 胜率 {shadow_win}% vs 生产 {prod_win}%（+{win_edge:.1f}），"
                f"均收益 {shadow_avg}% vs {prod_avg}% — 可申请升级 PR"
            )

    return {
        "prodRecords": len(prod_records),
        "shadowRecords": len(shadow_records),
        "shadowWeeks": shadow_weeks,
        "symbolOverlapRecent": overlap,
        "prodMaturedT5": prod_matured,
        "shadowMaturedT5": shadow_matured,
        "prodWinRateT5": prod_win,
        "prodAvgReturnT5": prod_avg,
        "shadowWinRateT5": shadow_win,
        "shadowAvgReturnT5": shadow_avg,
        "pairedCount": paired_count,
        "pairedShadowWinRate": paired_win,
        "pairedAvgEdgeT5": paired_edge,
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
    _append_shadow_history(
        state,
        picks,
        now,
        market_context={
            "mood": market.get("summary", {}).get("mood"),
            "regime": detect_market_regime(
                market.get("summary"),
                (ctx.get("macro") or {}).get("summary"),
            ),
        },
    )
    state["comparison"] = compare_tracks()
    OUTPUT.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Shadow reco: {len(picks)} picks · records {len(state['history']['records'])} · {state['comparison']['reason']}")
    return state


if __name__ == "__main__":
    run_shadow_update()
