#!/usr/bin/env python3
"""汇总各数据模块新鲜度与策略进化指标，写入 data/site_status.json。"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "site_status.json"

STALE_MINUTES = {
    "market": 45,
    "macro": 45,
    "truth": 60,
    "wencai": 150,
    "reports": 60 * 48,
    "backtest": 60 * 24 * 10,
}

PIPELINES = (
    {
        "id": "market",
        "name": "行情·荐股·模拟盘",
        "schedule": "每 5 分钟",
        "workflow": "update-market-data.yml",
        "files": ("market.json", "signals.json", "paper_account.json"),
    },
    {
        "id": "macro",
        "name": "宏观与跨资产",
        "schedule": "每 5 分钟",
        "workflow": "update-market-data.yml",
        "files": ("macro.json",),
    },
    {
        "id": "truth",
        "name": "Truth Social 镜像",
        "schedule": "每 10 分钟",
        "workflow": "update-truth-social.yml",
        "files": ("trump_truth.json",),
    },
    {
        "id": "wencai",
        "name": "问财自然语言筛选",
        "schedule": "每小时",
        "workflow": "update-wencai-data.yml",
        "files": ("wencai.json",),
    },
    {
        "id": "reports",
        "name": "投资决策研报",
        "schedule": "09:00 / 12:00 / 16:00 北京时间",
        "workflow": "generate-investment-report.yml",
        "files": ("reports/index.json",),
    },
    {
        "id": "backtest",
        "name": "策略周度回测",
        "schedule": "每周日",
        "workflow": "weekly-backtest.yml",
        "files": ("backtest.json", "paper_backtest.json"),
    },
)


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _parse_dt(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _updated_at(data: dict | list | None) -> str | None:
    if isinstance(data, dict):
        return data.get("updatedAt") or data.get("generatedAt")
    return None


def _pipeline_status(pipe_id: str, files: tuple[str, ...], now: datetime) -> tuple[str | None, str, int | None]:
    latest: str | None = None
    found = 0
    for name in files:
        data = _load_json(DATA_DIR / name)
        if data is None:
            continue
        found += 1
        ts = _updated_at(data)
        if ts and (latest is None or ts > latest):
            latest = ts
    if found == 0:
        return None, "missing", None
    if not latest:
        return None, "empty", None
    updated = _parse_dt(latest)
    age_min = int((now - updated).total_seconds() / 60) if updated else None
    limit = STALE_MINUTES.get(pipe_id, 120)
    if age_min is not None and age_min > limit:
        return latest, "stale", age_min
    return latest, "ok", age_min


def _evolution_block() -> dict:
    master = _load_json(DATA_DIR / "master_strategy_state.json") or {}
    versions = _load_json(DATA_DIR / "strategy_versions.json") or {}
    history = _load_json(DATA_DIR / "reco_history.json") or {}
    backtest = _load_json(DATA_DIR / "backtest.json") or {}
    attribution = _load_json(DATA_DIR / "reco_attribution.json") or {}
    candidates = _load_json(DATA_DIR / "strategy_candidates.json") or {}

    try:
        from strategy_config import STRATEGY_NAME, STRATEGY_VERSION
    except ImportError:
        STRATEGY_VERSION = "unknown"
        STRATEGY_NAME = "策略"

    perf = master.get("performance") or {}
    win_rates = [
        p.get("winRate")
        for p in perf.values()
        if isinstance(p, dict) and p.get("winRate") is not None
    ]
    avg_master_win = round(sum(win_rates) / len(win_rates), 1) if win_rates else None
    attr_summary = attribution.get("summary") or {}

    return {
        "strategyVersion": STRATEGY_VERSION,
        "strategyName": STRATEGY_NAME,
        "masterLearnRevision": master.get("revision"),
        "masterLearnUpdatedAt": master.get("updatedAt"),
        "masterAvgWinRate": avg_master_win,
        "recoHistoryRecords": len(history.get("records") or []),
        "strategyCatalogCount": len(versions.get("versions") or []),
        "currentPaperSystem": versions.get("current"),
        "backtestUpdatedAt": backtest.get("updatedAt"),
        "backtestWinRate": (backtest.get("summary") or {}).get("winRate"),
        "recoAvgReturnT5": attr_summary.get("avgReturnT5"),
        "recoWinRateT5": attr_summary.get("winRateT5"),
        "strategyUpgradePending": bool(candidates.get("recommendUpgrade")),
        "strategyUpgradeHint": candidates.get("upgradeReason") or "",
        "shadowReadyForPR": bool(
            (_load_json(DATA_DIR / "shadow_reco.json") or {}).get("comparison", {}).get("readyForUpgradePR")
        ),
    }


def build_payload() -> dict:
    now = datetime.now(timezone.utc).astimezone()
    pipelines = []
    stale_count = 0
    for spec in PIPELINES:
        updated_at, status, age_min = _pipeline_status(spec["id"], spec["files"], now)
        if status == "stale":
            stale_count += 1
        pipelines.append(
            {
                "id": spec["id"],
                "name": spec["name"],
                "schedule": spec["schedule"],
                "workflow": spec["workflow"],
                "updatedAt": updated_at,
                "status": status,
                "ageMinutes": age_min,
            }
        )

    ok_count = sum(1 for p in pipelines if p["status"] == "ok")
    evolution = _evolution_block()

    try:
        from evolution_log import recent_events

        recent_log = recent_events(6)
    except Exception:
        recent_log = (_load_json(DATA_DIR / "evolution_log.json") or {}).get("events", [])[:6]

    evolution_queue = _load_json(DATA_DIR / "evolution_queue.json") or {}

    return {
        "updatedAt": now.isoformat(timespec="seconds"),
        "mode": "github-actions",
        "summary": {
            "pipelinesTotal": len(pipelines),
            "pipelinesHealthy": ok_count,
            "pipelinesStale": stale_count,
            "automation": "持续运行中" if stale_count == 0 else f"{stale_count} 条流水线过期",
            "deploy": "GitHub Pages · master 推送即发布",
            "resources": "零增量成本：GitHub Actions + 现有 Secrets + Cursor PR",
        },
        "evolution": evolution,
        "evolutionQueue": evolution_queue,
        "recentLog": recent_log,
        "pipelines": pipelines,
        "triggeredBy": os.environ.get("GITHUB_WORKFLOW") or "local",
        "runId": os.environ.get("GITHUB_RUN_ID"),
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    ev = payload["evolution"]
    print(
        f"Wrote {OUTPUT} · ok {payload['summary']['pipelinesHealthy']}/"
        f"{payload['summary']['pipelinesTotal']} · stale {payload['summary']['pipelinesStale']} · "
        f"strategy {ev.get('strategyVersion')} · learn #{ev.get('masterLearnRevision')}"
    )


if __name__ == "__main__":
    main()
