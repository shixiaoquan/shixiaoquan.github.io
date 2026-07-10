#!/usr/bin/env python3
"""进化指令总线 — 汇总机器产出，供驾驶舱与 Cursor 单入口消费。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "evolution_queue.json"


def _load(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def build_queue() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    tasks: list[dict] = []

    shadow = _load("shadow_reco.json")
    cmp_ = shadow.get("comparison") or {}
    if cmp_.get("readyForUpgradePR"):
        params = shadow.get("candidateParams") or {}
        tasks.append(
            {
                "id": "shadow-upgrade-pr",
                "type": "strategy_pr",
                "priority": "high",
                "title": "影子轨验证通过 · 可申请升级战术参数",
                "reason": cmp_.get("reason"),
                "cursorPrompt": (
                    f"影子轨已满 4 周且优于生产。请更新 strategy_config.py："
                    f"BUY_SCORE={params.get('buyScore')}, BREAKOUT_SCORE_MIN={params.get('breakoutScoreMin')}，"
                    f"追加 strategy_versions.json 记录并开 PR。"
                ),
                "params": params,
            }
        )
    elif shadow.get("candidateParams"):
        tasks.append(
            {
                "id": "shadow-tracking",
                "type": "shadow_track",
                "priority": "medium",
                "title": "影子轨积累中",
                "reason": cmp_.get("reason", "并行记账"),
                "cursorPrompt": "无需操作，继续观察 shadow_reco.json comparison。",
            }
        )

    candidates = _load("strategy_candidates.json")
    shadow_pending = candidates.get("shadowCandidate") or (
        candidates.get("recommendUpgrade") and not cmp_.get("readyForUpgradePR")
    )
    if shadow_pending and not cmp_.get("readyForUpgradePR"):
        best = candidates.get("bestCandidate") or {}
        tasks.append(
            {
                "id": "candidate-explore",
                "type": "shadow_candidate",
                "priority": "medium",
                "title": "探索参数优于当前 · 已转入影子轨验证",
                "reason": candidates.get("upgradeReason"),
                "cursorPrompt": "勿直接改 strategy_config。确认 shadow_reco 满 4 周后再开 PR。",
                "params": {"buyScore": best.get("buyScore"), "breakoutScoreMin": best.get("breakoutScoreMin")},
            }
        )

    health = _load("pipeline_health.json")
    for item in health.get("stale") or []:
        tasks.append(
            {
                "id": f"fix-pipeline-{item.get('id')}",
                "type": "fix_pipeline",
                "priority": "high",
                "title": f"流水线过期 · {item.get('name')}",
                "reason": item.get("reason"),
                "cursorPrompt": f"检查工作流 {item.get('workflow')} 日志与 Secrets。",
            }
        )

    status = _load("site_status.json")
    if (status.get("summary") or {}).get("pipelinesStale", 0) > 0 and not health.get("stale"):
        tasks.append(
            {
                "id": "pipelines-stale",
                "type": "fix_pipeline",
                "priority": "medium",
                "title": "部分流水线数据过期",
                "reason": status.get("summary", {}).get("automation"),
                "cursorPrompt": "阅读 data/site_status.json pipelines 并修复对应 Actions。",
            }
        )

    tune = _load("tactic_tune.json")
    if tune.get("active"):
        tasks.append(
            {
                "id": "tactic-tune-active",
                "type": "tactic_tune",
                "priority": "low",
                "title": f"战术门槛自适应调整 {tune.get('buyScoreAdjust'):+d}",
                "reason": "; ".join(tune.get("notes") or []),
                "cursorPrompt": "可选：审阅 tactic_tune.json 是否需固化到 strategy_config。",
            }
        )

    ab = _load("paper_ab.json")
    if ab.get("leader") == "v1.2_relaxed":
        tasks.append(
            {
                "id": "paper-ab-hint",
                "type": "research",
                "priority": "low",
                "title": "A/B 回测：v1.2 宽松优于 v1.3",
                "reason": f"Δ期望 {ab.get('delta', {}).get('expectancy')}%",
                "cursorPrompt": "仅研究参考；生产升级仍以影子轨 forward 为准。",
            }
        )

    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: priority_order.get(t.get("priority", "low"), 9))

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "tasks": tasks[:12],
        "summary": {
            "total": len(tasks),
            "high": sum(1 for t in tasks if t.get("priority") == "high"),
            "topAction": tasks[0]["cursorPrompt"] if tasks else "暂无待办，系统正常运转。",
        },
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Evolution queue: {len(tasks)} tasks (high={payload['summary']['high']})")
    return payload


if __name__ == "__main__":
    build_queue()
