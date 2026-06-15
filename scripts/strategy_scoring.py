"""多因子评分 — 供 fetch_data / backtest 共用的离线计算逻辑（非在线服务）。"""

from __future__ import annotations

from strategy_config import (
    ATR_STOP_NORMAL,
    ATR_STOP_STRONG,
    BUY_SCORE,
    MAX_RSI_ENTRY,
    MIN_RELATIVE_STRENGTH,
    REQUIRE_BULL_MARKET,
    REQUIRE_MACD_POSITIVE,
    REWARD_RISK_RATIO,
    WATCH_SCORE,
)

MARKET_BENCHMARKS = {
    "A股": "000001.SS",
    "港股": "^HSI",
    "美股": "^GSPC",
}


def pct_change(current: float, previous: float) -> float | None:
    if previous in (0, None) or current is None:
        return None
    return round((current - previous) / previous * 100, 2)


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


def price_digits(price: float) -> int:
    if price >= 1000:
        return 2
    if price >= 10:
        return 2
    return 3


def score_series(
    closes: list[float],
    highs: list[float],
    lows: list[float],
    volumes: list[float],
    bench_closes: list[float],
    market: str = "美股",
    buy_score: float | None = None,
    watch_score: float | None = None,
) -> dict | None:
    """对截至最新一根 K 线的序列打分，与实盘荐股逻辑一致。"""
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

    bench_month = benchmark_return(bench_closes, 22) if bench_closes else None
    rel_strength = (
        round(month_chg - bench_month, 2) if month_chg is not None and bench_month is not None else None
    )

    if not all(v is not None for v in (sma20, sma60, rsi, atr, month_chg, quarter_chg, macd, macd_signal, macd_hist)):
        return None

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

    bull_market = True
    if bench_closes and len(bench_closes) >= 60:
        bench_price = bench_closes[-1]
        bench_sma60 = sma(bench_closes, 60)
        if bench_sma60 and bench_price > bench_sma60:
            score += 5
        elif bench_sma60 and bench_price < bench_sma60:
            score -= 3
            bull_market = False

    score = round(max(min(score, 100), 0), 1)

    # v1.1 强化过滤：不满足硬条件则降级为 hold
    hard_ok = True
    if REQUIRE_BULL_MARKET and not bull_market:
        hard_ok = False
    if rsi > MAX_RSI_ENTRY:
        hard_ok = False
    if rel_strength is not None and rel_strength < MIN_RELATIVE_STRENGTH:
        hard_ok = False
    if REQUIRE_MACD_POSITIVE and (macd_hist is None or macd_hist <= 0):
        hard_ok = False
    if not (sma10 and sma10 > sma20 > sma60):
        hard_ok = False

    buy_threshold = buy_score if buy_score is not None else BUY_SCORE
    watch_threshold = watch_score if watch_score is not None else WATCH_SCORE

    if score >= buy_threshold and hard_ok:
        signal, signal_label = "buy", "建议买入"
    elif score >= watch_threshold:
        signal, signal_label = "watch", "建议观察"
    else:
        signal, signal_label = "hold", "暂不参与"

    strong_trend = bool(sma10 and sma10 > sma20 > sma60 and score >= buy_threshold)
    atr_mult = ATR_STOP_STRONG if strong_trend else ATR_STOP_NORMAL
    stop_loss = round(price - atr_mult * atr, 2)
    target = round(price + atr_mult * atr * REWARD_RISK_RATIO, 2)

    return {
        "score": score,
        "signal": signal,
        "signalLabel": signal_label,
        "rsi": rsi,
        "monthChangePct": month_chg,
        "relativeStrength": rel_strength,
        "reasons": reasons[:5],
        "stopLossPrice": stop_loss,
        "targetPrice": target,
        "atrMult": atr_mult,
        "bullMarket": bull_market,
        "hardFiltersPassed": hard_ok,
    }
