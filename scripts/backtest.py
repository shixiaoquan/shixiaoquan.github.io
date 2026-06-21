#!/usr/bin/env python3
"""策略回测 — 离线构建脚本，用历史 K 线验证策略并写入 data/backtest.json。"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from strategy_config import (
    BACKTEST_COOLDOWN_BARS,
    BACKTEST_HOLD_DAYS,
    BACKTEST_PERIOD,
    PREVIOUS_BASELINE,
    PREVIOUS_VERSION,
    STRATEGY_VERSION,
)
from strategy_exit import simulate_exit
from strategy_scoring import MARKET_BENCHMARKS, MIN_BARS, compute_atr, score_series

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "backtest.json"

BACKTEST_UNIVERSE = [
    "600519.SS",
    "601318.SS",
    "0700.HK",
    "1810.HK",
    "AAPL",
    "NVDA",
]

MARKET_MAP = {
    "600519.SS": "A股",
    "601318.SS": "A股",
    "300750.SZ": "A股",
    "000858.SZ": "A股",
    "688981.SS": "A股",
    "600036.SS": "A股",
    "0700.HK": "港股",
    "9988.HK": "港股",
    "3690.HK": "港股",
    "1810.HK": "港股",
    "9992.HK": "港股",
    "9618.HK": "港股",
    "AAPL": "美股",
    "MSFT": "美股",
    "NVDA": "美股",
    "GOOGL": "美股",
    "AMZN": "美股",
    "META": "美股",
    "AMD": "美股",
}


def load_benchmark_series(period: str) -> dict[str, dict[str, float]]:
    """市场基准：日期 -> 收盘价。"""
    result: dict[str, dict[str, float]] = {}
    for market, bench_symbol in MARKET_BENCHMARKS.items():
        try:
            hist = yf.Ticker(bench_symbol).history(period=period, interval="1d")
        except Exception:
            continue
        if hist.empty:
            continue
        result[market] = {d.strftime("%Y-%m-%d"): float(row["Close"]) for d, row in hist.iterrows()}
    return result


def bench_closes_up_to(
    bench_by_date: dict[str, float], dates: list[str], idx: int
) -> list[float]:
    series: list[float] = []
    for d in dates[: idx + 1]:
        if d in bench_by_date:
            series.append(bench_by_date[d])
    return series


def simulate_symbol(symbol: str, bench_by_date: dict[str, float]) -> list[dict]:
    market = MARKET_MAP.get(symbol, "美股")
    try:
        hist = yf.Ticker(symbol).history(period=BACKTEST_PERIOD, interval="1d")
    except Exception:
        return []
    if hist.empty or len(hist) < MIN_BARS:
        return []

    closes = [float(v) for v in hist["Close"].tolist()]
    highs = [float(v) for v in hist["High"].tolist()]
    lows = [float(v) for v in hist["Low"].tolist()]
    volumes = [float(v) for v in hist["Volume"].tolist()]
    dates = [d.strftime("%Y-%m-%d") for d in hist.index]
    trades = []
    i = MIN_BARS
    while i < len(closes) - 1:
        bench_slice = bench_closes_up_to(bench_by_date, dates, i)
        scored = score_series(
            closes[: i + 1],
            highs[: i + 1],
            lows[: i + 1],
            volumes[: i + 1],
            bench_slice,
            market,
        )
        if not scored or scored["signal"] != "buy":
            i += 1
            continue

        entry = closes[i]
        entry_date = dates[i]
        atr = scored.get("atr") or compute_atr(highs[: i + 1], lows[: i + 1], closes[: i + 1]) or entry * 0.02
        exit_price, exit_date, reason = simulate_exit(
            entry, i, dates, closes, highs, lows, atr,
        )
        j = dates.index(exit_date) if exit_date in dates else i + 1
        i = j + 1 + BACKTEST_COOLDOWN_BARS

        ret = (exit_price - entry) / entry * 100
        trades.append(
            {
                "symbol": symbol,
                "market": market,
                "entryDate": entry_date,
                "exitDate": exit_date,
                "entryPrice": round(entry, 2),
                "exitPrice": round(exit_price, 2),
                "returnPct": round(ret, 2),
                "reason": reason,
                "score": scored["score"],
                "win": ret > 0,
            }
        )
    return trades


def compute_metrics(trades: list[dict]) -> dict:
    if not trades:
        return {
            "totalTrades": 0,
            "winRate": 0,
            "profitFactor": 0,
            "expectancy": 0,
            "avgWin": 0,
            "avgLoss": 0,
            "maxDrawdown": 0,
            "sharpe": 0,
            "annualReturn": 0,
        }

    wins = [t["returnPct"] for t in trades if t["returnPct"] > 0]
    losses = [t["returnPct"] for t in trades if t["returnPct"] <= 0]
    win_rate = len(wins) / len(trades) * 100
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = round(gross_profit / gross_loss, 2) if gross_loss else 999.0
    expectancy = round(win_rate / 100 * avg_win + (1 - win_rate / 100) * avg_loss, 2)

    equity = 100.0
    peak = 100.0
    max_dd = 0.0
    curve = [{"date": trades[0]["entryDate"], "value": 100.0}]
    for t in trades:
        equity *= 1 + t["returnPct"] / 100
        peak = max(peak, equity)
        dd = (equity - peak) / peak * 100
        max_dd = min(max_dd, dd)
        curve.append({"date": t["exitDate"], "value": round(equity, 2)})

    rets = [t["returnPct"] for t in trades]
    mean_r = sum(rets) / len(rets)
    std_r = math.sqrt(sum((r - mean_r) ** 2 for r in rets) / len(rets)) if len(rets) > 1 else 1
    sharpe = round(mean_r / std_r * math.sqrt(252 / max(BACKTEST_HOLD_DAYS, 1)), 2) if std_r else 0
    annual_return = round((equity / 100 - 1) * 100, 2)

    return {
        "totalTrades": len(trades),
        "winRate": round(win_rate, 1),
        "profitFactor": profit_factor,
        "expectancy": expectancy,
        "avgWin": round(avg_win, 2),
        "avgLoss": round(avg_loss, 2),
        "maxDrawdown": round(max_dd, 2),
        "sharpe": sharpe,
        "annualReturn": annual_return,
        "equityCurve": curve[-100:],
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    bench_maps = load_benchmark_series(BACKTEST_PERIOD)
    all_trades: list[dict] = []
    by_market: dict[str, list[dict]] = {}

    for symbol in BACKTEST_UNIVERSE:
        market = MARKET_MAP.get(symbol, "美股")
        bench_by_date = bench_maps.get(market, {})
        trades = simulate_symbol(symbol, bench_by_date)
        all_trades.extend(trades)
        by_market.setdefault(market, []).extend(trades)

    metrics = compute_metrics(all_trades)
    market_metrics = {m: compute_metrics(t) for m, t in by_market.items()}

    payload = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "strategyVersion": STRATEGY_VERSION,
        "period": BACKTEST_PERIOD,
        "universe": BACKTEST_UNIVERSE,
        "metrics": {k: v for k, v in metrics.items() if k != "equityCurve"},
        "equityCurve": metrics.get("equityCurve", []),
        "byMarket": {
            m: {k: v for k, v in mm.items() if k != "equityCurve"}
            for m, mm in market_metrics.items()
        },
        "recentTrades": sorted(all_trades, key=lambda x: x["exitDate"] or "", reverse=True)[:30],
        "compareWith": {
            "version": PREVIOUS_VERSION,
            "metrics": PREVIOUS_BASELINE,
            "delta": {
                "winRate": round(metrics["winRate"] - PREVIOUS_BASELINE["winRate"], 1),
                "expectancy": round(metrics["expectancy"] - PREVIOUS_BASELINE["expectancy"], 2),
                "profitFactor": round(metrics["profitFactor"] - PREVIOUS_BASELINE["profitFactor"], 2),
                "maxDrawdown": round(metrics["maxDrawdown"] - PREVIOUS_BASELINE["maxDrawdown"], 2),
            },
        },
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({metrics['totalTrades']} trades, expectancy {metrics['expectancy']})")


if __name__ == "__main__":
    main()
