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


def check_xiaomi_trader() -> None:
    data = _load(DATA_DIR / "xiaomi_trader.json")
    if not data:
        WARNINGS.append("xiaomi_trader.json 未生成")
        return
    for key in ("disclaimer", "calendar", "scenarios", "checklist"):
        if key not in data:
            ERRORS.append(f"xiaomi_trader 缺少 {key}")
    disclaimer = data.get("disclaimer") or ""
    if "不构成投资建议" not in disclaimer:
        ERRORS.append("xiaomi_trader disclaimer 缺少「不构成投资建议」")
    upcoming = (data.get("calendar") or {}).get("upcoming")
    if not isinstance(upcoming, list):
        ERRORS.append("xiaomi_trader.calendar.upcoming 不是列表")
    scenario_ids = [
        row.get("id")
        for row in (data.get("scenarios") or {}).get("items") or []
        if isinstance(row, dict)
    ]
    for scenario_id in ("bull", "base", "bear"):
        if scenario_id not in scenario_ids:
            ERRORS.append(f"xiaomi_trader 缺少情景 {scenario_id}")
    gate_ids = [
        row.get("id")
        for row in (data.get("checklist") or {}).get("gates") or []
        if isinstance(row, dict)
    ]
    for gate_id in ("catalyst", "valuation", "position", "exit"):
        if gate_id not in gate_ids:
            ERRORS.append(f"xiaomi_trader 缺少开仓门 {gate_id}")
    label = (data.get("scenarios") or {}).get("assumptionLabel") or ""
    if "假设" not in label:
        ERRORS.append("xiaomi_trader 情景未标明为假设")
    for key in ("stance", "indicators", "weeklyReview", "riskLimits"):
        if key not in data:
            ERRORS.append(f"xiaomi_trader 缺少 {key}")
    stance = data.get("stance") or {}
    if stance and "不" not in str(stance.get("headline") or "") and stance.get("tone") == "block":
        ERRORS.append("xiaomi_trader 拦住时立场标题没有说不")
    weekly_rows = (data.get("weeklyReview") or {}).get("rows")
    if data.get("weeklyReview") is not None and not isinstance(weekly_rows, list):
        ERRORS.append("xiaomi_trader.weeklyReview.rows 不是列表")
    iot = ((data.get("indicators") or {}).get("iotMargin")) or {}
    if data.get("indicators") and not iot.get("placeholder"):
        ERRORS.append("xiaomi_trader IoT 毛利率必须标明占位，除非种子改成已披露")

    radar = _load(DATA_DIR / "xiaomi_radar.json")
    if not radar:
        WARNINGS.append("xiaomi_radar.json 缺失")
        return
    if not isinstance(radar.get("items"), list):
        ERRORS.append("xiaomi_radar.items 不是列表")
    clusters = radar.get("clusters")
    if not isinstance(clusters, list) or not clusters:
        ERRORS.append("xiaomi_radar.clusters 缺失")
        return
    for cluster in clusters:
        if not isinstance(cluster, dict):
            ERRORS.append("xiaomi_radar 簇不是对象")
            continue
        for item in cluster.get("items") or []:
            if not isinstance(item, dict):
                continue
            if not item.get("source"):
                ERRORS.append(f"xiaomi_radar {item.get('id')} 缺少 source")
            if item.get("confidence") not in {"high", "medium", "low"}:
                ERRORS.append(f"xiaomi_radar {item.get('id')} confidence 无效")
            if "date" not in item:
                ERRORS.append(f"xiaomi_radar {item.get('id')} 缺少 date")


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
    check_xiaomi_trader()

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
