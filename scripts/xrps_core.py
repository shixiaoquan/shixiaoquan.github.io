"""XRPS-X 小米滚动仓 — 核心状态机与交易逻辑。"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime

from xrps_config import (
    CASH_PCT,
    CORE_PCT,
    MAX_POSITION_PCT,
    MIN_CASH_RESERVE_PCT,
    MONTHLY_DOWN_CORE_BUY,
    MONTHLY_TRIPLE_REDUCE_ROLLING,
    MONTHLY_UP_REDUCE,
    PAPER_INITIAL_CASH,
    PAPER_SYMBOL,
    PAPER_SYMBOL_HK_CODE,
    PAPER_SYMBOL_NAME,
    PEAK_LOOKBACK_DAYS,
    ROLLING_BUY_DRAWDOWNS,
    ROLLING_SELL_LEVELS,
    ROLLING_PCT,
    STRATEGY_CODE,
    STRATEGY_NAME,
    STRATEGY_VERSION,
)


def empty_account(now_iso: str) -> dict:
    return {
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": STRATEGY_CODE,
        "strategyName": STRATEGY_NAME,
        "initialCash": PAPER_INITIAL_CASH,
        "cash": PAPER_INITIAL_CASH,
        "coreShares": 0.0,
        "rollingShares": 0.0,
        "totalShares": 0.0,
        "avgCost": 0.0,
        "rollingAvgCost": 0.0,
        "equity": PAPER_INITIAL_CASH,
        "returnPct": 0.0,
        "positionPct": 0.0,
        "coreValue": 0.0,
        "rollingValue": 0.0,
        "focusSymbol": PAPER_SYMBOL,
        "focusName": PAPER_SYMBOL_NAME,
        "focusHkCode": PAPER_SYMBOL_HK_CODE,
        "peakPrice": 0.0,
        "triggeredSellLevels": [],
        "triggeredBuyLevels": [],
        "monthlyState": {
            "consecutiveDownMonths": 0,
            "lastMonthKey": None,
            "lastMonthReturnPct": None,
            "twoMonthReturnPct": None,
            "threeMonthReturnPct": None,
            "processedDownStreak": 0,
        },
        "trades": [],
        "equityCurve": [],
        "updatedAt": now_iso,
    }


def total_shares(account: dict) -> float:
    return round(account.get("coreShares", 0) + account.get("rollingShares", 0), 4)


def equity_at_price(account: dict, price: float) -> float:
    return round(account.get("cash", 0) + total_shares(account) * price, 2)


def weighted_avg_cost(old_shares: float, old_cost: float, add_shares: float, price: float) -> float:
    if old_shares + add_shares <= 0:
        return 0.0
    if old_shares <= 0:
        return price
    total_cost = old_shares * old_cost + add_shares * price
    return round(total_cost / (old_shares + add_shares), 4)


def build_monthly_bars(dates: list[str], closes: list[float]) -> list[dict]:
    """按月聚合 K 线，计算阴阳与月涨跌幅。"""
    buckets: dict[str, list[tuple[str, float]]] = {}
    for d, c in zip(dates, closes):
        key = d[:7]
        buckets.setdefault(key, []).append((d, c))

    months: list[dict] = []
    prev_close: float | None = None
    for key in sorted(buckets.keys()):
        rows = buckets[key]
        o = rows[0][1]
        c = rows[-1][1]
        ret = round((c - o) / o * 100, 2) if o else 0.0
        is_down = c < o
        cum_prev = round((c - prev_close) / prev_close * 100, 2) if prev_close else None
        months.append(
            {
                "key": key,
                "open": o,
                "close": c,
                "returnPct": ret,
                "isDown": is_down,
                "closeVsPrevPct": cum_prev,
            }
        )
        prev_close = c
    return months


def month_state_at_date(months: list[dict], date_str: str) -> dict:
    """截至某日（不含当月未完）的月线状态。"""
    target = date_str[:7]
    completed = [m for m in months if m["key"] < target]
    if not completed:
        return {
            "consecutiveDownMonths": 0,
            "lastMonthReturnPct": None,
            "twoMonthReturnPct": None,
            "threeMonthReturnPct": None,
        }

    streak = 0
    for m in reversed(completed):
        if m["isDown"]:
            streak += 1
        else:
            break

    last = completed[-1]
    two = None
    three = None
    if len(completed) >= 2 and completed[-2]["close"]:
        two = round((last["close"] - completed[-2]["open"]) / completed[-2]["open"] * 100, 2)
    if len(completed) >= 3 and completed[-3]["close"]:
        three = round((last["close"] - completed[-3]["open"]) / completed[-3]["open"] * 100, 2)

    return {
        "consecutiveDownMonths": streak,
        "lastMonthReturnPct": last["returnPct"],
        "twoMonthReturnPct": two,
        "threeMonthReturnPct": three,
    }


def peak_price(closes: list[float], idx: int, lookback: int = PEAK_LOOKBACK_DAYS) -> float:
    start = max(0, idx - lookback + 1)
    return max(closes[start : idx + 1])


def append_trade(account: dict, trade: dict) -> None:
    account.setdefault("trades", []).append(trade)


def record_buy(
    account: dict,
    bucket: str,
    shares: float,
    price: float,
    time: str,
    reason: str,
) -> bool:
    cost = round(shares * price, 2)
    if shares <= 0 or cost > account.get("cash", 0) + 1e-6:
        return False

    account["cash"] = round(account["cash"] - cost, 2)
    if bucket == "core":
        old = account.get("coreShares", 0)
        account["coreShares"] = round(old + shares, 4)
        account["avgCost"] = weighted_avg_cost(
            account.get("totalShares", 0) - shares,
            account.get("avgCost", 0),
            shares,
            price,
        )
    else:
        old = account.get("rollingShares", 0)
        account["rollingShares"] = round(old + shares, 4)
        account["rollingAvgCost"] = weighted_avg_cost(old, account.get("rollingAvgCost", 0), shares, price)
        account["avgCost"] = weighted_avg_cost(
            account.get("totalShares", 0) - shares,
            account.get("avgCost", 0),
            shares,
            price,
        )

    account["totalShares"] = total_shares(account)
    append_trade(
        account,
        {
            "type": "buy",
            "bucket": bucket,
            "symbol": PAPER_SYMBOL,
            "name": PAPER_SYMBOL_NAME,
            "price": price,
            "shares": round(shares, 4),
            "amount": cost,
            "reason": reason,
            "time": time,
        },
    )
    return True


def record_sell(
    account: dict,
    bucket: str,
    shares: float,
    price: float,
    time: str,
    reason: str,
) -> bool:
    if bucket == "core" or shares <= 0:
        return False

    available = account.get("rollingShares", 0)
    shares = min(shares, available)
    if shares <= 0:
        return False

    proceeds = round(shares * price, 2)
    cost_basis = account.get("rollingAvgCost", price)
    pnl = round((price - cost_basis) * shares, 2)
    pnl_pct = round((price - cost_basis) / cost_basis * 100, 2) if cost_basis else 0.0

    account["rollingShares"] = round(available - shares, 4)
    account["cash"] = round(account["cash"] + proceeds, 2)
    if account["rollingShares"] <= 0:
        account["rollingAvgCost"] = 0.0
    account["totalShares"] = total_shares(account)

    append_trade(
        account,
        {
            "type": "sell",
            "bucket": bucket,
            "symbol": PAPER_SYMBOL,
            "name": PAPER_SYMBOL_NAME,
            "price": price,
            "shares": round(shares, 4),
            "amount": proceeds,
            "pnl": pnl,
            "pnlPct": pnl_pct,
            "reason": reason,
            "time": time,
        },
    )
    return True


def refresh_metrics(account: dict, price: float, now_iso: str) -> None:
    eq = equity_at_price(account, price)
    account["equity"] = eq
    account["returnPct"] = round((eq - account["initialCash"]) / account["initialCash"] * 100, 2)
    account["coreValue"] = round(account.get("coreShares", 0) * price, 2)
    account["rollingValue"] = round(account.get("rollingShares", 0) * price, 2)
    account["totalShares"] = total_shares(account)
    account["positionPct"] = round((account["coreValue"] + account["rollingValue"]) / eq * 100, 1) if eq else 0
    account["updatedAt"] = now_iso


def bootstrap_core_if_needed(account: dict, price: float, time: str) -> None:
    """首次建立核心仓：用目标 40% 净值分批的第一笔（10% 资金）。"""
    if account.get("coreShares", 0) > 0 or price <= 0:
        return
    eq = equity_at_price(account, price)
    budget = eq * CORE_PCT * 0.25
    if budget > account["cash"] * 0.5:
        budget = account["cash"] * 0.1
    shares = round(budget / price, 4)
    record_buy(account, "core", shares, price, time, "首次核心仓建仓")


def apply_monthly_rules(account: dict, mstate: dict, price: float, time: str) -> None:
    eq = equity_at_price(account, price)
    ms = account.setdefault("monthlyState", {})
    streak = mstate.get("consecutiveDownMonths", 0)
    processed = ms.get("processedDownStreak", 0)

    if streak > processed:
        for need, pct in MONTHLY_DOWN_CORE_BUY:
            if streak >= need and processed < need:
                budget = eq * pct
                reserve = eq * MIN_CASH_RESERVE_PCT
                spend = min(budget, max(0, account["cash"] - reserve))
                shares = round(spend / price, 4) if price else 0
                if shares > 0:
                    record_buy(account, "core", shares, price, time, f"{need}连阴月加仓核心")
        ms["processedDownStreak"] = streak
    elif streak == 0:
        ms["processedDownStreak"] = 0

    if MONTHLY_TRIPLE_REDUCE_ROLLING and mstate.get("threeMonthReturnPct") is not None:
        if mstate["threeMonthReturnPct"] >= 100 and account.get("rollingShares", 0) > 0:
            record_sell(account, "rolling", account["rollingShares"], price, time, "三月翻倍清仓滚动仓")
            account["triggeredSellLevels"] = []
            return

    last_ret = mstate.get("lastMonthReturnPct")
    two_ret = mstate.get("twoMonthReturnPct")

    if two_ret is not None and two_ret >= MONTHLY_UP_REDUCE[1][0] * 100:
        sell_shares = round(account.get("rollingShares", 0) * MONTHLY_UP_REDUCE[1][1], 4)
        if sell_shares > 0:
            record_sell(account, "rolling", sell_shares, price, time, "近两月涨50%减滚动仓")
    elif last_ret is not None and last_ret >= MONTHLY_UP_REDUCE[0][0] * 100:
        sell_shares = round(account.get("rollingShares", 0) * MONTHLY_UP_REDUCE[0][1], 4)
        if sell_shares > 0:
            record_sell(account, "rolling", sell_shares, price, time, "单月涨20%减滚动仓")


def apply_rolling_grid(account: dict, price: float, peak: float, time: str) -> None:
    eq = equity_at_price(account, price)
    if eq <= 0 or price <= 0:
        return

    max_shares_value = eq * MAX_POSITION_PCT
    current_value = account["coreValue"] + account["rollingValue"] if "coreValue" in account else total_shares(account) * price

    # 滚动卖出：相对滚动成本
    cost = account.get("rollingAvgCost", 0)
    if cost > 0 and account.get("rollingShares", 0) > 0:
        gain = (price - cost) / cost
        for level, portion in ROLLING_SELL_LEVELS:
            key = f"sell_{int(level * 100)}"
            if gain >= level and key not in account.get("triggeredSellLevels", []):
                sell_shares = round(account["rollingShares"] * portion, 4)
                if record_sell(account, "rolling", sell_shares, price, time, f"滚动卖出+{int(level*100)}%"):
                    account.setdefault("triggeredSellLevels", []).append(key)

    # 滚动买回：相对峰值回撤
    if peak > 0:
        drawdown = (price - peak) / peak
        for dd, portion in ROLLING_BUY_DRAWDOWNS:
            key = f"buy_{int(abs(dd) * 100)}"
            if drawdown <= dd and key not in account.get("triggeredBuyLevels", []):
                if current_value >= max_shares_value:
                    continue
                reserve = eq * MIN_CASH_RESERVE_PCT
                budget = min(eq * portion, max(0, account["cash"] - reserve))
                shares = round(budget / price, 4)
                if shares > 0 and record_buy(account, "rolling", shares, price, time, f"回撤{int(abs(dd)*100)}%买回"):
                    account.setdefault("triggeredBuyLevels", []).append(key)

    # 新高峰重置买回档位
    if price >= peak * 0.98:
        account["triggeredBuyLevels"] = []


def process_day(
    account: dict,
    price: float,
    date_str: str,
    time_iso: str,
    mstate: dict,
    peak: float,
    *,
    skip_streak_catchup: bool = False,
) -> dict:
    account = copy.deepcopy(account)
    bootstrap_core_if_needed(account, price, time_iso)

    ms = account.setdefault("monthlyState", {})
    streak = mstate.get("consecutiveDownMonths", 0)
    if skip_streak_catchup and not account.get("xrpsInitialized"):
        ms["processedDownStreak"] = streak
        account["xrpsInitialized"] = True
    else:
        apply_monthly_rules(account, mstate, price, time_iso)
    refresh_metrics(account, price, time_iso)
    account["coreValue"] = round(account.get("coreShares", 0) * price, 2)
    account["rollingValue"] = round(account.get("rollingShares", 0) * price, 2)
    apply_rolling_grid(account, price, peak, time_iso)
    refresh_metrics(account, price, time_iso)
    account["peakPrice"] = peak
    account["monthlyState"] = {**account.get("monthlyState", {}), **mstate, "lastMonthKey": date_str[:7]}

    curve = account.get("equityCurve", [])
    point = {"time": time_iso, "equity": account["equity"], "shares": account["totalShares"]}
    if not curve or curve[-1].get("equity") != point["equity"] or curve[-1].get("shares") != point["shares"]:
        curve.append(point)
    account["equityCurve"] = curve[-500:]
    account["trades"] = account.get("trades", [])[-300:]
    return account


def build_strategy_doc(now_iso: str) -> dict:
    sell_rules = [
        {"label": f"涨幅 +{int(l*100)}%", "value": f"卖出滚动仓 {int(p*100)}%", "detail": "核心仓永不卖出"}
        for l, p in ROLLING_SELL_LEVELS
    ]
    buy_rules = [
        {"label": f"回撤 {int(abs(d)*100)}%", "value": f"买回 {int(p*100)}% 资金", "detail": "使用现金仓，保留最低现金"}
        for d, p in ROLLING_BUY_DRAWDOWNS
    ]
    return {
        "updatedAt": now_iso,
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": STRATEGY_CODE,
        "strategyName": STRATEGY_NAME,
        "focusSymbol": PAPER_SYMBOL,
        "focusName": PAPER_SYMBOL_NAME,
        "focusHkCode": PAPER_SYMBOL_HK_CODE,
        "summary": "暴跌买一点，横盘做一点，暴涨卖一点，永远留一点。目标：股数越来越多、成本越来越低、永远保留核心仓。",
        "schedule": "每 5 分钟（GitHub Actions update-market-data）",
        "account": {
            "initialCash": PAPER_INITIAL_CASH,
            "corePct": int(CORE_PCT * 100),
            "rollingPct": int(ROLLING_PCT * 100),
            "cashPct": int(CASH_PCT * 100),
            "maxPositionPct": int(MAX_POSITION_PCT * 100),
        },
        "flow": [
            {"step": 1, "title": "三仓结构", "desc": f"核心仓 {int(CORE_PCT*100)}% 永不卖；滚动仓 {int(ROLLING_PCT*100)}% 做T；现金 {int(CASH_PCT*100)}% 应对恐慌。"},
            {"step": 2, "title": "滚动网格", "desc": "上涨分批卖滚动仓，回撤分批买回，锁定波动利润。"},
            {"step": 3, "title": "月线系统", "desc": "5/6/7 连阴加仓核心；单月涨20%或两月涨50%减滚动；三月翻倍仅留核心。"},
            {"step": 4, "title": "风控", "desc": "不融资、不杠杆、不清仓、不满仓补仓、不追涨；仓位长期 ≤80%。"},
            {"step": 5, "title": "系统目标", "desc": "股数↑ 成本↓ 永远拥有核心仓，而非追求买在最低卖在最高。"},
        ],
        "buyRules": buy_rules + [
            {"label": "5连阴", "value": "核心仓 +5% 资金", "detail": "月线连阴加仓"},
            {"label": "6连阴", "value": "核心仓 +8% 资金", "detail": "月线连阴加仓"},
            {"label": "7连阴", "value": "核心仓 +12% 资金", "detail": "允许重仓核心"},
        ],
        "sellRules": sell_rules + [
            {"label": "单月涨20%", "value": "减滚动仓 15%", "detail": "仅卖滚动仓"},
            {"label": "两月涨50%", "value": "减滚动仓 25%", "detail": "大幅减仓"},
            {"label": "三月翻倍", "value": "清空滚动仓", "detail": "仅保留核心仓"},
        ],
        "positionSizing": {
            "formula": "核心仓长期持有；滚动仓按网格比例买卖；现金仓保留应对极端下跌",
            "corePct": CORE_PCT * 100,
            "rollingPct": ROLLING_PCT * 100,
            "cashPct": CASH_PCT * 100,
            "note": "核心仓永不卖出",
        },
        "signalFilters": [
            {"label": "核心仓", "value": "只买不卖", "enabled": True},
            {"label": "最大仓位", "value": f"≤ {int(MAX_POSITION_PCT*100)}%", "enabled": True},
            {"label": "现金底线", "value": f"≥ {int(MIN_CASH_RESERVE_PCT*100)}%", "enabled": True},
            {"label": "禁止追涨", "value": "仅回撤/连阴买入", "enabled": True},
        ],
        "riskParams": {
            "maxPositionPct": MAX_POSITION_PCT * 100,
            "peakLookbackDays": PEAK_LOOKBACK_DAYS,
            "motto": "暴跌买一点，横盘做一点，暴涨卖一点，永远留一点。",
        },
    }
