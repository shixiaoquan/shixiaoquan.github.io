#!/usr/bin/env python3
"""战术策略 A/B 对比 — v1.2 宽松 vs v1.3 生产参数（探索回测，零额外 API）。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import backtest as bt
import strategy_scoring as sc
from backtest import BACKTEST_UNIVERSE, MARKET_MAP, compute_metrics, load_benchmark_series, simulate_symbol

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "paper_ab.json"

VARIANTS = {
    "v1.3_production": {
        "label": "v1.3 生产（强趋势+突破）",
        "patches": {},
        "production": True,
    },
    "v1.2_relaxed": {
        "label": "v1.2 对照（放宽过滤）",
        "patches": {
            "BUY_SCORE": 75,
            "BREAKOUT_SCORE_MIN": 68,
            "REQUIRE_BREAKOUT_FOR_BUY": False,
            "REQUIRE_BULL_MARKET": False,
            "REQUIRE_BENCH_ABOVE_MA200": False,
        },
        "production": False,
    },
}


def _simulate_variant(name: str, spec: dict) -> dict:
    patches = dict(spec.get("patches") or {})
    period = "2y"
    if patches:
        ctx = patch.multiple(sc, **patches)
    else:
        from contextlib import nullcontext
        ctx = nullcontext()
    with ctx, patch.object(bt, "BACKTEST_PERIOD", period):
        bench = load_benchmark_series(period)
        trades = []
        for symbol in BACKTEST_UNIVERSE:
            market = MARKET_MAP.get(symbol, "美股")
            trades.extend(simulate_symbol(symbol, bench.get(market, {})))
    metrics = compute_metrics(trades)
    return {
        "id": name,
        "label": spec["label"],
        "period": period,
        "metrics": {k: v for k, v in metrics.items() if k != "equityCurve"},
        "recentTrades": sorted(trades, key=lambda x: x.get("exitDate") or "", reverse=True)[:5],
    }


def run_ab() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    results = {name: _simulate_variant(name, spec) for name, spec in VARIANTS.items()}
    prod = results["v1.3_production"]["metrics"]
    relaxed = results["v1.2_relaxed"]["metrics"]
    leader = "v1.3_production"
    if relaxed.get("expectancy", 0) > prod.get("expectancy", 0) + 0.2:
        leader = "v1.2_relaxed"

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "leader": leader,
        "variants": results,
        "delta": {
            "expectancy": round(relaxed.get("expectancy", 0) - prod.get("expectancy", 0), 2),
            "winRate": round(relaxed.get("winRate", 0) - prod.get("winRate", 0), 1),
        },
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Paper A/B: leader={leader} Δexp={payload['delta']['expectancy']}%")
    return payload


if __name__ == "__main__":
    run_ab()
