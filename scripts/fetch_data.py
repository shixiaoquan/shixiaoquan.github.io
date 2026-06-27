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
MAX_HISTORY_RECORDS = 200
SCORING_HISTORY_PERIOD = "2y"

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

NEWS_TICKERS = ["^GSPC", "^IXIC", "^HSI", "000001.SS", "1810.HK", "600519.SS", "AAPL", "NVDA"]

# 荐股候选池：按市场分组，覆盖 A 股 / 港股 / 美股
CANDIDATES = {
    # A 股
    "600519.SS": {"name": "贵州茅台", "sector": "白酒", "currency": "CNY", "market": "A股"},
    "300750.SZ": {"name": "宁德时代", "sector": "新能源", "currency": "CNY", "market": "A股"},
    "601318.SS": {"name": "中国平安", "sector": "保险", "currency": "CNY", "market": "A股"},
    "000858.SZ": {"name": "五粮液", "sector": "白酒", "currency": "CNY", "market": "A股"},
    "688981.SS": {"name": "中芯国际", "sector": "半导体", "currency": "CNY", "market": "A股"},
    "600036.SS": {"name": "招商银行", "sector": "银行", "currency": "CNY", "market": "A股"},
    "300308.SZ": {"name": "中际旭创", "sector": "光模块", "currency": "CNY", "market": "A股"},
    "688017.SS": {"name": "绿的谐波", "sector": "精密减速器", "currency": "CNY", "market": "A股"},
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

from strategy_config import (
    BREAKOUT_SCORE_MIN,
    BUY_SCORE,
    MIN_HISTORY_INTERVAL_MIN,
    RECO_PICK_STICKY_HOURS,
    REWARD_RISK_RATIO,
    RISK_PER_TRADE_PCT,
    STRATEGY_VERSION,
    WATCH_SCORE,
)
from strategy_scoring import (
    MARKET_BENCHMARKS,
    pct_change,
    price_digits,
    score_series,
    sma,
)
from reco_signals import update_reco_signals
from strategy_masters import build_master_recommendations

MAX_PICKS_PER_MARKET = 1
MARKETS = ("A股", "港股", "美股")


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



def normalize_news_item(item: dict, symbol: str) -> dict | None:
    """兼容 Yahoo Finance 新旧两种 news 返回格式。"""
    content = item.get("content") if isinstance(item.get("content"), dict) else item

    title = (content.get("title") or item.get("title") or "").strip()
    if not title:
        return None

    link = ""
    for key in ("clickThroughUrl", "canonicalUrl"):
        url_obj = content.get(key) or item.get(key)
        if isinstance(url_obj, dict) and url_obj.get("url"):
            link = url_obj["url"]
            break
    if not link:
        link = content.get("link") or content.get("url") or item.get("link") or item.get("url") or ""

    publisher = "Yahoo Finance"
    provider = content.get("provider") or item.get("publisher")
    if isinstance(provider, dict):
        publisher = provider.get("displayName") or publisher
    elif isinstance(provider, str):
        publisher = provider

    published_iso = None
    pub_date = content.get("pubDate") or content.get("displayTime")
    if pub_date:
        try:
            published_iso = datetime.fromisoformat(pub_date.replace("Z", "+00:00")).isoformat()
        except ValueError:
            published_iso = pub_date
    else:
        published = item.get("providerPublishTime")
        if published:
            published_iso = datetime.fromtimestamp(published, tz=timezone.utc).isoformat()

    summary = (content.get("summary") or content.get("description") or "").strip()

    return {
        "title": title,
        "link": link,
        "publisher": publisher,
        "related": symbol,
        "publishedAt": published_iso,
        "summary": summary[:200] if summary else "",
    }


def fetch_news() -> list[dict]:
    seen: set[str] = set()
    articles: list[dict] = []

    for symbol in NEWS_TICKERS:
        try:
            items = yf.Ticker(symbol).news or []
        except Exception:
            items = []

        for item in items[:8]:
            article = normalize_news_item(item, symbol)
            if not article or article["title"] in seen:
                continue
            seen.add(article["title"])
            articles.append(article)

    articles.sort(key=lambda x: x.get("publishedAt") or "", reverse=True)
    return articles[:20]


def fetch_benchmark_closes() -> dict[str, list[float]]:
    cache: dict[str, list[float]] = {}
    for market, symbol in MARKET_BENCHMARKS.items():
        try:
            hist = yf.Ticker(symbol).history(period=SCORING_HISTORY_PERIOD, interval="1d")
            if not hist.empty:
                cache[market] = [float(v) for v in hist["Close"].dropna().tolist()]
        except Exception:
            continue
    return cache


def analyze_candidate(symbol: str, meta: dict, benchmarks: dict[str, list[float]]) -> dict | None:
    """多因子趋势策略，评分逻辑与 strategy_scoring 模块一致。"""
    market = meta.get("market", "美股")
    try:
        hist = yf.Ticker(symbol).history(period=SCORING_HISTORY_PERIOD, interval="1d")
    except Exception:
        return None
    if hist.empty:
        return None

    closes = [float(v) for v in hist["Close"].dropna().tolist()]
    highs = [float(v) for v in hist["High"].dropna().tolist()]
    lows = [float(v) for v in hist["Low"].dropna().tolist()]
    volumes = [float(v) for v in hist["Volume"].dropna().tolist()]
    bench = benchmarks.get(market, [])

    scored = score_series(closes, highs, lows, volumes, bench, market, min_bars=65)
    if not scored:
        return None

    price = closes[-1]
    stop_loss = scored["stopLossPrice"]
    target = scored["targetPrice"]
    dist_stop = round((price - stop_loss) / price * 100, 1) if price and stop_loss else None
    dist_target = round((target - price) / price * 100, 1) if price and target else None
    atr_mult = scored["atrMult"]
    stop_pct = round((price - stop_loss) / price * 100, 1) if price else 0
    position_pct = round(min(RISK_PER_TRADE_PCT / stop_pct * 100, 25), 1) if stop_pct > 0 else 0
    digits = price_digits(price)
    sma20 = sma(closes, 20)
    pullback_zone = round(sma20 * 0.98, digits) if sma20 else price

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
        "score": scored["score"],
        "signal": scored["signal"],
        "signalLabel": scored["signalLabel"],
        "rsi": scored["rsi"],
        "monthChangePct": scored["monthChangePct"],
        "relativeStrength": scored["relativeStrength"],
        "reasons": scored["reasons"],
        "plan": plan,
        "stopLossPrice": stop_loss,
        "targetPrice": target,
        "distToStopPct": dist_stop,
        "distToTargetPct": dist_target,
        "regimeOk": scored.get("regimeOk"),
        "breakout": scored.get("breakout"),
        "breakoutLevel": scored.get("breakoutLevel"),
    }


