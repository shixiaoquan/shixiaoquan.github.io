#!/usr/bin/env python3
"""拉取宏观、汇率、商品与行业 ETF — 免费数据源聚合。"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "macro.json"

USER_AGENT = "shixiaoquan-dashboard/1.0 (GitHub Pages; macro fetch)"

# Yahoo Finance — 风险、利率、商品、补充指数、行业 ETF
YAHOO_MACRO = {
    "^VIX": {"name": "VIX 恐慌指数", "category": "risk", "unit": "index"},
    "^TNX": {"name": "美国10年期国债收益率", "category": "rates", "unit": "yield_pct", "digits": 2},
    "^IRX": {"name": "美国13周国库券收益率", "category": "rates", "unit": "yield_pct", "digits": 2},
    "GC=F": {"name": "黄金期货", "category": "commodity", "unit": "USD/oz", "currency": "USD"},
    "CL=F": {"name": "WTI 原油", "category": "commodity", "unit": "USD/bbl", "currency": "USD"},
    "HG=F": {"name": "铜期货", "category": "commodity", "unit": "USD/lb", "currency": "USD"},
    "000300.SS": {"name": "沪深300", "category": "index", "region": "中国", "currency": "CNY"},
    "399006.SZ": {"name": "创业板指", "category": "index", "region": "中国", "currency": "CNY"},
    "000688.SS": {"name": "科创50", "category": "index", "region": "中国", "currency": "CNY"},
}

YAHOO_FX = {
    "USDCNH=X": {"name": "美元/离岸人民币", "base": "USD", "quote": "CNH"},
    "USDCNY=X": {"name": "美元/在岸人民币", "base": "USD", "quote": "CNY"},
    "USDHKD=X": {"name": "美元/港币", "base": "USD", "quote": "HKD"},
    "USDJPY=X": {"name": "美元/日元", "base": "USD", "quote": "JPY"},
    "EURUSD=X": {"name": "欧元/美元", "base": "EUR", "quote": "USD"},
}

SECTOR_ETFS = {
    "XLK": "科技",
    "XLF": "金融",
    "XLE": "能源",
    "XLV": "健康",
    "XLI": "工业",
    "XLY": "可选消费",
    "XLP": "必需消费",
    "XLU": "公用事业",
    "XLB": "材料",
    "XLRE": "地产",
    "XLC": "通信",
}

# FRED 宏观序列（需 FRED_API_KEY）
FRED_SERIES = {
    "DGS10": {"name": "美10年期国债收益率", "unit": "pct", "digits": 2},
    "T10Y2Y": {"name": "10Y-2Y 利差", "unit": "spread", "digits": 2},
    "FEDFUNDS": {"name": "联邦基金利率", "unit": "pct", "digits": 2},
    "UNRATE": {"name": "美国失业率", "unit": "pct", "digits": 1},
    "DEXCHUS": {"name": "美元/人民币(官方)", "unit": "rate", "digits": 4},
    "CPIAUCSL": {"name": "美国CPI指数", "unit": "index", "digits": 1},
}

FINNHUB_WATCH = ("AAPL", "NVDA", "1810.HK", "0700.HK", "688981.SS")


def pct_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None or previous == 0:
        return None
    return round((current - previous) / previous * 100, 2)


def fetch_yahoo_item(symbol: str, meta: dict) -> dict | None:
    try:
        hist = yf.Ticker(symbol).history(period="1mo", interval="1d")
    except Exception:
        return None
    if hist.empty:
        return None

    closes = hist["Close"].dropna()
    if len(closes) < 1:
        return None

    latest = float(closes.iloc[-1])
    prev = float(closes.iloc[-2]) if len(closes) >= 2 else None
    week = float(closes.iloc[-6]) if len(closes) >= 6 else None
    month = float(closes.iloc[-22]) if len(closes) >= 22 else None

    digits = meta.get("digits", 2)
    unit = meta.get("unit", "index")

    if unit == "yield_pct":
        price_display = round(latest, digits)
    else:
        price_display = round(latest, digits if digits else 2)

    return {
        "symbol": symbol,
        "name": meta["name"],
        "category": meta.get("category", "other"),
        "unit": unit,
        "currency": meta.get("currency"),
        "region": meta.get("region"),
        "price": price_display,
        "changePct": pct_change(latest, prev),
        "weekChangePct": pct_change(latest, week),
        "monthChangePct": pct_change(latest, month),
        "source": "yahoo",
    }


def fetch_frankfurter() -> tuple[list[dict], str]:
    """ECB 参考汇率（Frankfurter，无需 API Key）。"""
    url = "https://api.frankfurter.app/latest?from=USD&to=CNY,HKD,JPY,EUR,GBP,CHF,SGD"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return [], f"error: {exc}"

    rates = data.get("rates") or {}
    items = []
    for code, rate in rates.items():
        items.append(
            {
                "symbol": f"USD{code}",
                "name": f"美元/{code}",
                "base": "USD",
                "quote": code,
                "price": round(float(rate), 4),
                "changePct": None,
                "weekChangePct": None,
                "monthChangePct": None,
                "source": "frankfurter",
                "note": f"ECB 参考 {data.get('date', '')}",
            }
        )
    return items, "ok"


def fetch_er_api_fallback() -> tuple[list[dict], str]:
    """open.er-api.com 备用（无需 Key，日限额）。"""
    url = "https://open.er-api.com/v6/latest/USD"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return [], f"error: {exc}"

    rates = data.get("rates") or {}
    targets = ("CNY", "HKD", "JPY", "EUR", "GBP")
    items = []
    for code in targets:
        if code not in rates:
            continue
        items.append(
            {
                "symbol": f"USD{code}",
                "name": f"美元/{code}",
                "base": "USD",
                "quote": code,
                "price": round(float(rates[code]), 4),
                "changePct": None,
                "source": "exchangerate-api",
                "note": "open.er-api.com",
            }
        )
    return items, "ok"


def merge_fx(yahoo_fx: list[dict], static_fx: list[dict]) -> list[dict]:
    """Yahoo 提供涨跌，Frankfurter/ER-API 补充参考价。"""
    by_quote: dict[str, dict] = {}
    for item in yahoo_fx:
        sym = item.get("symbol", "")
        quote = sym.replace("USD", "").replace("=X", "").replace("CNH", "CNH")
        if "CNH" in sym:
            by_quote["CNH"] = item
        elif "CNY" in sym:
            by_quote["CNY"] = item
        elif "HKD" in sym:
            by_quote["HKD"] = item
        elif "JPY" in sym:
            by_quote["JPY"] = item
        elif "EUR" in sym:
            by_quote["EUR"] = item

    for item in static_fx:
        q = item.get("quote", "")
        if q in by_quote:
            by_quote[q]["refPrice"] = item["price"]
            by_quote[q]["refSource"] = item["source"]
            by_quote[q]["refNote"] = item.get("note")
        else:
            by_quote[q] = item

    order = ["CNH", "CNY", "HKD", "JPY", "EUR", "GBP", "CHF", "SGD"]
    result = []
    for q in order:
        if q in by_quote:
            result.append(by_quote[q])
    for q, item in by_quote.items():
        if q not in order:
            result.append(item)
    return result


def http_get_json(url: str, timeout: int = 25) -> dict | list | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def fetch_fred_series(api_key: str, series_id: str, meta: dict) -> dict | None:
    params = urllib.parse.urlencode(
        {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 6,
        }
    )
    url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
    data = http_get_json(url)
    if not isinstance(data, dict):
        return None

    obs = [o for o in data.get("observations", []) if o.get("value") not in (".", None, "")]
    if not obs:
        return None

    latest = obs[0]
    prev = obs[1] if len(obs) > 1 else None
    month_ago = obs[5] if len(obs) > 5 else None

    try:
        val = float(latest["value"])
        prev_val = float(prev["value"]) if prev else None
        month_val = float(month_ago["value"]) if month_ago else None
    except (TypeError, ValueError):
        return None

    digits = meta.get("digits", 2)
    change = pct_change(val, prev_val)
    if series_id == "CPIAUCSL" and month_val:
        change = pct_change(val, month_val)

    return {
        "seriesId": series_id,
        "name": meta["name"],
        "unit": meta.get("unit", "index"),
        "price": round(val, digits),
        "changePct": change,
        "observedAt": latest.get("date"),
        "source": "fred",
    }


def fetch_fred_all(api_key: str | None) -> tuple[list[dict], str]:
    if not api_key:
        return [], "missing_key"
    items = []
    errors = 0
    for series_id, meta in FRED_SERIES.items():
        row = fetch_fred_series(api_key, series_id, meta)
        if row:
            items.append(row)
        else:
            errors += 1
    status = "ok" if items else "error"
    if items and errors:
        status = "partial"
    return items, status


def fetch_finnhub_news(api_key: str | None, category: str = "general", limit: int = 8) -> list[dict]:
    if not api_key:
        return []
    params = urllib.parse.urlencode({"category": category, "token": api_key})
    data = http_get_json(f"https://finnhub.io/api/v1/news?{params}")
    if not isinstance(data, list):
        return []

    items = []
    for row in data[:limit]:
        ts = row.get("datetime")
        published = None
        if ts:
            published = datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat()
        items.append(
            {
                "id": row.get("id"),
                "title": row.get("headline") or row.get("title"),
                "summary": (row.get("summary") or "")[:200],
                "source": row.get("source") or "Finnhub",
                "category": category,
                "link": row.get("url") or "",
                "publishedAt": published,
                "related": row.get("related") or "",
            }
        )
    return items


def fetch_finnhub_earnings(api_key: str | None, days: int = 7) -> list[dict]:
    if not api_key:
        return []
    today = datetime.now(timezone.utc).date()
    end = today + timedelta(days=days)
    params = urllib.parse.urlencode(
        {
            "from": today.isoformat(),
            "to": end.isoformat(),
            "token": api_key,
        }
    )
    data = http_get_json(f"https://finnhub.io/api/v1/calendar/earnings?{params}")
    if not isinstance(data, dict):
        return []

    rows = data.get("earningsCalendar") or []
    watch = set(FINNHUB_WATCH)
    items = []
    for row in rows[:40]:
        symbol = row.get("symbol") or ""
        if watch and symbol not in watch:
            continue
        items.append(
            {
                "symbol": symbol,
                "date": row.get("date"),
                "hour": row.get("hour"),
                "epsEstimate": row.get("epsEstimate"),
                "revenueEstimate": row.get("revenueEstimate"),
            }
        )
    if not items and rows:
        items = [
            {
                "symbol": row.get("symbol"),
                "date": row.get("date"),
                "hour": row.get("hour"),
                "epsEstimate": row.get("epsEstimate"),
                "revenueEstimate": row.get("revenueEstimate"),
            }
            for row in rows[:10]
        ]
    return items[:12]


def fetch_finnhub_all(api_key: str | None) -> tuple[dict, str]:
    if not api_key:
        return {"news": [], "earnings": []}, "missing_key"

    news = fetch_finnhub_news(api_key, "general", 8)
    forex_news = fetch_finnhub_news(api_key, "forex", 4)
    earnings = fetch_finnhub_earnings(api_key)

    seen: set[str] = set()
    merged_news = []
    for item in news + forex_news:
        title = item.get("title") or ""
        if not title or title in seen:
            continue
        seen.add(title)
        merged_news.append(item)
        if len(merged_news) >= 10:
            break

    status = "ok" if merged_news or earnings else "empty"
    return {"news": merged_news, "earnings": earnings}, status


def fetch_sectors() -> list[dict]:
    items = []
    for symbol, sector in SECTOR_ETFS.items():
        row = fetch_yahoo_item(symbol, {"name": sector, "category": "sector", "currency": "USD"})
        if row:
            row["sector"] = sector
            items.append(row)
    items.sort(key=lambda x: x.get("changePct") if x.get("changePct") is not None else -999, reverse=True)
    return items


def vix_regime(vix: float | None) -> str:
    if vix is None:
        return "unknown"
    if vix >= 25:
        return "high"
    if vix >= 18:
        return "elevated"
    if vix <= 14:
        return "low"
    return "normal"


def build_summary(
    risk: list,
    fx: list,
    sectors: list,
    commodities: list,
    fred: list | None = None,
) -> dict:
    vix_item = next((r for r in risk if r.get("symbol") == "^VIX"), None)
    tnx_item = next((r for r in risk if r.get("symbol") == "^TNX"), None)
    cnh = next((f for f in fx if "CNH" in f.get("symbol", "") or f.get("quote") == "CNH"), None)

    leader = sectors[0] if sectors else None
    laggard = sectors[-1] if sectors else None

    hints = []
    vix_val = vix_item.get("price") if vix_item else None
    regime = vix_regime(vix_val)
    if regime == "high":
        hints.append("VIX 处于高位，全球风险资产波动加大，宜控制战术仓位。")
    elif regime == "low":
        hints.append("VIX 偏低，市场 complacency 需警惕突发回调。")

    if tnx_item and tnx_item.get("changePct") is not None:
        if tnx_item["changePct"] > 0.5:
            hints.append("美债收益率上行，对高估值成长股形成压力。")
        elif tnx_item["changePct"] < -0.5:
            hints.append("美债收益率回落，利于风险资产估值修复。")

    if cnh and cnh.get("changePct") is not None:
        if cnh["changePct"] > 0.1:
            hints.append("离岸人民币走弱，关注港股与 A 股外资流向。")
        elif cnh["changePct"] < -0.1:
            hints.append("离岸人民币走强，利于中概与港股情绪。")

    if leader and laggard and leader.get("changePct") is not None:
        hints.append(
            f"美股行业轮动：{leader.get('sector')} 领涨（{leader.get('changePct'):+.2f}%），"
            f"{laggard.get('sector')} 靠后。"
        )

    gold = next((c for c in commodities if c.get("symbol") == "GC=F"), None)
    oil = next((c for c in commodities if c.get("symbol") == "CL=F"), None)
    if gold and oil and gold.get("changePct") is not None and oil.get("changePct") is not None:
        if gold["changePct"] > 0 and oil["changePct"] < 0:
            hints.append("黄金强、原油弱 — 偏避险/衰退交易特征。")
        elif gold["changePct"] < 0 and oil["changePct"] > 0:
            hints.append("原油强、黄金弱 — 偏再通胀/增长预期。")

    spread = next((f for f in (fred or []) if f.get("seriesId") == "T10Y2Y"), None)
    if spread and spread.get("price") is not None:
        if spread["price"] < 0:
            hints.append("FRED：10Y-2Y 利差为负（收益率曲线倒挂），需关注衰退预期。")
        elif spread["price"] < 0.5:
            hints.append("FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。")

    unrate = next((f for f in (fred or []) if f.get("seriesId") == "UNRATE"), None)
    if unrate and unrate.get("changePct") is not None and unrate["changePct"] > 0.1:
        hints.append("FRED：失业率边际上升，就业市场边际走弱。")

    return {
        "vix": vix_val,
        "vixRegime": regime,
        "us10yYield": tnx_item.get("price") if tnx_item else None,
        "usdCnh": cnh.get("price") if cnh else None,
        "usdCnhChangePct": cnh.get("changePct") if cnh else None,
        "sectorLeader": leader.get("sector") if leader else None,
        "sectorLaggard": laggard.get("sector") if laggard else None,
        "yieldSpread10y2y": spread.get("price") if spread else None,
        "hints": hints[:5],
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone()

    sources = []

    risk_rates_indices = []
    for symbol, meta in YAHOO_MACRO.items():
        row = fetch_yahoo_item(symbol, meta)
        if row:
            risk_rates_indices.append(row)
    sources.append({"id": "yahoo", "name": "Yahoo Finance", "status": "ok", "items": len(risk_rates_indices)})

    yahoo_fx = []
    for symbol, meta in YAHOO_FX.items():
        row = fetch_yahoo_item(symbol, {**meta, "category": "fx"})
        if row:
            row["base"] = meta["base"]
            row["quote"] = meta["quote"]
            yahoo_fx.append(row)

    frankfurter, f_status = fetch_frankfurter()
    sources.append({"id": "frankfurter", "name": "Frankfurter (ECB)", "status": f_status, "items": len(frankfurter)})

    if len(frankfurter) < 3:
        er_items, er_status = fetch_er_api_fallback()
        sources.append({"id": "exchangerate-api", "name": "ExchangeRate-API", "status": er_status, "items": len(er_items)})
        static_fx = er_items if er_items else frankfurter
    else:
        static_fx = frankfurter

    fx = merge_fx(yahoo_fx, static_fx)

    sectors = fetch_sectors()
    commodities = [r for r in risk_rates_indices if r.get("category") == "commodity"]
    risk = [r for r in risk_rates_indices if r.get("category") == "risk"]
    rates = [r for r in risk_rates_indices if r.get("category") == "rates"]
    extra_indices = [r for r in risk_rates_indices if r.get("category") == "index"]

    fred_key = os.environ.get("FRED_API_KEY") or None
    finnhub_key = os.environ.get("FINNHUB_API_KEY") or None
    fred_items, fred_status = fetch_fred_all(fred_key)
    sources.append(
        {
            "id": "fred",
            "name": "FRED (St. Louis Fed)",
            "status": fred_status,
            "items": len(fred_items),
            "cookieUsed": bool(fred_key),
        }
    )

    finnhub_data, fh_status = fetch_finnhub_all(finnhub_key)
    sources.append(
        {
            "id": "finnhub",
            "name": "Finnhub",
            "status": fh_status,
            "items": len(finnhub_data.get("news", [])) + len(finnhub_data.get("earnings", [])),
            "cookieUsed": bool(finnhub_key),
        }
    )

    summary = build_summary(risk + rates, fx, sectors, commodities, fred_items)

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "sources": sources,
        "summary": summary,
        "risk": risk,
        "rates": rates,
        "fx": fx,
        "commodities": commodities,
        "extraIndices": extra_indices,
        "sectors": sectors,
        "fred": fred_items,
        "finnhubNews": finnhub_data.get("news", []),
        "earningsCalendar": finnhub_data.get("earnings", []),
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Wrote {OUTPUT_FILE} "
        f"(risk {len(risk)}, fx {len(fx)}, sectors {len(sectors)}, "
        f"fred {len(fred_items)}, finnhub news {len(finnhub_data.get('news', []))})"
    )


if __name__ == "__main__":
    main()
