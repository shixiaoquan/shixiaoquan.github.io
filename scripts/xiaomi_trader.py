#!/usr/bin/env python3
"""小米交易员看板 — 合并人工种子与公开行情，写出 data/xiaomi_trader.json。

不替代 XRPS 滚动仓或 HK01810 箱体。不抓新闻。
情景数字来自种子文件，是假设，不是业绩预测。
"""

from __future__ import annotations

import json
from calendar import monthrange
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SEED_PATH = DATA_DIR / "xiaomi_trader_seed.json"
BOX_PATH = DATA_DIR / "hk01810_box.json"
MACRO_PATH = DATA_DIR / "macro.json"
PAPER_PATH = DATA_DIR / "paper_account.json"
RADAR_PATH = DATA_DIR / "xiaomi_radar.json"
OUTPUT = DATA_DIR / "xiaomi_trader.json"

HK_TZ = ZoneInfo("Asia/Hong_Kong")
YI = 100_000_000
USDHKD_PEG = 7.80
HORIZON_DEFAULT = 60
SOON_DAYS = 30
RECENT_DAYS = 7

SCENARIO_ORDER = ("bull", "base", "bear")
GATE_ORDER = ("catalyst", "valuation", "position", "exit")
GATE_LABELS = {
    "catalyst": "催化",
    "valuation": "估值",
    "position": "仓位",
    "exit": "退出",
}
STATUS_LABELS = {
    "pass": "自动通过",
    "caution": "需人工",
    "block": "自动拦住",
    "open": "待填写",
}
KIND_LABELS = {
    "earnings": "业绩",
    "delivery": "交付",
    "product": "产品",
    "data": "数据",
}
DEFAULT_PROMPTS = {
    "catalyst": "写下这笔要验证的催化、证据和最晚确认日。没有窗口就不开。",
    "valuation": "写下你能接受的经调整净利润倍数。现价更高时说明为什么还要买。",
    "position": "真实仓位写在本地笔记，不要放进公开仓库。未写上限视为此门未过。",
    "exit": "写下价格、时间和基本面三条失效条件。先到哪条就走。",
}
DISCLAIMER = "仅供研究参考，不构成投资建议。"


def today_hk() -> date:
    return datetime.now(HK_TZ).date()


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _round(value: float | None, digits: int = 1) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _add_months(year: int, month: int, offset: int) -> tuple[int, int]:
    index = year * 12 + (month - 1) + offset
    return index // 12, index % 12 + 1


def _clamp_day(year: int, month: int, day: int) -> date:
    last = monthrange(year, month)[1]
    return date(year, month, min(max(day, 1), last))


def _countdown_label(days: int) -> str:
    if days == 0:
        return "今天"
    if days == 1:
        return "明天"
    if days > 1:
        return f"{days} 天"
    if days == -1:
        return "昨天"
    return f"已过 {-days} 天"


def _https_url(value: object) -> str | None:
    if isinstance(value, str) and value.startswith("https://"):
        return value
    return None


def _event_item(raw: dict, date_str: str | None, *, item_id: str | None = None, title: str | None = None) -> dict:
    kind = raw.get("kind") if raw.get("kind") in KIND_LABELS else "data"
    return {
        "id": item_id or raw.get("id"),
        "kind": kind,
        "kindLabel": KIND_LABELS.get(kind, "事项"),
        "title": title or raw.get("title") or "未命名事项",
        "date": date_str,
        "source": raw.get("source") or "",
        "sourceUrl": _https_url(raw.get("sourceUrl")),
        "note": raw.get("note") or "",
    }


def _stamp_days(item: dict, as_of: date, horizon_days: int) -> int | None:
    parsed = _parse_date(item.get("date"))
    if parsed is None:
        return None
    days = (parsed - as_of).days
    item["daysUntil"] = days
    item["countdownLabel"] = _countdown_label(days)
    item["within30"] = 0 <= days <= SOON_DAYS
    item["within60"] = 0 <= days <= horizon_days
    return days


