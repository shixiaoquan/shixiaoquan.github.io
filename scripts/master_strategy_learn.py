"""大师策略在线学习 — 每次数据更新时根据历史荐股表现与市场环境微调权重。"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
STATE_FILE = DATA_DIR / "master_strategy_state.json"
HISTORY_FILE = DATA_DIR / "master_reco_history.json"

BASE_VERSION = "v1.2"
LEARNING_RATE = 0.04
MIN_WEIGHT = 0.55
MAX_WEIGHT = 1.55
MIN_SAMPLES_FOR_LEARN = 3
MAX_HISTORY = 300
MIN_HISTORY_HOURS = 24

MASTER_IDS = (
    "buffett",
    "graham",
    "lynch",
    "munger",
    "templeton",
    "soros",
    "serenity",
)

DEFAULT_FACTORS: dict[str, dict[str, float]] = {
    "buffett": {
        "roe": 1.0,
        "pe": 1.0,
        "margins": 1.0,
        "debt": 1.0,
        "trend": 1.0,
        "mcap": 1.0,
    },
    "graham": {
        "pe": 1.0,
        "pb": 1.0,
        "range": 1.0,
        "dividend": 1.0,
        "debt": 1.0,
    },
    "lynch": {
        "peg": 1.0,
        "earnings": 1.0,
        "revenue": 1.0,
        "sector": 1.0,
    },
    "munger": {
        "roe": 1.0,
        "margins": 1.0,
        "debt": 1.0,
        "pe": 1.0,
        "trend": 1.0,
    },
    "templeton": {
        "month": 1.0,
        "quarter": 1.0,
        "range": 1.0,
        "pe": 1.0,
        "roe": 1.0,
    },
    "soros": {
        "month": 1.0,
        "rs": 1.0,
        "trend": 1.0,
        "volume": 1.0,
        "beta": 1.0,
    },
    "serenity": {
        "sector": 1.0,
        "tag": 1.0,
        "mcap": 1.0,
        "growth": 1.0,
        "range": 1.0,
        "momentum": 1.0,
    },
}

REGIME_BOOSTS: dict[str, dict[str, float]] = {
    "risk_off": {"graham": 1.06, "templeton": 1.08, "buffett": 1.04, "soros": 0.94},
    "risk_on": {"soros": 1.08, "lynch": 1.06, "serenity": 1.08, "graham": 0.94},
    "neutral": {},
}


def _clamp_weight(val: float) -> float:
    return round(max(MIN_WEIGHT, min(MAX_WEIGHT, val)), 3)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def default_state() -> dict:
    return {
        "baseVersion": BASE_VERSION,
        "revision": 0,
        "updatedAt": None,
        "weights": deepcopy(DEFAULT_FACTORS),
        "performance": {mid: {"samples": 0, "winRate": None, "avgReturnPct": None} for mid in MASTER_IDS},
        "lastUpgrade": None,
        "upgradeNotes": {},
        "regime": "neutral",
    }


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("weights"), dict):
                state = default_state()
                state.update(data)
                for mid in MASTER_IDS:
                    state["weights"].setdefault(mid, deepcopy(DEFAULT_FACTORS[mid]))
                    for factor, default in DEFAULT_FACTORS[mid].items():
                        state["weights"][mid].setdefault(factor, default)
                    state["performance"].setdefault(mid, {"samples": 0, "winRate": None, "avgReturnPct": None})
                return state
        except (json.JSONDecodeError, OSError):
            pass
    return default_state()


def save_state(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_master_history() -> dict:
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("records"), list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"version": 1, "records": []}


def master_picks_fingerprint(master_reco: dict) -> str:
    parts = []
    for master in master_reco.get("masters") or []:
        for pick in master.get("picks") or []:
            parts.append(f"{master.get('id')}:{pick.get('symbol')}:{round(pick.get('matchScore', 0))}")
    return "|".join(sorted(parts))


def should_append_master_history(records: list[dict], master_reco: dict, recorded_at: datetime) -> bool:
    if not master_reco.get("masters"):
        return False
    if not records:
        return True
    last = records[-1]
    if master_picks_fingerprint(last) != master_picks_fingerprint(master_reco):
        return True
    last_time = _parse_dt(last.get("recordedAt"))
    if not last_time:
        return True
    current = recorded_at if recorded_at.tzinfo else recorded_at.replace(tzinfo=timezone.utc)
    elapsed_h = (current - last_time).total_seconds() / 3600
    return elapsed_h >= 6


def append_master_history(master_reco: dict, recorded_at: datetime) -> dict:
    history = load_master_history()
    records: list[dict] = history.get("records", [])
    compact_masters = []
    for master in master_reco.get("masters") or []:
        compact_masters.append(
            {
                "id": master.get("id"),
                "picks": [
                    {
                        "symbol": p.get("symbol"),
                        "name": p.get("name"),
                        "price": p.get("price"),
                        "matchScore": p.get("matchScore"),
                        "factors": p.get("factors") or {},
                    }
                    for p in master.get("picks") or []
                ],
            }
        )

    if should_append_master_history(records, master_reco, recorded_at):
        record = {
            "id": recorded_at.isoformat(timespec="seconds"),
            "recordedAt": recorded_at.isoformat(timespec="seconds"),
            "version": master_reco.get("version"),
            "masters": compact_masters,
        }
        records.append(record)
        records = records[-MAX_HISTORY:]
        history["records"] = records
        history["updatedAt"] = recorded_at.isoformat(timespec="seconds")
        history["total"] = len(records)
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {HISTORY_FILE} ({len(records)} records)")
    else:
        print("Master reco history unchanged, skip append.")
    return history


def _detect_regime(market: dict | None, macro: dict | None) -> str:
    mood = (market or {}).get("summary", {}).get("mood")
    vix = (macro or {}).get("summary", {}).get("vix")
    if vix is not None and vix >= 22:
        return "risk_off"
    if mood == "偏空" or (vix is not None and vix >= 18):
        return "risk_off"
    if mood == "偏多":
        return "risk_on"
    avg = (market or {}).get("summary", {}).get("avgChangePct")
    if avg is not None and avg > 0.5:
        return "risk_on"
    return "neutral"


def _evaluate_history(quote_map: dict[str, float], now: datetime) -> tuple[dict, list[dict]]:
    history = load_master_history()
    perf: dict[str, list[float]] = {mid: [] for mid in MASTER_IDS}
    learning_events: list[dict] = []

    for record in history.get("records", []):
        recorded_at = _parse_dt(record.get("recordedAt"))
        if not recorded_at:
            continue
        age_h = (now - recorded_at).total_seconds() / 3600
        if age_h < MIN_HISTORY_HOURS:
            continue

        for master in record.get("masters") or []:
            mid = master.get("id")
            if mid not in perf:
                continue
            for pick in master.get("picks") or []:
                symbol = pick.get("symbol")
                entry = pick.get("price")
                current = quote_map.get(symbol)
                if not entry or not current:
                    continue
                ret = round((current - entry) / entry * 100, 2)
                perf[mid].append(ret)
                factors = pick.get("factors") or {}
                if factors:
                    learning_events.append(
                        {
                            "masterId": mid,
                            "symbol": symbol,
                            "returnPct": ret,
                            "factors": factors,
                        }
                    )

    performance = {}
    for mid, returns in perf.items():
        if not returns:
            performance[mid] = {"samples": 0, "winRate": None, "avgReturnPct": None}
        else:
            wins = sum(1 for r in returns if r > 0)
            performance[mid] = {
                "samples": len(returns),
                "winRate": round(wins / len(returns) * 100, 1),
                "avgReturnPct": round(sum(returns) / len(returns), 2),
            }
    return performance, learning_events


def _upgrade_weights(state: dict, learning_events: list[dict], regime: str) -> tuple[dict, dict[str, str]]:
    weights = deepcopy(state.get("weights") or default_state()["weights"])
    notes: dict[str, str] = {}
    changed = False

    by_master: dict[str, list[dict]] = {mid: [] for mid in MASTER_IDS}
    for event in learning_events:
        mid = event.get("masterId")
        if mid in by_master:
            by_master[mid].append(event)

    for mid, events in by_master.items():
        if len(events) < MIN_SAMPLES_FOR_LEARN:
            continue
        factor_deltas: dict[str, list[float]] = {}
        for event in events:
            ret = event.get("returnPct") or 0
            direction = 1 if ret > 0 else -1 if ret < 0 else 0
            if direction == 0:
                continue
            magnitude = min(abs(ret) / 15, 1.0)
            for factor, contribution in (event.get("factors") or {}).items():
                if not contribution:
                    continue
                factor_deltas.setdefault(factor, []).append(direction * magnitude * LEARNING_RATE)

        master_notes = []
        for factor, deltas in factor_deltas.items():
            if factor not in weights.get(mid, {}):
                continue
            delta = sum(deltas) / len(deltas)
            old = weights[mid][factor]
            new = _clamp_weight(old + delta)
            if abs(new - old) >= 0.01:
                weights[mid][factor] = new
                changed = True
                if delta > 0:
                    master_notes.append(f"{factor}↑")
                else:
                    master_notes.append(f"{factor}↓")

        if master_notes:
            notes[mid] = "近期表现反馈：" + "、".join(master_notes[:4])

    regime_boost = REGIME_BOOSTS.get(regime) or {}
    if regime_boost:
        regime_notes = []
        for mid, boost in regime_boost.items():
            if mid not in weights:
                continue
            for factor in weights[mid]:
                old = weights[mid][factor]
                new = _clamp_weight(old * boost)
                if abs(new - old) >= 0.01:
                    weights[mid][factor] = new
                    changed = True
            if boost != 1.0:
                regime_notes.append(f"{mid}×{boost:.2f}")
        if regime_notes:
            notes["_regime"] = f"市场环境({regime})：" + "、".join(regime_notes[:5])

    if changed:
        state["weights"] = weights
    return state, notes


def upgrade_master_strategies(
    quote_map: dict[str, float],
    market: dict | None = None,
    macro: dict | None = None,
    now: datetime | None = None,
) -> dict:
    """每次站点数据更新时调用：评估历史 → 微调权重 → 持久化。"""
    now = now or datetime.now(timezone.utc).astimezone()
    state = load_state()
    performance, learning_events = _evaluate_history(quote_map, now)
    regime = _detect_regime(market, macro)

    prev_weights = deepcopy(state.get("weights", {}))
    state, notes = _upgrade_weights(state, learning_events, regime)

    state["performance"] = performance
    state["regime"] = regime
    state["updatedAt"] = now.isoformat(timespec="seconds")

    weight_changed = json.dumps(prev_weights, sort_keys=True) != json.dumps(state.get("weights"), sort_keys=True)
    if weight_changed:
        state["revision"] = int(state.get("revision") or 0) + 1
        state["lastUpgrade"] = now.isoformat(timespec="seconds")
        state["upgradeNotes"] = notes
        print(f"Master strategy upgraded → {BASE_VERSION}.{state['revision']} ({regime})")
        try:
            from evolution_log import append_event

            append_event(
                "master_learn",
                {
                    "revision": state["revision"],
                    "regime": regime,
                    "notes": notes,
                },
            )
        except Exception as exc:
            print(f"evolution_log skip: {exc}")
    else:
        state["upgradeNotes"] = notes or state.get("upgradeNotes") or {}

    save_state(state)
    return state


def format_version(state: dict) -> str:
    rev = int(state.get("revision") or 0)
    return f"{state.get('baseVersion', BASE_VERSION)}.{rev}"


def get_master_weights(master_id: str, state: dict | None = None) -> dict[str, float]:
    state = state or load_state()
    defaults = DEFAULT_FACTORS.get(master_id, {})
    saved = (state.get("weights") or {}).get(master_id, {})
    return {k: float(saved.get(k, v)) for k, v in defaults.items()}
