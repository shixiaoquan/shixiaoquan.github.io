#!/usr/bin/env python3
"""决策质量分 — 宏观 / 问财 / 大师共识 / Truth 舆情四维加权。"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

WEIGHTS = {
    "macro": 0.25,
    "wencai": 0.25,
    "masters": 0.30,
    "truth": 0.20,
}

MOOD_SCORE = {"偏多": 85, "偏空": 35, "震荡": 55}
WENCAI_MOOD_SCORE = {"强势": 80, "震荡": 55, "弱势": 30}


def _load(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _macro_score(macro: dict | None, market_summary: dict | None) -> tuple[float, str]:
    mood = (market_summary or {}).get("mood") or "震荡"
    base = float(MOOD_SCORE.get(mood, 55))
    if macro:
        vix_row = next((r for r in (macro.get("risk") or []) if r.get("symbol") == "^VIX"), None)
        if vix_row and vix_row.get("changePct") is not None:
            vix_chg = float(vix_row["changePct"])
            if vix_chg > 5:
                base -= 12
            elif vix_chg < -5:
                base += 8
    return max(0, min(100, base)), f"市场{mood}"


def _wencai_score(wencai: dict | None) -> tuple[float, str]:
    if not wencai:
        return 50.0, "问财未就绪"
    mood = wencai.get("mood") or "震荡"
    up = wencai.get("limitUp") or 0
    down = wencai.get("limitDown") or 0
    if up > down * 2:
        mood = "强势"
    elif down > up * 2:
        mood = "弱势"
    return float(WENCAI_MOOD_SCORE.get(mood, 55)), f"问财{mood}"


def _masters_score(master_reco: dict | None, pick: dict) -> tuple[float, str]:
    if not master_reco:
        return 50.0, "大师未就绪"
    symbol = pick.get("symbol")
    market = pick.get("market")
    hits = 0
    total = 0
    for block in master_reco.get("masters") or []:
        total += 1
        for item in block.get("picks") or []:
            if item.get("symbol") == symbol:
                hits += 2
                break
            if item.get("market") == market and item.get("score", 0) >= 70:
                hits += 1
    if total == 0:
        return 50.0, "无大师数据"
    ratio = hits / (total * 2)
    return max(0, min(100, 40 + ratio * 60)), f"大师共识 {hits}/{total}"


def _truth_score(truth: dict | None, pick: dict) -> tuple[float, str]:
    if not truth:
        return 50.0, "Truth 未就绪"
    sector = (pick.get("sector") or "").lower()
    economy_tags = {"energy", "trade", "economy", "military", "iran"}
    now = datetime.now(timezone.utc)
    hot = 0
    for post in truth.get("posts") or []:
        published = post.get("publishedAt")
        if not published:
            continue
        try:
            dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if now - dt > timedelta(hours=48):
            continue
        tags = {t.get("id") for t in post.get("tags") or []}
        if tags & economy_tags:
            hot += 1
    # 能源/半导体等板块与舆情热度弱相关
    sector_boost = 0
    if sector and any(k in sector for k in ("半导体", "能源", "银行", "消费")):
        sector_boost = 5
    score = 50 + min(hot * 8, 30) + sector_boost
    return max(0, min(100, score)), f"舆情热度 {hot}"


def score_pick(
    pick: dict,
    *,
    market_summary: dict | None = None,
    macro: dict | None = None,
    wencai: dict | None = None,
    master_reco: dict | None = None,
    truth: dict | None = None,
) -> dict:
    macro_s, macro_n = _macro_score(macro, market_summary)
    wencai_s, wencai_n = _wencai_score(wencai)
    master_s, master_n = _masters_score(master_reco, pick)
    truth_s, truth_n = _truth_score(truth, pick)

    total = (
        macro_s * WEIGHTS["macro"]
        + wencai_s * WEIGHTS["wencai"]
        + master_s * WEIGHTS["masters"]
        + truth_s * WEIGHTS["truth"]
    )
    total = round(total, 1)
    if total >= 70:
        label = "高"
    elif total >= 50:
        label = "中"
    else:
        label = "低"

    return {
        "decisionScore": total,
        "decisionLabel": label,
        "decisionComponents": {
            "macro": {"score": round(macro_s, 1), "note": macro_n},
            "wencai": {"score": round(wencai_s, 1), "note": wencai_n},
            "masters": {"score": round(master_s, 1), "note": master_n},
            "truth": {"score": round(truth_s, 1), "note": truth_n},
        },
    }


def load_context_files() -> dict:
    return {
        "macro": _load(DATA_DIR / "macro.json"),
        "wencai": _load(DATA_DIR / "wencai.json"),
        "truth": _load(DATA_DIR / "trump_truth.json"),
    }


def enrich_picks(
    picks: list[dict],
    market_summary: dict | None,
    master_reco: dict | None,
    ctx: dict | None = None,
) -> list[dict]:
    ctx = ctx or load_context_files()
    enriched = []
    for pick in picks:
        scored = score_pick(
            pick,
            market_summary=market_summary,
            macro=ctx.get("macro"),
            wencai=ctx.get("wencai"),
            master_reco=master_reco,
            truth=ctx.get("truth"),
        )
        enriched.append({**pick, **scored})
    return enriched
