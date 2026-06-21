"""出场逻辑 — 回测与模拟盘共用（跟踪止损）。"""

from __future__ import annotations

from strategy_config import (
    ATR_BREAKEVEN_MULT,
    ATR_STOP_INITIAL,
    ATR_TRAILING,
    BACKTEST_HOLD_DAYS,
    USE_TRAILING_STOP,
)
from strategy_scoring import compute_atr


def initial_stop_price(entry: float, atr: float) -> float:
    return round(entry - ATR_STOP_INITIAL * atr, 2)


def effective_stop(
    entry: float,
    atr: float,
    highest: float,
    current_stop: float,
) -> float:
    """计算当日有效止损（只上移不下移）。"""
    floor = initial_stop_price(entry, atr)
    stop = max(current_stop, floor)
    if USE_TRAILING_STOP and atr > 0:
        trail = round(highest - ATR_TRAILING * atr, 2)
        stop = max(stop, trail)
    if atr > 0 and highest >= entry + ATR_BREAKEVEN_MULT * atr:
        stop = max(stop, round(entry, 2))
    return stop


def simulate_exit(
    entry: float,
    entry_idx: int,
    dates: list[str],
    closes: list[float],
    highs: list[float],
    lows: list[float],
    atr_at_entry: float,
    max_hold_days: int | None = None,
) -> tuple[float, str, str]:
    """模拟持仓出场，返回 (exit_price, exit_date, reason)。"""
    hold_limit = max_hold_days if max_hold_days is not None else BACKTEST_HOLD_DAYS
    stop = initial_stop_price(entry, atr_at_entry)
    highest = entry

    last_j = min(entry_idx + hold_limit, len(closes) - 1)
    for j in range(entry_idx + 1, last_j + 1):
        highest = max(highest, highs[j])
        stop = effective_stop(entry, atr_at_entry, highest, stop)
        if lows[j] <= stop:
            return stop, dates[j], "trail" if stop > initial_stop_price(entry, atr_at_entry) else "stop"

    j = last_j
    return closes[j], dates[j], "expiry"
