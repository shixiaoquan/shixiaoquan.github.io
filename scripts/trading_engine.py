#!/usr/bin/env python3
"""XRPS-X 小米滚动仓 — 模拟盘引擎，写入 data/*.json。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from xrps_config import PAPER_INITIAL_CASH, PAPER_SYMBOL, PAPER_SYMBOL_MARKET, STRATEGY_VERSION
from xrps_core import (
    build_monthly_bars,
    build_strategy_doc,
    empty_account,
    equity_at_price,
    month_state_at_date,
    peak_price,
    process_day,
    refresh_metrics,
)
from strategy_scoring import MARKET_BENCHMARKS

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PAPER_FILE = DATA_DIR / "paper_account.json"
PAPER_STRATEGY_FILE = DATA_DIR / "paper_strategy.json"
DIAGNOSTICS_FILE = DATA_DIR / "diagnostics.json"
VERSIONS_FILE = DATA_DIR / "strategy_versions.json"
MARKET_FILE = DATA_DIR / "market.json"


def load_json(path: Path, default: dict) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return default.copy() if isinstance(default, dict) else default


def save_json(path: Path, data: dict | list) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_history() -> tuple[list[str], list[float]]:
    try:
        hist = yf.Ticker(PAPER_SYMBOL).history(period="max", interval="1d")
    except Exception:
        return [], []
    if hist.empty:
        return [], []
    dates = [d.strftime("%Y-%m-%d") for d in hist.index]
    closes = [float(v) for v in hist["Close"].tolist()]
    return dates, closes


def current_price(quote_map: dict[str, float], closes: list[float]) -> float | None:
    if quote_map.get(PAPER_SYMBOL):
        return float(quote_map[PAPER_SYMBOL])
    return closes[-1] if closes else None


def ensure_strategy_version() -> None:
    from xrps_config import STRATEGY_NAME

    data = load_json(VERSIONS_FILE, {"current": STRATEGY_VERSION, "versions": []})
    versions = data.get("versions", [])
    if not any(v["version"] == STRATEGY_VERSION for v in versions):
        versions.append(
            {
                "version": STRATEGY_VERSION,
                "name": STRATEGY_NAME,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "params": {"system": "XRPS-X", "symbol": PAPER_SYMBOL},
            }
        )
    data["current"] = STRATEGY_VERSION
    data["versions"] = versions
    save_json(VERSIONS_FILE, data)


def migrate_account(account: dict, now_iso: str) -> dict:
    if account.get("strategyCode") == "XRPS-X" or account.get("strategyVersion", "").startswith("XRPS"):
        return account
    print("Migrating paper account to XRPS-X")
    fresh = empty_account(now_iso)
    fresh["xrpsInitialized"] = False
    return fresh


def run_xrps(account: dict, quote_map: dict[str, float], now: datetime) -> dict:
    now_iso = now.isoformat(timespec="seconds")
    today = now.date().isoformat()

    dates, closes = load_history()
    price = current_price(quote_map, closes)
    if not price or not dates:
        refresh_metrics(account, account.get("lastPrice", 0) or PAPER_INITIAL_CASH, now_iso)
        return account

    account = migrate_account(account, now_iso)

    if account.get("lastProcessedDate") == today:
        refresh_metrics(account, price, now_iso)
        account["lastPrice"] = price
        return account

    months = build_monthly_bars(dates, closes)
    idx = len(dates) - 1
    mstate = month_state_at_date(months, today)
    peak = peak_price(closes, idx)

    account = process_day(account, price, today, now_iso, mstate, peak, skip_streak_catchup=True)
    account["lastProcessedDate"] = today
    account["lastPrice"] = price
    return account


def build_xrps_action_plan(account: dict, price: float | None) -> dict:
    """生成 XRPS 下一档触发与月线状态，供前端行动清单使用。"""
    ms = account.get("monthlyState") or {}
    rolling_cost = account.get("rollingAvgCost") or account.get("avgCost") or 0
    peak = account.get("peakPrice") or price or 0
    triggered_sell = set(account.get("triggeredSellLevels") or [])
    triggered_buy = set(account.get("triggeredBuyLevels") or [])

    sell_levels = [
        ("sell_15", 0.15, "涨 15%"),
        ("sell_25", 0.25, "涨 25%"),
        ("sell_40", 0.40, "涨 40%"),
        ("sell_60", 0.60, "涨 60%"),
    ]
    buy_levels = [
        ("buy_10", -0.10, "回撤 10%"),
        ("buy_20", -0.20, "回撤 20%"),
        ("buy_30", -0.30, "回撤 30%"),
    ]

    next_sell = None
    for key, pct, label in sell_levels:
        if key in triggered_sell:
            continue
        trigger = round(rolling_cost * (1 + pct), 2) if rolling_cost else None
        gap = round((trigger - price) / price * 100, 1) if trigger and price else None
        next_sell = {"key": key, "label": label, "triggerPrice": trigger, "gapPct": gap}
        break

    next_buy = None
    for key, pct, label in buy_levels:
        if key in triggered_buy:
            continue
        trigger = round(peak * (1 + pct), 2) if peak else None
        gap = round((price - trigger) / price * 100, 1) if trigger and price else None
        next_buy = {"key": key, "label": label, "triggerPrice": trigger, "gapPct": gap}
        break

    streak = ms.get("consecutiveDownMonths") or 0
    stage = "normal"
    if not account.get("coreShares") and not account.get("rollingShares"):
        stage = "bootstrap"
    elif streak >= 5 and not any(t.get("type") == "sell" for t in account.get("trades", [])):
        stage = "accumulate"
    elif account.get("rollingShares") and account.get("triggeredSellLevels"):
        stage = "rolling"

    return {
        "stage": stage,
        "price": price,
        "nextSell": next_sell,
        "nextBuy": next_buy,
        "monthly": {
            "consecutiveDownMonths": streak,
            "lastMonthReturnPct": ms.get("lastMonthReturnPct"),
            "twoMonthReturnPct": ms.get("twoMonthReturnPct"),
            "threeMonthReturnPct": ms.get("threeMonthReturnPct"),
        },
    }


def build_diagnostics(account: dict, backtest: dict | None, now_iso: str, price: float | None = None) -> dict:
    trades = account.get("trades", [])
    sells = [t for t in trades if t.get("type") == "sell"]
    wins = sum(1 for t in sells if (t.get("pnl") or 0) > 0)
    win_rate = round(wins / len(sells) * 100, 1) if sells else None

    suggestions = []
    if account.get("positionPct", 0) > 80:
        suggestions.append("仓位超过 80%，暂停加仓，等待滚动减仓。")
    if account.get("returnPct", 0) < 0:
        suggestions.append("净值回撤中，依靠连阴加仓与回撤网格积累股数，勿恐慌清仓。")
    ms = account.get("monthlyState") or {}
    streak = ms.get("consecutiveDownMonths") or 0
    if streak >= 5:
        suggestions.append(
            f"已 {streak} 连阴月（上月 {ms.get('lastMonthReturnPct', '--')}%），"
            "核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。"
        )
    if not suggestions:
        suggestions.append("XRPS-X 运行正常：股数优先、成本优先、核心仓保留。")

    return {
        "updatedAt": now_iso,
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": "XRPS-X",
        "focusSymbol": PAPER_SYMBOL,
        "summary": {
            "totalShares": account.get("totalShares"),
            "avgCost": account.get("avgCost"),
            "paperReturn": account.get("returnPct"),
            "positionPct": account.get("positionPct"),
            "rollingWinRate": win_rate,
            "backtestReturn": (backtest or {}).get("periods", {}).get("all", {}).get("metrics", {}).get("totalReturnPct"),
        },
        "suggestions": suggestions,
        "xrpsActionPlan": build_xrps_action_plan(account, price),
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone()
    now_iso = now.isoformat(timespec="seconds")

    market = load_json(MARKET_FILE, {})
    quote_map = market.get("quoteMap", {})

    ensure_strategy_version()
    save_json(PAPER_STRATEGY_FILE, build_strategy_doc(now_iso))

    account = load_json(PAPER_FILE, empty_account(now_iso))
    account = run_xrps(account, quote_map, now)
    save_json(PAPER_FILE, account)
    print(f"Wrote {PAPER_FILE} (shares {account.get('totalShares')}, equity {account.get('equity')})")

    backtest = load_json(DATA_DIR / "paper_backtest.json", {}) if (DATA_DIR / "paper_backtest.json").exists() else None
    focus_price = quote_map.get(PAPER_SYMBOL) or account.get("lastPrice")
    save_json(DIAGNOSTICS_FILE, build_diagnostics(account, backtest, now_iso, focus_price))
    print(f"Wrote {DIAGNOSTICS_FILE}")


if __name__ == "__main__":
    main()