def _monthly_occurrences(raw: dict, as_of: date, horizon_days: int) -> list[dict]:
    try:
        day = int(raw.get("dayOfMonth") or 1)
    except (TypeError, ValueError):
        day = 1
    start = date(as_of.year, as_of.month, 1)
    found: list[dict] = []
    for offset in range(0, 4):
        year, month = _add_months(start.year, start.month, offset)
        occ = _clamp_day(year, month, day)
        days = (occ - as_of).days
        if days < 0 or days > horizon_days:
            continue
        base_title = raw.get("title") or "月度事项"
        if raw.get("kind") == "delivery":
            prev_year, prev_month = _add_months(year, month, -1)
            title = f"{base_title} · 披露{prev_year}年{prev_month}月交付"
        else:
            title = f"{base_title} · {occ.isoformat()}"
        found.append(
            _event_item(
                raw,
                occ.isoformat(),
                item_id=f"{raw.get('id')}:{occ.isoformat()}",
                title=title,
            )
        )
    return found


def expand_calendar(events: list | None, as_of: date, horizon_days: int = HORIZON_DEFAULT) -> dict:
    """把种子事件展开成未来 horizon 天、以及刚过去 7 天。"""
    upcoming: list[dict] = []
    recent: list[dict] = []
    undated: list[dict] = []
    horizon = horizon_days if isinstance(horizon_days, int) and horizon_days > 0 else HORIZON_DEFAULT

    for raw in events or []:
        if not isinstance(raw, dict):
            continue
        if raw.get("recurrence") == "monthly":
            occurrences = _monthly_occurrences(raw, as_of, horizon)
            for item in occurrences:
                days = _stamp_days(item, as_of, horizon)
                if days is not None and 0 <= days <= horizon:
                    upcoming.append(item)
            continue

        item = _event_item(raw, raw.get("date") if isinstance(raw.get("date"), str) else None)
        if item["date"] is None:
            undated.append(item)
            continue
        days = _stamp_days(item, as_of, horizon)
        if days is None:
            undated.append(item)
            continue
        if 0 <= days <= horizon:
            upcoming.append(item)
        elif -RECENT_DAYS <= days < 0:
            recent.append(item)

    upcoming.sort(key=lambda row: (row["daysUntil"], str(row.get("title"))))
    recent.sort(key=lambda row: row["daysUntil"], reverse=True)
    return {
        "asOf": as_of.isoformat(),
        "horizonDays": horizon,
        "soonDays": SOON_DAYS,
        "next": upcoming[0] if upcoming else None,
        "upcoming": upcoming,
        "recent": recent,
        "undated": undated,
    }


def _fx_price(macro: dict | None, symbol: str) -> float | None:
    if not macro:
        return None
    for row in macro.get("fx") or []:
        if not isinstance(row, dict) or row.get("symbol") != symbol:
            continue
        price = row.get("price")
        if isinstance(price, (int, float)) and price > 0:
            return float(price)
    return None


def cny_per_hkd(macro: dict | None) -> tuple[float | None, str]:
    usdcny = _fx_price(macro, "USDCNY=X") or _fx_price(macro, "USDCNH=X")
    usdhkd = _fx_price(macro, "USDHKD=X")
    note_parts: list[str] = []
    if usdhkd is None:
        usdhkd = USDHKD_PEG
        note_parts.append(f"宏观缺少 USDHKD，暂用 {USDHKD_PEG:.2f} 联系汇率近似")
    else:
        note_parts.append(f"USDHKD {usdhkd:.4f}")
    if usdcny is None:
        note_parts.append("宏观缺少 USDCNY/USDCNH，人民币市值暂缺")
        return None, "；".join(note_parts)
    used = "USDCNY" if _fx_price(macro, "USDCNY=X") else "USDCNH"
    note_parts.insert(0, f"{used} {usdcny:.4f}")
    return usdcny / usdhkd, "；".join(note_parts)


def market_cap_hkd_yi(price: float | None, shares: float | None) -> float | None:
    if price is None or not shares or shares <= 0 or price <= 0:
        return None
    return float(price) * float(shares) / YI


