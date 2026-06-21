#!/usr/bin/env python3
"""信号跟踪与模拟盘 — 离线构建脚本，写入 data/*.json（非在线服务）。"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from strategy_config import (
    BUY_SCORE,
    MAX_RSI_ENTRY,
    MAX_POSITION_PCT,
    MIN_RELATIVE_STRENGTH,
    PAPER_BUY_ONLY,
    PAPER_INITIAL_CASH,
    PAPER_MAX_POSITIONS,
    REQUIRE_BULL_MARKET,
    REQUIRE_MACD_POSITIVE,
    REWARD_RISK_RATIO,
    RISK_PER_TRADE_PCT,
    SIGNAL_MAX_HOLD_DAYS,
    STRATEGY_NAME,
    STRATEGY_VERSION,
    WATCH_SCORE,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SIGNALS_FILE = DATA_DIR / "signals.json"
PAPER_FILE = DATA_DIR / "paper_account.json"
PAPER_STRATEGY_FILE = DATA_DIR / "paper_strategy.json"
VERSIONS_FILE = DATA_DIR / "strategy_versions.json"
DIAGNOSTICS_FILE = DATA_DIR / "diagnostics.json"
HISTORY_FILE = DATA_DIR / "reco_history.json"
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


def parse_dt(iso: str) -> datetime:
    dt = datetime.fromisoformat(iso)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def pct_change(current: float, base: float) -> float | None:
    if not base:
        return None
    return round((current - base) / base * 100, 2)


def ensure_strategy_version() -> dict:
    data = load_json(VERSIONS_FILE, {"current": STRATEGY_VERSION, "versions": []})
    versions = data.get("versions", [])
    if not any(v["version"] == STRATEGY_VERSION for v in versions):
        versions.append(
            {
                "version": STRATEGY_VERSION,
                "name": STRATEGY_NAME,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "params": {
                    "buyScore": 78,
                    "watchScore": 62,
                    "rewardRiskRatio": 2.0,
                    "maxHoldDays": SIGNAL_MAX_HOLD_DAYS,
                    "requireBullMarket": True,
                    "paperBuyOnly": PAPER_BUY_ONLY,
                },
            }
        )
    data["current"] = STRATEGY_VERSION
    data["versions"] = versions
    save_json(VERSIONS_FILE, data)
    return data


def create_signal_from_pick(pick: dict, record_id: str, recorded_at: str) -> dict:
    entry = pick["price"]
    stop = pick.get("stopLossPrice") or entry * 0.92
    target = pick.get("targetPrice") or entry * 1.08
    return {
        "id": f"{record_id}:{pick['symbol']}",
        "recordId": record_id,
        "symbol": pick["symbol"],
        "name": pick["name"],
        "market": pick["market"],
        "currency": pick.get("currency", "USD"),
        "strategyVersion": STRATEGY_VERSION,
        "signal": pick.get("signal"),
        "signalLabel": pick.get("signalLabel"),
        "score": pick.get("score"),
        "entryPrice": entry,
        "stopLossPrice": stop,
        "targetPrice": target,
        "openedAt": recorded_at,
        "status": "open",
        "currentPrice": entry,
        "maxGainPct": 0.0,
        "maxDrawdownPct": 0.0,
        "returnPct": 0.0,
        "closedAt": None,
        "closeReason": None,
    }


def update_open_signal(signal: dict, price: float, now: datetime) -> None:
    signal["currentPrice"] = price
    entry = signal["entryPrice"]
    ret = pct_change(price, entry) or 0.0
    signal["returnPct"] = ret
    signal["maxGainPct"] = round(max(signal.get("maxGainPct", 0), ret), 2)
    signal["maxDrawdownPct"] = round(min(signal.get("maxDrawdownPct", 0), ret), 2)

    opened = parse_dt(signal["openedAt"])
    hold_days = (now - opened).days
    signal["holdDays"] = hold_days

    stop = signal.get("stopLossPrice")
    target = signal.get("targetPrice")

    if stop and price <= stop:
        signal["status"] = "closed_stop"
        signal["closeReason"] = "触发止损"
        signal["closedAt"] = now.isoformat(timespec="seconds")
    elif target and price >= target:
        signal["status"] = "closed_target"
        signal["closeReason"] = "触发止盈"
        signal["closedAt"] = now.isoformat(timespec="seconds")
    elif hold_days >= SIGNAL_MAX_HOLD_DAYS:
        signal["status"] = "closed_expired"
        signal["closeReason"] = f"持有超 {SIGNAL_MAX_HOLD_DAYS} 天"
        signal["closedAt"] = now.isoformat(timespec="seconds")


def sync_signals(quote_map: dict[str, float], now: datetime) -> dict:
    history = load_json(HISTORY_FILE, {"records": []})
    data = load_json(SIGNALS_FILE, {"signals": []})
    signals: list[dict] = data.get("signals", [])
    existing_ids = {s["id"] for s in signals}

    # 从最新荐股记录创建新信号
    for record in history.get("records", [])[-3:]:
        record_id = record.get("id") or record.get("recordedAt", "")
        recorded_at = record.get("recordedAt", now.isoformat())
        for pick in record.get("picks", []):
            sid = f"{record_id}:{pick['symbol']}"
            if sid in existing_ids:
                continue
            signals.append(create_signal_from_pick(pick, record_id, recorded_at))
            existing_ids.add(sid)

    # 更新所有未平仓信号
    for signal in signals:
        if signal["status"] != "open":
            continue
        price = quote_map.get(signal["symbol"])
        if price is not None:
            update_open_signal(signal, price, now)

    data["signals"] = signals[-500:]
    data["updatedAt"] = now.isoformat(timespec="seconds")
    data["openCount"] = sum(1 for s in signals if s["status"] == "open")
    data["closedCount"] = sum(1 for s in signals if s["status"] != "open")
    save_json(SIGNALS_FILE, data)
    print(f"Wrote {SIGNALS_FILE} ({len(signals)} signals, {data['openCount']} open)")
    return data


def position_size_pct(score: float, signal_type: str) -> float:
    if signal_type == "buy":
        return min(20.0 + (score - BUY_SCORE) * 0.5, 25.0)
    return 10.0


def append_equity_point(curve: list[dict], now: datetime, equity: float) -> list[dict]:
    """净值曲线去重：净值未变且距上一点不足 5 分钟则不追加。"""
    point = {"time": now.isoformat(timespec="seconds"), "equity": equity}
    if not curve:
        return [point]
    last = curve[-1]
    if last.get("equity") == equity:
        try:
            last_dt = parse_dt(last["time"])
            if (now - last_dt).total_seconds() < 300:
                return curve
        except (KeyError, ValueError):
            pass
    curve.append(point)
    return curve[-500:]


def run_paper_trading(signals_data: dict, quote_map: dict[str, float], now: datetime) -> dict:
    account = load_json(
        PAPER_FILE,
        {
            "initialCash": PAPER_INITIAL_CASH,
            "cash": PAPER_INITIAL_CASH,
            "equity": PAPER_INITIAL_CASH,
            "positions": [],
            "trades": [],
            "equityCurve": [],
        },
    )
    positions = {p["symbol"]: p for p in account.get("positions", [])}
    trades = account.get("trades", [])

    # 开仓：对新 open 信号且未持仓
    open_signals = [s for s in signals_data.get("signals", []) if s["status"] == "open"]
    for sig in open_signals:
        if len(positions) >= PAPER_MAX_POSITIONS:
            break
        if sig["symbol"] in positions:
            continue
        if PAPER_BUY_ONLY and sig.get("signal") != "buy":
            continue
        if not PAPER_BUY_ONLY and sig.get("signal") not in ("buy", "watch"):
            continue

        price = quote_map.get(sig["symbol"]) or sig["entryPrice"]
        alloc_pct = position_size_pct(sig.get("score", 60), sig.get("signal", "watch"))
        equity = account.get("equity", account["cash"])
        amount = equity * alloc_pct / 100
        if amount > account["cash"] or price <= 0:
            continue

        shares = round(amount / price, 4)
        cost = round(shares * price, 2)
        account["cash"] = round(account["cash"] - cost, 2)
        positions[sig["symbol"]] = {
            "symbol": sig["symbol"],
            "name": sig["name"],
            "market": sig["market"],
            "shares": shares,
            "entryPrice": price,
            "cost": cost,
            "signalId": sig["id"],
            "openedAt": now.isoformat(timespec="seconds"),
        }
        trades.append(
            {
                "type": "buy",
                "symbol": sig["symbol"],
                "name": sig["name"],
                "price": price,
                "shares": shares,
                "amount": cost,
                "time": now.isoformat(timespec="seconds"),
                "signalId": sig["id"],
            }
        )

    # 平仓：信号已关闭
    closed_ids = {
        s["id"]
        for s in signals_data.get("signals", [])
        if s["status"] != "open" and s.get("closedAt")
    }
    for symbol, pos in list(positions.items()):
        if pos.get("signalId") not in closed_ids:
            continue
        price = quote_map.get(symbol) or pos["entryPrice"]
        proceeds = round(pos["shares"] * price, 2)
        pnl = round(proceeds - pos["cost"], 2)
        pnl_pct = pct_change(proceeds, pos["cost"])
        account["cash"] = round(account["cash"] + proceeds, 2)
        trades.append(
            {
                "type": "sell",
                "symbol": symbol,
                "name": pos["name"],
                "price": price,
                "shares": pos["shares"],
                "amount": proceeds,
                "pnl": pnl,
                "pnlPct": pnl_pct,
                "time": now.isoformat(timespec="seconds"),
                "signalId": pos.get("signalId"),
            }
        )
        del positions[symbol]

    # 计算净值
    position_value = sum(
        pos["shares"] * (quote_map.get(sym) or pos["entryPrice"]) for sym, pos in positions.items()
    )
    account["positions"] = list(positions.values())
    account["equity"] = round(account["cash"] + position_value, 2)
    account["returnPct"] = pct_change(account["equity"], account["initialCash"])
    account["trades"] = trades[-200:]

    curve = account.get("equityCurve", [])
    account["equityCurve"] = append_equity_point(curve, now, account["equity"])
    account["updatedAt"] = now.isoformat(timespec="seconds")
    save_json(PAPER_FILE, account)
    print(f"Wrote {PAPER_FILE} (equity {account['equity']})")
    return account


def build_diagnostics(signals_data: dict, backtest: dict | None, paper: dict) -> dict:
    closed = [s for s in signals_data.get("signals", []) if s["status"] != "open"]
    open_sigs = [s for s in signals_data.get("signals", []) if s["status"] == "open"]

    wins = sum(1 for s in closed if (s.get("returnPct") or 0) > 0)
    tracked = len(closed)
    win_rate = round(wins / tracked * 100, 1) if tracked else None
    avg_return = (
        round(sum(s.get("returnPct", 0) for s in closed) / tracked, 2) if tracked else None
    )

    by_market: dict[str, dict] = {}
    for s in closed:
        m = s.get("market", "未知")
        by_market.setdefault(m, {"count": 0, "wins": 0, "sumRet": 0.0})
        by_market[m]["count"] += 1
        if (s.get("returnPct") or 0) > 0:
            by_market[m]["wins"] += 1
        by_market[m]["sumRet"] += s.get("returnPct", 0)

    market_stats = []
    for m, st in by_market.items():
        market_stats.append(
            {
                "market": m,
                "trades": st["count"],
                "winRate": round(st["wins"] / st["count"] * 100, 1) if st["count"] else 0,
                "avgReturn": round(st["sumRet"] / st["count"], 2) if st["count"] else 0,
            }
        )

    suggestions = []
    if win_rate is not None and win_rate < 50:
        suggestions.append("实盘信号胜率偏低，建议提高 BUY_SCORE 阈值或加强市场环境过滤。")
    if paper.get("returnPct") is not None and paper["returnPct"] < 0:
        suggestions.append("模拟账户亏损，建议缩小仓位或暂停弱信号(watch)开仓。")
    if backtest and backtest.get("metrics", {}).get("expectancy", 0) < 0:
        suggestions.append("回测期望值为负，策略需优化参数后再实盘。")
    weak_market = min(market_stats, key=lambda x: x["winRate"], default=None)
    if weak_market and weak_market["winRate"] < 45:
        suggestions.append(f"{weak_market['market']}市场表现最弱，考虑降低该市场权重。")
    if not suggestions:
        suggestions.append("系统运行正常，继续保持纪律性交易与定期回测。")

    close_reasons: dict[str, int] = {}
    for s in closed:
        r = s.get("closeReason") or s.get("status", "unknown")
        close_reasons[r] = close_reasons.get(r, 0) + 1

    diag = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "strategyVersion": STRATEGY_VERSION,
        "summary": {
            "openSignals": len(open_sigs),
            "closedSignals": tracked,
            "winRate": win_rate,
            "avgReturn": avg_return,
            "paperReturn": paper.get("returnPct"),
            "backtestExpectancy": (backtest or {}).get("metrics", {}).get("expectancy"),
        },
        "byMarket": market_stats,
        "closeReasons": close_reasons,
        "suggestions": suggestions,
    }
    save_json(DIAGNOSTICS_FILE, diag)
    print(f"Wrote {DIAGNOSTICS_FILE}")
    return diag


def build_paper_strategy(now: datetime) -> dict:
    """导出模拟盘买卖规则，供前端展示（与 strategy_config / 引擎逻辑同步）。"""
    buy_only_label = "仅 buy 信号" if PAPER_BUY_ONLY else "buy 与 watch 信号"
    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "strategyVersion": STRATEGY_VERSION,
        "strategyName": STRATEGY_NAME,
        "summary": "每 5 分钟随行情更新自动运行：荐股产生信号 → 模拟盘按规则买卖，无人工干预。",
        "schedule": "每 5 分钟（GitHub Actions update-market-data）",
        "account": {
            "initialCash": PAPER_INITIAL_CASH,
            "maxPositions": PAPER_MAX_POSITIONS,
            "buyOnly": PAPER_BUY_ONLY,
            "buyOnlyLabel": buy_only_label,
        },
        "flow": [
            {"step": 1, "title": "荐股评分", "desc": "fetch_data 对 A股/港股/美股标的多因子打分，写入 reco_history 与 signals。"},
            {"step": 2, "title": "生成信号", "desc": "最近 3 次荐股快照中每只标的创建一条信号，持续跟踪现价与盈亏。"},
            {"step": 3, "title": "自动买入", "desc": f"对未平仓 buy 信号：最多 {PAPER_MAX_POSITIONS} 仓，按评分分配仓位后市价买入。"},
            {"step": 4, "title": "持仓监控", "desc": f"每轮检查止损 / 止盈 / 持有 {SIGNAL_MAX_HOLD_DAYS} 天，触发则关闭信号。"},
            {"step": 5, "title": "自动卖出", "desc": "信号关闭后，模拟盘按最新价卖出对应持仓，现金回笼。"},
        ],
        "buyRules": [
            {"id": "signal_buy", "label": "信号类型", "value": buy_only_label, "detail": f"评分 ≥ {BUY_SCORE} 且通过硬过滤才标记为 buy"},
            {"id": "signal_open", "label": "信号状态", "value": "open（未平仓）", "detail": "仅对新产生的 open 信号尝试开仓"},
            {"id": "max_pos", "label": "仓位上限", "value": f"最多 {PAPER_MAX_POSITIONS} 只", "detail": "已达上限则跳过新开仓"},
            {"id": "no_dup", "label": "不重复建仓", "value": "同一标的仅持有一笔", "detail": "已持仓标的不再买入"},
            {"id": "cash", "label": "资金约束", "value": "可用现金充足", "detail": "分配金额超过现金则跳过"},
        ],
        "sellRules": [
            {"id": "stop", "label": "止损平仓", "value": "现价 ≤ 止损价", "detail": "止损价 = 入场价 − ATR × 倍数（强趋势 1.5，否则 2.0）"},
            {"id": "target", "label": "止盈平仓", "value": "现价 ≥ 止盈价", "detail": f"止盈价 = 入场价 + ATR × 倍数 × {REWARD_RISK_RATIO}（盈亏比）"},
            {"id": "expiry", "label": "到期平仓", "value": f"持有 ≥ {SIGNAL_MAX_HOLD_DAYS} 天", "detail": "超期按现价强制关闭信号"},
            {"id": "paper_sync", "label": "模拟盘卖出", "value": "信号关闭即卖", "detail": "引擎检测到 signalId 已关闭，按市价卖出全部份额"},
        ],
        "positionSizing": {
            "formula": "buy 信号：min(20 + (评分 − BUY) × 0.5, 25)% × 当前净值",
            "buyScoreBase": BUY_SCORE,
            "minPct": 20.0,
            "maxPct": MAX_POSITION_PCT,
            "watchPct": 10.0,
            "note": "watch 信号在 buyOnly 模式下不参与模拟盘开仓",
        },
        "signalFilters": [
            {"label": "买入评分门槛", "value": f"≥ {BUY_SCORE}", "enabled": True},
            {"label": "观察评分门槛", "value": f"≥ {WATCH_SCORE}（不触发模拟买入）", "enabled": True},
            {"label": "大盘多头", "value": "基准指数站上 60 日均线", "enabled": REQUIRE_BULL_MARKET},
            {"label": "RSI 上限", "value": f"≤ {MAX_RSI_ENTRY}", "enabled": True},
            {"label": "相对强度", "value": f"≥ {MIN_RELATIVE_STRENGTH}%（跑赢基准）", "enabled": True},
            {"label": "MACD 柱", "value": "MACD 柱状图 > 0", "enabled": REQUIRE_MACD_POSITIVE},
            {"label": "均线结构", "value": "10 > 20 > 60 日均线多头排列", "enabled": True},
        ],
        "riskParams": {
            "riskPerTradePct": RISK_PER_TRADE_PCT,
            "rewardRiskRatio": REWARD_RISK_RATIO,
            "maxHoldDays": SIGNAL_MAX_HOLD_DAYS,
        },
    }
    save_json(PAPER_STRATEGY_FILE, payload)
    print(f"Wrote {PAPER_STRATEGY_FILE}")
    return payload


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone()

    market = load_json(MARKET_FILE, {})
    quote_map = market.get("quoteMap", {})

    ensure_strategy_version()
    build_paper_strategy(now)
    signals_data = sync_signals(quote_map, now)
    paper = run_paper_trading(signals_data, quote_map, now)

    backtest = load_json(DATA_DIR / "backtest.json", {}) if (DATA_DIR / "backtest.json").exists() else None
    build_diagnostics(signals_data, backtest, paper)


if __name__ == "__main__":
    main()
