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
HISTORY_FILE = DATA_DIR / "reco_history.json"
MAX_HISTORY_RECORDS = 500
MIN_HISTORY_INTERVAL_MIN = 30  # 推荐不变时，至少间隔 30 分钟记一条

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

# 荐股候选池：按市场分组，覆盖 A 股 / 港股 / 美股
CANDIDATES = {
    # A 股
    "600519.SS": {"name": "贵州茅台", "sector": "白酒", "currency": "CNY", "market": "A股"},
    "300750.SZ": {"name": "宁德时代", "sector": "新能源", "currency": "CNY", "market": "A股"},
    "601318.SS": {"name": "中国平安", "sector": "保险", "currency": "CNY", "market": "A股"},
    "000858.SZ": {"name": "五粮液", "sector": "白酒", "currency": "CNY", "market": "A股"},
    "688981.SS": {"name": "中芯国际", "sector": "半导体", "currency": "CNY", "market": "A股"},
    "600036.SS": {"name": "招商银行", "sector": "银行", "currency": "CNY", "market": "A股"},
    # 港股
    "0700.HK": {"name": "腾讯控股", "sector": "互联网", "currency": "HKD", "market": "港股"},
    "9988.HK": {"name": "阿里巴巴", "sector": "电商云计算", "currency": "HKD", "market": "港股"},
    "3690.HK": {"name": "美团", "sector": "本地生活", "currency": "HKD", "market": "港股"},
    "1810.HK": {"name": "小米集团", "sector": "消费电子", "currency": "HKD", "market": "港股"},
    "9992.HK": {"name": "泡泡玛特", "sector": "潮玩零售", "currency": "HKD", "market": "港股"},
    "9618.HK": {"name": "京东集团", "sector": "电商", "currency": "HKD", "market": "港股"},
    # 美股
    "AAPL": {"name": "苹果", "sector": "消费电子", "currency": "USD", "market": "美股"},
    "MSFT": {"name": "微软", "sector": "软件云计算", "currency": "USD", "market": "美股"},
    "NVDA": {"name": "英伟达", "sector": "半导体", "currency": "USD", "market": "美股"},
    "GOOGL": {"name": "谷歌", "sector": "互联网", "currency": "USD", "market": "美股"},
    "AMZN": {"name": "亚马逊", "sector": "电商云计算", "currency": "USD", "market": "美股"},
    "META": {"name": "Meta", "sector": "社交广告", "currency": "USD", "market": "美股"},
    "AMD": {"name": "AMD", "sector": "半导体", "currency": "USD", "market": "美股"},
}

# 各市场基准指数（用于相对强弱与市场环境判断）
MARKET_BENCHMARKS = {
    "A股": "000001.SS",
    "港股": "^HSI",
    "美股": "^GSPC",
}

# 策略参数
RISK_PER_TRADE_PCT = 2.0
REWARD_RISK_RATIO = 2.5
BUY_SCORE = 72
WATCH_SCORE = 58
MAX_PICKS_PER_MARKET = 1
MARKETS = ("A股", "港股", "美股")


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


def ema(values: list[float], period: int) -> list[float]:
    if not values:
        return []
    k = 2 / (period + 1)
    result = [values[0]]
    for v in values[1:]:
        result.append(v * k + result[-1] * (1 - k))
    return result


def compute_macd(closes: list[float]) -> tuple[float | None, float | None, float | None]:
    """返回 (MACD线, 信号线, 柱状图) 最新值。"""
    if len(closes) < 35:
        return None, None, None
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = [a - b for a, b in zip(ema12, ema26)]
    signal = ema(macd_line, 9)
    hist = macd_line[-1] - signal[-1]
    return round(macd_line[-1], 4), round(signal[-1], 4), round(hist, 4)


def fetch_benchmark_closes() -> dict[str, list[float]]:
    cache: dict[str, list[float]] = {}
    for market, symbol in MARKET_BENCHMARKS.items():
        try:
            hist = yf.Ticker(symbol).history(period="6mo", interval="1d")
            if not hist.empty:
                cache[market] = [float(v) for v in hist["Close"].dropna().tolist()]
        except Exception:
            continue
    return cache


def benchmark_return(closes: list[float], days: int) -> float | None:
    if len(closes) < days + 1:
        return None
    return pct_change(closes[-1], closes[-days - 1])