def implied_pe(market_cap_cny_yi: float | None, profit_yi: float | None) -> float | None:
    if market_cap_cny_yi is None or profit_yi is None:
        return None
    if profit_yi <= 0:
        return None
    return round(float(market_cap_cny_yi) / float(profit_yi), 1)


def _price_from_box(box: dict | None) -> float | None:
    quote = (box or {}).get("quote") or {}
    price = quote.get("price")
    if isinstance(price, (int, float)):
        return float(price)
    return None


def _advice_for(box: dict | None, price: float | None) -> dict:
    if price is None:
        advice = (box or {}).get("advice")
        return advice if isinstance(advice, dict) else {}
    try:
        from hk01810_box import decide
    except ImportError:
        advice = (box or {}).get("advice")
        return advice if isinstance(advice, dict) else {}
    return decide(price)


def _position_in_box(box: dict | None, price: float | None) -> float | None:
    levels = (box or {}).get("levels") or {}
    low = levels.get("boxLow")
    high = levels.get("boxHigh")
    if price is None or not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
        stored = (box or {}).get("positionInBox")
        return float(stored) if isinstance(stored, (int, float)) else None
    if high == low:
        return None
    return round(max(0.0, min(1.0, (float(price) - float(low)) / (float(high) - float(low)))), 3)


def _public_sim(paper: dict | None) -> dict | None:
    if not paper:
        return None
    def _num(key: str, digits: int = 2) -> float | None:
        value = paper.get(key)
        if isinstance(value, (int, float)):
            return round(float(value), digits)
        return None

    position = _num("positionPct", 1)
    if position is None and _num("equity") is None:
        return None
    return {
        "label": "XRPS-X 公开模拟盘（站点已有数据，不是真实账户）",
        "strategyCode": paper.get("strategyCode"),
        "positionPct": position,
        "equityHkd": _num("equity"),
        "cashHkd": _num("cash"),
        "coreValueHkd": _num("coreValue"),
        "rollingValueHkd": _num("rollingValue"),
        "returnPct": _num("returnPct", 1),
    }


def _fmt_hkd(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:,.0f}"


def _gate(status: str, summary: str, prompt: str, note: str, *, downgrade_pass_without_note: bool = False) -> dict:
    clean_note = note.strip()
    if downgrade_pass_without_note and status == "pass" and not clean_note:
        status = "caution"
    if status not in STATUS_LABELS:
        status = "open"
    return {
        "status": status,
        "statusLabel": STATUS_LABELS[status],
        "summary": summary,
        "humanPrompt": prompt,
        "humanNote": clean_note,
    }


def _limit_number(limits: dict | None, key: str, default: float) -> float:
    raw = (limits or {}).get(key)
    if isinstance(raw, (int, float)):
        return float(raw)
    return default


def build_catalyst_gate(
    calendar: dict,
    *,
    human_note: str = "",
    block_within_days: int = 21,
) -> tuple[str, str]:
    upcoming = calendar.get("upcoming") or []
    earnings = [row for row in upcoming if row.get("kind") == "earnings"]
    noted = bool((human_note or "").strip())
    if earnings:
        event = earnings[0]
        days = event.get("daysUntil")
        near = isinstance(days, int) and days <= block_within_days
        base = (
            f"{event.get('countdownLabel')}后是业绩窗口：{event.get('title')}（{event.get('date')}）。"
            "催化要写清赌的是交付、利润还是预期差。"
        )
        if near and not noted:
            return "block", base + "窗口内没有写下赌注，叙事不得写成现在加仓。"
        if noted:
            return "caution", base + "备注已写，但业绩还没落地，催化门仍不自动放行。"
        return "caution", base + "窗口还没近到拦截线，仍然不能单凭日历开仓。"
    if not upcoming:
        return "block", "未来 60 天没有已填写日期的催化。没有窗口，叙事不得写成即将开仓。"
    nxt = calendar.get("next") or {}
    return (
        "caution",
        f"未来 {calendar.get('horizonDays', HORIZON_DEFAULT)} 天内最近的事项是{nxt.get('title')}（{nxt.get('countdownLabel')}）。这还不是一条写清了的开仓催化。",
    )


