#!/usr/bin/env python3
"""根据 reco_attribution 反哺战术门槛调整（写入 tactic_tune.json）。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ATTR_FILE = DATA_DIR / "reco_attribution.json"
OUTPUT = DATA_DIR / "tactic_tune.json"

MIN_SAMPLES = 8
MIN_DECISION_SAMPLES = 4
MIN_MARKET_SAMPLES = 4
MIN_REGIME_SAMPLES = 4
LOW_WIN_RATE = 45.0
HIGH_WIN_RATE = 58.0
LOW_DECISION_WIN = 40.0


def _load_attr() -> dict:
    if not ATTR_FILE.exists():
        return {}
    try:
        return json.loads(ATTR_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def run_tune() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    attr = _load_attr()
    summary = attr.get("summary") or {}
    by_signal = summary.get("bySignal") or {}
    by_decision = summary.get("byDecisionLabel") or {}
    by_market = summary.get("byMarket") or {}
    by_regime = summary.get("byRegime") or {}
    buy_stats = by_signal.get("buy") or {}
    watch_stats = by_signal.get("watch") or {}

    buy_count = buy_stats.get("count") or 0
    buy_win = buy_stats.get("winRate")
    if buy_win is None:
        buy_win = summary.get("winRateT5")
    buy_avg = buy_stats.get("avgT5") or summary.get("avgReturnT5")

    adjust = 0
    notes: list[str] = []

    if buy_count >= MIN_SAMPLES and buy_win is not None and buy_win < LOW_WIN_RATE:
        adjust += 2
        notes.append(f"buy 信号 T+5 胜率 {buy_win}% 偏低，门槛 +2")
    elif buy_count >= MIN_SAMPLES and buy_win is not None and buy_win > HIGH_WIN_RATE:
        adjust -= 1
        notes.append(f"buy 信号 T+5 胜率 {buy_win}% 良好，门槛 -1")

    high = by_decision.get("高") or {}
    mid = by_decision.get("中") or {}
    low = by_decision.get("低") or {}

    if (high.get("count") or 0) >= MIN_DECISION_SAMPLES and high.get("winRate") is not None:
        if high["winRate"] >= HIGH_WIN_RATE:
            adjust -= 1
            notes.append(f"高决策分 T+5 胜率 {high['winRate']}% 良好，门槛 -1")
        elif high["winRate"] < LOW_WIN_RATE:
            adjust += 1
            notes.append(f"高决策分 T+5 胜率 {high['winRate']}% 不及预期，门槛 +1")

    if (low.get("count") or 0) >= MIN_DECISION_SAMPLES and low.get("winRate") is not None:
        if low["winRate"] < LOW_DECISION_WIN:
            adjust += 1
            notes.append(f"低决策分 T+5 胜率 {low['winRate']}% 拖累，门槛 +1")

    if (mid.get("count") or 0) >= MIN_DECISION_SAMPLES:
        mid_win = mid.get("winRate")
        if mid_win is not None and (high.get("count") or 0) < MIN_DECISION_SAMPLES:
            if mid_win >= HIGH_WIN_RATE:
                adjust -= 1
                notes.append(f"中决策分 T+5 胜率 {mid_win}% 良好，门槛 -1")
            elif mid_win < LOW_WIN_RATE:
                adjust += 1
                notes.append(f"中决策分 T+5 胜率 {mid_win}% 偏低，门槛 +1")

    market_candidates = [
        (name, by_market.get(name) or {})
        for name in ("A股", "港股", "美股")
        if (by_market.get(name) or {}).get("count", 0) >= MIN_MARKET_SAMPLES
        and (by_market.get(name) or {}).get("winRate") is not None
    ]
    if market_candidates:
        worst_name, worst = min(market_candidates, key=lambda x: x[1]["winRate"])
        best_name, best = max(market_candidates, key=lambda x: x[1]["winRate"])
        if worst["winRate"] < LOW_WIN_RATE:
            adjust += 1
            notes.append(f"{worst_name} T+5 胜率 {worst['winRate']}% 拖累，门槛 +1")
        elif best["winRate"] >= HIGH_WIN_RATE:
            adjust -= 1
            notes.append(f"{best_name} T+5 胜率 {best['winRate']}% 领先，门槛 -1")

    risk_off = by_regime.get("risk_off") or {}
    if (risk_off.get("count") or 0) >= MIN_REGIME_SAMPLES and (risk_off.get("winRate") or 100) < LOW_WIN_RATE:
        adjust += 1
        notes.append(f"偏空环境 T+5 胜率 {risk_off['winRate']}% 偏弱，门槛 +1")

    risk_on = by_regime.get("risk_on") or {}
    if (risk_on.get("count") or 0) >= MIN_REGIME_SAMPLES and (risk_on.get("winRate") or 0) >= HIGH_WIN_RATE:
        adjust -= 1
        notes.append(f"偏多环境 T+5 胜率 {risk_on['winRate']}% 良好，门槛 -1")

    adjust = _clamp(adjust, -3, 4)

    watch_count = watch_stats.get("count") or 0
    if watch_count >= MIN_SAMPLES * 2 and buy_count < MIN_SAMPLES:
        notes.append("buy 样本不足，主要依据 watch 池、市场与决策分桶观察")

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "buyScoreAdjust": adjust,
        "breakoutScoreAdjust": adjust,
        "attribution": {
            "buySamples": buy_count,
            "winRateT5": buy_win,
            "avgReturnT5": buy_avg,
            "byDecisionLabel": by_decision,
            "byMarket": by_market,
            "byRegime": by_regime,
        },
        "notes": notes,
        "active": adjust != 0,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Tactic tune: buyScoreAdjust={adjust} ({'; '.join(notes) or 'neutral'})")
    return payload


if __name__ == "__main__":
    run_tune()
