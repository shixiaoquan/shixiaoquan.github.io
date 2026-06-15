#!/usr/bin/env python3
"""策略参数网格搜索 — 离线构建脚本，每周与回测一并运行，写入 data/param_sweep.json。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

from backtest import run_backtest
from strategy_config import BACKTEST_PERIOD, BUY_SCORE, STRATEGY_VERSION, WATCH_SCORE

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "param_sweep.json"

BUY_SCORE_GRID = [72, 74, 76, 78, 80]
WATCH_SCORE_GRID = [56, 58, 60, 62, 64]
MIN_TRADES = 8


def sweep() -> list[dict]:
    results: list[dict] = []
    for buy_score, watch_score in product(BUY_SCORE_GRID, WATCH_SCORE_GRID):
        if watch_score >= buy_score - 8:
            continue
        _, metrics, _ = run_backtest(buy_score=buy_score, watch_score=watch_score)
        results.append(
            {
                "buyScore": buy_score,
                "watchScore": watch_score,
                "totalTrades": metrics["totalTrades"],
                "winRate": metrics["winRate"],
                "expectancy": metrics["expectancy"],
                "profitFactor": metrics["profitFactor"],
                "maxDrawdown": metrics["maxDrawdown"],
                "sharpe": metrics["sharpe"],
                "annualReturn": metrics["annualReturn"],
            }
        )
    return results


def pick_best(results: list[dict]) -> dict | None:
    eligible = [r for r in results if r["totalTrades"] >= MIN_TRADES]
    if not eligible:
        return None
    return max(eligible, key=lambda r: (r["expectancy"], r["profitFactor"], r["winRate"]))


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    results = sweep()
    best = pick_best(results)
    current = next(
        (r for r in results if r["buyScore"] == BUY_SCORE and r["watchScore"] == WATCH_SCORE),
        None,
    )

    payload = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "strategyVersion": STRATEGY_VERSION,
        "period": BACKTEST_PERIOD,
        "grid": {"buyScore": BUY_SCORE_GRID, "watchScore": WATCH_SCORE_GRID},
        "minTrades": MIN_TRADES,
        "current": current,
        "best": best,
        "recommendation": None,
        "results": sorted(results, key=lambda r: (-r["expectancy"], -r["winRate"])),
    }

    if best and current:
        if best["buyScore"] == current["buyScore"] and best["watchScore"] == current["watchScore"]:
            payload["recommendation"] = "当前参数已在网格搜索中表现最优，无需调整。"
        elif best["expectancy"] > current["expectancy"] + 0.15:
            payload["recommendation"] = (
                f"建议考虑 BUY_SCORE={best['buyScore']}、WATCH_SCORE={best['watchScore']} "
                f"（期望 {best['expectancy']}% vs 当前 {current['expectancy']}%）。"
            )
        else:
            payload["recommendation"] = "当前参数与最优组合接近，维持现状即可。"
    elif best:
        payload["recommendation"] = (
            f"网格最优：BUY_SCORE={best['buyScore']}、WATCH_SCORE={best['watchScore']}。"
        )

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({len(results)} combos, best expectancy {best['expectancy'] if best else 'n/a'})")


if __name__ == "__main__":
    main()