def build_valuation_gate(
    price: float | None,
    advice: dict,
    base_pe: float | None,
    limits: dict | None = None,
    history_pe: float | None = None,
) -> tuple[str, str]:
    action = (advice or {}).get("action")
    label = (advice or {}).get("actionLabel") or "观望"
    add_cap = _limit_number(limits, "maxBasePeToAdd", 22)
    rich = _limit_number(limits, "richBasePe", 30)
    if price is None or base_pe is None:
        return "open", "股价或基准情景倍数缺失，估值门不能判断。"

    reasons: list[str] = []
    blocked = False
    if base_pe > rich:
        blocked = True
        reasons.append(f"基准情景 {base_pe:.1f} 倍，高于贵价线 {rich:.0f} 倍")
    elif base_pe > add_cap:
        blocked = True
        reasons.append(f"基准情景 {base_pe:.1f} 倍，高于加仓线 {add_cap:.0f} 倍")
    else:
        reasons.append(f"基准情景 {base_pe:.1f} 倍，未超过加仓线 {add_cap:.0f} 倍")

    if history_pe is not None:
        reasons.append(f"相对上半年经调整净利润年化约 {history_pe:.1f} 倍，这不是多年历史估值带")

    if action in {"sell", "breakout_up", "exit"}:
        blocked = True
        reasons.append(f"箱体建议「{label}」，价格位置也不支持新开多")
    elif action == "buy":
        reasons.append(f"箱体在买区（{label}），只说明位置，不能单独打开估值门")
    else:
        reasons.append(f"箱体建议「{label}」")
        if not blocked:
            return "caution", f"现价 {price:.2f} 港元。" + "。".join(reasons) + "。位置中性，不新开多。"

    if blocked:
        return "block", f"现价 {price:.2f} 港元。" + "。".join(reasons) + "。估值门拦住，不新开多。"
    return "pass", f"现价 {price:.2f} 港元。" + "。".join(reasons) + "。倍数和买区都不反对，仍不是目标价。"


def build_position_gate(
    sim: dict | None,
    position_in_box: float | None,
    limits: dict | None = None,
) -> tuple[str, str]:
    if isinstance(position_in_box, (int, float)):
        box_txt = f"股价在日常箱子里的位置约 {position_in_box * 100:.0f}%。"
    else:
        box_txt = "箱体位置暂缺。"
    add_ceiling = _limit_number(limits, "addCeilingPct", 40)
    max_position = _limit_number(limits, "maxPositionPct", 80)
    if not sim or sim.get("positionPct") is None:
        return "open", f"{box_txt}公开模拟盘不可用。真实仓位不要写进这个网站，仓位门因此开着但不可用。"
    held = float(sim["positionPct"])
    detail = (
        f"{box_txt}XRPS 公开模拟盘仓位 {held}% "
        f"（权益约 {_fmt_hkd(sim.get('equityHkd'))} 港元，现金约 {_fmt_hkd(sim.get('cashHkd'))} 港元）。"
        f"交易台加仓线 {add_ceiling:.0f}%，XRPS 总仓上限 {max_position:.0f}%。这不是真实持仓。"
    )
    if held >= add_ceiling:
        return "block", detail + "模拟盘已经不低于加仓线，叙事不得再写成加仓。"
    return "caution", detail + "仓位低于加仓线，但真实账户上限还没写，此门不通过。"


def build_exit_gate(advice: dict, levels: dict | None, limits: dict | None = None) -> tuple[str, str]:
    stops = [str(item) for item in (limits or {}).get("fundamentalStops") or [] if str(item).strip()]
    stop_txt = "基本面退出：" + "；".join(stops) + "。" if stops else "种子里还没有基本面退出条件。"
    if not advice and not stops:
        return "open", "没有箱体规则，也没有基本面退出。先写价格、时间和业绩三条再谈开仓。"
    bottom = (levels or {}).get("bottom")
    bottom_txt = f"收盘跌破 {float(bottom):.2f} 按箱体清仓。" if isinstance(bottom, (int, float)) else ""
    box_txt = ""
    if advice:
        box_txt = (
            f"箱体：空仓「{advice.get('emptyAdvice') or '—'}」，"
            f"持仓「{advice.get('holdingAdvice') or '—'}」。{bottom_txt}"
        )
    return (
        "pass",
        f"{stop_txt}{box_txt}退出要同时看业绩和价格。人工备注空着时，此门仍算未过。",
    )


