#!/usr/bin/env python3
"""战术策略参数轻量网格搜索 — 复用 backtest 逻辑，产出候选供 Cursor 开 PR。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import strategy_scoring as sc
from backtest import BACKTEST_UNIVERSE, MARKET_MAP, compute_metrics, load_benchmark_series, simulate_symbol
from evolution_log import append_event
from strategy_config import BREAKOUT_SCORE_MIN, BUY_SCORE, STRATEGY_VERSION

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "strategy_candidates.json"

BUY_GRID = (72, 75, 78, 80)
BREAKOUT_GRID = (68, 72, 75)


def _run_combo(buy_score: int, breakout_min: int) -> dict:
    with patch.object(sc, "BUY_SCORE", buy_score), patch.object(sc, "BREAKOUT_SCORE_MIN", breakout_min):
        bench = load_benchmark_series("1y")
        trades = []
        for symbol in BACKTEST_UNIVERSE:
            market = MARKET_MAP.get(symbol, "美股")
            trades.extend(simulate_symbol(symbol, bench.get(market, {})))
    metrics = compute_metrics(trades)
    return {
        "buyScore": buy_score,
        "breakoutScoreMin": breakout_min,
        "metrics": metrics,
        "totalTrades": metrics.get("totalTrades", 0),
        "winRate": metrics.get("winRate", 0),
        "expectancy": metrics.get("expectancy", 0),
        "profitFactor": metrics.get("profitFactor", 0),
    }


def run_sweep() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    current = _run_combo(BUY_SCORE, BREAKOUT_SCORE_MIN)
    candidates = []
    for buy in BUY_GRID:
        for breakout in BREAKOUT_GRID:
            if buy == BUY_SCORE and breakout == BREAKOUT_SCORE_MIN:
                continue
            candidates.append(_run_combo(buy, breakout))

    candidates.sort(
        key=lambda c: (c["expectancy"], c["winRate"], c["profitFactor"]),
        reverse=True,
    )
    best = candidates[0] if candidates else None
    recommend = False
    reason = ""
    if best and best["totalTrades"] >= 5:
        if best["expectancy"] > current["expectancy"] + 0.15 and best["winRate"] >= current["winRate"] - 2:
            recommend = True
            reason = (
                f"期望收益 {best['expectancy']}% > 当前 {current['expectancy']}% · "
                f"buy={best['buyScore']} breakout={best['breakoutScoreMin']}"
            )

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "current": {
            "strategyVersion": STRATEGY_VERSION,
            "buyScore": BUY_SCORE,
            "breakoutScoreMin": BREAKOUT_SCORE_MIN,
            "metrics": current,
        },
        "bestCandidate": best,
        "topCandidates": candidates[:5],
        "recommendUpgrade": recommend,
        "upgradeReason": reason,
        "cursorHint": (
            "若 recommendUpgrade 为 true，请 Cursor Agent 创建分支更新 strategy_config.py 并开 PR"
            if recommend
            else "暂无优于当前的参数组合"
        ),
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    append_event(
        "param_sweep",
        {
            "recommendUpgrade": recommend,
            "currentExpectancy": current.get("expectancy"),
            "bestExpectancy": (best or {}).get("expectancy"),
            "reason": reason or "hold",
        },
    )
    print(f"Param sweep: current exp={current['expectancy']}% best={((best or {}).get('expectancy'))}% upgrade={recommend}")
    return payload


if __name__ == "__main__":
    run_sweep()
