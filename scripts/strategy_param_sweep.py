#!/usr/bin/env python3
"""战术策略参数探索搜索 — 在放宽过滤的探索模式下网格搜索，产出候选供 Cursor 审阅。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import backtest as bt
import strategy_scoring as sc
from backtest import BACKTEST_UNIVERSE, MARKET_MAP, compute_metrics, load_benchmark_series, simulate_symbol
from evolution_log import append_event
from strategy_config import BREAKOUT_SCORE_MIN, BUY_SCORE, STRATEGY_VERSION

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "strategy_candidates.json"

BUY_GRID = (68, 72, 75, 78)
BREAKOUT_GRID = (62, 68, 72)
EXPLORE_PERIOD = "2y"

# 探索模式：放宽 v1.3 强过滤以积累样本，生产环境仍用 strategy_config 原值
EXPLORE_RELAX = {
    "REQUIRE_BREAKOUT_FOR_BUY": False,
    "REQUIRE_BULL_MARKET": False,
    "REQUIRE_BENCH_ABOVE_MA200": False,
    "REQUIRE_MACD_POSITIVE": False,
    "MIN_RELATIVE_STRENGTH": 0.0,
}


def _run_combo(buy_score: int, breakout_min: int, *, production: bool = False) -> dict:
    patches = {"BUY_SCORE": buy_score, "BREAKOUT_SCORE_MIN": breakout_min}
    if not production:
        patches.update(EXPLORE_RELAX)

    with patch.multiple(sc, **patches), patch.object(bt, "BACKTEST_PERIOD", EXPLORE_PERIOD):
        bench = load_benchmark_series(EXPLORE_PERIOD)
        trades = []
        for symbol in BACKTEST_UNIVERSE:
            market = MARKET_MAP.get(symbol, "美股")
            trades.extend(simulate_symbol(symbol, bench.get(market, {})))
    metrics = compute_metrics(trades)
    return {
        "buyScore": buy_score,
        "breakoutScoreMin": breakout_min,
        "mode": "production" if production else "exploration",
        "period": EXPLORE_PERIOD,
        "totalTrades": metrics.get("totalTrades", 0),
        "winRate": metrics.get("winRate", 0),
        "expectancy": metrics.get("expectancy", 0),
        "profitFactor": metrics.get("profitFactor", 0),
        "sharpe": metrics.get("sharpe", 0),
        "maxDrawdown": metrics.get("maxDrawdown", 0),
    }


def run_sweep() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    current_prod = _run_combo(BUY_SCORE, BREAKOUT_SCORE_MIN, production=True)
    current_explore = _run_combo(BUY_SCORE, BREAKOUT_SCORE_MIN, production=False)

    candidates = []
    for buy in BUY_GRID:
        for breakout in BREAKOUT_GRID:
            if buy == BUY_SCORE and breakout == BREAKOUT_SCORE_MIN:
                continue
            candidates.append(_run_combo(buy, breakout, production=False))

    candidates.sort(
        key=lambda c: (c["expectancy"], c["winRate"], c["profitFactor"]),
        reverse=True,
    )
    best = candidates[0] if candidates else None
    recommend = False
    shadow_candidate = False
    reason = ""
    insufficient = current_explore["totalTrades"] < 5

    if insufficient:
        reason = (
            f"探索模式样本不足（{current_explore['totalTrades']} 笔），"
            "已使用 2y+放宽过滤；请继续积累 reco 归因"
        )
    elif best and best["totalTrades"] >= 5:
        if best["expectancy"] > current_explore["expectancy"] + 0.12 and best["winRate"] >= current_explore["winRate"] - 3:
            # 不直接 recommend 生产升级，转影子轨 forward 验证
            shadow_candidate = True
            reason = (
                f"探索候选 buy={best['buyScore']} breakout={best['breakoutScoreMin']} "
                f"期望 {best['expectancy']}% — 已写入影子轨，满 4 周后可提 PR"
            )
        else:
            reason = "hold"

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "current": {
            "strategyVersion": STRATEGY_VERSION,
            "buyScore": BUY_SCORE,
            "breakoutScoreMin": BREAKOUT_SCORE_MIN,
            "production": current_prod,
            "exploration": current_explore,
        },
        "bestCandidate": best,
        "topCandidates": candidates[:5],
        "recommendUpgrade": recommend,
        "shadowCandidate": shadow_candidate,
        "upgradeReason": reason,
        "insufficientSamples": insufficient,
        "cursorHint": (
            "候选已转入影子轨 shadow_reco.json；勿直接改 strategy_config"
            if shadow_candidate
            else reason
        ),
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    append_event(
        "param_sweep",
        {
            "recommendUpgrade": recommend,
            "currentExpectancy": current_explore.get("expectancy"),
            "bestExpectancy": (best or {}).get("expectancy"),
            "totalTrades": current_explore.get("totalTrades"),
            "reason": reason,
        },
    )
    print(
        f"Param sweep: explore trades={current_explore['totalTrades']} "
        f"exp={current_explore['expectancy']}% best={((best or {}).get('expectancy'))}% upgrade={recommend}"
    )
    return payload


if __name__ == "__main__":
    run_sweep()
