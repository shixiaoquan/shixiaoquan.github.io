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
LOW_WIN_RATE = 45.0
HIGH_WIN_RATE = 58.0


def run_tune() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    attr = {}
    if ATTR_FILE.exists():
        try:
            attr = json.loads(ATTR_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            attr = {}

    summary = attr.get("summary") or {}
    by_signal = summary.get("bySignal") or {}
    buy_stats = by_signal.get("buy") or {}
    watch_stats = by_signal.get("watch") or {}

    buy_count = buy_stats.get("count") or 0
    buy_win = summary.get("winRateT5")
    buy_avg = buy_stats.get("avgT5") or summary.get("avgReturnT5")

    adjust = 0
    notes: list[str] = []

    if buy_count >= MIN_SAMPLES and buy_win is not None and buy_win < LOW_WIN_RATE:
        adjust = 2
        notes.append(f"buy 信号 T+5 胜率 {buy_win}% 偏低，门槛 +2")
    elif buy_count >= MIN_SAMPLES and buy_win is not None and buy_win > HIGH_WIN_RATE:
        adjust = -1
        notes.append(f"buy 信号 T+5 胜率 {buy_win}% 良好，门槛 -1")

    watch_count = watch_stats.get("count") or 0
    if watch_count >= MIN_SAMPLES * 2 and buy_count < MIN_SAMPLES:
        notes.append("buy 样本不足，主要依据 watch 池观察")

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "buyScoreAdjust": adjust,
        "breakoutScoreAdjust": adjust,
        "attribution": {
            "buySamples": buy_count,
            "winRateT5": buy_win,
            "avgReturnT5": buy_avg,
        },
        "notes": notes,
        "active": adjust != 0,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Tactic tune: buyScoreAdjust={adjust} ({'; '.join(notes) or 'neutral'})")
    return payload


if __name__ == "__main__":
    run_tune()
