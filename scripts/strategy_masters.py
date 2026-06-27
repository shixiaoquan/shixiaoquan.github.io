"""投资大师风格荐股 — 基于公开基本面与价格特征的多风格打分。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import yfinance as yf

from strategy_scoring import MARKET_BENCHMARKS, pct_change, sma

MASTER_VERSION = "v1.1.0"
PICKS_PER_MASTER = 2
MIN_MATCH_SCORE = 48


@dataclass(frozen=True)
class MasterProfile:
    id: str
    name: str
    name_en: str
    style: str
    philosophy: str
    principles: tuple[str, ...]
    holding: str


MASTER_PROFILES: tuple[MasterProfile, ...] = (
    MasterProfile(
        id="buffett",
        name="沃伦·巴菲特",
        name_en="Warren Buffett",
        style="价值投资",
        philosophy="以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。",
        principles=("护城河与品牌", "ROE 持续高位", "负债可控", "管理层诚信", "能力圈内投资"),
        holding="3–10 年+",
    ),
    MasterProfile(
        id="graham",
        name="本杰明·格雷厄姆",
        name_en="Benjamin Graham",
        style="深度价值",
        philosophy="安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。",
        principles=("低 PE / 低 PB", "安全边际", "分散组合", "避免投机", "重视资产负债表"),
        holding="1–3 年",
    ),
    MasterProfile(
        id="lynch",
        name="彼得·林奇",
        name_en="Peter Lynch",
        style="成长合理价 GARP",
        philosophy="投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。",
        principles=("PEG < 1.5", "业务可理解", "盈利与营收增长", "行业渗透空间", "实地调研思维"),
        holding="1–5 年",
    ),
    MasterProfile(
        id="munger",
        name="查理·芒格",
        name_en="Charlie Munger",
        style="优质复利",
        philosophy="以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。",
        principles=("高 ROE 复利", "轻资产高毛利", "逆向思维", "少而精的决策", "长期主义"),
        holding="5 年+",
    ),
    MasterProfile(
        id="templeton",
        name="约翰·邓普顿",
        name_en="John Templeton",
        style="逆向投资",
        philosophy="在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。",
        principles=("极度悲观时买入", "52 周低位区间", "基本面未恶化", "全球视野", "耐心持有"),
        holding="2–5 年",
    ),
    MasterProfile(
        id="soros",
        name="乔治·索罗斯",
        name_en="George Soros",
        style="宏观趋势",
        philosophy="反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。",
        principles=("趋势确认", "相对强度", "宏观共振", "快速止损", "顺势而为"),
        holding="数周–数月",
    ),
    MasterProfile(
        id="serenity",
        name="白毛股神 Serenity",
        name_en="Serenity (@aleabitoreddit)",
        style="卡脖子 · 瓶颈猎手",
        philosophy=(
            "Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，"
            "寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。"
        ),
        principles=(
            "瓶颈猎手",
            "终端需求向上游追溯",
            "小盘+高壁垒+低覆盖",
            "机构定价前布局",
            "证伪点止损",
        ),
        holding="6–18 个月",
    ),
)


# Serenity 产业链瓶颈标签（候选池内），用于加分与展示
SERENITY_BOTTLENECK_TAGS: dict[str, tuple[str, str]] = {
    "688981.SS": ("晶圆制造", "AI 算力上游产能瓶颈"),
    "688017.SS": ("精密减速器", "人形机器人卡脖子环节"),
    "300308.SZ": ("光模块", "CPO/光互连供应链瓶颈"),
    "AMD": ("GPU/CPU", "算力供应链关键环节"),
    "NVDA": ("AI 芯片", "终端龙头 — 非瓶颈主战场"),
    "300750.SZ": ("动力电池", "数据中心备电/储能环节"),
    "1810.HK": ("智能硬件", "机器人/IoT 终端生态"),
    "9992.HK": ("潮玩零售", "非核心瓶颈 — 降权"),
}

SERENITY_SECTOR_SCORE: dict[str, float] = {
    "半导体": 22,
    "光模块": 24,
    "精密减速器": 24,
    "新能源": 10,
    "消费电子": 12,
    "软件云计算": 6,
    "电商云计算": 4,
    "互联网": 2,
    "白酒": -22,
    "保险": -20,
    "银行": -18,
    "潮玩零售": -12,
}


def _norm_ratio(val: float | None, as_pct: bool = True) -> float | None:
    if val is None:
        return None
    try:
        v = float(val)
    except (TypeError, ValueError):
        return None
    if as_pct and 0 < abs(v) <= 1.5:
        return round(v * 100, 2)
    return round(v, 2)


def _clamp_score(score: float) -> float:
    return round(max(0.0, min(100.0, score)), 1)


def fetch_candidate_context(symbol: str, meta: dict) -> dict | None:
    """拉取单只候选的基本面 + 价格上下文。"""
    market = meta.get("market", "美股")
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2y", interval="1d")
        info = ticker.info or {}
    except Exception:
        return None

    if hist.empty:
        return None

    closes = [float(v) for v in hist["Close"].dropna().tolist()]
    highs = [float(v) for v in hist["High"].dropna().tolist()]
    lows = [float(v) for v in hist["Low"].dropna().tolist()]
    volumes = [float(v) for v in hist["Volume"].dropna().tolist()]
    price = closes[-1]

    week_ago = closes[-6] if len(closes) >= 6 else None
    month_ago = closes[-22] if len(closes) >= 22 else None
    quarter_ago = closes[-66] if len(closes) >= 66 else None

    hi52 = info.get("fiftyTwoWeekHigh") or (max(highs[-252:]) if len(highs) >= 20 else None)
    lo52 = info.get("fiftyTwoWeekLow") or (min(lows[-252:]) if len(lows) >= 20 else None)
    pct_from_high = None
    pct_from_low = None
    if hi52 and lo52 and hi52 > lo52:
        pct_from_high = round((price - hi52) / hi52 * 100, 2)
        pct_from_low = round((price - lo52) / lo52 * 100, 2)
        range_pos = (price - lo52) / (hi52 - lo52)
    else:
        range_pos = 0.5

    ma200 = sma(closes, 200)
    ma50 = sma(closes, 50)
    above_ma200 = price >= ma200 if ma200 else None
    above_ma50 = price >= ma50 if ma50 else None

    bench_symbol = MARKET_BENCHMARKS.get(market)
    rel_strength = None
    if bench_symbol:
        try:
            bench_closes = [
                float(v)
                for v in yf.Ticker(bench_symbol).history(period="6mo", interval="1d")["Close"].dropna().tolist()
            ]
            if len(bench_closes) >= 22 and month_ago:
                stock_m = pct_change(price, month_ago)
                bench_m = pct_change(bench_closes[-1], bench_closes[-22])
                if stock_m is not None and bench_m is not None:
                    rel_strength = round(stock_m - bench_m, 2)
        except Exception:
            pass

    avg_vol = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else None
    vol_ratio = round(volumes[-1] / avg_vol, 2) if avg_vol and avg_vol > 0 else None

    pe = info.get("trailingPE") or info.get("forwardPE")
    pb = info.get("priceToBook")
    roe = _norm_ratio(info.get("returnOnEquity"))
    margins = _norm_ratio(info.get("profitMargins"))
    debt = info.get("debtToEquity")
    rev_growth = _norm_ratio(info.get("revenueGrowth"))
    earn_growth = _norm_ratio(info.get("earningsGrowth"))
    div_yield = _norm_ratio(info.get("dividendYield"), as_pct=False)
    if div_yield is not None and div_yield < 1:
        div_yield = round(div_yield * 100, 2)
    beta = info.get("beta")
    mcap = info.get("marketCap")

    peg = None
    if pe and earn_growth and earn_growth > 0:
        peg = round(pe / earn_growth, 2)

    return {
        "symbol": symbol,
        "name": meta["name"],
        "market": market,
        "sector": meta.get("sector"),
        "currency": meta.get("currency", "USD"),
        "price": round(price, 2),
        "monthChangePct": pct_change(price, month_ago),
        "quarterChangePct": pct_change(price, quarter_ago),
        "weekChangePct": pct_change(price, week_ago),
        "pctFrom52wHigh": pct_from_high,
        "pctFrom52wLow": pct_from_low,
        "rangePosition": round(range_pos, 2),
        "aboveMa200": above_ma200,
        "aboveMa50": above_ma50,
        "relativeStrength": rel_strength,
        "volumeRatio": vol_ratio,
        "pe": round(pe, 2) if pe else None,
        "pb": round(pb, 2) if pb else None,
        "roe": roe,
        "profitMargins": margins,
        "debtToEquity": round(debt, 2) if debt is not None else None,
        "revenueGrowth": rev_growth,
        "earningsGrowth": earn_growth,
        "peg": peg,
        "dividendYield": div_yield,
        "beta": round(beta, 2) if beta is not None else None,
        "marketCap": mcap,
    }


def _score_buffett(ctx: dict) -> tuple[float, list[str]]:
    score = 50.0
    reasons: list[str] = []

    roe = ctx.get("roe")
    if roe is not None:
        if roe >= 20:
            score += 18
            reasons.append(f"ROE {roe}% — 资本回报优秀，符合巴菲特护城河标准")
        elif roe >= 12:
            score += 10
            reasons.append(f"ROE {roe}% — 盈利能力稳健")
        else:
            score -= 8

    pe = ctx.get("pe")
    if pe is not None:
        if pe <= 25:
            score += 12
            reasons.append(f"PE {pe} — 估值在能力圈合理区间")
        elif pe <= 35:
            score += 4
        else:
            score -= 10
            reasons.append(f"PE {pe} 偏高 — 需更大安全边际才符合巴菲特买价")

    margins = ctx.get("profitMargins")
    if margins is not None and margins >= 15:
        score += 8
        reasons.append(f"净利率 {margins}% — 业务具备定价权")

    debt = ctx.get("debtToEquity")
    if debt is not None:
        if debt < 80:
            score += 6
            reasons.append("负债率可控，财务风险较低")
        elif debt > 150:
            score -= 8

    if ctx.get("aboveMa200") is True and ctx.get("rangePosition", 1) < 0.75:
        score += 8
        reasons.append("长期趋势向上且未严重高估 — 可分批建仓")
    elif ctx.get("rangePosition", 1) < 0.35:
        score += 10
        reasons.append("价格接近 52 周低位 — 优质资产回调机会")

    mcap = ctx.get("marketCap")
    if mcap and mcap >= 50e9:
        score += 4
        reasons.append("龙头体量，业务护城河更易验证")

    return _clamp_score(score), reasons[:4]


def _score_graham(ctx: dict) -> tuple[float, list[str]]:
    score = 45.0
    reasons: list[str] = []

    pe = ctx.get("pe")
    if pe is not None:
        if pe < 12:
            score += 22
            reasons.append(f"PE {pe} — 深度价值区间，安全边际充足")
        elif pe < 18:
            score += 12
            reasons.append(f"PE {pe} — 低于市场平均，具备安全边际")
        elif pe > 30:
            score -= 15

    pb = ctx.get("pb")
    if pb is not None:
        if pb < 1.2:
            score += 18
            reasons.append(f"PB {pb} — 资产折价，经典格雷厄姆信号")
        elif pb < 2:
            score += 8
        elif pb > 5:
            score -= 8

    rp = ctx.get("rangePosition")
    if rp is not None and rp < 0.3:
        score += 12
        reasons.append("价格处于 52 周区间下沿 — 悲观定价带来安全边际")
    elif rp is not None and rp < 0.5:
        score += 6

    div = ctx.get("dividendYield")
    if div is not None and div >= 2:
        score += 5
        reasons.append(f"股息率 {div}% — 提供下行保护垫")

    debt = ctx.get("debtToEquity")
    if debt is not None and debt > 200:
        score -= 10
        reasons.append("负债过高 — 不符合格雷厄姆防御型标准")

    return _clamp_score(score), reasons[:4]


def _score_lynch(ctx: dict) -> tuple[float, list[str]]:
    score = 48.0
    reasons: list[str] = []

    peg = ctx.get("peg")
    earn_g = ctx.get("earningsGrowth")
    rev_g = ctx.get("revenueGrowth")
    pe = ctx.get("pe")

    if peg is not None:
        if peg < 1:
            score += 22
            reasons.append(f"PEG {peg} — 成长相对估值便宜，林奇「十倍股」潜力")
        elif peg < 1.5:
            score += 14
            reasons.append(f"PEG {peg} — 成长合理价，符合 GARP 框架")
        elif peg > 2.5:
            score -= 10

    if earn_g is not None:
        if earn_g >= 20:
            score += 12
            reasons.append(f"盈利增速 {earn_g}% — 成长故事可验证")
        elif earn_g >= 10:
            score += 6
        elif earn_g < 0:
            score -= 12

    if rev_g is not None and rev_g >= 10:
        score += 6
        reasons.append(f"营收增速 {rev_g}% — 业务扩张持续")

    if pe is not None and pe < 35 and earn_g and earn_g > 15:
        score += 4

    sector = ctx.get("sector") or ""
    if sector in ("半导体", "新能源", "互联网", "软件云计算", "电商云计算"):
        score += 4
        reasons.append(f"{sector} — 林奇偏好的可理解成长行业")

    return _clamp_score(score), reasons[:4]


def _score_munger(ctx: dict) -> tuple[float, list[str]]:
    score = 50.0
    reasons: list[str] = []

    roe = ctx.get("roe")
    if roe is not None:
        if roe >= 25:
            score += 20
            reasons.append(f"ROE {roe}% — 优质复利机器，芒格会长期持有")
        elif roe >= 18:
            score += 12
        else:
            score -= 6

    margins = ctx.get("profitMargins")
    if margins is not None and margins >= 25:
        score += 14
        reasons.append(f"净利率 {margins}% — 轻资产高毛利特征")
    elif margins is not None and margins >= 15:
        score += 6

    debt = ctx.get("debtToEquity")
    if debt is not None and debt < 60:
        score += 8
        reasons.append("低杠杆 — 符合芒格「避免愚蠢」原则")

    pe = ctx.get("pe")
    if pe is not None and roe and roe >= 20:
        if pe <= 40:
            score += 8
            reasons.append("优质公司合理溢价可接受 — 以合理价格买伟大公司")
        else:
            score -= 4

    if ctx.get("aboveMa200") is True:
        score += 6
        reasons.append("长期趋势完好 — 复利故事未被破坏")

    return _clamp_score(score), reasons[:4]


def _score_templeton(ctx: dict) -> tuple[float, list[str]]:
    score = 42.0
    reasons: list[str] = []

    month = ctx.get("monthChangePct")
    quarter = ctx.get("quarterChangePct")
    rp = ctx.get("rangePosition")

    if month is not None and month < -8:
        score += 16
        reasons.append(f"近一月 {month}% — 市场悲观，邓普顿式逆向机会")
    elif month is not None and month < -3:
        score += 8
    elif month is not None and month > 15:
        score -= 10

    if quarter is not None and quarter < -15:
        score += 10
        reasons.append(f"近三月 {quarter}% — 深度回调，关注基本面是否错杀")

    if rp is not None and rp < 0.25:
        score += 14
        reasons.append("价格接近 52 周底部 — 「极度悲观时买入」")
    elif rp is not None and rp < 0.4:
        score += 8

    pe = ctx.get("pe")
    if pe is not None and pe < 25:
        score += 8
        reasons.append(f"PE {pe} — 悲观中仍有估值支撑")
    elif pe is not None and pe > 50:
        score -= 8
        reasons.append("估值仍高 — 可能只是成长回落而非错杀")

    roe = ctx.get("roe")
    if roe is not None and roe >= 12:
        score += 6
        reasons.append("盈利能力仍在 — 逆向不是接飞刀")

    return _clamp_score(score), reasons[:4]


def _score_soros(ctx: dict) -> tuple[float, list[str]]:
    score = 45.0
    reasons: list[str] = []

    month = ctx.get("monthChangePct")
    rs = ctx.get("relativeStrength")
    vol = ctx.get("volumeRatio")

    if month is not None:
        if month >= 8:
            score += 16
            reasons.append(f"近一月 +{month}% — 趋势强劲，反身性正反馈")
        elif month >= 3:
            score += 10
        elif month < -5:
            score -= 6

    if rs is not None:
        if rs >= 5:
            score += 14
            reasons.append(f"相对强度 +{rs}% — 跑赢大盘，宏观共振")
        elif rs >= 2:
            score += 8
        elif rs < -5:
            score -= 8

    if ctx.get("aboveMa50") is True and ctx.get("aboveMa200") is True:
        score += 10
        reasons.append("均线多头排列 — 趋势交易确认")

    if vol is not None and vol >= 1.3:
        score += 6
        reasons.append(f"量比 {vol} — 资金参与度高")

    beta = ctx.get("beta")
    if beta is not None and beta >= 1.1 and month and month > 0:
        score += 4
        reasons.append("高 Beta 放大趋势 — 索罗斯式进攻配置")

    return _clamp_score(score), reasons[:4]


def _score_serenity(ctx: dict) -> tuple[float, list[str]]:
    """X @aleabitoreddit — 卡脖子投资法 / Bottleneck Hunter。"""
    score = 38.0
    reasons: list[str] = []
    symbol = ctx.get("symbol", "")

    tag = SERENITY_BOTTLENECK_TAGS.get(symbol)
    sector = ctx.get("sector") or (tag[0] if tag else "")
    sector_bonus = SERENITY_SECTOR_SCORE.get(sector, 0)
    if sector_bonus:
        score += sector_bonus
        if sector_bonus > 0:
            reasons.append(f"{sector} — AI/机器人供应链瓶颈相关环节")
        else:
            reasons.append(f"{sector} — 非 Serenity 核心瓶颈赛道")

    if tag:
        layer, note = tag
        if "非瓶颈" in note or "降权" in note or "终端龙头" in note:
            score -= 12
            reasons.append(f"{layer}：{note}")
        else:
            score += 14
            reasons.append(f"紫苏叶环节 · {layer} — {note}")

    mcap = ctx.get("marketCap")
    if mcap is not None:
        if mcap < 30e9:
            score += 16
            reasons.append("小市值 — 机构覆盖不足、重估弹性大")
        elif mcap < 100e9:
            score += 10
            reasons.append("中市值 — 仍处价格发现窗口")
        elif mcap < 300e9:
            score += 2
        elif mcap > 1e12:
            score -= 22
            reasons.append("超大盘龙头 — 「买瓶颈不买品牌」框架下降权")
        elif mcap > 400e9:
            score -= 14
            reasons.append("大盘蓝筹 — 非典型卡脖子小盘标的")

    earn_g = ctx.get("earningsGrowth")
    rev_g = ctx.get("revenueGrowth")
    if earn_g is not None and earn_g >= 15:
        score += 10
        reasons.append(f"盈利增速 {earn_g}% — 瓶颈环节需求释放")
    elif earn_g is not None and earn_g >= 5:
        score += 4
    if rev_g is not None and rev_g >= 10:
        score += 6

    rp = ctx.get("rangePosition")
    if rp is not None and rp < 0.45:
        score += 10
        reasons.append("52 周区间偏低 — 或在机构大规模覆盖前")
    elif rp is not None and rp > 0.85:
        score -= 8
        reasons.append("接近日内/年内高位 — 警惕情绪末段追价")

    month = ctx.get("monthChangePct")
    if month is not None:
        if 0 < month <= 18:
            score += 6
            reasons.append(f"近一月 +{month}% — 重估进行中但未必过热")
        elif month > 35:
            score -= 10
            reasons.append("短期涨幅过大 — 社交情绪驱动后慎追")

    rs = ctx.get("relativeStrength")
    if rs is not None and rs >= 3:
        score += 6

    beta = ctx.get("beta")
    if beta is not None and beta >= 1.15:
        score += 4

    margins = ctx.get("profitMargins")
    if margins is not None and margins >= 20:
        score += 5
        reasons.append(f"净利率 {margins}% — 环节稀缺性/定价权")

    return _clamp_score(score), reasons[:5]


SCORERS: dict[str, Callable[[dict], tuple[float, list[str]]]] = {
    "buffett": _score_buffett,
    "graham": _score_graham,
    "lynch": _score_lynch,
    "munger": _score_munger,
    "templeton": _score_templeton,
    "soros": _score_soros,
    "serenity": _score_serenity,
}


def _signal_from_score(score: float) -> tuple[str, str]:
    if score >= 72:
        return "buy", "符合风格 · 建议关注"
    if score >= 58:
        return "watch", "部分符合 · 观察等待"
    return "watch", "弱匹配 · 仅供参考"


def _build_plan(profile: MasterProfile, ctx: dict, score: float) -> dict:
    price = ctx.get("price")
    currency = ctx.get("currency", "")
    if profile.id == "buffett":
        entry = f"围绕 {price} {currency} 分批建仓，优先在回调至年线附近加仓；不追短线热点。"
        holding = f"持有期 {profile.holding}；关注 ROE 与护城河是否恶化。"
        risk = "基本面永久性损伤时退出；不因正常波动止损。"
    elif profile.id == "graham":
        entry = f"仅在 {price} 附近或更低、且 PE/PB 维持低位时分批买入；拒绝「便宜但坏」的公司。"
        holding = f"持有至估值修复至合理区间（{profile.holding}）。"
        risk = "负债恶化或盈利持续下滑时减仓；分散持有降低单一风险。"
    elif profile.id == "lynch":
        entry = f"确认 PEG 与盈利增速匹配后，于 {price} 附近建仓；季度财报验证成长逻辑。"
        holding = f"成长故事兑现或 PEG > 2 时考虑获利（{profile.holding}）。"
        risk = "盈利增速断崖式下滑时退出；不因短期回调轻易清仓。"
    elif profile.id == "munger":
        entry = f"以 {price} 为参考价，在优质复利逻辑未变前提下长期持有；好公司少动。"
        holding = f"{profile.holding}；与伟大企业共同成长。"
        risk = "商业模式被颠覆或管理层重大失误时退出。"
    elif profile.id == "templeton":
        entry = f"市场极度悲观、价格 {price} 处于低位区间时逆向买入；需确认基本面未实质性恶化。"
        holding = f"等待情绪修复（{profile.holding}）；耐心是关键。"
        risk = "若逆向逻辑被证伪（基本面崩塌），果断止损。"
    elif profile.id == "serenity":
        entry = (
            f"在 {price} {currency} 附近建立 conviction 仓位；"
            "从终端需求（算力/光互连/机器人）向上游追溯，独立验证瓶颈是否仍不可替代。"
        )
        holding = (
            f"{profile.holding}；等待供应链重估、扩产瓶颈确认或并购催化，"
            "接受小盘科技股的较大波动。"
        )
        risk = (
            "证伪点：技术路线变更、客户找到替代供应商、瓶颈环节扩产后稀缺性消失；"
            "不因 X/社交热度末段追高。"
        )
    else:
        entry = f"趋势确认后于 {price} 附近顺势建仓；宏观与相对强度共振时加仓。"
        holding = f"短中期趋势交易（{profile.holding.strip()}）；趋势破坏即减仓。"
        risk = "跌破关键均线或相对强度转负时严格止损；反身性逆转要快。"

    position = "单大师风格内建议 1–2 只核心标的；与战术策略、XRPS 战役仓独立配置。"
    return {"entry": entry, "holding": holding, "risk": risk, "position": position}


def _pick_row(profile: MasterProfile, ctx: dict, score: float, reasons: list[str]) -> dict:
    signal, label = _signal_from_score(score)
    metrics = {
        "pe": ctx.get("pe"),
        "pb": ctx.get("pb"),
        "roe": ctx.get("roe"),
        "peg": ctx.get("peg"),
        "earningsGrowth": ctx.get("earningsGrowth"),
        "profitMargins": ctx.get("profitMargins"),
        "monthChangePct": ctx.get("monthChangePct"),
        "relativeStrength": ctx.get("relativeStrength"),
        "rangePosition": ctx.get("rangePosition"),
    }
    if profile.id == "serenity":
        mcap = ctx.get("marketCap")
        if mcap is not None:
            metrics["marketCapB"] = round(mcap / 1e9, 1)
        tag = SERENITY_BOTTLENECK_TAGS.get(ctx.get("symbol", ""))
        if tag:
            metrics["bottleneckLayer"] = tag[0]

    row = {
        "symbol": ctx["symbol"],
        "name": ctx["name"],
        "market": ctx["market"],
        "sector": ctx.get("sector"),
        "currency": ctx.get("currency"),
        "price": ctx.get("price"),
        "matchScore": score,
        "signal": signal,
        "signalLabel": label,
        "reasons": reasons,
        "plan": _build_plan(profile, ctx, score),
        "metrics": metrics,
    }
    return row


def _master_extra(profile: MasterProfile) -> dict:
    if profile.id == "serenity":
        return {
            "xHandle": "@aleabitoreddit",
            "platform": "X",
            "sourceNote": "规则化模拟其公开的「卡脖子/紫苏叶」框架，非本人操作建议",
        }
    return {}


def build_master_recommendations(candidates: dict) -> dict:
    contexts: list[dict] = []
    for symbol, meta in candidates.items():
        ctx = fetch_candidate_context(symbol, meta)
        if ctx:
            contexts.append(ctx)

    masters_out = []
    for profile in MASTER_PROFILES:
        scorer = SCORERS[profile.id]
        ranked: list[tuple[float, dict, list[str]]] = []
        for ctx in contexts:
            score, reasons = scorer(ctx)
            if score >= MIN_MATCH_SCORE:
                ranked.append((score, ctx, reasons))
        ranked.sort(key=lambda x: (-x[0], x[1]["symbol"]))

        picks = [_pick_row(profile, ctx, score, reasons) for score, ctx, reasons in ranked[:PICKS_PER_MASTER]]

        masters_out.append(
            {
                "id": profile.id,
                "name": profile.name,
                "nameEn": profile.name_en,
                "style": profile.style,
                "philosophy": profile.philosophy,
                "principles": list(profile.principles),
                "holdingHorizon": profile.holding,
                "picks": picks,
                **_master_extra(profile),
            }
        )

    return {
        "version": MASTER_VERSION,
        "strategy": (
            f"{MASTER_VERSION} 投资大师风格荐股："
            f"基于 Yahoo 基本面与价格特征，模拟 {len(MASTER_PROFILES)} 位大师选股逻辑；"
            f"每位大师推荐 {PICKS_PER_MASTER} 只，与战术 v1.3 相互独立。"
        ),
        "disclaimer": (
            "大师风格荐股为规则化模拟，非真实人物操作建议；"
            "Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；"
            "基本面数据可能有延迟或缺失，仅供研究，不构成投资建议。"
        ),
        "masters": masters_out,
    }
