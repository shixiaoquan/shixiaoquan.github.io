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
SIGNALS_FILE = DATA_DIR / "signals.json"
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


def build_signals_snapshot(account: dict, now_iso: str) -> dict:
    return {
        "updatedAt": now_iso,
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": "XRPS-X",
        "focusSymbol": PAPER_SYMBOL,
        "signals": [],
        "openCount": 0,
        "closedCount": 0,
        "xrpsState": {
            "totalShares": account.get("totalShares"),
            "avgCost": account.get("avgCost"),
            "positionPct": account.get("positionPct"),
            "monthlyState": account.get("monthlyState"),
        },
    }


def build_diagnostics(account: dict, backtest: dict | None, now_iso: str) -> dict:
    trades = account.get("trades", [])
    sells = [t for t in trades if t.get("type") == "sell"]
    wins = sum(1 for t in sells if (t.get("pnl") or 0) > 0)
    win_rate = round(wins / len(sells) * 100, 1) if sells else None

    suggestions = []
    if account.get("positionPct", 0) > 80:
        suggestions.append("仓位超过 80%，暂停加仓，等待滚动减仓。")
    if account.get("returnPct", 0) < 0:
        suggestions.append("净值回撤中，依靠连阴加仓与回撤网格积累股数，勿恐慌清仓。")
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

    save_json(SIGNALS_FILE, build_signals_snapshot(account, now_iso))
    print(f"Wrote {SIGNALS_FILE}")

    backtest = load_json(DATA_DIR / "paper_backtest.json", {}) if (DATA_DIR / "paper_backtest.json").exists() else None
    save_json(DIAGNOSTICS_FILE, build_diagnostics(account, backtest, now_iso))
    print(f"Wrote {DIAGNOSTICS_FILE}")


if __name__ == "__main__":
    main()