def stabilize_picks(picks: list[dict], analyzed: list[dict], now: datetime) -> list[dict]:
    """v1.3：24 小时内不因小幅评分波动频繁换标的。"""
    if not OUTPUT_FILE.exists() or not picks:
        return picks
    try:
        prev = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        prev_time = datetime.fromisoformat(prev["updatedAt"])
        if prev_time.tzinfo is None:
            prev_time = prev_time.replace(tzinfo=timezone.utc)
        current = now if now.tzinfo else now.replace(tzinfo=timezone.utc)
        hours = (current - prev_time).total_seconds() / 3600
        if hours >= RECO_PICK_STICKY_HOURS:
            return picks
        prev_picks = prev.get("recommendations", {}).get("picks", [])
        if not prev_picks:
            return picks
    except (json.JSONDecodeError, OSError, KeyError, ValueError):
        return picks

    by_symbol = {a["symbol"]: a for a in analyzed}
    stabilized: list[dict] = []
    for market in MARKETS:
        new_pick = next((p for p in picks if p["market"] == market), None)
        if not new_pick:
            continue
        old_pick = next((p for p in prev_picks if p.get("market") == market), None)
        if not old_pick or old_pick.get("symbol") == new_pick.get("symbol"):
            stabilized.append(new_pick)
            continue
        fresh_old = by_symbol.get(old_pick["symbol"])
        fresh_new = by_symbol.get(new_pick["symbol"])
        if fresh_new and fresh_new.get("signal") == "buy" and fresh_old and fresh_old.get("signal") != "buy":
            stabilized.append(new_pick)
            continue
        if fresh_old and fresh_old.get("score", 0) >= WATCH_SCORE:
            stabilized.append(fresh_old)
        else:
            stabilized.append(new_pick)
    stabilized.sort(key=lambda x: (0 if x["signal"] == "buy" else 1, -x["score"]))
    return stabilized[: len(MARKETS)]


