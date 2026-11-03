/** 小米交易员看板 — 读 data/xiaomi_trader.json 与 data/xiaomi_radar.json */

const XIAOMI_TRADER_URL = "data/xiaomi_trader.json";
const XIAOMI_RADAR_URL = "data/xiaomi_radar.json";

const XM_KINDS = new Set(["earnings", "delivery", "product", "data"]);
const XM_STATUSES = new Set(["pass", "caution", "block", "open"]);
const XM_SCENARIOS = new Set(["bull", "base", "bear"]);
const XM_TONES = new Set(["strength", "pressure", "watch"]);

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
  const n = Number(value);
  const sign = n > 0 ? "+" : "";
  return `${sign}${n.toFixed(1)}%`;
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

function xmLink(url, label) {
  if (typeof url !== "string" || !url.startsWith("https://")) return "";
  const text = label || url;
  return `<a href="${xmEscape(url)}" rel="noopener noreferrer">${xmEscape(text)}</a>`;
}

function xmEventCard(event) {
  const soon = event.within30 ? `<span class="xm-badge xm-badge--soon">30 天内</span>` : `<span class="xm-badge">60 天内</span>`;
  const source = event.sourceUrl
    ? xmLink(event.sourceUrl, event.source || "来源")
    : xmEscape(event.source || "");
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
    </li>
  `;
}

function renderXiaomiTrader(trader, radar, marketData) {
  const root = document.getElementById("xiaomi-trader-root");
  if (!root) return;
  if (!trader) {
    root.innerHTML = `
      <p class="xm-disclaimer">仅供研究参考，不构成投资建议。</p>
      <p class="empty">小米交易员看板数据还没生成。本地可运行 python scripts/xiaomi_trader.py。</p>
    `;
    renderCockpitXiaomi(null);
    return;
  }

  xiaomiTraderData = trader;
  xiaomiRadarData = radar;
  const calendar = trader.calendar || {};
  const scenarios = trader.scenarios || {};
  const checklist = trader.checklist || {};
  const valuation = trader.valuation || {};
  const anchor = trader.anchor || {};
  const box = trader.box || {};
  const narrative = trader.narrative || {};
  const auto = trader.autoDelivery || {};
  const live = xmLivePrice(marketData);
  const filePrice = valuation.priceHkd;
  const price = filePrice != null ? filePrice : live.price;
  const priceNote = filePrice != null ? "看板快照" : "页面行情";
  const drift =
    live.price != null && filePrice != null && Math.abs(live.price - filePrice) > 0.009
      ? `<p class="xm-hero__asof">页面行情 ${xmNum(live.price, 2)}，与快照不一致。倍数和四道门仍按快照，下次数据任务重算。</p>`
      : "";
  const updated = typeof formatDateTime === "function" ? formatDateTime(trader.updatedAt) : trader.updatedAt || "—";
  const next = calendar.next;
  const counts = checklist.counts || {};
  const blocked = counts.block || 0;

  const upcoming = (calendar.upcoming || []).map(xmEventCard).join("") || `<li class="xm-event"><div></div><div><p class="xm-event__title">未来 ${calendar.horizonDays || 60} 天没有已填写日期的事项</p></div></li>`;
  const undated = (calendar.undated || [])
    .map(
      (event) => `
      <li class="xm-event">
        <div><p class="xm-event__when">待定</p><p class="xm-event__date">人工补日期</p></div>
        <div>
          <span class="xm-badge ${xmKindClass(event.kind)}">${xmEscape(event.kindLabel || "事项")}</span>
          <p class="xm-event__title">${xmEscape(event.title)}</p>
          <p class="xm-note">${xmEscape(event.note || "")}</p>
        </div>
      </li>`
    )
    .join("");

  const scenarioRows = (scenarios.items || [])
    .map(
      (row) => `
      <tr class="${xmScenarioClass(row.id)}">
        <td>${xmEscape(row.label)}</td>
        <td>${xmNum(row.revenueYi, 0)}</td>
        <td>${xmNum(row.adjustedNetProfitYi, 0)}</td>
        <td>${row.impliedPe == null ? "—" : `${xmNum(row.impliedPe, 1)} 倍`}</td>
        <td>${xmEscape(row.narrative)}</td>
      </tr>`
    )
    .join("");

  const gates = (checklist.gates || [])
    .map(
      (gate) => `
      <article class="xm-gate ${xmStatusClass(gate.status)}">
        <div class="xm-gate__head">
          <h3 class="xm-gate__label">${xmEscape(gate.label)}</h3>
          <p class="xm-gate__status">${xmEscape(gate.statusLabel || gate.status || "")}</p>
        </div>
        <p class="xm-gate__summary">${xmEscape(gate.summary)}</p>
        <p class="xm-gate__prompt">人工：${xmEscape(gate.humanPrompt || "")}</p>
        ${
          gate.humanNote
            ? `<p class="xm-gate__note">已写备注：${xmEscape(gate.humanNote)}</p>`
            : `<p class="xm-gate__note">备注仍空。改 data/xiaomi_trader_seed.json 后重新生成数据。</p>`
        }
      </article>`
    )
    .join("");

  const radarItems = ((radar && radar.items) || [])
    .map(
      (item) => `
      <li class="xm-radar__item">
        <div>
          <p class="${xmToneClass(item.tone)}">${xmEscape(xmToneLabel(item.tone))}</p>
          <p class="xm-radar__meta">${xmEscape(item.pillar || "")}</p>
        </div>
        <div>
          <p class="xm-radar__title">${xmEscape(item.title)}</p>
          <p class="xm-radar__detail">${xmEscape(item.detail)}</p>
          <p class="xm-radar__meta">${xmEscape(item.source || "")}${item.asOf ? ` · ${xmEscape(item.asOf)}` : ""}</p>
        </div>
      </li>`
    )
    .join("");

  const anchorUrl = xmLink(anchor.sourceUrl, "中期业绩公告");
  const sim = trader.publicSim;

  root.innerHTML = `
    <header class="xm-hero">
      <div>
        <p class="xm-hero__eyebrow">Xiaomi trader · 业务与纪律</p>
        <h2 class="xm-hero__title">${xmEscape(trader.name || "小米集团")}</h2>
        <p class="xm-hero__headline">${xmEscape(narrative.headline || "")}</p>
        <p class="xm-hero__body">${xmEscape(narrative.body || "")}</p>
      </div>
      <div class="xm-hero__aside">
        <p class="xm-hero__price">${xmNum(price, 2)} <span>港元</span></p>
        <p class="xm-hero__meta">${xmEscape(priceNote)} · 箱体 ${xmEscape((box.advice || {}).actionLabel || "—")}</p>
        <p class="xm-hero__asof">${xmEscape(trader.symbol || "1810.HK")} · 数据 ${xmEscape(updated)}</p>
        ${drift}
      </div>
    </header>
    <p class="xm-disclaimer">${xmEscape(trader.disclaimer || "仅供研究参考，不构成投资建议。")} 情景是假设，不是预测。XRPS 模拟盘不是真实持仓。本页不替代箱体策略和滚动仓。</p>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>日历</h2>
        <p>未来 ${calendar.horizonDays || 60} 天 · 基准日 ${xmEscape(calendar.asOf || "—")} · 30 天内优先看</p>
      </div>
      ${
        next
          ? `<div class="xm-next">
              <div>
                <p class="xm-kicker">下一窗口</p>
                <p class="xm-next__title">${xmEscape(next.title)}</p>
                <p class="xm-next__note">${xmEscape(next.date || "")} · ${xmEscape(next.kindLabel || "")}</p>
              </div>
              <p class="xm-next__count">${xmEscape(next.countdownLabel || "—")}</p>
            </div>`
          : `<p class="xm-note">未来 ${calendar.horizonDays || 60} 天没有已写日期的窗口。</p>`
      }
      <ul class="xm-list">${upcoming}</ul>
      ${
        undated
          ? `<h3 class="xm-subtitle">日期未定</h3><ul class="xm-list">${undated}</ul>`
          : ""
      }
      <div class="xm-facts">
        <article class="xm-fact-card">
          <p class="xm-kicker">10 月交付下限</p>
          <p><strong>${xmInt(auto.octoberLowerBound)}</strong> 辆</p>
          <p class="xm-fact">公司披露于 ${xmEscape(auto.octoberAnnouncedOn || "—")}</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">9 月交付</p>
          <p><strong>${xmInt(auto.septemberUnits)}</strong> 辆</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">前 10 个月下限</p>
          <p><strong>${xmInt(auto.ytdLowerBoundThroughOctober)}</strong> 辆</p>
          <p class="xm-fact">${xmEscape(auto.ytdNote || "")}</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">全年目标（引述）</p>
          <p><strong>${xmInt(auto.fyTarget)}</strong> 辆</p>
          <p class="xm-fact">${xmEscape(auto.fyTargetNote || "")}</p>
        </article>
      </div>
      <p class="xm-table-note">${xmEscape(auto.skyNomad || "")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>情景表</h2>
        <p>${xmEscape(scenarios.assumptionLabel || "情景假设，不是业绩预测")} · ${xmEscape(scenarios.horizon || "")} · ${xmEscape(scenarios.profitMetricLabel || "经调整净利润")}</p>
      </div>
      <div class="xm-facts">
        <article class="xm-fact-card">
          <p class="xm-kicker">已披露收入</p>
          <p><strong>${xmNum(anchor.revenueYi, 1)}</strong> 亿元</p>
          <p class="xm-fact">${xmPct(anchor.revenueYoyPct)} · ${xmEscape(anchor.periodLabel || "")}</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">已披露经调整净利润</p>
          <p><strong>${xmNum(anchor.adjustedNetProfitYi, 1)}</strong> 亿元</p>
          <p class="xm-fact">${xmPct(anchor.adjustedNetProfitYoyPct)}</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">同期 IFRS 净利润</p>
          <p><strong>${xmNum(anchor.ifrsNetProfitYi, 1)}</strong> 亿元</p>
          <p class="xm-fact">${xmPct(anchor.ifrsNetProfitYoyPct)} · 情景表不用这个口径</p>
        </article>
        <article class="xm-fact-card">
          <p class="xm-kicker">现价对应市值</p>
          <p><strong>${xmNum(valuation.marketCapCnyYi, 0)}</strong> 亿元</p>
          <p class="xm-fact">${xmNum(valuation.marketCapHkdYi, 0)} 亿港元 · ${xmEscape(valuation.fxNote || "")}</p>
        </article>
      </div>
      <p class="xm-table-note">${xmEscape(anchor.profitNote || "")} ${anchorUrl}</p>
      <div class="table-wrap">
        <table class="data-table xm-scenarios">
          <thead>
            <tr>
              <th>情景</th>
              <th>收入（亿元）</th>
              <th>经调整净利润（亿元）</th>
              <th>现价隐含倍数</th>
              <th>叙事（假设）</th>
            </tr>
          </thead>
          <tbody>${scenarioRows}</tbody>
        </table>
      </div>
      <p class="xm-table-note">${xmEscape(valuation.multipleNote || "")} ${xmEscape(valuation.sharesNote || "")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>开仓 checklist</h2>
        <p>${blocked ? "有门被拦住，按纪律不新开多。" : "四门都要过。自动结论只填公开数据，人工备注仍要自己写。"} 通过 ${counts.pass || 0} · 需人工 ${ (counts.caution || 0) + (counts.open || 0) } · 拦住 ${blocked}</p>
      </div>
      <div class="xm-gates">${gates}</div>
      <p class="xm-table-note">${xmEscape(checklist.editHint || "")}${
        sim
          ? ` 模拟盘对照：${xmEscape(sim.label || "")}，仓位 ${xmNum(sim.positionPct, 1)}%，收益 ${xmPct(sim.returnPct)}。`
          : ""
      }</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>业务雷达</h2>
        <p>人工样本，来自 data/xiaomi_radar.json，没有新闻爬虫</p>
      </div>
      ${
        radarItems
          ? `<ul class="xm-radar">${radarItems}</ul>`
          : `<p class="empty">${xmEscape((trader.radar || {}).error || radar?.disclaimer || "雷达样本为空。")}</p>`
      }
      <p class="xm-table-note">${xmEscape((radar && radar.disclaimer) || "仅供研究参考，不构成投资建议。")}</p>
    </section>
  `;

  renderCockpitXiaomi(trader);
}

function xmToneLabel(tone) {
  if (tone === "strength") return "强项";
  if (tone === "pressure") return "压力";
  return "观察";
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
  const next = trader.calendar?.next;
  const counts = trader.checklist?.counts || {};
  const blocked = (trader.checklist?.gates || []).find((gate) => gate.status === "block");
  const hint = blocked
    ? `${blocked.label}门拦住，不新开多`
    : `四门：通过 ${counts.pass || 0}，其余待人工`;
  el.innerHTML = `
    <p class="xm-cockpit__next">${xmEscape(next?.countdownLabel || "—")}</p>
    <p class="xm-cockpit__title">${xmEscape(next?.title || "未来 60 天无已写窗口")}</p>
    <p class="xm-cockpit__hint">${xmEscape(hint)} · 仅供研究参考</p>
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