def price_digits(price: float) -> int:
    if price >= 1000:
        return 2
    if price >= 10:
        return 2
    return 3


def analyze_candidate(symbol: str, meta: dict, benchmarks: dict[str, list[float]]) -> dict | None:
    """多因子趋势策略（满分 100），覆盖 A 股 / 港股 / 美股。

  评分维度：
  - 趋势结构（25）：均线多头排列 + 价格结构
  - 动量（20）：1 月 / 3 月涨幅
  - 相对强弱（15）：跑赢所属市场基准指数
  - RSI（15）：趋势健康区，避免超买追高
  - MACD（10）：金叉或柱状图转正
  - 量能（10）：资金流入确认
  - 市场环境（5）：所属市场指数处于多头
  """
    market = meta.get("market", "美股")
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
    sma10 = sma(closes, 10)
    sma20 = sma(closes, 20)
    sma60 = sma(closes, 60)
    rsi = compute_rsi(closes)
    atr = compute_atr(highs, lows, closes)
    macd, macd_signal, macd_hist = compute_macd(closes)
    month_chg = pct_change(price, closes[-22]) if len(closes) >= 22 else None
    quarter_chg = pct_change(price, closes[-63]) if len(closes) >= 63 else pct_change(price, closes[0])

    bench = benchmarks.get(market, [])
    bench_month = benchmark_return(bench, 22) if bench else None
    rel_strength = round(month_chg - bench_month, 2) if month_chg is not None and bench_month is not None else None

    if not all(v is not None for v in (sma20, sma60, rsi, atr, month_chg, quarter_chg, macd, macd_signal, macd_hist)):
        return None

    score = 0.0
    reasons: list[str] = []

    # 趋势结构 25 分
    if price > sma20:
        score += 8
        reasons.append("价格站上 20 日均线")
    if price > sma60:
        score += 7
        reasons.append("价格站上 60 日均线")
    if sma10 and sma10 > sma20 > sma60:
        score += 10
        reasons.append("均线多头排列（10日 > 20日 > 60日）")
    elif sma20 > sma60:
        score += 5
        reasons.append("中期均线多头排列")

    # 动量 20 分
    if month_chg > 0:
        score += min(month_chg * 1.2, 10)
        reasons.append(f"近 1 月上涨 {month_chg:.1f}%")
    if quarter_chg > 0:
        score += min(quarter_chg * 0.4, 10)
        reasons.append(f"近 3 月上涨 {quarter_chg:.1f}%")

    # 相对强弱 15 分（跑赢所属市场才有超额收益潜力）
    if rel_strength is not None:
        if rel_strength > 5:
            score += 15
            reasons.append(f"近 1 月跑赢{market}基准 {rel_strength:.1f}%")
        elif rel_strength > 0:
            score += 10
            reasons.append(f"近 1 月略强于{market}基准")
        elif rel_strength > -3:
            score += 4
        else:
            score -= 5
            reasons.append(f"近 1 月弱于{market}基准 {rel_strength:.1f}%")

    # RSI 15 分
    if 48 <= rsi <= 62:
        score += 15
        reasons.append(f"RSI {rsi} 趋势健康区")
    elif 40 <= rsi < 48:
        score += 10
        reasons.append(f"RSI {rsi} 偏低，关注反弹")
    elif 62 < rsi <= 70:
        score += 8
        reasons.append(f"RSI {rsi} 偏强")
    elif rsi > 75:
        score -= 12
        reasons.append(f"RSI {rsi} 超买，不宜追高")
    else:
        score += 3

    # MACD 10 分
    if macd > macd_signal and macd_hist > 0:
        score += 10
        reasons.append("MACD 金叉且柱状图转正")
    elif macd_hist > 0:
        score += 6
        reasons.append("MACD 动能回升")
    elif macd > macd_signal:
        score += 4

    # 量能 10 分
    vol5, vol20 = sma(volumes, 5), sma(volumes, 20)
    if vol5 and vol20:
        vol_ratio = vol5 / vol20
        if vol_ratio > 1.3:
            score += 10
            reasons.append("成交量显著放大")
        elif vol_ratio > 1.05:
            score += 6
            reasons.append("成交量温和放大")

    # 市场环境 5 分
    if bench and len(bench) >= 60:
        bench_price = bench[-1]
        bench_sma60 = sma(bench, 60)
        if bench_sma60 and bench_price > bench_sma60:
            score += 5
            reasons.append(f"{market}大盘处于中期上升趋势")
        elif bench_sma60 and bench_price < bench_sma60:
            score -= 3
            reasons.append(f"{market}大盘偏弱，注意系统性风险")

    score = round(max(min(score, 100), 0), 1)

    if score >= BUY_SCORE:
        signal, signal_label = "buy", "建议买入"
    elif score >= WATCH_SCORE:
        signal, signal_label = "watch", "建议观察"
    else:
        signal, signal_label = "hold", "暂不参与"

    # 动态止损：趋势强用 1.5 倍 ATR，一般趋势 2 倍 ATR
    atr_mult = 1.5 if score >= BUY_SCORE and sma10 and sma10 > sma20 > sma60 else 2.0
    stop_loss = round(price - atr_mult * atr, 2)
    target = round(price + atr_mult * atr * REWARD_RISK_RATIO, 2)
    stop_pct = round((price - stop_loss) / price * 100, 1)
    position_pct = round(min(RISK_PER_TRADE_PCT / stop_pct * 100, 25), 1) if stop_pct > 0 else 0

    digits = price_digits(price)
    pullback_zone = round(sma20 * 0.98, digits)
    plan = {
        "entry": (
            f"现价 {price:.{digits}f} 轻仓试探；回踩 20 日均线 {sma20:.{digits}f} "
            f"或 {pullback_zone:.{digits}f} 附近分批加仓"
        ),
        "stopLoss": f"跌破 {stop_loss:.{digits}f}（约 -{stop_pct}%，{atr_mult:.1f} 倍 ATR）坚决止损",
        "target": f"第一目标 {target:.{digits}f}（盈亏比 1:{REWARD_RISK_RATIO:.1f}），可分批止盈",
        "position": (
            f"{market}标的建议仓位 ≤ 总资金 {position_pct}%"
            f"（单笔风险 {RISK_PER_TRADE_PCT}%）；三市场分散配置"
        ),
    }

    return {
        "symbol": symbol,
        "name": meta["name"],
        "market": market,
        "sector": meta.get("sector"),
        "currency": meta.get("currency", "USD"),
        "price": round(price, 2),
        "score": score,
        "signal": signal,
        "signalLabel": signal_label,
        "rsi": rsi,
        "monthChangePct": month_chg,
        "relativeStrength": rel_strength,
        "reasons": reasons[:5],
        "plan": plan,
    }


