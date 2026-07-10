#!/usr/bin/env python3
"""市场环境识别 — 供 history 快照、归因分桶与 tactic_tune 复用。"""

from __future__ import annotations


def detect_market_regime(
    market_summary: dict | None,
    macro_summary: dict | None = None,
) -> str:
    """返回 risk_on | risk_off | neutral。"""
    mood = (market_summary or {}).get("mood")
    vix = (macro_summary or {}).get("vix")
    if vix is not None and vix >= 22:
        return "risk_off"
    if mood == "偏空" or (vix is not None and vix >= 18):
        return "risk_off"
    if mood == "偏多":
        return "risk_on"
    avg = (market_summary or {}).get("avgChangePct")
    if avg is not None and avg > 0.5:
        return "risk_on"
    return "neutral"


def regime_label(regime: str | None) -> str:
    return {
        "risk_on": "偏多",
        "risk_off": "偏空",
        "neutral": "震荡",
    }.get(regime or "", "未知")
