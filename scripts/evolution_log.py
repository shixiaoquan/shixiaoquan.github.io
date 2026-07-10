"""进化事件日志 — 追加写入 data/evolution_log.json，供看板与 Cursor 审阅。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "data" / "evolution_log.json"
MAX_EVENTS = 80


def _load() -> dict:
    if LOG_FILE.exists():
        try:
            data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"version": 1, "events": []}


def append_event(event_type: str, payload: dict | None = None) -> dict:
    """追加一条进化事件并持久化。"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = _load()
    events = data.setdefault("events", [])
    entry = {
        "at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "type": event_type,
        **(payload or {}),
    }
    events.insert(0, entry)
    data["events"] = events[:MAX_EVENTS]
    data["updatedAt"] = entry["at"]
    LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry


def recent_events(limit: int = 8) -> list[dict]:
    return (_load().get("events") or [])[:limit]
