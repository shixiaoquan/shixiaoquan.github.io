#!/usr/bin/env python3
"""流水线健康检查 — 检测数据过期，供 Actions 开/关 GitHub Issue（零外部通知成本）。"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
STATUS_FILE = DATA_DIR / "site_status.json"
ISSUE_TITLE = "[自动] 数据流水线异常"

# 交易时段阈值；休市时 market/macro 放宽（见 market_calendar）
STALE_MINUTES = {
    "market": 45,
    "macro": 45,
    "truth": 90,  # 10min 调度，允许并发推送延迟
    "wencai": 150,
    "reports": 60 * 48,
    "backtest": 60 * 24 * 10,
}

STALE_MINUTES_CLOSED = {
    **STALE_MINUTES,
    "market": 60 * 18,  # 休市过夜不告警
    "macro": 60 * 18,
}


def _parse_dt(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _limits() -> dict[str, int]:
    try:
        from market_calendar import market_intensity

        if market_intensity() == "closed":
            return STALE_MINUTES_CLOSED
    except Exception:
        pass
    return STALE_MINUTES


def check_stale() -> tuple[list[dict], list[dict]]:
    if not STATUS_FILE.exists():
        return [], [{"id": "site_status", "issue": "site_status.json 缺失"}]
    data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).astimezone()
    limits = _limits()
    stale: list[dict] = []
    healthy: list[dict] = []
    for pipe in data.get("pipelines") or []:
        pid = pipe.get("id")
        updated = _parse_dt(pipe.get("updatedAt"))
        limit = limits.get(pid, 120)
        if pipe.get("status") != "ok" or not updated:
            stale.append({**pipe, "reason": pipe.get("status") or "no timestamp"})
            continue
        age_min = (now - updated).total_seconds() / 60
        if age_min > limit:
            stale.append({**pipe, "reason": f"过期 {int(age_min)} 分钟（阈值 {limit}）"})
        else:
            healthy.append(pipe)
    return healthy, stale


def format_issue_body(stale: list[dict]) -> str:
    lines = [
        "此 Issue 由 `continuous-evolution` 工作流自动创建。",
        "",
        "以下数据流水线超过新鲜度阈值：",
        "",
    ]
    for p in stale:
        lines.append(
            f"- **{p.get('name')}** (`{p.get('id')}`): {p.get('reason')} · "
            f"工作流 `{p.get('workflow')}`"
        )
    lines.extend(
        [
            "",
            "排查建议：",
            "1. 打开 [Actions](https://github.com/shixiaoquan/shixiaoquan.github.io/actions) 查看失败日志",
            "2. 检查 Secrets（WENCAI_COOKIE 等）是否过期",
            "3. 修复后本 Issue 将在下次健康检查通过时自动关闭",
            "",
            "<!-- pipeline-health-bot -->",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    healthy, stale = check_stale()
    print(f"Healthy: {len(healthy)}, Stale: {len(stale)}")
    for p in stale:
        print(f"  STALE {p.get('id')}: {p.get('reason')}")

    if os.environ.get("GITHUB_ACTIONS") != "true":
        return 1 if stale else 0

    out = ROOT / "data" / "pipeline_health.json"
    out.write_text(
        json.dumps(
            {
                "checkedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "stale": stale,
                "healthyCount": len(healthy),
                "issueTitle": ISSUE_TITLE,
                "issueBody": format_issue_body(stale) if stale else "",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