def build_recommendations() -> dict:
    benchmarks = fetch_benchmark_closes()
    analyzed = []
    for symbol, meta in CANDIDATES.items():
        result = analyze_candidate(symbol, meta, benchmarks)
        if result:
            analyzed.append(result)

    # 每个市场各选评分最高且达观察门槛的 1 只，确保 A 股 / 港股 / 美股全覆盖
    picks: list[dict] = []
    for market in MARKETS:
        market_pool = [a for a in analyzed if a["market"] == market and a["signal"] in ("buy", "watch")]
        market_pool.sort(key=lambda x: x["score"], reverse=True)
        if market_pool:
            picks.append(market_pool[0])
        else:
            # 该市场无达标标的时，展示最高分供参考（标记为观察）
            fallback = sorted(
                [a for a in analyzed if a["market"] == market],
                key=lambda x: x["score"],
                reverse=True,
            )
            if fallback and fallback[0]["score"] >= 45:
                top = fallback[0].copy()
                top["signal"] = "watch"
                top["signalLabel"] = "弱信号观察"
                picks.append(top)

    picks.sort(key=lambda x: (0 if x["signal"] == "buy" else 1, -x["score"]))

    market_summary = []
    for market in MARKETS:
        pool = [a for a in analyzed if a["market"] == market]
        if pool:
            best = max(pool, key=lambda x: x["score"])
            market_summary.append(f"{market}最高 {best['name']}({best['score']}分)")

    return {
        "strategy": (
            "多因子趋势策略（A股/港股/美股各选1只）：趋势结构25分、动量20分、"
            f"相对强弱15分、RSI15分、MACD10分、量能10分、市场环境5分；"
            f"≥{BUY_SCORE}买入，≥{WATCH_SCORE}观察。止损按ATR动态调整，盈亏比1:{REWARD_RISK_RATIO}。"
        ),
        "marketScan": " · ".join(market_summary),
        "disclaimer": "量化信号仅供参考，不构成投资建议。请分散配置三市场、严格执行止损。",
        "picks": picks[: len(MARKETS)],
    }, {a["symbol"]: a["price"] for a in analyzed if a.get("price")}


