#!/usr/bin/env python3
"""XRPS-X 小米滚动仓 — 历史回测，写入 data/paper_backtest.json + 曲线侧车文件。"""

from __future__ import annotations

import json
import shutil
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf

from strategy_config import PAPER_BACKTEST_PERIODS
from xrps_config import PAPER_INITIAL_CASH, PAPER_IPO_DATE, PAPER_SYMBOL, PAPER_SYMBOL_HK_CODE, PAPER_SYMBOL_NAME, STRATEGY_VERSION
from xrps_core import (
    build_monthly_bars,
    empty_account,
    month_state_at_date,
    peak_price,
    process_day,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "paper_backtest.json"
CURVES_DIR = DATA_DIR / "paper_backtest_curves"
MIN_BARS = 60
CURVE_MAX_POINTS = 60


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_symbol_history() -> tuple[list[str], list[float]]:
    try:
        hist = yf.Ticker(PAPER_SYMBOL).history(period="max", interval="1d")
    except Exception:
        return [], []
    if hist.empty:
        return [], []
    dates = [d.strftime("%Y-%m-%d") for d in hist.index]
    closes = [float(v) for v in hist["Close"].tolist()]
    return dates, closes


def build_period_specs(today: date) -> tuple[list[tuple[str, str, date, date]], list[str], list[str]]:
    ipo = parse_date(PAPER_IPO_DATE)
    rolling: list[tuple[str, str, date, date]] = [("all", "上市以来", ipo, today)]
    rolling_keys = ["all"]
    max_roll = max(1, min((today - ipo).days // 365, 20))
    for n in range(1, max_roll + 1):
        start = max(ipo, today - timedelta(days=365 * n))
        rolling.append((f"{n}y", f"近 {n} 年", start, today))
        rolling_keys.append(f"{n}y")

    calendar_keys: list[str] = []
    calendar: list[tuple[str, str, date, date]] = []
    for year in range(ipo.year, today.year + 1):
        start = ipo if year == ipo.year else date(year, 1, 1)
        end = today if year == today.year else date(year, 12, 31)
        if start <= end:
            calendar.append((str(year), f"{year} 年", start, end))
            calendar_keys.append(str(year))
    return rolling + calendar, rolling_keys, calendar_keys


def run_full_simulation(dates: list[str], closes: list[float], months: list[dict]) -> tuple[dict, list[dict]]:
    account = empty_account(f"{dates[0]}T00:00:00")
    daily: list[dict] = []

    for idx, (d, price) in enumerate(zip(dates, closes)):
        mstate = month_state_at_date(months, d)
        peak = peak_price(closes, idx)
        account = process_day(account, price, d, f"{d}T16:00:00", mstate, peak)
        daily.append(
            {
                "date": d,
                "equity": account["equity"],
                "shares": account["totalShares"],
                "avgCost": account.get("avgCost", 0),
                "tradeCount": len(account.get("trades", [])),
            }
        )
    return account, daily


def snapshot_on_or_before(daily: list[dict], date_str: str) -> dict | None:
    best = None
    for row in daily:
        if row["date"] <= date_str:
            best = row
        else:
            break
    return best


def downsample_curve(curve: list[dict], max_points: int = CURVE_MAX_POINTS) -> list[dict]:
    if len(curve) <= max_points:
        return curve
    step = max(1, len(curve) // max_points)
    sampled = curve[::step]
    if sampled[-1] != curve[-1]:
        sampled.append(curve[-1])
    return sampled[-max_points:]


def metrics_for_period(
    daily: list[dict],
    trades: list[dict],
    eval_start: date,
    eval_end: date,
    label: str,
) -> dict:
    start_str = eval_start.isoformat()
    end_str = eval_end.isoformat()

    start_snap = snapshot_on_or_before(daily, start_str)
    end_snap = snapshot_on_or_before(daily, end_str)

    if not end_snap:
        empty_m = {
            "totalReturnPct": 0.0,
            "finalEquity": PAPER_INITIAL_CASH,
            "initialShares": 0.0,
            "finalShares": 0.0,
            "shareGrowthPct": 0.0,
            "finalAvgCost": 0.0,
            "totalTrades": 0,
            "winRate": 0.0,
            "maxDrawdown": 0.0,
        }
        return {
            "label": label,
            "startDate": start_str,
            "endDate": end_str,
            "metrics": empty_m,
            "equityCurve": [],
            "trades": [],
        }

    start_eq = start_snap["equity"] if start_snap else PAPER_INITIAL_CASH
    end_eq = end_snap["equity"]
    start_shares = start_snap["shares"] if start_snap else 0
    end_shares = end_snap["shares"]

    ret = round((end_eq - start_eq) / start_eq * 100, 2) if start_eq else 0
    share_growth = round((end_shares - start_shares) / start_shares * 100, 2) if start_shares else round(end_shares, 2)

    period_trades = [t for t in trades if start_str <= t.get("time", "")[:10] <= end_str]
    sells = [t for t in period_trades if t.get("type") == "sell"]
    wins = sum(1 for t in sells if (t.get("pnl") or 0) > 0)
    win_rate = round(wins / len(sells) * 100, 1) if sells else 0.0

    peak = start_eq
    max_dd = 0.0
    curve = []
    for row in daily:
        if row["date"] < start_str or row["date"] > end_str:
            continue
        peak = max(peak, row["equity"])
        dd = (row["equity"] - peak) / peak * 100 if peak else 0
        max_dd = min(max_dd, dd)
        curve.append({"date": row["date"], "equity": row["equity"], "shares": row["shares"]})

    return {
        "label": label,
        "startDate": start_str,
        "endDate": end_str,
        "metrics": {
            "totalReturnPct": ret,
            "finalEquity": round(end_eq, 2),
            "initialShares": round(start_shares, 2),
            "finalShares": round(end_shares, 2),
            "shareGrowthPct": share_growth,
            "finalAvgCost": end_snap.get("avgCost", 0),
            "totalTrades": len(period_trades),
            "winRate": win_rate,
            "maxDrawdown": round(max_dd, 2),
        },
        "equityCurve": downsample_curve(curve),
        "trades": period_trades,
    }


def write_curve_file(period_key: str, curve: list[dict]) -> str:
    CURVES_DIR.mkdir(parents=True, exist_ok=True)
    rel = f"paper_backtest_curves/{period_key}.json"
    path = DATA_DIR / rel
    path.write_text(json.dumps({"period": period_key, "equityCurve": curve}, ensure_ascii=False), encoding="utf-8")
    return rel


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone()
    today = now.date()

    dates, closes = load_symbol_history()
    if len(dates) < MIN_BARS:
        print("Insufficient history")
        return

    if CURVES_DIR.exists():
        shutil.rmtree(CURVES_DIR)
    CURVES_DIR.mkdir(parents=True, exist_ok=True)

    months = build_monthly_bars(dates, closes)
    account, daily = run_full_simulation(dates, closes, months)
    trades = account.get("trades", [])

    specs, rolling_keys, calendar_keys = build_period_specs(today)
    periods: dict[str, dict] = {}

    for key, label, start, end in specs:
        block = metrics_for_period(daily, trades, start, end, label)
        curve = block.pop("equityCurve", [])
        block.pop("trades", None)
        curve_file = write_curve_file(key, curve) if curve else None
        if curve_file:
            block["curveFile"] = curve_file
        periods[key] = block
        m = block["metrics"]
        print(
            f"{key}: return {m['totalReturnPct']}%, shares {m['initialShares']}→{m['finalShares']}, "
            f"trades {m['totalTrades']}"
        )

    period_order = rolling_keys + calendar_keys
    featured = ["all", *list(PAPER_BACKTEST_PERIODS)]

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "symbol": PAPER_SYMBOL,
        "name": PAPER_SYMBOL_NAME,
        "hkCode": PAPER_SYMBOL_HK_CODE,
        "ipoDate": PAPER_IPO_DATE,
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": "XRPS-X",
        "initialCash": PAPER_INITIAL_CASH,
        "periodOrder": period_order,
        "periodGroups": {"rolling": rolling_keys, "calendar": calendar_keys},
        "featuredPeriods": featured,
        "trades": trades,
        "periods": periods,
    }
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({len(trades)} trades, {len(periods)} periods, curves in {CURVES_DIR})")


if __name__ == "__main__":
    main()
