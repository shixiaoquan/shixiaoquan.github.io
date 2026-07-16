"""多因子评分 — 供 fetch_data / backtest / 模拟盘共用的离线计算逻辑。"""

from __future__ import annotations

from strategy_config import (
    BREAKOUT_LOOKBACK,
    BREAKOUT_SCORE_MIN,
    BREAKOUT_VOLUME_RATIO,
    BUY_SCORE,
    MAX_RSI_ENTRY,
    MIN_RELATIVE_STRENGTH,
    REQUIRE_ABOVE_MA200,
    REQUIRE_BENCH_ABOVE_MA200,
    REQUIRE_BULL_MARKET,
    REQUIRE_BREAKOUT_FOR_BUY,
    REQUIRE_MACD_POSITIVE,
    REWARD_RISK_RATIO,
    WATCH_SCORE,
)
from strategy_config import ATR_STOP_INITIAL, ATR_TRAILING

MARKET_BENCHMARKS = {
    "A股": "000001.SS",
    "港股": "^HSI",
    "美股": "^GSPC",
}

MIN_BARS = 200


def pct_change(current: float, previous: float) -> float | None:
    if previous in (0, None) or current is None:
        return None
    return round((current - previous) / previous * 100, 2)


def price_digits(price: float) -> int:
    """按价格量级决定展示小数位。"""
    if price is None or price <= 0:
        return 2
    if price >= 1000:
        return 2
    if price >= 100:
        return 2
    if price >= 10:
        return 2
    return 3


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


def compute_rsi(closes: list[float], period: int = 14) -> float | None:
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


def compute_macd(closes: list[float]) -> tuple[float | None, float | None, float | None]:
    if len(closes) < 35:
        return None, None, None
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = [a - b for a, b in zip(ema12, ema26)]
    signal = ema(macd_line, 9)
    hist = macd_line[-1] - signal[-1]
    return round(macd_line[-1], 4), round(signal[-1], 4), round(hist, 4)


def benchmark_return(closes: list[float], days: int) -> float | None:
    if len(closes) < days + 1:
        return None
    return pct_change(closes[-1], closes[-days - 1])


def detect_regime(
    price: float,
    closes: list[float],
    bench_closes: list[float],
) -> dict:
    """Regime：个股与基准均在 MA200 之上才允许做多。"""
    sma200 = sma(closes, 200) if len(closes) >= 200 else None
    bench_sma200 = sma(bench_closes, 200) if bench_closes and len(bench_closes) >= 200 else None
    bench_price = bench_closes[-1] if bench_closes else None

    stock_ok = True if sma200 is None else price > sma200
    bench_ok = True
    bull_market = True

    if bench_closes and len(bench_closes) >= 60:
        bench_sma60 = sma(bench_closes, 60)
        if bench_sma60 and bench_price and bench_price < bench_sma60:
            bull_market = False

    if REQUIRE_ABOVE_MA200 and sma200 is not None:
        stock_ok = price > sma200
    if REQUIRE_BENCH_ABOVE_MA200 and bench_sma200 is not None and bench_price is not None:
        bench_ok = bench_price > bench_sma200

    regime_ok = stock_ok and bench_ok
    if REQUIRE_BULL_MARKET:
        regime_ok = regime_ok and bull_market

    return {
        "regimeOk": regime_ok,
        "stockAboveMa200": stock_ok,
        "benchAboveMa200": bench_ok,
        "bullMarket": bull_market,
        "sma200": sma200,
    }


def detect_breakout(
    closes: list[float],
    highs: list[float],
    volumes: list[float],
) -> dict:
    """平台突破：收盘创 N 日新高且放量。"""
    lookback = min(BREAKOUT_LOOKBACK, len(highs) - 2)
    if lookback < 10:
        return {"breakout": False, "breakoutLevel": None, "volumeRatio": None}

    prior_high = max(highs[-(lookback + 1) : -1])
    price = closes[-1]
    vol5, vol20 = sma(volumes, 5), sma(volumes, 20)
    vol_ratio = round(vol5 / vol20, 2) if vol5 and vol20 else None
    breakout = price >= prior_high and vol_ratio is not None and vol_ratio >= BREAKOUT_VOLUME_RATIO

    return {
        "breakout": breakout,
        "breakoutLevel": round(prior_high, 2),
        "volumeRatio": vol_ratio,
    }