def _human_by_id(seed: dict) -> dict[str, dict]:
    gates = ((seed.get("checklist") or {}).get("gates")) or []
    found: dict[str, dict] = {}
    for gate in gates:
        if isinstance(gate, dict) and gate.get("id") in GATE_LABELS:
            found[str(gate["id"])] = gate
    return found


def build_stance(narrative: dict, gates: list[dict]) -> dict:
    blocked = [gate for gate in gates if gate["status"] == "block"]
    pending = [gate for gate in gates if gate["status"] != "pass"]
    research = narrative or {}
    if blocked:
        names = "、".join(gate["label"] for gate in blocked)
        tone = "block"
        headline = f"不新开多。{names}把门拦住了。"
        allowed = ["更新假设对照", "等交付或三季报改写事实", "价格回到加仓线和买区再重算四门"]
        forbidden = ["把交付好转写成现在加仓", "用情景倍数代替已披露业绩", "在 IoT 毛利率空着时谈论毛利率改善"]
    elif pending:
        names = "、".join(gate["label"] for gate in pending)
        tone = "caution"
        headline = f"只研究，不开新仓。{names}还没过。"
        allowed = ["维护研究叙事", "把人工备注写进种子文件后再生成"]
        forbidden = ["在四门未全过时给出开仓结论"]
    else:
        tone = "pass"
        headline = "四门都过，才可以讨论开仓。这仍不是投资建议。"
        allowed = ["按写下来的仓位和退出条件讨论一笔"]
        forbidden = ["把通过四门写成已经该买"]
    return {
        "tone": tone,
        "headline": headline,
        "allowed": allowed,
        "forbidden": forbidden,
        "researchHeadline": research.get("headline") or "",
        "researchBody": research.get("body") or "",
        "researchLabel": "研究叙事。它描述业务，不能覆盖上面的立场。",
    }


def build_indicators(seed: dict) -> dict:
    raw = seed.get("indicators") or {}
    auto = raw.get("autoMonthly") or {}
    points = []
    for point in auto.get("points") or []:
        if not isinstance(point, dict):
            continue
        value = point.get("value")
        if not isinstance(value, (int, float)):
            continue
        quality = point.get("quality") if point.get("quality") in {"reported", "lower_bound"} else "reported"
        points.append({"period": point.get("period"), "value": int(value), "quality": quality})
    reported = [point["value"] for point in points if point["quality"] == "reported"]
    latest = points[-1] if points else None
    return {
        "autoMonthly": {
            "label": auto.get("label") or "汽车月交付",
            "unit": auto.get("unit") or "辆",
            "source": auto.get("source") or "",
            "fyTarget": auto.get("fyTarget"),
            "points": points,
            "latest": latest,
            "reportedAverage": round(sum(reported) / len(reported)) if reported else None,
        },
        "phone": raw.get("phone") or {"placeholder": True, "available": False, "note": "没有出货和 ASP。"},
        "memoryCost": raw.get("memoryCost") or {"placeholder": True, "note": "没有存储成本数字。"},
        "iotMargin": raw.get("iotMargin") or {"placeholder": True, "value": None, "note": "IoT 毛利率占位。"},
        "groupGrossMargin": raw.get("groupGrossMargin") or {},
    }


