#!/usr/bin/env python3
"""Fetch global market indices, watchlist stocks, and news for the dashboard."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "market.json"

INDICES = {
    "^GSPC": {"name": "标普 500", "region": "美国", "currency": "USD"},
    "^DJI": {"name": "道琼斯", "region": "美国", "currency": "USD"},
    "^IXIC": {"name": "纳斯达克", "region": "美国", "currency": "USD"},
    "^HSI": {"name": "恒生指数", "region": "香港", "currency": "HKD"},
    "^N225": {"name": "日经 225", "region": "日本", "currency": "JPY"},
    "000001.SS": {"name": "上证指数", "region": "中国", "currency": "CNY"},
}

STOCKS = {
    "1810.HK": {"name": "小米集团", "sector": "消费电子", "currency": "HKD"},
    "9992.HK": {"name": "泡泡玛特", "sector": "潮玩零售", "currency": "HKD"},
    "000660.KS": {"name": "SK 海力士", "sector": "半导体", "currency": "KRW"},
}

NEWS_TICKERS = ["^GSPC", "1810.HK", "9992.HK", "000660.KS"]

# 荐股候选池：流动性好的大盘股，覆盖美股科技与港股核心资产
CANDIDATES = {
    "AAPL": {"name": "苹果", "sector": "消费电子", "currency": "USD"},
    "MSFT": {"name": "微软", "sector": "软件云计算", "currency": "USD"},
    "NVDA": {"name": "英伟达", "sector": "半导体", "currency": "USD"},
    "GOOGL": {"name": "谷歌", "sector": "互联网", "currency": "USD"},
    "AMZN": {"name": "亚马逊", "sector": "电商云计算", "currency": "USD"},
    "META": {"name": "Meta", "sector": "社交广告", "currency": "USD"},
    "TSLA": {"name": "特斯拉", "sector": "新能源车", "currency": "USD"},
    "AMD": {"name": "AMD", "sector": "半导体", "currency": "USD"},
    "0700.HK": {"name": "腾讯控股", "sector": "互联网", "currency": "HKD"},
    "9988.HK": {"name": "阿里巴巴", "sector": "电商云计算", "currency": "HKD"},
    "3690.HK": {"name": "美团", "sector": "本地生活", "currency": "HKD"},
    "1810.HK": {"name": "小米集团", "sector": "消费电子", "currency": "HKD"},
    "9992.HK": {"name": "泡泡玛特", "sector": "潮玩零售", "currency": "HKD"},
    "000660.KS": {"name": "SK 海力士", "sector": "半导体", "currency": "KRW"},
}

# 策略参数
RISK_PER_TRADE_PCT = 2.0   # 单笔交易最大亏损占总资金比例
REWARD_RISK_RATIO = 2.0    # 目标盈亏比
BUY_SCORE = 70             # 达到该分数给出买入信号
WATCH_SCORE = 55           # 达到该分数列入观察
MAX_PICKS = 3


def pct_change(current: float, previous: float) -> float | None:
    if previous in (0, None) or current is None:
        return None
    return round((current - previous) / previous * 100, 2)


def fetch_quote(symbol: str, meta: dict) -> dict:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="3mo", interval="1d")
    info = {}
    try:
        info = ticker.fast_info
    except Exception:
        info = {}

    latest_close = None
    prev_close = None
    sparkline: list[float] = []

    if not hist.empty:
        closes = hist["Close"].dropna()
        if len(closes) >= 1:
            latest_close = round(float(closes.iloc[-1]), 2)
            sparkline = [round(float(v), 2) for v in closes.tail(30).tolist()]
        if len(closes) >= 2:
            prev_close = round(float(closes.iloc[-2]), 2)

    change = None
    change_pct = None
    if latest_close is not None and prev_close is not None:
        change = round(latest_close - prev_close, 2)
        change_pct = pct_change(latest_close, prev_close)

    week_ago_close = None
    month_ago_close = None
    if not hist.empty:
        closes = hist["Close"].dropna()
        if len(closes) >= 6:
            week_ago_close = float(closes.iloc[-6])
        if len(closes) >= 22:
            month_ago_close = float(closes.iloc[-22])

    return {
        "symbol": symbol,
        "name": meta["name"],
        "region": meta.get("region"),
        "sector": meta.get("sector"),
        "currency": meta.get("currency", "USD"),
        "price": latest_close,
        "change": change,
        "changePct": change_pct,
        "weekChangePct": pct_change(latest_close, week_ago_close) if week_ago_close else None,
        "monthChangePct": pct_change(latest_close, month_ago_close) if month_ago_close else None,
        "sparkline": sparkline,
        "marketCap": getattr(info, "market_cap", None) if hasattr(info, "market_cap") else info.get("market_cap"),
        "volume": getattr(info, "last_volume", None) if hasattr(info, "last_volume") else info.get("last_volume"),
    }


def fetch_news() -> list[dict]:
    seen: set[str] = set()
    articles: list[dict] = []

    for symbol in NEWS_TICKERS:
        try:
            items = yf.Ticker(symbol).news or []
        except Exception:
            items = []

        for item in items[:6]:
            title = item.get("title", "").strip()
            link = item.get("link") or item.get("url") or ""
            if not title or title in seen:
                continue
            seen.add(title)
            published = item.get("providerPublishTime")
            published_iso = None
            if published:
                published_iso = datetime.fromtimestamp(published, tz=timezone.utc).isoformat()
            articles.append(
                {
                    "title": title,
                    "link": link,
                    "publisher": item.get("publisher", "Yahoo Finance"),
                    "related": symbol,
                    "publishedAt": published_iso,
                }
            )

    articles.sort(key=lambda x: x.get("publishedAt") or "", reverse=True)
    return articles[:18]


def compute_rsi(closes: list[float], period: int = 14) -> float | None:
    """Wilder 平滑 RSI。"""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - 100 / (1 + rs), 1)


def compute_atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> float | None:
    """平均真实波幅，用于设定止损宽度。"""
    if len(closes) < period + 1:
        return None
    trs = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    return round(sum(trs[-period:]) / period, 4)


def sma(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def analyze_candidate(symbol: str, meta: dict) -> dict | None:
    """趋势跟踪 + 动量评分策略。

    评分维度（满分 100）：
    - 趋势（40 分）：价格在 20 日 / 60 日均线上方，且短均线在长均线上方（多头排列）
    - 动量（30 分）：1 月 / 3 月相对涨幅，奖励持续走强的标的
    - RSI 健康度（20 分）：45-65 为理想趋势区，>75 视为超买扣分
    - 量能（10 分）：近 5 日均量高于 20 日均量，代表资金关注
    """
    try:
        hist = yf.Ticker(symbol).history(period="6mo", interval="1d")
    except Exception:
        return None
    if hist.empty:
        return None

    closes = [float(v) for v in hist["Close"].dropna().tolist()]
    highs = [float(v) for v in hist["High"].dropna().tolist()]
    lows = [float(v) for v in hist["Low"].dropna().tolist()]
    volumes = [float(v) for v in hist["Volume"].dropna().tolist()]
    if len(closes) < 65:
        return None

    price = closes[-1]
    sma20 = sma(closes, 20)
    sma60 = sma(closes, 60)
    rsi = compute_rsi(closes)
    atr = compute_atr(highs, lows, closes)
    month_chg = pct_change(price, closes[-22]) if len(closes) >= 22 else None
    quarter_chg = pct_change(price, closes[0])

    if not all(v is not None for v in (sma20, sma60, rsi, atr, month_chg, quarter_chg)):
        return None

    score = 0.0
    reasons: list[str] = []

    # 趋势 40 分
    if price > sma20:
        score += 15
        reasons.append("价格站上 20 日均线")
    if price > sma60:
        score += 10
        reasons.append("价格站上 60 日均线")
    if sma20 > sma60:
        score += 15
        reasons.append("均线多头排列（20日 > 60日）")

    # 动量 30 分
    if month_chg > 0:
        score += min(month_chg * 1.5, 15)
        reasons.append(f"近 1 月上涨 {month_chg:.1f}%")
    if quarter_chg > 0:
        score += min(quarter_chg * 0.5, 15)
        reasons.append(f"近 3 月上涨 {quarter_chg:.1f}%")

    # RSI 健康度 20 分
    if 45 <= rsi <= 65:
        score += 20
        reasons.append(f"RSI {rsi} 处于健康趋势区")
    elif 35 <= rsi < 45 or 65 < rsi <= 75:
        score += 10
        reasons.append(f"RSI {rsi} 中性")
    elif rsi > 75:
        score -= 10
        reasons.append(f"RSI {rsi} 超买，注意追高风险")

    # 量能 10 分
    vol5, vol20 = sma(volumes, 5), sma(volumes, 20)
    if vol5 and vol20 and vol5 > vol20:
        score += 10
        reasons.append("近期成交量放大，资金关注度提升")

    score = round(max(score, 0), 1)

    if score >= BUY_SCORE:
        signal, signal_label = "buy", "建议买入"
    elif score >= WATCH_SCORE:
        signal, signal_label = "watch", "建议观察"
    else:
        signal, signal_label = "hold", "暂不参与"

    # 操作计划：ATR 止损 + 固定盈亏比目标 + 风险敞口决定仓位
    stop_loss = round(price - 2 * atr, 2)
    target = round(price + 2 * atr * REWARD_RISK_RATIO, 2)
    stop_pct = round((price - stop_loss) / price * 100, 1)
    position_pct = round(min(RISK_PER_TRADE_PCT / stop_pct * 100, 30), 1) if stop_pct > 0 else 0

    digits = 2 if price >= 10 else 3
    plan = {
        "entry": f"现价 {price:.{digits}f} 附近分批买入，或回踩 20 日均线 {sma20:.{digits}f} 时加仓",
        "stopLoss": f"跌破 {stop_loss:.{digits}f}（约 -{stop_pct}%，2 倍 ATR）坚决止损",
        "target": f"目标价 {target:.{digits}f}（盈亏比 1:{REWARD_RISK_RATIO:.0f}），到达后可分批止盈",
        "position": f"建议仓位不超过总资金 {position_pct}%（单笔风险控制在 {RISK_PER_TRADE_PCT}% 以内）",
    }

    return {
        "symbol": symbol,
        "name": meta["name"],
        "sector": meta.get("sector"),
        "currency": meta.get("currency", "USD"),
        "price": round(price, 2),
        "score": score,
        "signal": signal,
        "signalLabel": signal_label,
        "rsi": rsi,
        "monthChangePct": month_chg,
        "reasons": reasons[:4],
        "plan": plan,
    }


def build_recommendations() -> dict:
    analyzed = []
    for symbol, meta in CANDIDATES.items():
        result = analyze_candidate(symbol, meta)
        if result:
            analyzed.append(result)

    analyzed.sort(key=lambda x: x["score"], reverse=True)
    picks = [a for a in analyzed if a["signal"] in ("buy", "watch")][:MAX_PICKS]

    return {
        "strategy": "趋势跟踪 + 动量评分：均线多头排列（40 分）、1/3 月动量（30 分）、RSI 健康度（20 分）、量能（10 分）；"
        f"得分 ≥{BUY_SCORE} 给出买入信号，≥{WATCH_SCORE} 列入观察。止损按 2 倍 ATR，目标盈亏比 1:{REWARD_RISK_RATIO:.0f}。",
        "disclaimer": "量化信号仅供参考，不构成投资建议。股市有风险，请严格执行止损纪律。",
        "picks": picks,
    }


def build_summary(indices: list[dict]) -> dict:
    valid = [i for i in indices if i.get("changePct") is not None]
    up = sum(1 for i in valid if i["changePct"] > 0)
    down = sum(1 for i in valid if i["changePct"] < 0)
    flat = len(valid) - up - down
    avg = round(sum(i["changePct"] for i in valid) / len(valid), 2) if valid else 0

    if avg > 0.3:
        mood = "偏多"
    elif avg < -0.3:
        mood = "偏空"
    else:
        mood = "震荡"

    return {
        "tracked": len(valid),
        "up": up,
        "down": down,
        "flat": flat,
        "avgChangePct": avg,
        "mood": mood,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    indices = [fetch_quote(symbol, meta) for symbol, meta in INDICES.items()]
    stocks = [fetch_quote(symbol, meta) for symbol, meta in STOCKS.items()]
    news = fetch_news()
    recommendations = build_recommendations()

    payload = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "summary": build_summary(indices),
        "indices": indices,
        "stocks": stocks,
        "news": news,
        "recommendations": recommendations,
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
