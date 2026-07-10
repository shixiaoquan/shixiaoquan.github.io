#!/usr/bin/env python3
"""进化队列高优任务检查 — 供 Actions 开/关 GitHub Issue。"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
QUEUE_FILE = DATA_DIR / "evolution_queue.json"
ISSUE_TITLE = "[自动] 进化队列高优任务待审阅"


def _load_queue() -> dict:
    if not QUEUE_FILE.exists():
        return {}
    try:
        return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def find_actionable_tasks(queue: dict) -> list[dict]:
    tasks = queue.get("tasks") or []
    actionable = []
    for task in tasks:
        priority = task.get("priority")
        task_type = task.get("type")
        if priority == "high" or task_type in ("strategy_pr", "shadow_track"):
            if task.get("id") == "shadow-tracking":
                continue
            actionable.append(task)
    return actionable


def format_issue_body(tasks: list[dict]) -> str:
    lines = [
        "此 Issue 由 `continuous-evolution` 工作流自动创建。",
        "",
        "以下进化任务需要 Cursor / 人工审阅：",
        "",
    ]
    for task in tasks[:8]:
        lines.append(f"- **{task.get('title')}** (`{task.get('id')}`)")
        if task.get("reason"):
            lines.append(f"  - {task['reason']}")
        if task.get("cursorPrompt"):
            lines.append(f"  - Cursor：`{task['cursorPrompt']}`")
    lines.extend(
        [
            "",
            "处理建议：",
            "1. 阅读 `data/evolution_queue.json` 与 `data/shadow_reco.json`",
            "2. 按 `.github/EVOLUTION_PLAYBOOK.md` 开 PR 或修复流水线",
            "3. 任务完成后本 Issue 将在下次检查通过时自动关闭",
            "",
            "<!-- evolution-queue-bot -->",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    queue = _load_queue()
    tasks = find_actionable_tasks(queue)
    print(f"Evolution queue actionable: {len(tasks)}")
    for task in tasks:
        print(f"  {task.get('priority')} {task.get('id')}: {task.get('title')}")

    if os.environ.get("GITHUB_ACTIONS") != "true":
        return 1 if tasks else 0

    out = DATA_DIR / "evolution_queue_health.json"
    out.write_text(
        json.dumps(
            {
                "checkedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "actionable": tasks,
                "issueTitle": ISSUE_TITLE,
                "issueBody": format_issue_body(tasks) if tasks else "",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return 1 if tasks else 0


if __name__ == "__main__":
    sys.exit(main())