def build_recommendations(now: datetime | None = None) -> dict:
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
    picks = stabilize_picks(picks, analyzed, now or datetime.now(timezone.utc))

    market_summary = []
    for market in MARKETS:
        pool = [a for a in analyzed if a["market"] == market]
        if pool:
            best = max(pool, key=lambda x: x["score"])
            market_summary.append(f"{market}最高 {best['name']}({best['score']}分)")

    candidate_scan = sorted(
        [
            {
                "symbol": a["symbol"],
                "name": a["name"],
                "market": a["market"],
                "score": a["score"],
                "signal": a["signal"],
                "signalLabel": a["signalLabel"],
                "price": a.get("price"),
                "rsi": a.get("rsi"),
                "relativeStrength": a.get("relativeStrength"),
                "regimeOk": a.get("regimeOk"),
                "breakout": a.get("breakout"),
                "distToStopPct": a.get("distToStopPct"),
                "distToTargetPct": a.get("distToTargetPct"),
            }
            for a in analyzed
        ],
        key=lambda x: -x["score"],
    )

    return {
        "strategy": (
            f"{STRATEGY_VERSION} 强趋势+突破过滤（各市场 1 只）："
            f"Regime 过滤 + 仅突破买入；≥{BREAKOUT_SCORE_MIN} 突破分、≥{WATCH_SCORE} 观察。"
            f"24h 粘性换仓、止损 ATR、盈亏比 1:{REWARD_RISK_RATIO}。"
        ),
        "marketScan": " · ".join(market_summary),
        "disclaimer": "战术实验策略，仅供研究；非 XRPS 战役持仓。请分散配置、严格执行止损。",
        "picks": picks[: len(MARKETS)],
        "candidateScan": candidate_scan,
    }, {a["symbol"]: a["price"] for a in analyzed if a.get("price")}, {
        a["symbol"]: a["monthChangePct"]
        for a in analyzed
        if a.get("monthChangePct") is not None
    }


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
        "stopLossPrice": pick.get("stopLossPrice"),
        "targetPrice": pick.get("targetPrice"),
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


def append_reco_history(recommendations: dict, recorded_at: datetime) -> tuple[dict, str | None]:
    """将本次荐股快照追加到 reco_history.json。"""
    picks = recommendations.get("picks") or []
    history = load_reco_history()
    records: list[dict] = history.get("records", [])

    if should_append_history(records, picks, recorded_at):
        record_id = recorded_at.isoformat(timespec="seconds")
        records.append(
            {
                "id": record_id,
                "recordedAt": record_id,
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
        return history, record_id
    else:
        print("Reco history unchanged, skip append.")
        last_id = records[-1]["id"] if records else None
        return history, last_id


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

    now = datetime.now(timezone.utc).astimezone()
    indices = [fetch_quote(symbol, meta) for symbol, meta in INDICES.items()]
    stocks = [fetch_quote(symbol, meta) for symbol, meta in STOCKS.items()]
    news = fetch_news()
    recommendations, quote_map, change_map = build_recommendations(now)

    macro = None
    macro_file = DATA_DIR / "macro.json"
    if macro_file.exists():
        try:
            macro = json.loads(macro_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            macro = None

    market_ctx = {
        "summary": build_summary(indices),
        "marketRadar": build_market_radar(indices),
    }
    master_recommendations = build_master_recommendations(
        CANDIDATES, quote_map, market_ctx, macro, now
    )
    for item in stocks:
        if item.get("symbol") and item.get("changePct") is not None:
            change_map[item["symbol"]] = item["changePct"]

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "summary": build_summary(indices),
        "marketRadar": build_market_radar(indices),
        "quoteMap": quote_map,
        "changeMap": change_map,
        "indices": indices,
        "stocks": stocks,
        "news": news,
        "recommendations": recommendations,
        "masterRecommendations": master_recommendations,
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")

    history, reco_id = append_reco_history(recommendations, now)
    update_reco_signals(
        recommendations.get("picks") or [],
        quote_map,
        now,
        reco_record_id=reco_id,
    )


if __name__ == "__main__":
    main()
