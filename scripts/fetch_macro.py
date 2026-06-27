#!/usr/bin/env python3
"""拉取宏观、汇率、商品与行业 ETF — 免费数据源聚合。"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
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


def build_summary(risk: list, fx: list, sectors: list, commodities: list) -> dict:
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

    return {
        "vix": vix_val,
        "vixRegime": regime,
        "us10yYield": tnx_item.get("price") if tnx_item else None,
        "usdCnh": cnh.get("price") if cnh else None,
        "usdCnhChangePct": cnh.get("changePct") if cnh else None,
        "sectorLeader": leader.get("sector") if leader else None,
        "sectorLaggard": laggard.get("sector") if laggard else None,
        "hints": hints[:4],
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

    summary = build_summary(risk + rates, fx, sectors, commodities)

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
    }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Wrote {OUTPUT_FILE} "
        f"(risk {len(risk)}, fx {len(fx)}, sectors {len(sectors)}, indices {len(extra_indices)})"
    )


if __name__ == "__main__":
    main()
