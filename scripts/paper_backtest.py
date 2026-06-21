#!/usr/bin/env python3
"""小米专用模拟盘回测 — 离线构建脚本，写入 data/paper_backtest.json。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from strategy_config import (
    BACKTEST_COOLDOWN_BARS,
    BACKTEST_HOLD_DAYS,
    BUY_SCORE,
    PAPER_BACKTEST_PERIODS,
    PAPER_INITIAL_CASH,
    PAPER_SYMBOL,
    PAPER_SYMBOL_HK_CODE,
    PAPER_SYMBOL_MARKET,
    PAPER_SYMBOL_NAME,
    STRATEGY_VERSION,
)
from strategy_scoring import compute_atr, score_series

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "paper_backtest.json"

PERIOD_LABELS = {
    "1y": "近 1 年",
    "2y": "近 2 年",
    "3y": "近 3 年",
    "4y": "近 4 年",
}

BENCHMARK = "^HSI"


def position_size_pct(score: float) -> float:
    return min(20.0 + (score - BUY_SCORE) * 0.5, 25.0)


def load_benchmark(period: str) -> dict[str, float]:
    try:
        hist = yf.Ticker(BENCHMARK).history(period=period, interval="1d")
    except Exception:
        return {}
    if hist.empty:
        return {}
    return {d.strftime("%Y-%m-%d"): float(row["Close"]) for d, row in hist.iterrows()}


def bench_closes_up_to(bench_by_date: dict[str, float], dates: list[str], idx: int) -> list[float]:
    series: list[float] = []
    for d in dates[: idx + 1]:
        if d in bench_by_date:
            series.append(bench_by_date[d])
    return series


def simulate_period(period: str, initial_cash: float) -> dict:
    bench_by_date = load_benchmark(period)
    try:
        hist = yf.Ticker(PAPER_SYMBOL).history(period=period, interval="1d")
    except Exception:
        hist = None
    if hist is None or hist.empty or len(hist) < 80:
        return {
            "label": PERIOD_LABELS.get(period, period),
            "metrics": {
                "totalReturnPct": 0.0,
                "finalEquity": initial_cash,
                "totalTrades": 0,
                "winRate": 0.0,
                "maxDrawdown": 0.0,
            },
            "equityCurve": [],
            "trades": [],
        }

    closes = [float(v) for v in hist["Close"].tolist()]
    highs = [float(v) for v in hist["High"].tolist()]
    lows = [float(v) for v in hist["Low"].tolist()]
    volumes = [float(v) for v in hist["Volume"].tolist()]
    dates = [d.strftime("%Y-%m-%d") for d in hist.index]

    cash = initial_cash
    equity = initial_cash
    trades: list[dict] = []
    equity_curve: list[dict] = [{"date": dates[65], "equity": round(equity, 2)}]
    peak = equity
    max_dd = 0.0

    i = 65
    while i < len(closes) - 1:
        bench_slice = bench_closes_up_to(bench_by_date, dates, i)
        scored = score_series(
            closes[: i + 1],
            highs[: i + 1],
            lows[: i + 1],
            volumes[: i + 1],
            bench_slice,
            PAPER_SYMBOL_MARKET,
        )
        if not scored or scored["signal"] != "buy":
            i += 1
            continue

        entry = closes[i]
        entry_date = dates[i]
        stop = scored["stopLossPrice"]
        target = scored["targetPrice"]
        alloc_pct = position_size_pct(scored["score"])
        amount = equity * alloc_pct / 100
        if amount > cash or entry <= 0:
            i += 1
            continue

        shares = round(amount / entry, 4)
        cost = round(shares * entry, 2)
        cash = round(cash - cost, 2)

        exit_price = None
        exit_date = None
        reason = None

        for j in range(i + 1, min(i + 1 + BACKTEST_HOLD_DAYS, len(closes))):
            low, high = lows[j], highs[j]
            if low <= stop:
                exit_price, exit_date, reason = stop, dates[j], "stop"
                i = j + 1 + BACKTEST_COOLDOWN_BARS
                break
            if high >= target:
                exit_price, exit_date, reason = target, dates[j], "target"
                i = j + 1 + BACKTEST_COOLDOWN_BARS
                break
        else:
            j = min(i + BACKTEST_HOLD_DAYS, len(closes) - 1)
            exit_price, exit_date, reason = closes[j], dates[j], "expiry"
            i = j + 1 + BACKTEST_COOLDOWN_BARS

        proceeds = round(shares * exit_price, 2)
        pnl = round(proceeds - cost, 2)
        pnl_pct = round((proceeds - cost) / cost * 100, 2) if cost else 0.0
        cash = round(cash + proceeds, 2)
        equity = cash
        peak = max(peak, equity)
        dd = (equity - peak) / peak * 100 if peak else 0.0
        max_dd = min(max_dd, dd)

        trades.append(
            {
                "entryDate": entry_date,
                "exitDate": exit_date,
                "entryPrice": round(entry, 2),
                "exitPrice": round(exit_price, 2),
                "shares": shares,
                "amount": cost,
                "pnl": pnl,
                "pnlPct": pnl_pct,
                "reason": reason,
                "score": scored["score"],
                "win": pnl > 0,
            }
        )
        equity_curve.append({"date": exit_date, "equity": round(equity, 2)})

    final_equity = equity
    total_return = round((final_equity - initial_cash) / initial_cash * 100, 2)
    wins = sum(1 for t in trades if t["win"])
    win_rate = round(wins / len(trades) * 100, 1) if trades else 0.0

    return {
        "label": PERIOD_LABELS.get(period, period),
        "metrics": {
            "totalReturnPct": total_return,
            "finalEquity": round(final_equity, 2),
            "totalTrades": len(trades),
            "winRate": win_rate,
            "maxDrawdown": round(max_dd, 2),
        },
        "equityCurve": equity_curve[-200:],
        "trades": trades,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    periods: dict[str, dict] = {}
    for period in PAPER_BACKTEST_PERIODS:
        periods[period] = simulate_period(period, PAPER_INITIAL_CASH)
        m = periods[period]["metrics"]
        print(f"{period}: {m['totalTrades']} trades, return {m['totalReturnPct']}%, equity {m['finalEquity']}")

    payload = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "symbol": PAPER_SYMBOL,
        "name": PAPER_SYMBOL_NAME,
        "hkCode": PAPER_SYMBOL_HK_CODE,
        "initialCash": PAPER_INITIAL_CASH,
        "strategyVersion": STRATEGY_VERSION,
        "periods": periods,
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
