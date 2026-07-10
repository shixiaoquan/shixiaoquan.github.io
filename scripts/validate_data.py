#!/usr/bin/env python3
"""数据契约校验 — CI 提交前 Schema Gate。"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def _load(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        ERRORS.append(f"{path.name}: JSON 无效 ({exc})")
        return None


def _parse_dt(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _age_hours(text: str | None) -> float | None:
    dt = _parse_dt(text)
    if not dt:
        return None
    now = datetime.now(timezone.utc).astimezone()
    return (now - dt).total_seconds() / 3600


def check_market_core() -> None:
    data = _load(DATA_DIR / "market_core.json")
    if not data:
        WARNINGS.append("market_core.json 缺失（将回退 market.json）")
        data = _load(DATA_DIR / "market.json")
    if not data:
        ERRORS.append("market.json / market_core.json 均缺失")
        return
    for key in ("updatedAt", "summary", "quoteMap", "indices"):
        if key not in data:
            ERRORS.append(f"market 缺少字段 {key}")


def check_reports() -> None:
    idx = _load(DATA_DIR / "reports" / "index.json")
    if not idx:
        ERRORS.append("reports/index.json 缺失")
        return
    age = _age_hours(idx.get("updatedAt"))
    if age is not None and age > 72:
        WARNINGS.append(f"研报超过 72h 未更新（{age:.0f}h）")


def check_strategy_candidates() -> None:
    data = _load(DATA_DIR / "strategy_candidates.json")
    if not data:
        return
    if data.get("recommendUpgrade") and not data.get("insufficientSamples"):
        best = data.get("bestCandidate") or {}
        trades = best.get("totalTrades") or 0
        if trades < 10:
            ERRORS.append(f"recommendUpgrade=true 但 bestCandidate 仅 {trades} 笔（需≥10 或走影子轨）")
        if not _load(DATA_DIR / "shadow_reco.json"):
            WARNINGS.append("recommendUpgrade 已置位但 shadow_reco.json 不存在")


def check_shadow() -> None:
    data = _load(DATA_DIR / "shadow_reco.json")
    if not data:
        WARNINGS.append("shadow_reco.json 未生成")
        return
    if not data.get("candidateParams"):
        ERRORS.append("shadow_reco 缺少 candidateParams")
    records = (data.get("history") or {}).get("records") or []
    if len(records) >= 4:
        attr = _load(DATA_DIR / "shadow_attribution.json")
        if not attr:
            WARNINGS.append("影子轨有历史但 shadow_attribution.json 未生成")


def check_evolution_queue() -> None:
    data = _load(DATA_DIR / "evolution_queue.json")
    if not data:
        WARNINGS.append("evolution_queue.json 未生成")
        return
    if "tasks" not in data:
        ERRORS.append("evolution_queue 缺少 tasks")


def check_reco_history() -> None:
    data = _load(DATA_DIR / "reco_history_recent.json")
    if not data:
        WARNINGS.append("reco_history_recent.json 缺失")
        return
    records = data.get("records") or []
    if records:
        last = records[-1]
        picks = last.get("picks") or []
        if picks and "decisionScore" not in picks[0]:
            WARNINGS.append("reco 历史尚未含 decisionScore（旧记录可忽略）")


def main() -> int:
    check_market_core()
    check_reports()
    check_strategy_candidates()
    check_shadow()
    check_evolution_queue()
    check_reco_history()

    for w in WARNINGS:
        print(f"WARN: {w}")
    for e in ERRORS:
        print(f"ERROR: {e}")

    if ERRORS:
        print(f"Schema gate FAILED ({len(ERRORS)} errors)")
        return 1
    print(f"Schema gate OK ({len(WARNINGS)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
