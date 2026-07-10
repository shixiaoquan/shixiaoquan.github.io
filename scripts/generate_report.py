#!/usr/bin/env python3
"""生成机构风格投资决策日报（晨会 / 午间 / 收盘前瞻）。"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = DATA_DIR / "reports"
INDEX_FILE = REPORTS_DIR / "index.json"

BJT = ZoneInfo("Asia/Shanghai")

SLOT_META = {
    "morning": {
        "label": "晨会纪要",
        "subtitle": "开盘前研判 · 当日策略与风险框架",
        "focus": "隔夜信息消化、开盘仓位与触发位校准、本日首要关注事项。",
    },
    "noon": {
        "label": "午间速递",
        "subtitle": "上午盘面回顾 · 午后策略调整",
        "focus": "上午行情验证、战术信号与战役网格是否触发、午后操作节奏。",
    },
    "afternoon": {
        "label": "收盘前瞻",
        "subtitle": "午后至收盘策略 · 隔夜风险预案",
        "focus": "尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。",
    },
}

MAX_REPORTS = 90
MAX_NEWS = 6
MAX_CANDIDATES = 8


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def fmt_pct(value, signed: bool = True) -> str:
    if value is None:
        return "—"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "—"
    if signed and v > 0:
        return f"+{v:.2f}%"
    return f"{v:.2f}%"


def fmt_num(value, digits: int = 2) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return "—"


def fmt_dt_bjt(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        return dt.astimezone(BJT).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso


def detect_slot(now_bjt: datetime) -> str:
    hour = now_bjt.hour
    if hour < 11:
        return "morning"
    if hour < 14:
        return "noon"
    return "afternoon"


def mood_comment(mood: str | None) -> str:
    mapping = {
        "偏多": "风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。",
        "偏空": "风险厌恶情绪抬升，战术新开仓宜降频或观望；战役仓按网格纪律执行，避免情绪化减仓。",
        "震荡": "指数方向不明，结构分化概率加大，宜精选个股、控制仓位，等待方向选择。",
    }
    return mapping.get(mood or "", "情绪指标中性，以纪律执行为主。")


def radar_narrative(radar: list[dict]) -> str:
    if not radar:
        return "三市场雷达数据暂缺，建议结合指数速览自行判断区域强弱。"
    parts = []
    for item in radar:
        mkt = item.get("market", "")
        chg = item.get("changePct")
        label = item.get("label", "")
        parts.append(f"**{mkt}** {fmt_pct(chg)}（{label}）")
    weak = [r["market"] for r in radar if r.get("status") == "weak"]
    strong = [r["market"] for r in radar if r.get("status") == "strong"]
    tail = ""
    if strong:
        tail += f"相对强势区域：{'、'.join(strong)}。"
    if weak:
        tail += f"相对弱势区域：{'、'.join(weak)}，战术配置宜降权。"
    return "；".join(parts) + "。" + tail


def wencai_narrative(wencai: dict | None) -> str:
    if not wencai:
        return "问财数据未更新，A股短线情绪指标暂缺。"
    sent = wencai.get("sentiment") or {}
    up = sent.get("limitUp")
    down = sent.get("limitDown")
    mood = sent.get("mood", "—")
    stale = any(s.get("status") == "stale" for s in wencai.get("screens", []))
    stale_note = "（部分榜单沿用缓存，盘中宜以实时行情为准）" if stale else ""

    if up is None and down is None:
        return f"问财情绪：{mood}{stale_note}。"

    ratio = ""
    if up is not None and down is not None and down > 0:
        ratio = f"，涨跌停比约 **{up / down:.1f} : 1**"
    elif up is not None and down == 0:
        ratio = "，跌停家数为零，短线情绪偏热"

    if up is not None and down is not None:
        if up > down * 1.5:
            tone = "赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。"
        elif down > up:
            tone = "跌多涨少，短线资金偏谨慎，追高需格外克制。"
        else:
            tone = "涨跌家数相对均衡，结构性机会为主。"
    else:
        tone = "以结构性行情看待。"

    return (
        f"问财统计涨停 **{up if up is not None else '—'}** 家、"
        f"跌停 **{down if down is not None else '—'}** 家，情绪定性 **{mood}**{ratio}。{tone}{stale_note}"
    )


def index_highlights(indices: list[dict], limit: int = 4) -> str:
    if not indices:
        return ""
    sorted_idx = sorted(
        [i for i in indices if i.get("changePct") is not None],
        key=lambda x: abs(x["changePct"]),
        reverse=True,
    )[:limit]
    if not sorted_idx:
        return ""
    lines = [
        f"- **{i['name']}** {fmt_num(i.get('price'))}，日涨跌 {fmt_pct(i.get('changePct'))}"
        f"（周 {fmt_pct(i.get('weekChangePct'))} / 月 {fmt_pct(i.get('monthChangePct'))}）"
        for i in sorted_idx
    ]
    return "\n".join(lines)


def xrps_section(paper: dict | None, diag: dict | None) -> str:
    if not paper:
        return "战役模拟盘数据暂缺，无法生成 XRPS 持仓研判。"

    plan = (diag or {}).get("xrpsActionPlan") or {}
    ms = plan.get("monthly") or paper.get("monthlyState") or {}
    price = plan.get("price") or paper.get("lastPrice")
    name = paper.get("focusName", "小米集团")
    symbol = paper.get("focusSymbol", "1810.HK")

    lines = [
        f"**标的**：{name}（{symbol}）",
        f"**模拟净值**：收益率 {fmt_pct(paper.get('returnPct'))}，"
        f"仓位 {fmt_num(paper.get('positionPct'), 1)}%，"
        f"持股 {fmt_num(paper.get('totalShares'), 0)} 股，均价 {fmt_num(paper.get('avgCost'))}。",
    ]

    streak = ms.get("consecutiveDownMonths")
    if streak:
        lines.append(
            f"**月线状态**：连续 **{streak}** 个月收跌，上月 {fmt_pct(ms.get('lastMonthReturnPct'))}，"
            f"近两月累计 {fmt_pct(ms.get('twoMonthReturnPct'))}，"
            f"近三月累计 {fmt_pct(ms.get('threeMonthReturnPct'))}。"
            "我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。"
        )

    stage = plan.get("stage", "")
    stage_map = {
        "accumulate": "建仓积累期——侧重摊薄成本、增加股数，滚动网格尚未全面激活。",
        "rolling": "滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。",
        "bootstrap": "待建仓——等待首次核心仓信号。",
        "normal": "正常运行——核心仓保留，滚动网格待命。",
    }
    lines.append(f"**阶段判断**：{stage_map.get(stage, '按纪律跟踪。')}")

    next_sell = plan.get("nextSell")
    next_buy = plan.get("nextBuy")
    if price:
        lines.append(f"**现价参考**：{fmt_num(price)} HKD。")
    if next_sell and next_sell.get("triggerPrice"):
        lines.append(
            f"- 下一档**滚动卖出**（{next_sell.get('label')}）：触发价 **{fmt_num(next_sell['triggerPrice'])}**，"
            f"距现价 {fmt_pct(next_sell.get('gapPct'))}。"
        )
    if next_buy and next_buy.get("triggerPrice"):
        lines.append(
            f"- 下一档**回撤买回**（{next_buy.get('label')}）：触发价 **{fmt_num(next_buy['triggerPrice'])}**，"
            f"距现价 {fmt_pct(next_buy.get('gapPct'))}。"
        )

    for s in (diag or {}).get("suggestions") or []:
        lines.append(f"- {s}")

    bt_ret = (diag or {}).get("summary", {}).get("backtestReturn")
    if bt_ret is not None:
        lines.append(
            f"**长期参照**：上市以来 XRPS 回测收益率 {fmt_pct(bt_ret)}，"
            "短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。"
        )

    return "\n\n".join(lines)


def tactical_section(market: dict | None, signals: dict | None) -> str:
    reco = (market or {}).get("recommendations") or {}
    picks = reco.get("picks") or []
    scan = reco.get("candidateScan") or []
    open_sigs = [s for s in (signals or {}).get("signals", []) if s.get("status") == "open"]

    parts = []

    if reco.get("marketScan"):
        parts.append(f"**全市场扫描**：{reco['marketScan']}")

    if picks:
        parts.append("**今日各市场代表标的**（v1.3 强趋势+突破过滤）：")
        for p in picks:
            breakout = "已突破" if p.get("breakout") else "待突破"
            regime = "趋势过滤通过" if p.get("regimeOk") else "趋势过滤未过"
            parts.append(
                f"- **{p.get('name')}**（{p.get('market')}）| {p.get('signalLabel')} | "
                f"评分 {p.get('score')} | {breakout} | {regime} | "
                f"止损缓冲 {fmt_num(p.get('distToStopPct'), 1)}% / 目标空间 {fmt_num(p.get('distToTargetPct'), 1)}%"
                + (
                    f" | 决策 {p.get('decisionScore')}"
                    if p.get("decisionScore") is not None
                    else ""
                )
            )
            if p.get("reasons"):
                parts.append(f"  - 逻辑：{'；'.join(p['reasons'][:3])}")
    else:
        parts.append("当前无达标荐股标的，**空仓等待**亦是 v1.3 策略下的合理选择。")

    buy_count = sum(1 for p in picks if p.get("signal") == "buy")
    if buy_count == 0 and picks:
        parts.append(
            "> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；"
            "趋势良好但未突破时维持 watch，避免追涨噪音。"
        )

    if open_sigs:
        parts.append("\n**战术持仓跟踪**（实验策略，非战役仓）：")
        for s in open_sigs:
            alert = " ⚠️ 接近止损" if (s.get("distToStopPct") or 99) < 5 else ""
            parts.append(
                f"- **{s.get('name')}**（{s.get('market')}）| 浮盈 {fmt_pct(s.get('returnPct'))} | "
                f"距止损 {fmt_num(s.get('distToStopPct'), 1)}% | 距目标 +{fmt_num(s.get('distToTargetPct'), 1)}% | "
                f"持有 {s.get('holdDays', 0)} 天{alert}"
            )
    else:
        parts.append("\n暂无 open 战术信号持仓。")

    if scan:
        top = [c for c in scan if c.get("signal") in ("buy", "watch")][:MAX_CANDIDATES]
        if top:
            parts.append("\n**候选池前列**（按评分）：")
            for c in top:
                parts.append(
                    f"- {c.get('name')} {c.get('score')}分 {c.get('signalLabel')} "
                    f"RSI {fmt_num(c.get('rsi'), 1)} RS {fmt_pct(c.get('relativeStrength'))}"
                )

    return "\n\n".join(parts)


def evolution_section() -> str:
    """持续进化状态 — 影子轨、队列、战术自适应。"""
    queue = load_json(DATA_DIR / "evolution_queue.json", {})
    shadow = load_json(DATA_DIR / "shadow_reco.json", {})
    paired = load_json(DATA_DIR / "paired_attribution.json", {})
    tune = load_json(DATA_DIR / "tactic_tune.json", {})

    parts = ["**系统进化看板**（GitHub Actions 自动维护）"]
    cmp_ = shadow.get("comparison") or {}
    if cmp_.get("reason"):
        parts.append(f"- 影子轨：{cmp_['reason']}")
    paired_sum = paired.get("summary") or {}
    if paired_sum.get("pairedCount"):
        parts.append(
            f"- 配对归因：{paired_sum['pairedCount']} 对 · "
            f"影子胜率 {paired_sum.get('shadowWinRate')}% · "
            f"均边际 {fmt_num(paired_sum.get('avgEdgeT5'))}%"
        )
    if tune.get("active"):
        parts.append(
            f"- 战术自适应：门槛 {tune.get('buyScoreAdjust'):+d} · "
            f"{'; '.join((tune.get('notes') or [])[:2])}"
        )
    tasks = queue.get("tasks") or []
    if tasks:
        top = tasks[0]
        parts.append(f"- 队列待办：**{top.get('title')}** — {top.get('cursorPrompt', '')[:120]}")
    else:
        parts.append("- 进化队列：空闲，系统正常运转")
    if cmp_.get("readyForUpgradePR"):
        parts.append("> **提示**：影子轨验证通过，可请 Cursor 按 EVOLUTION_PLAYBOOK 开策略升级 PR。")
    return "\n\n".join(parts)


def master_reco_section(market: dict | None) -> str:
    data = (market or {}).get("masterRecommendations") or {}
    masters = data.get("masters") or []
    if not masters:
        return "大师风格荐股数据暂缺。"

    learning = data.get("learning") or {}
    parts = [
        f"基于候选池基本面与价格特征，模拟 **{len(masters)}** 位投资大师选股框架（{data.get('version', 'v1.2')}）。"
    ]
    if learning.get("regime"):
        parts.append(
            f"*在线学习：市场环境 {learning['regime']} · 修订 r{learning.get('revision', 0)}"
            f"{(' · ' + learning['notes']['_regime']) if learning.get('notes', {}).get('_regime') else ''}*"
        )
    for master in masters:
        picks = master.get("picks") or []
        parts.append(f"\n### {master.get('name')} · {master.get('style')}")
        parts.append(f"*{master.get('philosophy', '')}*")
        if not picks:
            parts.append("- 当前无达标标的")
            continue
        for p in picks:
            m = p.get("metrics") or {}
            metric_bits = []
            if m.get("pe") is not None:
                metric_bits.append(f"PE {fmt_num(m['pe'], 1)}")
            if m.get("peg") is not None:
                metric_bits.append(f"PEG {fmt_num(m['peg'], 2)}")
            if m.get("roe") is not None:
                metric_bits.append(f"ROE {fmt_num(m['roe'], 1)}%")
            metrics_s = " · ".join(metric_bits) if metric_bits else "—"
            parts.append(
                f"- **{p.get('name')}**（{p.get('market')}）| 匹配 {p.get('matchScore')} | "
                f"{p.get('signalLabel')} | {metrics_s}"
            )
            if p.get("reasons"):
                parts.append(f"  - {'；'.join(p['reasons'][:2])}")

    parts.append(f"\n*{data.get('disclaimer', '')}*")
    return "\n\n".join(parts)


def news_section(market: dict | None, wencai: dict | None) -> str:
    items = []
    for n in (market or {}).get("news") or []:
        items.append({**n, "source": "yahoo"})
    for n in (wencai or {}).get("news") or []:
        items.append({**n, "source": "wencai"})

    seen: set[str] = set()
    unique = []
    for n in sorted(items, key=lambda x: x.get("publishedAt") or "", reverse=True):
        title = (n.get("title") or "").strip()
        if not title or title in seen:
            continue
        seen.add(title)
        unique.append(n)
        if len(unique) >= MAX_NEWS:
            break

    if not unique:
        return "暂无可用资讯条目。"

    lines = []
    for n in unique:
        src = "问财" if n.get("source") == "wencai" else "Yahoo"
        rel = n.get("related", "")
        lines.append(f"- [{src}] **{n['title']}**{'（' + rel + '）' if rel else ''}")
        if n.get("summary"):
            summary = re.sub(r"\s+", " ", n["summary"])[:120]
            lines.append(f"  {summary}…")
    return "\n".join(lines)


def executive_summary(
    slot: str,
    market: dict | None,
    wencai: dict | None,
    paper: dict | None,
    signals: dict | None,
    diag: dict | None,
) -> str:
    meta = SLOT_META[slot]
    summary = (market or {}).get("summary") or {}
    mood = summary.get("mood", "—")
    avg = summary.get("avgChangePct")
    open_count = (signals or {}).get("openCount", 0)
    paper_ret = (paper or {}).get("returnPct")
    streak = ((diag or {}).get("xrpsActionPlan") or {}).get("monthly", {}).get("consecutiveDownMonths")

    parts = [f"本报告为**{meta['label']}**，{meta['focus']}"]

    parts.append(
        f"全球跟踪指数平均涨跌 **{fmt_pct(avg)}**，综合情绪 **{mood}**。"
        f"{mood_comment(mood)}"
    )

    w_mood = (wencai or {}).get("sentiment", {}).get("mood")
    if w_mood:
        parts.append(f"A股问财短线情绪 **{w_mood}**，与全球指数判断对照使用。")

    if streak and streak >= 5:
        parts.append(
            f"战役仓小米 XRPS 处于 **{streak} 连阴月**积累阶段，模拟收益率 {fmt_pct(paper_ret)}；"
            "策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。"
        )
    elif paper_ret is not None:
        parts.append(f"战役仓 XRPS 模拟收益率 {fmt_pct(paper_ret)}，按网格与月线纪律执行。")

    if open_count:
        parts.append(f"战术实验有 **{open_count}** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。")
    else:
        picks = ((market or {}).get("recommendations") or {}).get("picks") or []
        if not any(p.get("signal") == "buy" for p in picks):
            parts.append("战术端暂无 buy 突破信号，建议以观察为主。")

    return "\n\n".join(parts)


def watchlist(slot: str, market: dict | None, paper: dict | None, signals: dict | None, diag: dict | None) -> str:
    items = []
    plan = (diag or {}).get("xrpsActionPlan") or {}
    next_sell = plan.get("nextSell") or {}
    next_buy = plan.get("nextBuy") or {}

    if next_sell.get("triggerPrice"):
        items.append(f"小米滚动卖出触发：{next_sell.get('label')} @ {fmt_num(next_sell['triggerPrice'])}")
    if next_buy.get("triggerPrice"):
        items.append(f"小米回撤买回触发：{next_buy.get('label')} @ {fmt_num(next_buy['triggerPrice'])}")

    for sig in (signals or {}).get("signals", []) or []:
        if sig.get("status") != "open":
            continue
        if (sig.get("distToStopPct") or 99) < 8:
            items.append(f"⚠️ {sig.get('name')} 距止损仅 {fmt_num(sig.get('distToStopPct'), 1)}%")

    for p in ((market or {}).get("recommendations") or {}).get("picks") or []:
        if p.get("signal") == "buy":
            items.append(f"新 buy 信号：{p.get('name')}（{p.get('market')}）")
        elif p.get("breakout") is False and (p.get("score") or 0) >= 75:
            items.append(f"待突破观察：{p.get('name')} 突破位 {fmt_num(p.get('breakoutLevel'))}")

    if slot == "afternoon":
        items.append("收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）")

    if not items:
        items.append("无紧急触发项；维持观察，等待网格或突破信号。")

    return "\n".join(f"{i + 1}. {t}" for i, t in enumerate(items[:8]))


def macro_section(macro: dict | None) -> str:
    if not macro:
        return "宏观跨资产数据暂缺。"
    s = macro.get("summary") or {}
    lines = []
    if s.get("vix") is not None:
        lines.append(f"- **VIX** {fmt_num(s['vix'], 1)}（{s.get('vixRegime', '—')}）")
    if s.get("us10yYield") is not None:
        lines.append(f"- **美10Y收益率** {fmt_num(s['us10yYield'], 2)}%")
    if s.get("yieldSpread10y2y") is not None:
        spread = s["yieldSpread10y2y"]
        tag = "倒挂" if spread < 0 else "偏窄" if spread < 0.5 else "正常"
        lines.append(f"- **10Y-2Y 利差（FRED）** {fmt_num(spread, 2)}%（{tag}）")
    if s.get("usdCnh") is not None:
        chg = fmt_pct(s.get("usdCnhChangePct")) if s.get("usdCnhChangePct") is not None else "—"
        lines.append(f"- **USDCNH** {fmt_num(s['usdCnh'], 4)}（日 {chg}）")
    if s.get("sectorLeader"):
        lines.append(
            f"- **美股行业**：{s.get('sectorLeader')} 领涨，{s.get('sectorLaggard')} 靠后"
        )

    fred_rows = macro.get("fred") or []
    if fred_rows:
        lines.append("\n**FRED 官方序列**")
        for row in fred_rows[:6]:
            chg = fmt_pct(row.get("changePct")) if row.get("changePct") is not None else "—"
            lines.append(
                f"- {row.get('name', row.get('seriesId'))}：{row.get('price')}（变动 {chg}，{row.get('observedAt', '—')}）"
            )

    news = macro.get("finnhubNews") or []
    if news:
        lines.append("\n**Finnhub 宏观要闻**")
        for item in news[:5]:
            title = item.get("title") or "—"
            src = item.get("source") or "Finnhub"
            lines.append(f"- [{title}]({item.get('link') or '#'})（{src}）")

    earnings = macro.get("earningsCalendar") or []
    if earnings:
        lines.append("\n**财报日历（关注标的）**")
        for row in earnings[:6]:
            eps = row.get("epsEstimate")
            eps_s = fmt_num(eps, 2) if eps is not None else "—"
            lines.append(
                f"- **{row.get('symbol', '—')}** {row.get('date', '—')} "
                f"{row.get('hour') or ''} · EPS预期 {eps_s}"
            )

    for h in s.get("hints") or []:
        lines.append(f"- {h}")
    src = "、".join(x.get("name", "") for x in macro.get("sources") or [])
    if src:
        lines.append(f"\n*数据源：{src}*")
    return "\n".join(lines) if lines else "暂无宏观摘要。"


def build_report(slot: str, now_bjt: datetime | None = None) -> tuple[str, dict]:
    now_bjt = now_bjt or datetime.now(BJT)
    meta = SLOT_META[slot]
    date_str = now_bjt.strftime("%Y-%m-%d")
    time_str = now_bjt.strftime("%H:%M")
    report_id = f"{date_str}-{slot}"

    market = load_json(DATA_DIR / "market.json", {})
    wencai = load_json(DATA_DIR / "wencai.json", {})
    paper = load_json(DATA_DIR / "paper_account.json", {})
    signals = load_json(DATA_DIR / "signals.json", {})
    diag = load_json(DATA_DIR / "diagnostics.json", {})
    backtest = load_json(DATA_DIR / "backtest.json", {})
    macro = load_json(DATA_DIR / "macro.json", {})

    exec_sum = executive_summary(slot, market, wencai, paper, signals, diag)
    macro_text = macro_section(macro)
    radar = radar_narrative(market.get("marketRadar") or [])
    wencai_text = wencai_narrative(wencai)
    idx_text = index_highlights(market.get("indices") or [])

    bt = backtest.get("metrics") or {}
    bt_note = ""
    if bt.get("totalTrades", 0) == 0:
        bt_note = (
            f"\n\n> 战术回测（{backtest.get('strategyVersion', 'v1.3')}）当前区间 **0 笔成交**，"
            "反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。"
        )
    elif bt.get("winRate") is not None:
        bt_note = (
            f"\n\n实验室回测：胜率 {bt.get('winRate')}%，期望值 {fmt_num(bt.get('expectancy'))}%，"
            f"最大回撤 {fmt_pct(bt.get('maxDrawdown'))}（样本 {bt.get('totalTrades')} 笔，仅供研究）。"
        )

    body = f"""# 投资决策日报 · {meta['label']}

