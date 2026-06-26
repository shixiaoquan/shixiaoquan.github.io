"""战术荐股信号跟踪 — 轻量生命周期，写入 data/signals.json。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from strategy_config import SIGNAL_MAX_HOLD_DAYS, STRATEGY_VERSION

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SIGNALS_FILE = DATA_DIR / "signals.json"
MAX_SIGNALS = 200
TRAIL_GIVEBACK_PCT = 50
TRAIL_MIN_GAIN_PCT = 8.0

OPEN_STATUS = "open"
CLOSED_STATUSES = frozenset(
    {"closed_stop", "closed_trail", "closed_target", "closed_expired"}
)


def load_signals() -> dict:
    if SIGNALS_FILE.exists():
        try:
            data = json.loads(SIGNALS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("signals"), list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": "tactical",
        "disclaimer": "实验策略信号跟踪，仅供复盘，非 XRPS 模拟盘。",
        "signals": [],
        "openCount": 0,
        "closedCount": 0,
    }


def save_signals(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SIGNALS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _parse_dt(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _hold_days(opened_at: str, now: datetime) -> int:
    try:
        start = _parse_dt(opened_at)
        end = now if now.tzinfo else now.replace(tzinfo=timezone.utc)
        return max(0, (end - start).days)
    except (ValueError, TypeError):
        return 0


def _close_signal(sig: dict, price: float, now_iso: str, status: str, reason: str) -> None:
    sig["status"] = status
    sig["exitPrice"] = round(price, 2)
    sig["exitAt"] = now_iso
    sig["closeReason"] = reason
    entry = sig.get("entryPrice") or 0
    if entry:
        sig["returnPct"] = round((price - entry) / entry * 100, 2)


def _new_signal(pick: dict, now_iso: str, reco_id: str | None) -> dict:
    return {
        "id": f"{now_iso}#{pick['symbol']}",
        "symbol": pick["symbol"],
        "name": pick["name"],
        "market": pick["market"],
        "signal": pick.get("signal", "buy"),
        "score": pick.get("score"),
        "status": OPEN_STATUS,
        "entryPrice": pick.get("price"),
        "openedAt": now_iso,
        "currentPrice": pick.get("price"),
        "exitPrice": None,
        "exitAt": None,
        "stopLossPrice": pick.get("stopLossPrice"),
        "targetPrice": pick.get("targetPrice"),
        "returnPct": 0.0,
        "maxGainPct": 0.0,
        "maxDrawdownPct": 0.0,
        "holdDays": 0,
        "closeReason": None,
        "recoRecordId": reco_id,
    }


def _update_open(sig: dict, price: float, now: datetime, now_iso: str) -> None:
    entry = sig.get("entryPrice") or 0
    if not entry:
        return

    ret = (price - entry) / entry * 100
    sig["currentPrice"] = round(price, 2)
    sig["returnPct"] = round(ret, 2)
    sig["maxGainPct"] = round(max(sig.get("maxGainPct", ret), ret), 2)
    sig["maxDrawdownPct"] = round(min(sig.get("maxDrawdownPct", ret), ret), 2)
    sig["holdDays"] = _hold_days(sig.get("openedAt", now_iso), now)

    stop = sig.get("stopLossPrice")
    if stop is not None and price <= stop:
        _close_signal(sig, price, now_iso, "closed_stop", "止损")
        return

    target = sig.get("targetPrice")
    if target is not None and price >= target:
        _close_signal(sig, price, now_iso, "closed_target", "止盈")
        return

    max_gain = sig.get("maxGainPct", 0)
    if max_gain >= TRAIL_MIN_GAIN_PCT and ret <= max_gain * (1 - TRAIL_GIVEBACK_PCT / 100):
        _close_signal(sig, price, now_iso, "closed_trail", "跟踪止损")
        return

    if sig["holdDays"] >= SIGNAL_MAX_HOLD_DAYS:
        _close_signal(sig, price, now_iso, "closed_expired", "持有到期")


def _trim_signals(signals: list[dict]) -> list[dict]:
    open_sigs = [s for s in signals if s.get("status") == OPEN_STATUS]
    closed = [s for s in signals if s.get("status") in CLOSED_STATUSES]
    closed.sort(key=lambda s: s.get("exitAt") or s.get("openedAt") or "", reverse=True)
    keep_closed = max(0, MAX_SIGNALS - len(open_sigs))
    return open_sigs + closed[:keep_closed]


def _build_summary(signals: list[dict]) -> dict:
    closed = [s for s in signals if s.get("status") in CLOSED_STATUSES]
    open_sigs = [s for s in signals if s.get("status") == OPEN_STATUS]
    wins = sum(1 for s in closed if (s.get("returnPct") or 0) > 0)
    tracked = [s for s in closed if s.get("returnPct") is not None]
    avg_return = (
        round(sum(s["returnPct"] for s in tracked) / len(tracked), 2) if tracked else None
    )
    return {
        "openCount": len(open_sigs),
        "closedCount": len(closed),
        "winRate": round(wins / len(closed) * 100, 1) if closed else None,
        "avgReturn": avg_return,
    }


def update_reco_signals(
    picks: list[dict],
    quote_map: dict[str, float],
    now: datetime,
    reco_record_id: str | None = None,
) -> dict:
    """根据最新荐股与行情更新战术信号。"""
    now_iso = now.isoformat(timespec="seconds")
    data = load_signals()
    signals: list[dict] = data.get("signals", [])

    for sig in signals:
        if sig.get("status") != OPEN_STATUS:
            continue
        price = quote_map.get(sig["symbol"])
        if price is None:
            continue
        _update_open(sig, float(price), now, now_iso)

    open_symbols = {s["symbol"] for s in signals if s.get("status") == OPEN_STATUS}
    for pick in picks:
        if pick.get("signal") != "buy":
            continue
        if pick["symbol"] in open_symbols:
            continue
        signals.append(_new_signal(pick, now_iso, reco_record_id))
        open_symbols.add(pick["symbol"])

    signals = _trim_signals(signals)
    summary = _build_summary(signals)

    payload = {
        "updatedAt": now_iso,
        "strategyVersion": STRATEGY_VERSION,
        "strategyCode": "tactical",
        "disclaimer": data.get("disclaimer") or "实验策略信号跟踪，仅供复盘，非 XRPS 模拟盘。",
        "signals": signals,
        "openCount": summary["openCount"],
        "closedCount": summary["closedCount"],
        "summary": summary,
    }
    save_signals(payload)
    print(
        f"Wrote {SIGNALS_FILE} (open {summary['openCount']}, closed {summary['closedCount']})"
    )
    return payload