def build_weekly_review(seed: dict, as_of: date) -> dict:
    raw = seed.get("weeklyReview") or {}
    week_of = as_of - timedelta(days=as_of.weekday())
    rows = []
    counts = {"met": 0, "missed": 0, "pending": 0, "behind": 0, "mixed": 0}
    for row in raw.get("rows") or []:
        if not isinstance(row, dict):
            continue
        verdict = row.get("verdict") if row.get("verdict") in counts else "pending"
        counts[verdict] += 1
        rows.append(
            {
                "id": row.get("id"),
                "topic": row.get("topic") or "",
                "assumption": row.get("assumption") or "",
                "actual": row.get("actual") or "",
                "verdict": verdict,
                "source": row.get("source") or "",
                "asOf": row.get("asOf"),
            }
        )
    return {
        "title": raw.get("title") or "本周假设对照",
        "weekOf": week_of.isoformat(),
        "asOf": as_of.isoformat(),
        "rows": rows,
        "counts": counts,
        "note": "实际栏只写已经公开的事实。没公布的保持待验证，不用预览填上。",
    }


def build_checklist(
    seed: dict,
    calendar: dict,
    *,
    price: float | None,
    advice: dict,
    base_pe: float | None,
    history_pe: float | None,
    sim: dict | None,
    position_in_box: float | None,
    levels: dict | None,
    limits: dict | None,
) -> dict:
    humans = _human_by_id(seed)
    limits = limits or {}
    catalyst_note = str((humans.get("catalyst") or {}).get("humanNote") or "")
    builders = {
        "catalyst": lambda: build_catalyst_gate(
            calendar,
            human_note=catalyst_note,
            block_within_days=int(_limit_number(limits, "catalystBlockWithinDays", 21)),
        ),
        "valuation": lambda: build_valuation_gate(price, advice, base_pe, limits, history_pe),
        "position": lambda: build_position_gate(sim, position_in_box, limits),
        "exit": lambda: build_exit_gate(advice, levels, limits),
    }
    gates = []
    for gate_id in GATE_ORDER:
        status, summary = builders[gate_id]()
        human = humans.get(gate_id) or {}
        prompt = human.get("humanPrompt") or DEFAULT_PROMPTS[gate_id]
        note = human.get("humanNote") or ""
        gates.append(
            {
                "id": gate_id,
                "label": GATE_LABELS[gate_id],
                **_gate(
                    status,
                    summary,
                    str(prompt),
                    str(note),
                    downgrade_pass_without_note=(gate_id == "exit"),
                ),
            }
        )
    counts = {key: 0 for key in STATUS_LABELS}
    for gate in gates:
        counts[gate["status"]] = counts.get(gate["status"], 0) + 1
    return {
        "gates": gates,
        "counts": counts,
        "readyToOpen": counts["pass"] == len(gates) and counts["block"] == 0,
        "editHint": "四门决定页首立场。人工判断写在 data/xiaomi_trader_seed.json 的 checklist.gates[].humanNote，再运行 scripts/xiaomi_trader.py。公开页面不保存浏览器里的临时修改。",
    }


def _scenario_items(seed: dict, market_cap_cny: float | None) -> list[dict]:
    raw_items = ((seed.get("scenarios") or {}).get("items")) or []
    by_id = {row.get("id"): row for row in raw_items if isinstance(row, dict)}
    label_fallback = {"bull": "乐观", "base": "基准", "bear": "悲观"}
    items = []
    metric = (seed.get("scenarios") or {}).get("profitMetric") or "adjusted_net_profit"
    metric_label = (seed.get("scenarios") or {}).get("profitMetricLabel") or "经调整净利润（Non-IFRS）"
    for scenario_id in SCENARIO_ORDER:
        raw = by_id.get(scenario_id) or {}
        profit = raw.get("adjustedNetProfitYi")
        profit_num = float(profit) if isinstance(profit, (int, float)) else None
        revenue = raw.get("revenueYi")
        items.append(
            {
                "id": scenario_id,
                "label": raw.get("label") or label_fallback[scenario_id],
                "revenueYi": _round(revenue, 1) if isinstance(revenue, (int, float)) else None,
                "profitMetric": metric,
                "profitMetricLabel": metric_label,
                "adjustedNetProfitYi": _round(profit_num, 1) if profit_num is not None else None,
                "impliedPe": implied_pe(market_cap_cny, profit_num),
                "narrative": raw.get("narrative") or "种子文件缺少这段假设。",
            }
        )
    return items