**{now_bjt.strftime('%Y年%m月%d日')} {time_str}（北京时间）** · {meta['subtitle']}

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：{fmt_dt_bjt(market.get('updatedAt'))} · 宏观：{fmt_dt_bjt(macro.get('updatedAt'))} · 问财：{fmt_dt_bjt(wencai.get('updatedAt'))}

---

## 核心观点

{exec_sum}

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 {market.get('summary', {}).get('tracked', '—')} 只主要指数：上涨 **{market.get('summary', {}).get('up', '—')}** 只、
下跌 **{market.get('summary', {}).get('down', '—')}** 只，平均涨跌 **{fmt_pct(market.get('summary', {}).get('avgChangePct'))}**。

{radar}

**波动居前指数：**

{idx_text or '- 暂无指数明细'}

### 1.2 A股短线情绪

{wencai_text}

### 1.3 宏观与跨资产

{macro_text}

### 1.4 本时段研判侧重

{meta['focus']}

---

## 二、战役持仓（XRPS-X 小米滚动仓）

{xrps_section(paper, diag)}

---

## 三、战术实验（荐股 v1.3）

{tactical_section(market, signals)}
{bt_note}

---

## 四、投资大师风格荐股

{master_reco_section(market)}

---

## 五、持续进化状态

{evolution_section()}

