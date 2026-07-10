#!/usr/bin/env python3
"""reco_history 归档 + 生成前端用的 recent 切片。"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ARCHIVE_DIR = DATA_DIR / "archive"
HISTORY_FILE = DATA_DIR / "reco_history.json"
RECENT_FILE = DATA_DIR / "reco_history_recent.json"

KEEP_IN_MAIN = 80
RECENT_FOR_UI = 60
ARCHIVE_AFTER_DAYS = 90


def _load(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "records": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"version": 1, "records": []}
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "records": []}


def _parse_dt(text: str) -> datetime | None:
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def run_archive() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    history = _load(HISTORY_FILE)
    records = history.get("records") or []
    if not records:
        return {"archived": 0, "kept": 0}

    cutoff = now - timedelta(days=ARCHIVE_AFTER_DAYS)
    to_archive = []
    to_keep = []
    for rec in records:
        ts = _parse_dt(rec.get("recordedAt") or "")
        if ts and ts < cutoff:
            to_archive.append(rec)
        else:
            to_keep.append(rec)

    if len(to_keep) > KEEP_IN_MAIN:
        overflow = to_keep[: len(to_keep) - KEEP_IN_MAIN]
        to_archive.extend(overflow)
        to_keep = to_keep[-KEEP_IN_MAIN:]

    archived_count = 0
    if to_archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        month_key = now.strftime("%Y-%m")
        archive_file = ARCHIVE_DIR / f"reco_{month_key}.json"
        existing = _load(archive_file)
        merged_ids = {r.get("id") for r in existing.get("records") or []}
        new_rows = [r for r in to_archive if r.get("id") not in merged_ids]
        if new_rows:
            existing.setdefault("records", []).extend(new_rows)
            existing["updatedAt"] = now.isoformat(timespec="seconds")
            archive_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
            archived_count = len(new_rows)

    history["records"] = to_keep
    history["updatedAt"] = now.isoformat(timespec="seconds")
    history["total"] = len(to_keep)
    history["archivedTotal"] = int(history.get("archivedTotal") or 0) + archived_count
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

    recent = {
        "version": 1,
        "updatedAt": now.isoformat(timespec="seconds"),
        "records": to_keep[-RECENT_FOR_UI:],
        "total": len(to_keep[-RECENT_FOR_UI:]),
    }
    RECENT_FILE.write_text(json.dumps(recent, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Archive: moved {archived_count}, kept {len(to_keep)}, recent UI {recent['total']}")
    return {"archived": archived_count, "kept": len(to_keep), "recent": recent["total"]}


def write_recent_slice(history: dict | None = None) -> None:
    """fetch_data 每次更新后同步 recent 切片。"""
    history = history or _load(HISTORY_FILE)
    records = history.get("records") or []
    now = datetime.now(timezone.utc).astimezone()
    recent = {
        "version": 1,
        "updatedAt": now.isoformat(timespec="seconds"),
        "records": records[-RECENT_FOR_UI:],
        "total": min(len(records), RECENT_FOR_UI),
    }
    RECENT_FILE.write_text(json.dumps(recent, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    run_archive()
