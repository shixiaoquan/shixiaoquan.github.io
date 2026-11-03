#!/usr/bin/env python3
"""小米业务雷达 — 把策展收件箱聚成簇，写出 data/xiaomi_radar.json。

不抓网页。新事实追加到 data/xiaomi_radar_inbox.json，再运行本脚本。
行情流水线会调用它，所以收件箱更新后下一次数据任务会重算。
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
INBOX_PATH = DATA_DIR / "xiaomi_radar_inbox.json"
OUTPUT = DATA_DIR / "xiaomi_radar.json"
HK_TZ = ZoneInfo("Asia/Hong_Kong")

CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1}
CONFIDENCE_LABEL = {"high": "高", "medium": "中", "low": "低"}
TONE_LABEL = {"strength": "强项", "pressure": "压力", "watch": "观察"}
DISCLAIMER = "仅供研究参考，不构成投资建议。"
DEFAULT_STALE_DAYS = 21


def today_hk() -> date:
    return datetime.now(HK_TZ).date()


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _https(value: object) -> str | None:
    if isinstance(value, str) and value.startswith("https://"):
        return value
    return None


def _confidence(value: object) -> str:
    if value in CONFIDENCE_RANK:
        return str(value)
    return "low"


def _tone(value: object) -> str:
    if value in TONE_LABEL:
        return str(value)
    return "watch"


def normalize_item(raw: dict, as_of: date, stale_days: int) -> dict | None:
    if not isinstance(raw, dict):
        return None
    title = str(raw.get("title") or "").strip()
    source = str(raw.get("source") or "").strip()
    if not title or not source:
        return None
    item_id = str(raw.get("id") or title)
    parsed = _parse_date(raw.get("date") or raw.get("asOf"))
    age = (as_of - parsed).days if parsed else None
    evergreen = bool(raw.get("evergreen"))
    stale = bool(parsed and age is not None and age > stale_days and not evergreen)
    if parsed is None:
        stale = True
    confidence = _confidence(raw.get("confidence"))
    tone = _tone(raw.get("tone"))
    return {
        "id": item_id,
        "clusterId": str(raw.get("clusterId") or "uncategorized"),
        "pillar": str(raw.get("pillar") or "未分类"),
        "tone": tone,
        "toneLabel": TONE_LABEL[tone],
        "title": title,
        "detail": str(raw.get("detail") or ""),
        "source": source,
        "sourceUrl": _https(raw.get("sourceUrl")),
        "date": parsed.isoformat() if parsed else None,
        "confidence": confidence,
        "confidenceLabel": CONFIDENCE_LABEL[confidence],
        "evergreen": evergreen,
        "stale": stale,
        "ageDays": age,
    }


def build_radar(inbox: dict | None, *, as_of: date | None = None) -> dict:
    inbox = inbox or {}
    as_of = as_of or today_hk()
    try:
        stale_days = int(inbox.get("staleAfterDays") or DEFAULT_STALE_DAYS)
    except (TypeError, ValueError):
        stale_days = DEFAULT_STALE_DAYS
    if stale_days < 1:
        stale_days = DEFAULT_STALE_DAYS

    normalized: list[dict] = []
    dropped = 0
    for raw in inbox.get("items") or []:
        item = normalize_item(raw, as_of, stale_days)
        if item is None:
            dropped += 1
            continue
        normalized.append(item)

    labels = inbox.get("clusters") if isinstance(inbox.get("clusters"), dict) else {}
    grouped: dict[str, list[dict]] = {}
    for item in normalized:
        grouped.setdefault(item["clusterId"], []).append(item)

    clusters = []
    for cluster_id, members in grouped.items():
        members.sort(key=lambda row: (row.get("date") or "", row["id"]), reverse=True)
        meta = labels.get(cluster_id) if isinstance(labels.get(cluster_id), dict) else {}
        worst = min(CONFIDENCE_RANK[row["confidence"]] for row in members)
        confidence = next(key for key, rank in CONFIDENCE_RANK.items() if rank == worst)
        latest = next((row["date"] for row in members if row.get("date")), None)
        clusters.append(
            {
                "id": cluster_id,
                "title": meta.get("title") or members[0]["pillar"],
                "pillar": meta.get("pillar") or members[0]["pillar"],
                "summary": meta.get("summary") or "",
                "confidence": confidence,
                "confidenceLabel": CONFIDENCE_LABEL[confidence],
                "latestDate": latest,
                "staleCount": sum(1 for row in members if row["stale"]),
                "items": members,
            }
        )
    clusters.sort(key=lambda row: (row.get("latestDate") or "", row["id"]), reverse=True)

    flat = sorted(normalized, key=lambda row: (row.get("date") or "", row["id"]), reverse=True)
    now = datetime.now(HK_TZ).isoformat(timespec="seconds")
    return {
        "version": 2,
        "generatedBy": "scripts/xiaomi_radar.py",
        "updatedAt": now,
        "asOf": as_of.isoformat(),
        "disclaimer": inbox.get("disclaimer") or DISCLAIMER,
        "feed": {
            "mode": "curated",
            "inbox": "data/xiaomi_radar_inbox.json",
            "staleAfterDays": stale_days,
            "dropped": dropped,
            "note": "把带 source、date、confidence 的条目追加到收件箱后运行 scripts/xiaomi_radar.py。没有爬虫。",
        },
        "clusters": clusters,
        "items": flat,
    }


def run() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_radar(_load(INBOX_PATH), as_of=today_hk())
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Xiaomi radar: clusters={len(payload['clusters'])} "
        f"items={len(payload['items'])} dropped={payload['feed']['dropped']}"
    )
    return payload


if __name__ == "__main__":
    run()