def compact_pick(pick: dict) -> dict:
    """压缩荐股快照，用于历史存储。"""
    return {
        "symbol": pick["symbol"],
        "name": pick["name"],
        "market": pick["market"],
        "sector": pick.get("sector"),
        "currency": pick.get("currency"),
        "price": pick["price"],
        "score": pick["score"],
        "signal": pick["signal"],
        "signalLabel": pick["signalLabel"],
        "rsi": pick.get("rsi"),
        "relativeStrength": pick.get("relativeStrength"),
        "plan": pick.get("plan", {}),
    }


def picks_fingerprint(picks: list[dict]) -> str:
    parts = sorted(f"{p['symbol']}:{p['signal']}:{round(p['score'])}" for p in picks)
    return "|".join(parts)


def load_reco_history() -> dict:
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("records"), list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"version": 1, "records": []}


def should_append_history(records: list[dict], picks: list[dict], recorded_at: datetime) -> bool:
    if not picks:
        return False
    if not records:
        return True

    last = records[-1]
    if picks_fingerprint(last.get("picks", [])) != picks_fingerprint(picks):
        return True

    try:
        last_time = datetime.fromisoformat(last["recordedAt"])
        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)
        current = recorded_at if recorded_at.tzinfo else recorded_at.replace(tzinfo=timezone.utc)
        elapsed_min = (current - last_time).total_seconds() / 60
        return elapsed_min >= MIN_HISTORY_INTERVAL_MIN
    except (KeyError, ValueError):
        return True


def append_reco_history(recommendations: dict, recorded_at: datetime) -> dict:
    """将本次荐股快照追加到 reco_history.json。"""
    picks = recommendations.get("picks") or []
    history = load_reco_history()
    records: list[dict] = history.get("records", [])

    if should_append_history(records, picks, recorded_at):
        records.append(
            {
                "id": recorded_at.isoformat(timespec="seconds"),
                "recordedAt": recorded_at.isoformat(timespec="seconds"),
                "marketScan": recommendations.get("marketScan", ""),
                "picks": [compact_pick(p) for p in picks],
            }
        )
        records = records[-MAX_HISTORY_RECORDS:]
        history["records"] = records
        history["updatedAt"] = recorded_at.isoformat(timespec="seconds")
        history["total"] = len(records)
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {HISTORY_FILE} ({len(records)} records)")
    else:
        print("Reco history unchanged, skip append.")

    return history


def build_market_radar(indices: list[dict]) -> list[dict]:
    """三市场雷达：从指数涨跌推断各市场当日强弱。"""
    groups = {
        "美股": ["^GSPC", "^DJI", "^IXIC"],
        "港股": ["^HSI"],
        "A股": ["000001.SS"],
    }
    by_symbol = {i["symbol"]: i for i in indices}
    radar = []
    for market, symbols in groups.items():
        valid = [by_symbol[s] for s in symbols if s in by_symbol and by_symbol[s].get("changePct") is not None]
        if not valid:
            continue
        avg = round(sum(v["changePct"] for v in valid) / len(valid), 2)
        if avg > 0.3:
            status, label = "strong", "偏强"
        elif avg < -0.3:
            status, label = "weak", "偏弱"
        else:
            status, label = "neutral", "震荡"
        radar.append({
            "market": market,
            "changePct": avg,
            "status": status,
            "label": label,
            "indices": [by_symbol[s]["name"] for s in symbols if s in by_symbol],
        })
    return radar


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
    recommendations, quote_map = build_recommendations()
    now = datetime.now(timezone.utc).astimezone()

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "summary": build_summary(indices),
        "marketRadar": build_market_radar(indices),
        "quoteMap": quote_map,
        "indices": indices,
        "stocks": stocks,
        "news": news,
        "recommendations": recommendations,
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")

    append_reco_history(recommendations, now)


if __name__ == "__main__":
    main()
