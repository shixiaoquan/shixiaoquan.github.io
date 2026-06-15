#!/usr/bin/env python3
"""策略回测引擎 — 用历史 K 线验证策略期望收益。"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from strategy_config import (
    BACKTEST_HOLD_DAYS,
    BACKTEST_PERIOD,
    REWARD_RISK_RATIO,
    STRATEGY_VERSION,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "backtest.json"

# 每市场 2 只代表股，控制回测耗时
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


def sma(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def compute_atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> float | None:
    if len(closes) < period + 1:
        return None
    trs = []
    for i in range(1, len(closes)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        trs.append(tr)
    return sum(trs[-period:]) / period


def entry_signal(closes: list[float], idx: int) -> bool:
    """简化入场：多头排列。"""
    if idx < 60:
        return False
    slice_c = closes[: idx + 1]
    price = slice_c[-1]
    s20 = sma(slice_c, 20)
    s60 = sma(slice_c, 60)
    if not s20 or not s60:
        return False
    return price > s20 > s60


def simulate_symbol(symbol: str) -> list[dict]:
    try:
        hist = yf.Ticker(symbol).history(period=BACKTEST_PERIOD, interval="1d")
    except Exception:
        return []
    if hist.empty or len(hist) < 80:
        return []

    closes = [float(v) for v in hist["Close"].tolist()]
    highs = [float(v) for v in hist["High"].tolist()]
    lows = [float(v) for v in hist["Low"].tolist()]
    dates = [d.strftime("%Y-%m-%d") for d in hist.index]
    trades = []
    i = 60
    while i < len(closes) - 1:
        if not entry_signal(closes, i):
            i += 1
            continue

        entry = closes[i]
        entry_date = dates[i]
        atr = compute_atr(highs[: i + 1], lows[: i + 1], closes[: i + 1]) or entry * 0.02
        stop = entry - 2 * atr
        target = entry + 2 * atr * REWARD_RISK_RATIO
        exit_price = None
        exit_date = None
        reason = None

        for j in range(i + 1, min(i + 1 + BACKTEST_HOLD_DAYS, len(closes))):
            low, high, close = lows[j], highs[j], closes[j]
            if low <= stop:
                exit_price, exit_date, reason = stop, dates[j], "stop"
                i = j + 1
                break
            if high >= target:
                exit_price, exit_date, reason = target, dates[j], "target"
                i = j + 1
                break
        else:
            j = min(i + BACKTEST_HOLD_DAYS, len(closes) - 1)
            exit_price, exit_date, reason = closes[j], dates[j], "expiry"
            i = j + 1

        ret = (exit_price - entry) / entry * 100
        trades.append(
            {
                "symbol": symbol,
                "market": MARKET_MAP.get(symbol, "未知"),
                "entryDate": entry_date,
                "exitDate": exit_date,
                "entryPrice": round(entry, 2),
                "exitPrice": round(exit_price, 2),
                "returnPct": round(ret, 2),
                "reason": reason,
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

    # 权益曲线与最大回撤
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
    all_trades: list[dict] = []
    by_market: dict[str, list[dict]] = {}

    for symbol in BACKTEST_UNIVERSE:
        trades = simulate_symbol(symbol)
        all_trades.extend(trades)
        m = MARKET_MAP.get(symbol, "未知")
        by_market.setdefault(m, []).extend(trades)

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
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({metrics['totalTrades']} trades, expectancy {metrics['expectancy']})")


if __name__ == "__main__":
    main()
