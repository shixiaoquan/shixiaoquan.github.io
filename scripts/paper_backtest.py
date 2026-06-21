#!/usr/bin/env python3
"""小米专用模拟盘回测 — 离线构建脚本，写入 data/paper_backtest.json。"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf

from strategy_config import (
    BACKTEST_COOLDOWN_BARS,
    BACKTEST_HOLD_DAYS,
    BUY_SCORE,
    PAPER_INITIAL_CASH,
    PAPER_IPO_DATE,
    PAPER_SYMBOL,
    PAPER_SYMBOL_HK_CODE,
    PAPER_SYMBOL_MARKET,
    PAPER_SYMBOL_NAME,
    STRATEGY_VERSION,
)
from strategy_exit import simulate_exit
from strategy_scoring import MIN_BARS, compute_atr, score_series

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "paper_backtest.json"

BENCHMARK = "^HSI"
MIN_BARS_LOCAL = MIN_BARS


def position_size_pct(score: float) -> float:
    return min(20.0 + (score - BUY_SCORE) * 0.5, 25.0)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def bench_closes_up_to(bench_by_date: dict[str, float], dates: list[str], idx: int) -> list[float]:
    series: list[float] = []
    for d in dates[: idx + 1]:
        if d in bench_by_date:
            series.append(bench_by_date[d])
    return series


def load_symbol_history() -> tuple[list[str], list[float], list[float], list[float], list[float]]:
    try:
        hist = yf.Ticker(PAPER_SYMBOL).history(period="max", interval="1d")
    except Exception:
        hist = None
    if hist is None or hist.empty:
        return [], [], [], [], []
    dates = [d.strftime("%Y-%m-%d") for d in hist.index]
    closes = [float(v) for v in hist["Close"].tolist()]
    highs = [float(v) for v in hist["High"].tolist()]
    lows = [float(v) for v in hist["Low"].tolist()]
    volumes = [float(v) for v in hist["Volume"].tolist()]
    return dates, closes, highs, lows, volumes


def load_benchmark_history() -> dict[str, float]:
    try:
        hist = yf.Ticker(BENCHMARK).history(period="max", interval="1d")
    except Exception:
        return {}
    if hist.empty:
        return {}
    return {d.strftime("%Y-%m-%d"): float(row["Close"]) for d, row in hist.iterrows()}


def build_period_specs(today: date) -> tuple[list[tuple[str, str, date, date]], list[str], list[str]]:
    """生成 (key, label, start, end)、滚动 keys、自然年 keys。"""
    ipo = parse_date(PAPER_IPO_DATE)
    last_date = today
    days_listed = (last_date - ipo).days
    max_roll_years = max(1, min(days_listed // 365, 20))

    rolling: list[tuple[str, str, date, date]] = []
    rolling_keys: list[str] = []

    rolling.append(("all", "上市以来", ipo, last_date))
    rolling_keys.append("all")

    for n in range(1, max_roll_years + 1):
        start = last_date - timedelta(days=365 * n)
        if start < ipo:
            start = ipo
        key = f"{n}y"
        rolling.append((key, f"近 {n} 年", start, last_date))
        rolling_keys.append(key)

    calendar: list[tuple[str, str, date, date]] = []
    calendar_keys: list[str] = []
    for year in range(ipo.year, last_date.year + 1):
        start = date(year, 1, 1) if year > ipo.year else ipo
        end = date(year, 12, 31) if year < last_date.year else last_date
        if start > end:
            continue
        key = str(year)
        calendar.append((key, f"{year} 年", start, end))
        calendar_keys.append(key)

    return rolling + calendar, rolling_keys, calendar_keys


def simulate_range(
    dates: list[str],
    closes: list[float],
    highs: list[float],
    lows: list[float],
    volumes: list[float],
    bench_by_date: dict[str, float],
    eval_start: date,
    eval_end: date,
    initial_cash: float,
    label: str,
) -> dict:
    empty = {
        "label": label,
        "startDate": eval_start.isoformat(),
        "endDate": eval_end.isoformat(),
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
    if len(dates) < MIN_BARS_LOCAL:
        return empty

    start_str = eval_start.isoformat()
    end_str = eval_end.isoformat()

    cash = initial_cash
    equity = initial_cash
    trades: list[dict] = []
    equity_curve: list[dict] = []
    peak = equity
    max_dd = 0.0

    i = MIN_BARS_LOCAL
    while i < len(closes) - 1:
        if dates[i] < start_str:
            i += 1
            continue
        if dates[i] > end_str:
            break

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
        atr = scored.get("atr") or compute_atr(highs[: i + 1], lows[: i + 1], closes[: i + 1]) or entry * 0.02
        alloc_pct = position_size_pct(scored["score"])
        amount = equity * alloc_pct / 100
        if amount > cash or entry <= 0:
            i += 1
            continue

        shares = round(amount / entry, 4)
        cost = round(shares * entry, 2)
        cash = round(cash - cost, 2)

        exit_price, exit_date, reason = simulate_exit(
            entry, i, dates, closes, highs, lows, atr,
        )
        j = dates.index(exit_date) if exit_date in dates else i + 1
        i = j + 1 + BACKTEST_COOLDOWN_BARS

        proceeds = round(shares * exit_price, 2)
        pnl = round(proceeds - cost, 2)
        pnl_pct = round((proceeds - cost) / cost * 100, 2) if cost else 0.0
        cash = round(cash + proceeds, 2)
        equity = cash
        peak = max(peak, equity)
        dd = (equity - peak) / peak * 100 if peak else 0.0
        max_dd = min(max_dd, dd)

        if not equity_curve:
            equity_curve.append({"date": entry_date, "equity": round(initial_cash, 2)})
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
                "entryType": scored.get("entryType"),
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
        "label": label,
        "startDate": eval_start.isoformat(),
        "endDate": eval_end.isoformat(),
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
    now = datetime.now(timezone.utc).astimezone()
    today = now.date()

    dates, closes, highs, lows, volumes = load_symbol_history()
    bench_by_date = load_benchmark_history()
    if not dates:
        print("No history for", PAPER_SYMBOL)
        return

    specs, rolling_keys, calendar_keys = build_period_specs(today)
    periods: dict[str, dict] = {}
    for key, label, start, end in specs:
        periods[key] = simulate_range(
            dates, closes, highs, lows, volumes, bench_by_date,
            start, end, PAPER_INITIAL_CASH, label,
        )
        m = periods[key]["metrics"]
        print(f"{key} ({label}): {m['totalTrades']} trades, return {m['totalReturnPct']}%")

    listed_years = today.year - parse_date(PAPER_IPO_DATE).year + 1
    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "symbol": PAPER_SYMBOL,
        "name": PAPER_SYMBOL_NAME,
        "hkCode": PAPER_SYMBOL_HK_CODE,
        "ipoDate": PAPER_IPO_DATE,
        "listedYears": listed_years,
        "initialCash": PAPER_INITIAL_CASH,
        "strategyVersion": STRATEGY_VERSION,
        "periodOrder": rolling_keys + calendar_keys,
        "periodGroups": {
            "rolling": rolling_keys,
            "calendar": calendar_keys,
        },
        "periods": periods,
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({len(periods)} periods, IPO {PAPER_IPO_DATE})")


if __name__ == "__main__":
    main()
