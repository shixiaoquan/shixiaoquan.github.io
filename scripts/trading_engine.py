#!/usr/bin/env python3
"""信号跟踪与模拟盘 — 离线构建脚本，写入 data/*.json（非在线服务）。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from strategy_config import (
    ATR_STOP_INITIAL,
    ATR_TRAILING,
    BREAKOUT_LOOKBACK,
    BREAKOUT_SCORE_MIN,
    BREAKOUT_VOLUME_RATIO,
    BUY_SCORE,
    MAX_RSI_ENTRY,
    MAX_POSITION_PCT,
    MIN_RELATIVE_STRENGTH,
    PAPER_BUY_ONLY,
    PAPER_INITIAL_CASH,
    PAPER_MAX_POSITIONS,
    PAPER_SYMBOL,
    PAPER_SYMBOL_HK_CODE,
    PAPER_SYMBOL_MARKET,
    PAPER_SYMBOL_NAME,
    REQUIRE_ABOVE_MA200,
    REQUIRE_BENCH_ABOVE_MA200,
    REQUIRE_BULL_MARKET,
    REQUIRE_MACD_POSITIVE,
    REWARD_RISK_RATIO,
    RISK_PER_TRADE_PCT,
    SIGNAL_MAX_HOLD_DAYS,
    STRATEGY_NAME,
    STRATEGY_VERSION,
    USE_TRAILING_STOP,
    WATCH_SCORE,
)
from strategy_exit import effective_stop, initial_stop_price
from strategy_scoring import MARKET_BENCHMARKS, MIN_BARS, score_series

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SIGNALS_FILE = DATA_DIR / "signals.json"
PAPER_FILE = DATA_DIR / "paper_account.json"
PAPER_STRATEGY_FILE = DATA_DIR / "paper_strategy.json"
VERSIONS_FILE = DATA_DIR / "strategy_versions.json"
DIAGNOSTICS_FILE = DATA_DIR / "diagnostics.json"
MARKET_FILE = DATA_DIR / "market.json"

XIAOMI_SIGNAL_ID = f"xiaomi:{PAPER_SYMBOL}"


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
                    "buyScore": BUY_SCORE,
                    "breakoutScoreMin": BREAKOUT_SCORE_MIN,
                    "watchScore": WATCH_SCORE,
                    "rewardRiskRatio": REWARD_RISK_RATIO,
                    "maxHoldDays": SIGNAL_MAX_HOLD_DAYS,
                    "requireBullMarket": REQUIRE_BULL_MARKET,
                    "paperBuyOnly": PAPER_BUY_ONLY,
                    "focusSymbol": PAPER_SYMBOL,
                },
            }
        )
    data["current"] = STRATEGY_VERSION
    data["versions"] = versions
    save_json(VERSIONS_FILE, data)
    return data


def score_xiaomi(quote_map: dict[str, float]) -> dict | None:
    """对小米 1810.HK 打分（需 ≥200 根 K 线用于 MA200）。"""
    try:
        hist = yf.Ticker(PAPER_SYMBOL).history(period="max", interval="1d")
        bench_hist = yf.Ticker(MARKET_BENCHMARKS[PAPER_SYMBOL_MARKET]).history(period="max", interval="1d")
    except Exception:
        return None
    if hist.empty or len(hist) < MIN_BARS:
        return None

    closes = [float(v) for v in hist["Close"].tolist()]
    highs = [float(v) for v in hist["High"].tolist()]
    lows = [float(v) for v in hist["Low"].tolist()]
    volumes = [float(v) for v in hist["Volume"].tolist()]
    bench_closes = [float(v) for v in bench_hist["Close"].tolist()] if not bench_hist.empty else []

    scored = score_series(closes, highs, lows, volumes, bench_closes, PAPER_SYMBOL_MARKET)
    if not scored:
        return None

    price = quote_map.get(PAPER_SYMBOL) or closes[-1]
    scored["price"] = price
    return scored


def create_signal_from_score(scored: dict, now: datetime) -> dict:
    price = scored["price"]
    atr = scored.get("atr") or price * 0.02
    stop = scored.get("stopLossPrice") or initial_stop_price(price, atr)
    return {
        "id": XIAOMI_SIGNAL_ID,
        "recordId": "xiaomi-live",
        "symbol": PAPER_SYMBOL,
        "name": PAPER_SYMBOL_NAME,
        "market": PAPER_SYMBOL_MARKET,
        "currency": "HKD",
        "strategyVersion": STRATEGY_VERSION,
        "signal": scored.get("signal"),
        "signalLabel": scored.get("signalLabel"),
        "entryType": scored.get("entryType"),
        "score": scored.get("score"),
        "entryPrice": price,
        "stopLossPrice": stop,
        "targetPrice": scored.get("targetPrice"),
        "atr": atr,
        "highestPrice": price,
        "openedAt": now.isoformat(timespec="seconds"),
        "status": "open",
        "currentPrice": price,
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

    atr = signal.get("atr") or entry * 0.02
    highest = round(max(signal.get("highestPrice", entry), price), 2)
    signal["highestPrice"] = highest
    current_stop = signal.get("stopLossPrice", initial_stop_price(entry, atr))
    signal["stopLossPrice"] = effective_stop(entry, atr, highest, current_stop)
    stop = signal["stopLossPrice"]

    if stop and price <= stop:
        init_stop = initial_stop_price(entry, atr)
        if USE_TRAILING_STOP and stop > init_stop:
            signal["status"] = "closed_trail"
            signal["closeReason"] = "触发跟踪止损"
        else:
            signal["status"] = "closed_stop"
            signal["closeReason"] = "触发止损"
        signal["closedAt"] = now.isoformat(timespec="seconds")
    elif hold_days >= SIGNAL_MAX_HOLD_DAYS:
        signal["status"] = "closed_expired"
        signal["closeReason"] = f"持有超 {SIGNAL_MAX_HOLD_DAYS} 天"
        signal["closedAt"] = now.isoformat(timespec="seconds")


def sync_signals(quote_map: dict[str, float], now: datetime) -> dict:
    data = load_json(SIGNALS_FILE, {"signals": []})
    signals: list[dict] = [s for s in data.get("signals", []) if s.get("symbol") == PAPER_SYMBOL]

    scored = score_xiaomi(quote_map)
    open_signal = next((s for s in signals if s["status"] == "open"), None)

    if scored and scored.get("signal") == "buy" and open_signal is None:
        signals.append(create_signal_from_score(scored, now))
    elif open_signal:
        price = quote_map.get(PAPER_SYMBOL) or scored.get("price") if scored else open_signal["entryPrice"]
        if price is not None:
            update_open_signal(open_signal, price, now)
        if scored and open_signal["status"] == "open":
            open_signal["score"] = scored.get("score")
            open_signal["signal"] = scored.get("signal")
            open_signal["signalLabel"] = scored.get("signalLabel")
            if scored.get("atr"):
                open_signal["atr"] = scored["atr"]

    data["signals"] = signals[-100:]
    data["focusSymbol"] = PAPER_SYMBOL
    data["updatedAt"] = now.isoformat(timespec="seconds")
    data["openCount"] = sum(1 for s in signals if s["status"] == "open")
    data["closedCount"] = sum(1 for s in signals if s["status"] != "open")
    save_json(SIGNALS_FILE, data)
    print(f"Wrote {SIGNALS_FILE} ({len(signals)} signals, {data['openCount']} open)")
    return data


def reset_paper_account(now: datetime) -> dict:
    return {
        "initialCash": PAPER_INITIAL_CASH,
        "cash": PAPER_INITIAL_CASH,
        "equity": PAPER_INITIAL_CASH,
        "positions": [],
        "trades": [],
        "equityCurve": [],
        "focusSymbol": PAPER_SYMBOL,
        "focusName": PAPER_SYMBOL_NAME,
        "focusHkCode": PAPER_SYMBOL_HK_CODE,
        "updatedAt": now.isoformat(timespec="seconds"),
    }


def position_size_pct(score: float, signal_type: str) -> float:
    if signal_type == "buy":
        return min(20.0 + (score - BUY_SCORE) * 0.5, 25.0)
    return 10.0


def append_equity_point(curve: list[dict], now: datetime, equity: float) -> list[dict]:
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
        reset_paper_account(now),
    )

    if account.get("focusSymbol") != PAPER_SYMBOL:
        print(f"Migrating paper account to {PAPER_SYMBOL} (was {account.get('focusSymbol', 'unknown')})")
        account = reset_paper_account(now)

    positions = {p["symbol"]: p for p in account.get("positions", []) if p["symbol"] == PAPER_SYMBOL}
    account["positions"] = list(positions.values())
    trades = account.get("trades", [])

    open_signals = [
        s for s in signals_data.get("signals", [])
        if s["status"] == "open" and s["symbol"] == PAPER_SYMBOL
    ]
    for sig in open_signals:
        if len(positions) >= PAPER_MAX_POSITIONS:
            break
        if PAPER_SYMBOL in positions:
            continue
        if PAPER_BUY_ONLY and sig.get("signal") != "buy":
            continue

        price = quote_map.get(PAPER_SYMBOL) or sig["entryPrice"]
        alloc_pct = position_size_pct(sig.get("score", 60), sig.get("signal", "watch"))
        equity = account.get("equity", account["cash"])
        amount = equity * alloc_pct / 100
        if amount > account["cash"] or price <= 0:
            continue

        shares = round(amount / price, 4)
        cost = round(shares * price, 2)
        account["cash"] = round(account["cash"] - cost, 2)
        positions[PAPER_SYMBOL] = {
            "symbol": PAPER_SYMBOL,
            "name": PAPER_SYMBOL_NAME,
            "market": PAPER_SYMBOL_MARKET,
            "shares": shares,
            "entryPrice": price,
            "cost": cost,
            "signalId": sig["id"],
            "openedAt": now.isoformat(timespec="seconds"),
        }
        trades.append(
            {
                "type": "buy",
                "symbol": PAPER_SYMBOL,
                "name": PAPER_SYMBOL_NAME,
                "price": price,
                "shares": shares,
                "amount": cost,
                "time": now.isoformat(timespec="seconds"),
                "signalId": sig["id"],
            }
        )

    closed_ids = {
        s["id"]
        for s in signals_data.get("signals", [])
        if s["status"] != "open" and s.get("closedAt") and s["symbol"] == PAPER_SYMBOL
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

    position_value = sum(
        pos["shares"] * (quote_map.get(sym) or pos["entryPrice"]) for sym, pos in positions.items()
    )
    account["positions"] = list(positions.values())
    account["equity"] = round(account["cash"] + position_value, 2)
    account["returnPct"] = pct_change(account["equity"], account["initialCash"])
    account["trades"] = trades[-200:]
    account["focusSymbol"] = PAPER_SYMBOL
    account["focusName"] = PAPER_SYMBOL_NAME
    account["focusHkCode"] = PAPER_SYMBOL_HK_CODE

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

    close_reasons: dict[str, int] = {}
    for s in closed:
        r = s.get("closeReason") or s.get("status", "unknown")
        close_reasons[r] = close_reasons.get(r, 0) + 1

    suggestions = []
    if win_rate is not None and win_rate < 50:
        suggestions.append("小米信号胜率偏低，建议提高 BUY_SCORE 阈值或加强市场环境过滤。")
    if paper.get("returnPct") is not None and paper["returnPct"] < 0:
        suggestions.append("模拟账户亏损，建议缩小仓位或暂停弱信号开仓。")
    if backtest and backtest.get("metrics", {}).get("expectancy", 0) < 0:
        suggestions.append("回测期望值为负，策略需优化参数后再实盘。")
    if not suggestions:
        suggestions.append("小米模拟盘运行正常，继续保持纪律性交易与定期回测。")

    diag = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "strategyVersion": STRATEGY_VERSION,
        "focusSymbol": PAPER_SYMBOL,
        "summary": {
            "openSignals": len(open_sigs),
            "closedSignals": tracked,
            "winRate": win_rate,
            "avgReturn": avg_return,
            "paperReturn": paper.get("returnPct"),
            "backtestExpectancy": (backtest or {}).get("metrics", {}).get("expectancy"),
        },
        "closeReasons": close_reasons,
        "suggestions": suggestions,
    }
    save_json(DIAGNOSTICS_FILE, diag)
    print(f"Wrote {DIAGNOSTICS_FILE}")
    return diag


def build_paper_strategy(now: datetime) -> dict:
    buy_only_label = "仅 buy 信号" if PAPER_BUY_ONLY else "buy 与 watch 信号"
    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "strategyVersion": STRATEGY_VERSION,
        "strategyName": STRATEGY_NAME,
        "focusSymbol": PAPER_SYMBOL,
        "focusName": PAPER_SYMBOL_NAME,
        "focusHkCode": PAPER_SYMBOL_HK_CODE,
        "summary": f"专注 {PAPER_SYMBOL_NAME}：Regime 过滤 + 平台突破/趋势双入场 + ATR 跟踪止损，适配港股一波流。",
        "schedule": "每 5 分钟（GitHub Actions update-market-data）",
        "account": {
            "initialCash": PAPER_INITIAL_CASH,
            "maxPositions": PAPER_MAX_POSITIONS,
            "buyOnly": PAPER_BUY_ONLY,
            "buyOnlyLabel": buy_only_label,
        },
        "flow": [
            {"step": 1, "title": "Regime 过滤", "desc": "个股与恒指均在 MA200 之上，且恒指站上 MA60，否则禁止做多。"},
            {"step": 2, "title": "入场信号", "desc": f"突破 {BREAKOUT_LOOKBACK} 日平台且放量 ≥{BREAKOUT_VOLUME_RATIO}x；或趋势评分 ≥{BUY_SCORE} 且价 > MA20 > MA60。"},
            {"step": 3, "title": "自动买入", "desc": f"buy 信号开仓，最多 {PAPER_MAX_POSITIONS} 仓，按评分分配 20～25% 仓位。"},
            {"step": 4, "title": "跟踪止损", "desc": f"初始止损 {ATR_STOP_INITIAL}×ATR；盈利后 {ATR_TRAILING}×ATR 跟踪，保本后止损不低于成本。"},
            {"step": 5, "title": "自动卖出", "desc": f"触发止损/跟踪止损，或持有满 {SIGNAL_MAX_HOLD_DAYS} 天到期平仓。"},
        ],
        "buyRules": [
            {"id": "regime", "label": "Regime", "value": "多头环境", "detail": "小米与恒指均在 MA200 之上"},
            {"id": "breakout", "label": "突破入场", "value": f"{BREAKOUT_LOOKBACK} 日新高 + 放量", "detail": f"评分 ≥ {BREAKOUT_SCORE_MIN}，RSI ≤ {MAX_RSI_ENTRY}"},
            {"id": "trend", "label": "趋势入场", "value": f"评分 ≥ {BUY_SCORE}", "detail": "价 > MA20 > MA60，相对强度 ≥ 0"},
            {"id": "max_pos", "label": "仓位上限", "value": f"最多 {PAPER_MAX_POSITIONS} 只", "detail": "专注单标的"},
            {"id": "cash", "label": "资金约束", "value": "可用现金充足", "detail": "分配金额超过现金则跳过"},
        ],
        "sellRules": [
            {"id": "stop", "label": "初始止损", "value": f"入场 − {ATR_STOP_INITIAL}×ATR", "detail": "宽止损适应港股波动"},
            {"id": "trail", "label": "跟踪止损", "value": f"最高价 − {ATR_TRAILING}×ATR", "detail": "盈利后让利润奔跑，只上移不下移"},
            {"id": "breakeven", "label": "保本", "value": "盈利 ≥ 1×ATR", "detail": "止损上移至成本价"},
            {"id": "expiry", "label": "到期平仓", "value": f"持有 ≥ {SIGNAL_MAX_HOLD_DAYS} 天", "detail": "超期按现价强制平仓"},
        ],
        "positionSizing": {
            "formula": "buy 信号：min(20 + (评分 − BUY) × 0.5, 25)% × 当前净值",
            "buyScoreBase": BUY_SCORE,
            "minPct": 20.0,
            "maxPct": MAX_POSITION_PCT,
            "watchPct": 10.0,
            "note": "突破入场评分门槛可低至 68 分",
        },
        "signalFilters": [
            {"label": "趋势评分门槛", "value": f"≥ {BUY_SCORE}", "enabled": True},
            {"label": "突破评分门槛", "value": f"≥ {BREAKOUT_SCORE_MIN}", "enabled": True},
            {"label": "个股 MA200", "value": "收盘价在 200 日均线之上", "enabled": REQUIRE_ABOVE_MA200},
            {"label": "恒指 MA200", "value": "恒指在 200 日均线之上", "enabled": REQUIRE_BENCH_ABOVE_MA200},
            {"label": "恒指 MA60", "value": "大盘多头过滤", "enabled": REQUIRE_BULL_MARKET},
            {"label": "RSI 上限", "value": f"≤ {MAX_RSI_ENTRY}", "enabled": True},
            {"label": "相对强度", "value": f"≥ {MIN_RELATIVE_STRENGTH}%", "enabled": True},
            {"label": "MACD 柱", "value": "趋势入场时需 > 0", "enabled": REQUIRE_MACD_POSITIVE},
        ],
        "riskParams": {
            "riskPerTradePct": RISK_PER_TRADE_PCT,
            "rewardRiskRatio": REWARD_RISK_RATIO,
            "maxHoldDays": SIGNAL_MAX_HOLD_DAYS,
            "atrStopInitial": ATR_STOP_INITIAL,
            "atrTrailing": ATR_TRAILING,
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
