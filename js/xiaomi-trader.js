/** 小米交易员台 — 立场由四门决定，雷达来自可重算的策展簇 */

const XIAOMI_TRADER_URL = "data/xiaomi_trader.json";
const XIAOMI_RADAR_URL = "data/xiaomi_radar.json";

const XM_KINDS = new Set(["earnings", "delivery", "product", "data"]);
const XM_STATUSES = new Set(["pass", "caution", "block", "open"]);
const XM_SCENARIOS = new Set(["bull", "base", "bear"]);
const XM_TONES = new Set(["strength", "pressure", "watch"]);
const XM_VERDICTS = {
  met: "符合",
  missed: "不符",
  pending: "待验证",
  behind: "落后",
  mixed: "分化",
};

let xiaomiTraderData = null;
let xiaomiRadarData = null;

function xmEscape(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function xmNum(value, digits = 1) {
  if (value == null || Number.isNaN(Number(value))) return "—";
  return Number(value).toLocaleString("zh-CN", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function xmInt(value) {
  if (value == null || Number.isNaN(Number(value))) return "—";
  return Number(value).toLocaleString("zh-CN", { maximumFractionDigits: 0 });
}

function xmPct(value) {
  if (value == null || Number.isNaN(Number(value))) return "—";
  return `${Number(value) > 0 ? "+" : ""}${Number(value).toFixed(1)}%`;
}

function xmKindClass(kind) {
  return XM_KINDS.has(kind) ? `xm-kind--${kind}` : "xm-kind--other";
}

function xmStatusClass(status) {
  return XM_STATUSES.has(status) ? `xm-gate--${status}` : "xm-gate--open";
}

function xmScenarioClass(id) {
  return XM_SCENARIOS.has(id) ? `xm-scenario--${id}` : "";
}

function xmToneClass(tone) {
  return XM_TONES.has(tone) ? `xm-tone--${tone}` : "xm-tone--watch";
}

function xmBarClass(value, max) {
  if (!max) return "xm-bar--h0";
  const steps = Math.max(0, Math.min(10, Math.round((Number(value) / max) * 10)));
  return `xm-bar--h${steps * 10}`;
}

function xmLink(url, label) {
  if (typeof url !== "string" || !url.startsWith("https://")) return xmEscape(label || "");
  return `<a href="${xmEscape(url)}" rel="noopener noreferrer">${xmEscape(label || url)}</a>`;
}

function xmHashLinks(links) {
  return (links || [])
    .filter((link) => typeof link.href === "string" && link.href.startsWith("#"))
    .map((link) => `<a href="${xmEscape(link.href)}">${xmEscape(link.label || link.href)}</a>`)
    .join("");
}

function xmList(items) {
  if (!items || !items.length) return "";
  return `<ul class="xm-rule-list">${items.map((item) => `<li>${xmEscape(item)}</li>`).join("")}</ul>`;
}

function xmEventCard(event) {
  const soon = event.within30
    ? `<span class="xm-badge xm-badge--soon">30 天内</span>`
    : `<span class="xm-badge">60 天内</span>`;
  const source = event.sourceUrl ? xmLink(event.sourceUrl, event.source || "来源") : xmEscape(event.source || "");
  return `
    <li class="xm-event">
      <div>
        <p class="xm-event__when">${xmEscape(event.countdownLabel || "待定")}</p>
        <p class="xm-event__date">${xmEscape(event.date || "日期未定")}</p>
      </div>
      <div>
        <div class="xm-badges">
          <span class="xm-badge ${xmKindClass(event.kind)}">${xmEscape(event.kindLabel || "事项")}</span>
          ${event.date ? soon : ""}
        </div>
        <p class="xm-event__title">${xmEscape(event.title)}</p>
        <p class="xm-note">${xmEscape(event.note || "")}</p>
        <p class="xm-note xm-links">${source}</p>
      </div>
    </li>`;
}

function xmRadarClusters(radar) {
  const clusters = (radar && radar.clusters) || [];
  if (!clusters.length) {
    const items = (radar && radar.items) || [];
    if (!items.length) return "";
    return `<ul class="xm-radar">${items.map(xmRadarItem).join("")}</ul>`;
  }
  return clusters
    .map((cluster) => {
      const conf = ["high", "medium", "low"].includes(cluster.confidence) ? cluster.confidence : "low";
      return `
        <section class="xm-cluster">
          <div class="xm-cluster__head">
            <h3 class="xm-cluster__title">${xmEscape(cluster.title || cluster.pillar || "簇")}</h3>
            <p class="xm-conf--${conf}">置信 ${xmEscape(cluster.confidenceLabel || conf)} · ${cluster.staleCount ? `${cluster.staleCount} 条过期` : "在窗口内"}</p>
          </div>
          <p class="xm-note">${xmEscape(cluster.summary || "")}</p>
          <ul class="xm-radar">${(cluster.items || []).map(xmRadarItem).join("")}</ul>
        </section>`;
    })
    .join("");
}

function xmRadarItem(item) {
  const conf = ["high", "medium", "low"].includes(item.confidence) ? item.confidence : "low";
  return `
    <li class="xm-radar__item">
      <div>
        <p class="${xmToneClass(item.tone)}">${xmEscape(item.toneLabel || "观察")}</p>
        <p class="xm-radar__meta xm-conf--${conf}">${xmEscape(item.confidenceLabel || "")}</p>
        <p class="xm-radar__meta ${item.stale ? "xm-stale" : ""}">${item.stale ? "过期" : xmEscape(item.pillar || "")}</p>
      </div>
      <div>
        <p class="xm-radar__title">${xmEscape(item.title)}</p>
        <p class="xm-radar__detail">${xmEscape(item.detail)}</p>
        <p class="xm-radar__meta">${xmLink(item.sourceUrl, item.source)} · ${xmEscape(item.date || "无日期")}</p>
      </div>
    </li>`;
}

function renderXiaomiTrader(trader, radar, marketData) {
  const root = document.getElementById("xiaomi-trader-root");
  if (!root) return;
  if (!trader) {
    root.innerHTML = `
      <p class="xm-disclaimer">仅供研究参考，不构成投资建议。</p>
      <p class="empty">小米交易员台还没生成。运行 python scripts/xiaomi_trader.py。</p>`;
    renderCockpitXiaomi(null);
    return;
  }

  xiaomiTraderData = trader;
  xiaomiRadarData = radar;
  const stance = trader.stance || {};
  const calendar = trader.calendar || {};
  const scenarios = trader.scenarios || {};
  const checklist = trader.checklist || {};
  const valuation = trader.valuation || {};
  const anchor = trader.anchor || {};
  const box = trader.box || {};
  const indicators = trader.indicators || {};
  const weekly = trader.weeklyReview || {};
  const limits = trader.riskLimits || {};
  const sim = trader.publicSim;
  const gates = checklist.gates || [];
  const counts = checklist.counts || {};
  const live = xmLivePrice(marketData);
  const filePrice = valuation.priceHkd;
  const price = filePrice != null ? filePrice : live.price;
  const updated = typeof formatDateTime === "function" ? formatDateTime(trader.updatedAt) : trader.updatedAt || "—";
  const drift =
    live.price != null && filePrice != null && Math.abs(live.price - filePrice) > 0.009
      ? `<p class="xm-hero__asof">页面行情 ${xmNum(live.price, 2)} 与快照不一致。倍数和四门仍按快照。</p>`
      : "";
  const tone = ["block", "caution", "pass"].includes(stance.tone) ? stance.tone : "caution";
  const chips = gates
    .map(
      (gate) =>
        `<span class="xm-chip xm-chip--${XM_STATUSES.has(gate.status) ? gate.status : "open"}">${xmEscape(gate.label)} ${xmEscape(gate.statusLabel || "")}</span>`
    )
    .join("");

  const points = (indicators.autoMonthly && indicators.autoMonthly.points) || [];
  const maxDelivery = points.reduce((max, point) => Math.max(max, Number(point.value) || 0), 0);
  const bars = points
    .map((point) => {
      const bound = point.quality === "lower_bound";
      return `
        <div class="xm-bar ${xmBarClass(point.value, maxDelivery)} ${bound ? "xm-bar--bound" : ""}">
          <div class="xm-bar__fill"></div>
          <p class="xm-bar__value">${xmInt(point.value)}</p>
          <p class="xm-bar__label">${xmEscape(String(point.period || "").slice(5))}${bound ? " 下限" : ""}</p>
        </div>`;
    })
    .join("");

  const phone = indicators.phone || {};
  const memory = indicators.memoryCost || {};
  const iot = indicators.iotMargin || {};
  const gross = indicators.groupGrossMargin || {};
  const scenarioRows = (scenarios.items || [])
    .map((row) => {
      const cap = valuation.maxBasePeToAdd;
      let versus = "—";
      if (row.impliedPe != null && cap != null) {
        versus = row.impliedPe > cap ? `高于加仓线 ${xmNum(cap, 0)}` : `未超过加仓线 ${xmNum(cap, 0)}`;
      }
      return `
        <tr class="${xmScenarioClass(row.id)}">
          <td>${xmEscape(row.label)}</td>
          <td>${xmNum(row.revenueYi, 0)}</td>
          <td>${xmNum(row.adjustedNetProfitYi, 0)}</td>
          <td>${row.impliedPe == null ? "—" : `${xmNum(row.impliedPe, 1)} 倍`}</td>
          <td>${xmEscape(versus)}</td>
          <td>${xmEscape(row.narrative)}</td>
        </tr>`;
    })
    .join("");

  const reviewRows = (weekly.rows || [])
    .map((row) => {
      const verdict = XM_VERDICTS[row.verdict] ? row.verdict : "pending";
      return `
        <tr>
          <td>${xmEscape(row.topic)}</td>
          <td>${xmEscape(row.assumption)}</td>
          <td>${xmEscape(row.actual)}</td>
          <td class="xm-verdict xm-verdict--${verdict}">${XM_VERDICTS[verdict]}</td>
        </tr>`;
    })
    .join("");

  const gateCards = gates
    .map(
      (gate) => `
      <article class="xm-gate ${xmStatusClass(gate.status)}">
        <div class="xm-gate__head">
          <h3 class="xm-gate__label">${xmEscape(gate.label)}</h3>
          <p class="xm-gate__status">${xmEscape(gate.statusLabel || "")}</p>
        </div>
        <p class="xm-gate__summary">${xmEscape(gate.summary)}</p>
        <p class="xm-gate__prompt">人工：${xmEscape(gate.humanPrompt || "")}</p>
        <p class="xm-gate__note">${gate.humanNote ? `已写备注：${xmEscape(gate.humanNote)}` : "备注仍空。空备注不能把拦住改成通过。"}</p>
      </article>`
    )
    .join("");

  const upcoming = (calendar.upcoming || []).map(xmEventCard).join("");
  const undated = (calendar.undated || [])
    .map(
      (event) => `
      <li class="xm-event">
        <div><p class="xm-event__when">待定</p></div>
        <div>
          <p class="xm-event__title">${xmEscape(event.title)}</p>
          <p class="xm-note">${xmEscape(event.note || "")}</p>
        </div>
      </li>`
    )
    .join("");
  const stops = (limits.fundamentalStops || []).map((item) => `<li>${xmEscape(item)}</li>`).join("");
  const anchorUrl = xmLink(anchor.sourceUrl, "中期业绩公告");
  const radarBody = xmRadarClusters(radar);

  root.innerHTML = `
    <header class="xm-hero">
      <div>
        <p class="xm-hero__eyebrow">Xiaomi desk · 1810.HK</p>
        <h2 class="xm-hero__title">${xmEscape(trader.name || "小米集团")}</h2>
        <p class="xm-desk-links">${xmHashLinks(trader.links)}</p>
      </div>
      <div class="xm-hero__aside">
        <p class="xm-hero__price">${xmNum(price, 2)} <span>港元</span></p>
        <p class="xm-hero__meta">看板快照 · 箱体 ${xmEscape((box.advice || {}).actionLabel || "—")}</p>
        <p class="xm-hero__asof">${xmEscape(updated)}</p>
        ${drift}
      </div>
    </header>
    <p class="xm-disclaimer">${xmEscape(trader.disclaimer || "仅供研究参考，不构成投资建议。")} 情景是假设，不是预测。XRPS 模拟盘不是真实持仓。</p>

    <section class="xm-stance xm-stance--${tone}" aria-live="polite">
      <p class="xm-stance__kicker">交易台立场 · 由四门生成，不是研究标题</p>
      <h3 class="xm-stance__headline">${xmEscape(stance.headline || "四门未计算")}</h3>
      <div class="xm-chips">${chips}</div>
      <p class="xm-kicker">允许</p>
      ${xmList(stance.allowed)}
      <p class="xm-kicker">不许写进行动</p>
      ${xmList(stance.forbidden)}
    </section>

    <section class="xm-research">
      <p class="xm-kicker">${xmEscape(stance.researchLabel || "研究叙事")}</p>
      <h3>${xmEscape(stance.researchHeadline || "")}</h3>
      <p class="xm-note">${xmEscape(stance.researchBody || "")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>领先指标</h2>
        <p>只有带来源的数进图。没有的格子保持占位。</p>
      </div>
      <h3 class="xm-subtitle">${xmEscape((indicators.autoMonthly || {}).label || "汽车月交付")}</h3>
      <div class="xm-bars">${bars}</div>
      <p class="xm-table-note">${xmEscape((indicators.autoMonthly || {}).source || "")} 黄色柱是下限，不是精确值。已公布月份均值 ${xmInt((indicators.autoMonthly || {}).reportedAverage)} 辆。</p>
      <div class="xm-facts">
        <article class="xm-fact-card ${phone.placeholder ? "xm-placeholder" : ""}">
          <p class="xm-kicker">${xmEscape(phone.label || "手机")} ${phone.placeholder ? "· 占位" : ""}</p>
          <p><strong>${phone.available ? xmNum(phone.value, 1) : "无出货 / 无 ASP"}</strong></p>
          <p class="xm-fact">${xmEscape(phone.relatedLabel || "")} ${phone.relatedRevenueYi != null ? `${xmNum(phone.relatedRevenueYi, 1)} 亿元` : ""}</p>
          <p class="xm-fact">${xmEscape(phone.note || "")}</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">${xmEscape(memory.label || "存储与成本")}</p>
          <p><strong>无价格指数</strong></p>
          <p class="xm-fact">${xmEscape(memory.note || "")}</p>
        </article>
        <article class="xm-fact-card ${iot.placeholder ? "xm-placeholder" : ""}">
          <p class="xm-kicker">${xmEscape(iot.label || "IoT 毛利率")} · 占位</p>
          <p><strong>—</strong></p>
          <p class="xm-fact">${xmEscape(iot.note || "")}</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">${xmEscape(gross.label || "集团毛利率")}</p>
          <p><strong>${xmNum(gross.valuePct, 1)}%</strong></p>
          <p class="xm-fact">上年同期约 ${xmNum(gross.priorValuePct, 1)}%。${xmEscape(gross.note || "")}</p>
        </article>
      </div>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>估值与仓位</h2>
        <p>${xmEscape(scenarios.assumptionLabel || "情景假设")} · 加仓线 ${xmNum(valuation.maxBasePeToAdd, 0)} 倍 · 贵价线 ${xmNum(valuation.richBasePe, 0)} 倍</p>
      </div>
      <div class="xm-split">
        <div>
          <div class="xm-facts">
            <article class="xm-fact-card">
              <p class="xm-kicker">上半年年化倍数</p>
              <p><strong>${valuation.h1RunRatePe == null ? "—" : `${xmNum(valuation.h1RunRatePe, 1)} 倍`}</strong></p>
              <p class="xm-fact">经调整净利润年化 ${xmNum(valuation.h1RunRateProfitYi, 1)} 亿元</p>
            </article>
            <article class="xm-fact-card">
              <p class="xm-kicker">现价市值</p>
              <p><strong>${xmNum(valuation.marketCapCnyYi, 0)}</strong> 亿元</p>
              <p class="xm-fact">${xmEscape(valuation.fxNote || "")}</p>
            </article>
            <article class="xm-fact-card">
              <p class="xm-kicker">模拟盘仓位</p>
              <p><strong>${sim ? `${xmNum(sim.positionPct, 1)}%` : "—"}</strong></p>
              <p class="xm-fact">加仓线 ${xmNum(limits.addCeilingPct, 0)}% · XRPS 上限 ${xmNum(limits.maxPositionPct, 0)}% · 现金底线 ${xmNum(limits.minCashPct, 0)}%</p>
            </article>
            <article class="xm-fact-card">
              <p class="xm-kicker">箱体底部</p>
              <p><strong>${xmNum(limits.boxBottom, 2)}</strong></p>
              <p class="xm-fact">箱内位置 ${box.positionInBox == null ? "—" : `${Math.round(box.positionInBox * 100)}%`} · ${xmEscape((box.advice || {}).actionLabel || "—")}</p>
            </article>
          </div>
          <p class="xm-table-note">${xmEscape(valuation.historyNote || "")} ${xmEscape(limits.limitsNote || "")}</p>
          <p class="xm-table-note">已披露：收入 ${xmNum(anchor.revenueYi, 1)} 亿元（${xmPct(anchor.revenueYoyPct)}），经调整净利润 ${xmNum(anchor.adjustedNetProfitYi, 1)} 亿元（${xmPct(anchor.adjustedNetProfitYoyPct)}），IFRS 净利润 ${xmNum(anchor.ifrsNetProfitYi, 1)} 亿元。${anchorUrl}</p>
        </div>
        <div>
          <p class="xm-kicker">风险限度</p>
          <ul class="xm-rule-list">${stops}</ul>
          <p class="xm-desk-links">${xmHashLinks(trader.links)}</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table xm-scenarios">
          <thead>
            <tr>
              <th>情景</th>
              <th>收入（亿元）</th>
              <th>经调整净利润（亿元）</th>
              <th>现价倍数</th>
              <th>相对加仓线</th>
              <th>叙事（假设）</th>
            </tr>
          </thead>
          <tbody>${scenarioRows}</tbody>
        </table>
      </div>
      <p class="xm-table-note">${xmEscape(valuation.multipleNote || "")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>${xmEscape(weekly.title || "本周假设对照")}</h2>
        <p>周起始 ${xmEscape(weekly.weekOf || "—")} · 符合 ${weekly.counts?.met || 0} · 落后 ${weekly.counts?.behind || 0} · 待验证 ${weekly.counts?.pending || 0}</p>
      </div>
      <div class="table-wrap">
        <table class="data-table xm-scenarios">
          <thead><tr><th>题目</th><th>假设</th><th>已公开的实际</th><th>判定</th></tr></thead>
          <tbody>${reviewRows}</tbody>
        </table>
      </div>
      <p class="xm-table-note">${xmEscape(weekly.note || "")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>日历</h2>
        <p>未来 ${calendar.horizonDays || 60} 天 · 基准日 ${xmEscape(calendar.asOf || "—")}</p>
      </div>
      ${
        calendar.next
          ? `<div class="xm-next"><div><p class="xm-kicker">下一窗口</p><p class="xm-next__title">${xmEscape(calendar.next.title)}</p></div><p class="xm-next__count">${xmEscape(calendar.next.countdownLabel || "—")}</p></div>`
          : ""
      }
      <ul class="xm-list">${upcoming}</ul>
      ${undated ? `<h3 class="xm-subtitle">日期未定</h3><ul class="xm-list">${undated}</ul>` : ""}
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>开仓四门</h2>
        <p>通过 ${counts.pass || 0} · 需人工 ${(counts.caution || 0) + (counts.open || 0)} · 拦住 ${counts.block || 0}。拦住的门会改写页首立场。</p>
      </div>
      <div class="xm-gates">${gateCards}</div>
      <p class="xm-table-note">${xmEscape(checklist.editHint || "")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>业务雷达</h2>
        <p>策展收件箱聚成簇。每条有来源、日期和置信。${radar && radar.feed ? xmEscape(radar.feed.note || "") : "没有爬虫。"}</p>
      </div>
      ${radarBody || `<p class="empty">${xmEscape((trader.radar || {}).error || "雷达还没生成。")}</p>`}
      <p class="xm-table-note">${xmEscape((radar && radar.disclaimer) || "仅供研究参考，不构成投资建议。")}</p>
    </section>
  `;
  renderCockpitXiaomi(trader);
}

function xmLivePrice(marketData) {
  const stock = marketData?.stocks?.find((row) => row.symbol === "1810.HK");
  const fromMarket = stock?.price ?? marketData?.quoteMap?.["1810.HK"];
  if (typeof fromMarket === "number") return { price: fromMarket, source: "market" };
  return { price: null, source: null };
}

function renderCockpitXiaomi(trader) {
  const el = document.getElementById("cockpit-xiaomi");
  if (!el) return;
  if (!trader) {
    el.innerHTML = `<p class="empty">看板数据未加载</p>`;
    return;
  }
  const stance = trader.stance || {};
  const next = trader.calendar?.next;
  el.innerHTML = `
    <p class="xm-cockpit__next">${xmEscape(stance.headline || "立场未计算")}</p>
    <p class="xm-cockpit__title">${xmEscape(next ? `${next.countdownLabel} · ${next.title}` : "未来 60 天无已写窗口")}</p>
    <p class="xm-cockpit__hint">仅供研究参考，不构成投资建议</p>
  `;
}

async function refreshXiaomiTrader(marketData) {
  let trader = xiaomiTraderData;
  let radar = xiaomiRadarData;
  try {
    if (typeof fetchJson === "function") {
      const [nextTrader, nextRadar] = await Promise.all([
        fetchJson(XIAOMI_TRADER_URL),
        fetchJson(XIAOMI_RADAR_URL),
      ]);
      trader = nextTrader || trader;
      radar = nextRadar || radar;
    } else {
      const [traderRes, radarRes] = await Promise.all([
        fetch(`${XIAOMI_TRADER_URL}?t=${Date.now()}`, { cache: "no-store" }),
        fetch(`${XIAOMI_RADAR_URL}?t=${Date.now()}`, { cache: "no-store" }),
      ]);
      if (traderRes.ok) trader = await traderRes.json();
      if (radarRes.ok) radar = await radarRes.json();
    }
  } catch (err) {
    console.error("xiaomi trader load failed", err);
  }
  const md = marketData || (typeof window !== "undefined" ? window.marketData : null) || null;
  renderXiaomiTrader(trader, radar, md);
}

window.renderXiaomiTrader = renderXiaomiTrader;
window.renderCockpitXiaomi = renderCockpitXiaomi;
window.refreshXiaomiTrader = refreshXiaomiTrader;