def score_series(
    closes: list[float],
    highs: list[float],
    lows: list[float],
    volumes: list[float],
    bench_closes: list[float],
    market: str = "美股",
    min_bars: int = MIN_BARS,
    score_adjust: dict | None = None,
) -> dict | None:
    """对截至最新一根 K 线的序列打分。score_adjust 可含 buyScoreAdjust / breakoutScoreAdjust。"""
    if len(closes) < min_bars:
        return None

    adj = score_adjust or {}
    by_mkt_buy = (adj.get("buyScoreAdjustByMarket") or {}).get(market)
    by_mkt_brk = (adj.get("breakoutScoreAdjustByMarket") or {}).get(market)
    buy_delta = by_mkt_buy if by_mkt_buy is not None else adj.get("buyScoreAdjust") or 0
    brk_delta = by_mkt_brk if by_mkt_brk is not None else adj.get("breakoutScoreAdjust") or 0
    buy_threshold = BUY_SCORE + int(buy_delta)
    breakout_threshold = BREAKOUT_SCORE_MIN + int(brk_delta)

    price = closes[-1]
    sma10 = sma(closes, 10)
    sma20 = sma(closes, 20)
    sma60 = sma(closes, 60)
    rsi = compute_rsi(closes)
    atr = compute_atr(highs, lows, closes)
    macd, macd_signal, macd_hist = compute_macd(closes)
    month_chg = pct_change(price, closes[-22]) if len(closes) >= 22 else None
    quarter_chg = pct_change(price, closes[-63]) if len(closes) >= 63 else pct_change(price, closes[0])

    bench_month = benchmark_return(bench_closes, 22) if bench_closes else None
    rel_strength = (
        round(month_chg - bench_month, 2) if month_chg is not None and bench_month is not None else None
    )

    if not all(v is not None for v in (sma20, sma60, rsi, atr, month_chg, quarter_chg, macd, macd_signal, macd_hist)):
        return None

    regime = detect_regime(price, closes, bench_closes)
    breakout_info = detect_breakout(closes, highs, volumes)

    score = 0.0
    reasons: list[str] = []

    if price > sma20:
        score += 8
        reasons.append("价格站上 20 日均线")
    if price > sma60:
        score += 7
        reasons.append("价格站上 60 日均线")
    if sma10 and sma10 > sma20 > sma60:
        score += 10
        reasons.append("均线多头排列")
    elif sma20 > sma60:
        score += 5

    if month_chg > 0:
        score += min(month_chg * 1.2, 10)
    if quarter_chg > 0:
        score += min(quarter_chg * 0.4, 10)

    if rel_strength is not None:
        if rel_strength > 5:
            score += 15
        elif rel_strength > 0:
            score += 10
        elif rel_strength > -3:
            score += 4
        else:
            score -= 5

    if 48 <= rsi <= 62:
        score += 15
    elif 40 <= rsi < 48:
        score += 10
    elif 62 < rsi <= 70:
        score += 8
    elif rsi > 75:
        score -= 12
    else:
        score += 3

    if macd > macd_signal and macd_hist > 0:
        score += 10
    elif macd_hist > 0:
        score += 6
    elif macd > macd_signal:
        score += 4

    vol5, vol20 = sma(volumes, 5), sma(volumes, 20)
    if vol5 and vol20:
        vol_ratio = vol5 / vol20
        if vol_ratio > 1.3:
            score += 10
        elif vol_ratio > 1.05:
            score += 6

    if breakout_info["breakout"]:
        score += 12
        reasons.insert(0, f"突破 {BREAKOUT_LOOKBACK} 日平台且放量")

    if regime["regimeOk"]:
        score += 5
    else:
        score -= 8

    score = round(max(min(score, 100), 0), 1)

    trend_ok = bool(sma20 and price > sma20 > sma60)
    soft_ok = True
    if rsi > MAX_RSI_ENTRY:
        soft_ok = False
    if rel_strength is not None and rel_strength < MIN_RELATIVE_STRENGTH:
        soft_ok = False
    if REQUIRE_MACD_POSITIVE and (macd_hist is None or macd_hist <= 0):
        soft_ok = False

    entry_type = None
    if not regime["regimeOk"]:
        signal, signal_label = "hold", "暂不参与"
    elif breakout_info["breakout"] and score >= breakout_threshold and rsi <= MAX_RSI_ENTRY and soft_ok:
        signal, signal_label = "buy", "突破买入"
        entry_type = "breakout"
    elif (
        not REQUIRE_BREAKOUT_FOR_BUY
        and score >= buy_threshold
        and trend_ok
        and soft_ok
        and regime["bullMarket"]
    ):
        signal, signal_label = "buy", "趋势买入"
        entry_type = "trend"
    elif score >= buy_threshold and trend_ok and REQUIRE_BREAKOUT_FOR_BUY:
        signal, signal_label = "watch", "趋势达标待突破"
        entry_type = None
    elif score >= WATCH_SCORE:
        signal, signal_label = "watch", "建议观察"
    else:
        signal, signal_label = "hold", "暂不参与"

    stop_loss = round(price - ATR_STOP_INITIAL * atr, 2)
    target = round(price + ATR_TRAILING * atr * REWARD_RISK_RATIO, 2)

    return {
        "score": score,
        "signal": signal,
        "signalLabel": signal_label,
        "entryType": entry_type,
        "rsi": rsi,
        "monthChangePct": month_chg,
        "relativeStrength": rel_strength,
        "reasons": reasons[:5],
        "stopLossPrice": stop_loss,
        "targetPrice": target,
        "atr": atr,
        "atrMult": ATR_STOP_INITIAL,
        "trailingAtrMult": ATR_TRAILING,
        "bullMarket": regime["bullMarket"],
        "regimeOk": regime["regimeOk"],
        "breakout": breakout_info["breakout"],
        "breakoutLevel": breakout_info["breakoutLevel"],
        "volumeRatio": breakout_info["volumeRatio"],
        "hardFiltersPassed": regime["regimeOk"] and (entry_type is not None),
    }