def _box_view(box: dict | None, price: float | None, advice: dict, position_in_box: float | None) -> dict:
    levels = (box or {}).get("levels") or {}
    quote = (box or {}).get("quote") or {}
    keep_levels = {}
    for key in ("boxLow", "boxHigh", "bottom"):
        if isinstance(levels.get(key), (int, float)):
            keep_levels[key] = levels[key]
    return {
        "price": _round(price, 2) if price is not None else None,
        "asOf": quote.get("asOf"),
        "changePct": quote.get("changePct") if isinstance(quote.get("changePct"), (int, float)) else None,
        "positionInBox": position_in_box,
        "levels": keep_levels,
        "advice": {
            "action": advice.get("action"),
            "actionLabel": advice.get("actionLabel"),
            "tone": advice.get("tone"),
            "zoneId": advice.get("zoneId"),
            "title": advice.get("title"),
            "emptyAdvice": advice.get("emptyAdvice"),
            "holdingAdvice": advice.get("holdingAdvice"),
        },
    }


def build_payload(
    seed: dict | None,
    *,
    box: dict | None = None,
    macro: dict | None = None,
    paper: dict | None = None,
    radar: dict | None = None,
    as_of: date | None = None,
) -> dict:
    seed = seed or {}
    as_of = as_of or today_hk()
    calendar_seed = seed.get("calendar") or {}
    horizon = calendar_seed.get("horizonDays") or HORIZON_DEFAULT
    calendar = expand_calendar(calendar_seed.get("events"), as_of, horizon)

    price = _price_from_box(box)
    advice = _advice_for(box, price)
    position = _position_in_box(box, price)
    levels = (box or {}).get("levels") if isinstance((box or {}).get("levels"), dict) else {}
    sim = _public_sim(paper)

    shares = (seed.get("valuationBasis") or {}).get("shares")
    shares_num = float(shares) if isinstance(shares, (int, float)) and shares > 0 else None
    rate, fx_note = cny_per_hkd(macro)
    mcap_hkd = market_cap_hkd_yi(price, shares_num)
    mcap_cny = mcap_hkd * rate if mcap_hkd is not None and rate is not None else None
    mcap_cny_rounded = _round(mcap_cny, 1)

    scenario_meta = seed.get("scenarios") or {}
    items = _scenario_items(seed, mcap_cny_rounded)
    base = next((row for row in items if row["id"] == "base"), None)
    base_pe = base.get("impliedPe") if base else None
    anchor = seed.get("anchor") or {}
    h1_profit = anchor.get("adjustedNetProfitYi")
    h1_run_rate = float(h1_profit) * 2 if isinstance(h1_profit, (int, float)) else None
    history_pe = implied_pe(mcap_cny_rounded, h1_run_rate)
    limits = seed.get("riskLimits") if isinstance(seed.get("riskLimits"), dict) else {}
    checklist = build_checklist(
        seed,
        calendar,
        price=price,
        advice=advice,
        base_pe=base_pe,
        history_pe=history_pe,
        sim=sim,
        position_in_box=position,
        levels=levels,
        limits=limits,
    )
    stance = build_stance(seed.get("narrative") or {}, checklist["gates"])
    checklist["readyToOpen"] = stance["tone"] == "pass"

    radar_count = None
    radar_error = None
    cluster_count = None
    if radar is None:
        radar_error = "xiaomi_radar.json 缺失"
    elif not isinstance(radar.get("clusters"), list) or not isinstance(radar.get("items"), list):
        radar_error = "xiaomi_radar.json 缺少 clusters 或 items"
    else:
        radar_count = len(radar["items"])
        cluster_count = len(radar["clusters"])

    now = datetime.now(HK_TZ).isoformat(timespec="seconds")
    return {
        "version": 2,
        "generatedBy": "scripts/xiaomi_trader.py",
        "updatedAt": now,
        "symbol": seed.get("symbol") or "1810.HK",
        "name": seed.get("name") or "小米集团-W",
        "disclaimer": seed.get("disclaimer") or DISCLAIMER,
        "stance": stance,
        "narrative": seed.get("narrative") or {},
        "anchor": seed.get("anchor") or {},
        "autoDelivery": seed.get("autoDelivery") or {},
        "valuation": {
            "priceHkd": _round(price, 2) if price is not None else None,
            "shares": shares_num,
            "sharesAsOf": (seed.get("valuationBasis") or {}).get("sharesAsOf"),
            "sharesNote": (seed.get("valuationBasis") or {}).get("sharesNote") or "",
            "marketCapHkdYi": _round(mcap_hkd, 1),
            "cnyPerHkd": _round(rate, 4) if rate is not None else None,
            "fxNote": fx_note,
            "marketCapCnyYi": mcap_cny_rounded,
            "multipleNote": "隐含倍数 = 人民币市值 / 该情景经调整净利润。市值用箱体文件里的价格 × 上表股数。不是目标价。",
            "h1RunRateProfitYi": _round(h1_run_rate, 1) if h1_run_rate is not None else None,
            "h1RunRatePe": history_pe,
            "maxBasePeToAdd": _limit_number(limits, "maxBasePeToAdd", 22),
            "richBasePe": _limit_number(limits, "richBasePe", 30),
            "historyNote": "本站没有多年 PE 数据库。历史对照只用已披露上半年经调整净利润年化，不用荐股因子里的 pe 分数。",
        },
        "riskLimits": {
            "maxPositionPct": _limit_number(limits, "maxPositionPct", 80),
            "addCeilingPct": _limit_number(limits, "addCeilingPct", 40),
            "minCashPct": _limit_number(limits, "minCashPct", 10),
            "maxBasePeToAdd": _limit_number(limits, "maxBasePeToAdd", 22),
            "richBasePe": _limit_number(limits, "richBasePe", 30),
            "limitsNote": limits.get("limitsNote") or "",
            "fundamentalStops": limits.get("fundamentalStops") or [],
            "boxBottom": (levels or {}).get("bottom"),
        },
        "indicators": build_indicators(seed),
        "weeklyReview": build_weekly_review(seed, as_of),
        "links": [
            {"href": "#paper", "label": "XRPS 模拟盘"},
            {"href": "#hk01810", "label": "HK01810 箱体"},
        ],
        "box": _box_view(box, price, advice, position),
        "publicSim": sim,
        "calendar": calendar,
        "scenarios": {
            "horizon": scenario_meta.get("horizon") or "2026 全年",
            "profitMetric": scenario_meta.get("profitMetric") or "adjusted_net_profit",
            "profitMetricLabel": scenario_meta.get("profitMetricLabel") or "经调整净利润（Non-IFRS）",
            "assumptionLabel": scenario_meta.get("assumptionLabel") or "情景假设，不是业绩预测",
            "items": items,
        },
        "checklist": checklist,
        "radar": {
            "href": "data/xiaomi_radar.json",
            "itemCount": radar_count,
            "clusterCount": cluster_count,
            "error": radar_error,
        },
        "seedFile": "data/xiaomi_trader_seed.json",
    }


def run() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        from xiaomi_radar import run as run_radar

        run_radar()
    except Exception as exc:  # noqa: BLE001 — 雷达失败不挡住看板其余部分
        print(f"xiaomi_radar skip: {exc}")
    seed = _load_json(SEED_PATH) or {}
    payload = build_payload(
        seed,
        box=_load_json(BOX_PATH),
        macro=_load_json(MACRO_PATH),
        paper=_load_json(PAPER_PATH),
        radar=_load_json(RADAR_PATH),
        as_of=today_hk(),
    )
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nxt = (payload.get("calendar") or {}).get("next") or {}
    print(
        f"Xiaomi trader: price={payload['valuation'].get('priceHkd')} "
        f"next={nxt.get('date')} {nxt.get('title')} "
        f"checklist_block={payload['checklist']['counts'].get('block')} "
        f"stance={payload.get('stance', {}).get('tone')}"
    )
    return payload


if __name__ == "__main__":
    run()