---

## 六、资讯与主题线索

{news_section(market, wencai)}

---

## 七、风险提示

1. 本报告基于公开行情与规则化模型，**不构成投资建议**；战术实验与战役 XRPS 为相互独立的两套体系，请勿混仓决策。  
2. 港股 / 美股存在汇率、流动性及隔夜缺口风险；A股须关注涨跌停制度下的执行偏差。  
3. 问财等非官方数据源可能延迟或缓存；涨停榜等情绪指标需与实时盘口交叉验证。  
4. 模拟盘收益不代表未来表现；连阴月加仓逻辑基于历史回测，极端宏观冲击下可能失效。
5. 大师风格荐股为规则化模拟，非真实人物操作建议；基本面数据可能有延迟或缺失。

---

## 八、本时段关注清单

{watchlist(slot, market, paper, signals, diag)}

---

*报告 ID：`{report_id}` · 自动生成于 shixiaoquan.win 投资决策工作台*
"""

    excerpt = exec_sum.split("\n\n")[0][:160]
    meta_out = {
        "id": report_id,
        "date": date_str,
        "slot": slot,
        "slotLabel": meta["label"],
        "title": f"投资决策日报 · {meta['label']}",
        "subtitle": meta["subtitle"],
        "generatedAt": now_bjt.isoformat(timespec="seconds"),
        "path": f"data/reports/{report_id}.md",
        "excerpt": excerpt,
        "marketMood": market.get("summary", {}).get("mood"),
        "wencaiMood": (wencai.get("sentiment") or {}).get("mood"),
        "openSignals": (signals or {}).get("openCount", 0),
    }
    return body, meta_out


def update_index(entry: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    index = load_json(INDEX_FILE, {"reports": []})
    reports: list[dict] = index.get("reports", [])
    reports = [r for r in reports if r.get("id") != entry["id"]]
    reports.insert(0, entry)
    reports = reports[:MAX_REPORTS]
    index["reports"] = reports
    index["updatedAt"] = entry["generatedAt"]
    index["latest"] = entry
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="生成投资决策日报")
    parser.add_argument(
        "--slot",
        choices=["morning", "noon", "afternoon", "auto"],
        default="auto",
        help="报告时段（auto=按北京时间推断）",
    )
    args = parser.parse_args()

    now_bjt = datetime.now(BJT)
    slot = detect_slot(now_bjt) if args.slot == "auto" else args.slot

    body, meta = build_report(slot, now_bjt)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORTS_DIR / f"{meta['id']}.md"
    out_path.write_text(body, encoding="utf-8")
    update_index(meta)

    print(f"Wrote {out_path} ({meta['slotLabel']})")


if __name__ == "__main__":
    main()
