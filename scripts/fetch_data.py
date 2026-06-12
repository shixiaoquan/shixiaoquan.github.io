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

    payload = {
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "summary": build_summary(indices),
        "indices": indices,
        "stocks": stocks,
        "news": news,
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
