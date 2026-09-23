#!/usr/bin/env python3
"""HK01810（小米集团-W）箱体短线策略 — 产出 data/hk01810_box.json。

规则来自人工确认的高抛低吸框架：
- 日常箱子 25.44–29.10；底部失效线 21.30
- 买入分 3 份：25.44–26.00 / 23.00–24.00 / 21.50–22.30
- 卖出：28.20–28.80 卖 2 份，29.00–29.10 卖尾仓
- 箱体中部不操作；收盘站上 29.10 空仓不追；收盘跌破 21.30 清仓
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "hk01810_box.json"

SYMBOL = "1810.HK"
SYMBOL_ALIAS = "HK01810"
NAME = "小米集团-W"
CURRENCY = "HKD"
LOT_SIZE = 200
RULES_VERSION = "1.0.0"

BOX_LOW = 25.44
BOX_HIGH = 29.10
BOTTOM = 21.30
BOX_HEIGHT = round(BOX_HIGH - BOX_LOW, 2)

BUY_ZONES = [
    {"id": "t1", "label": "第1份", "low": 25.44, "high": 26.00, "weight": "1/3"},
    {"id": "t2", "label": "第2份", "low": 23.00, "high": 24.00, "weight": "1/3"},
    {"id": "t3", "label": "第3份", "low": 21.50, "high": 22.30, "weight": "1/3"},
]
SELL_ZONES = [
    {"id": "s1", "label": "卖出2份", "low": 28.20, "high": 28.80, "weight": "2/3"},
    {"id": "s2", "label": "卖出尾仓", "low": 29.00, "high": 29.10, "weight": "1/3"},
]


def _round(price: float | None, digits: int = 2) -> float | None:
    if price is None:
        return None
    return round(float(price), digits)


def decide(price: float | None) -> dict:
    """按参考价给出空仓 / 持仓两侧建议。优先看收盘价规则。"""
    if price is None:
        return {
            "action": "unavailable",
            "actionLabel": "行情不可用",
            "tone": "neutral",
            "operate": False,
            "title": "暂无可用报价",
            "detail": "刷新后重试，或等待行情流水线更新。",
            "emptyAdvice": "暂不操作",
            "holdingAdvice": "暂不操作",
            "zoneId": None,
        }

    p = float(price)

    if p < BOTTOM:
        return {
            "action": "exit",
            "actionLabel": "清仓离场",
            "tone": "danger",
            "operate": True,
            "title": f"收盘价 {p:.2f} 跌破底部 {BOTTOM:.2f}",
            "detail": "底部判断失效。持仓全部卖出；空仓不再抄底，等待新结构。",
            "emptyAdvice": "空仓观望，停止箱体内买点",
            "holdingAdvice": "清仓离场",
            "zoneId": "bottom",
        }

    if p > BOX_HIGH:
        target = _round(BOX_HIGH + BOX_HEIGHT)
        return {
            "action": "breakout_up",
            "actionLabel": "向上突破 · 不追",
            "tone": "warn",
            "operate": False,
            "title": f"收盘价 {p:.2f} 站上箱顶 {BOX_HIGH:.2f}",
            "detail": (
                f"日常箱子向上打开。按规则空仓不追高。"
                f"测量目标约 {target:.2f}；若跌回 28.50 下方视为假突破。"
            ),
            "emptyAdvice": "继续空仓，不在更高位置追",
            "holdingAdvice": "按突破规则另议；本策略默认已在上沿卖完",
            "zoneId": "breakout",
        }

    for zone in SELL_ZONES:
        if zone["low"] <= p <= zone["high"]:
            return {
                "action": "sell",
                "actionLabel": zone["label"],
                "tone": "sell",
                "operate": True,
                "title": f"进入卖区 {zone['low']:.2f}–{zone['high']:.2f}",
                "detail": f"现价 {p:.2f}。只卖已持有股份；卖完空仓，等下一次买区。",
                "emptyAdvice": "空仓不新开多单",
                "holdingAdvice": f"{zone['label']}（{zone['weight']}）",
                "zoneId": zone["id"],
            }

    for zone in BUY_ZONES:
        if zone["low"] <= p <= zone["high"]:
            return {
                "action": "buy",
                "actionLabel": f"买入{zone['label']}",
                "tone": "buy",
                "operate": True,
                "title": f"进入买区 {zone['low']:.2f}–{zone['high']:.2f}",
                "detail": (
                    f"现价 {p:.2f}。按收盘价确认后买入{zone['label']}（{zone['weight']}）。"
                    f"每手 {LOT_SIZE} 股。收盘跌破 {BOTTOM:.2f} 全部止损。"
                ),
                "emptyAdvice": f"买入{zone['label']}（{zone['weight']}）",
                "holdingAdvice": f"若尚未买过该档，可加{zone['label']}",
                "zoneId": zone["id"],
            }

    if BOX_LOW < p < 28.20:
        return {
            "action": "wait",
            "actionLabel": "箱体中部 · 观望",
            "tone": "neutral",
            "operate": False,
            "title": f"现价 {p:.2f} 在箱子中部",
            "detail": (
                f"买区在 {BUY_ZONES[0]['low']:.2f}–{BUY_ZONES[0]['high']:.2f} 及以下更深档；"
                f"卖区在 {SELL_ZONES[0]['low']:.2f} 以上。两边都不到，今天不操作。"
            ),
            "emptyAdvice": "继续空仓等待买区",
            "holdingAdvice": "持有不动，不加不减",
            "zoneId": "mid",
        }

    if 24.00 < p < BOX_LOW:
        return {
            "action": "wait",
            "actionLabel": "等待买区",
            "tone": "neutral",
            "operate": False,
            "title": f"现价 {p:.2f} 低于日常箱下沿",
            "detail": f"尚未进入第2份买区 23.00–24.00。收盘跌破 {BOTTOM:.2f} 则清仓逻辑启动。",
            "emptyAdvice": "等待进入 23.00–24.00",
            "holdingAdvice": "持有观察；不在空白区加仓",
            "zoneId": "gap_t1_t2",
        }

    if 22.30 < p < 23.00:
        return {
            "action": "wait",
            "actionLabel": "买区之间 · 观望",
            "tone": "neutral",
            "operate": False,
            "title": f"现价 {p:.2f} 在第2/第3份买区之间",
            "detail": "不在规则买区内，等收盘落入 23.00–24.00 或 21.50–22.30。",
            "emptyAdvice": "观望",
            "holdingAdvice": "持有观察",
            "zoneId": "gap_t2_t3",
        }

    if BOTTOM <= p < 21.50:
        return {
            "action": "watch",
            "actionLabel": "贴近失效线",
            "tone": "warn",
            "operate": False,
            "title": f"现价 {p:.2f} 贴近底部 {BOTTOM:.2f}",
            "detail": (
                f"尚未进入第3份买区 21.50–22.30。"
                f"回到该区间再买第3份；收盘跌破 {BOTTOM:.2f} 则清仓。"
            ),
            "emptyAdvice": "只观察，等 21.50–22.30",
            "holdingAdvice": "高度警戒；跌破清仓",
            "zoneId": "near_bottom",
        }

    return {
        "action": "wait",
        "actionLabel": "观望",
        "tone": "neutral",
        "operate": False,
        "title": f"现价 {p:.2f}",
        "detail": "未落入买卖区。",
        "emptyAdvice": "观望",
        "holdingAdvice": "持有观察",
        "zoneId": None,
    }


def fetch_quote() -> dict:
    ticker = yf.Ticker(SYMBOL)
    hist = ticker.history(period="60d", auto_adjust=False)
    if hist is None or hist.empty:
        raise RuntimeError(f"no history for {SYMBOL}")

    last = hist.iloc[-1]
    prev = hist.iloc[-2] if len(hist) > 1 else last
    last_price = float(last["Close"])
    prev_close = float(prev["Close"])
    change = last_price - prev_close
    change_pct = (change / prev_close * 100) if prev_close else None

    recent = []
    for idx, row in hist.tail(20).iterrows():
        day = idx.date().isoformat() if hasattr(idx, "date") else str(idx)[:10]
        recent.append(
            {
                "date": day,
                "open": _round(row["Open"]),
                "high": _round(row["High"]),
                "low": _round(row["Low"]),
                "close": _round(row["Close"]),
                "volume": int(row["Volume"]) if row["Volume"] == row["Volume"] else None,
            }
        )

    avg_volume = None
    vols = [r["volume"] for r in recent if r.get("volume")]
    if vols:
        avg_volume = int(sum(vols) / len(vols))

    return {
        "price": _round(last_price),
        "previousClose": _round(prev_close),
        "change": _round(change),
        "changePct": _round(change_pct),
        "dayOpen": _round(float(last["Open"])),
        "dayHigh": _round(float(last["High"])),
        "dayLow": _round(float(last["Low"])),
        "volume": int(last["Volume"]) if last["Volume"] == last["Volume"] else None,
        "avgVolume20": avg_volume,
        "asOf": recent[-1]["date"] if recent else None,
        "recentBars": recent,
    }


def build_payload(quote: dict | None = None, *, error: str | None = None) -> dict:
    now = datetime.now(timezone.utc).astimezone()
    quote = quote or {}
    price = quote.get("price")
    advice = decide(price)

    position_in_box = None
    if price is not None and BOX_HIGH != BOX_LOW:
        position_in_box = round(max(0.0, min(1.0, (float(price) - BOX_LOW) / (BOX_HIGH - BOX_LOW))), 3)

    return {
        "version": 1,
        "rulesVersion": RULES_VERSION,
        "updatedAt": now.isoformat(timespec="seconds"),
        "symbol": SYMBOL,
        "symbolAlias": SYMBOL_ALIAS,
        "name": NAME,
        "currency": CURRENCY,
        "lotSize": LOT_SIZE,
        "disclaimer": "箱体短线框架仅供个人复盘，不构成投资建议。按收盘价确认买卖区。",
        "levels": {
            "boxLow": BOX_LOW,
            "boxHigh": BOX_HIGH,
            "bottom": BOTTOM,
            "boxHeight": BOX_HEIGHT,
            "breakoutTarget": _round(BOX_HIGH + BOX_HEIGHT),
            "breakdownTarget": _round(BOX_LOW - BOX_HEIGHT),
            "fakeBreakoutBack": 28.50,
            "shortCover": 26.20,
        },
        "buyZones": BUY_ZONES,
        "sellZones": SELL_ZONES,
        "quote": quote,
        "positionInBox": position_in_box,
        "advice": advice,
        "error": error,
    }


def run() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    error = None
    quote: dict = {}
    try:
        quote = fetch_quote()
    except Exception as exc:  # noqa: BLE001 — 流水线容错，写出可渲染的降级 JSON
        error = str(exc)
        print(f"HK01810 box quote failed: {exc}")

    payload = build_payload(quote, error=error)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    advice = payload["advice"]
    print(
        f"HK01810 box: price={payload['quote'].get('price')} "
        f"action={advice.get('action')} · {advice.get('actionLabel')}"
    )
    return payload


if __name__ == "__main__":
    run()
