const DATA_URL = "data/market.json";
const HISTORY_URL = "data/reco_history.json";
const WENCAI_URL = "data/wencai.json";
const BACKTEST_URL = "data/backtest.json";
const SIGNALS_URL = "data/signals.json";
const PAPER_URL = "data/paper_account.json";
const PAPER_STRATEGY_URL = "data/paper_strategy.json";
const PAPER_BACKTEST_URL = "data/paper_backtest.json";
const DIAGNOSTICS_URL = "data/diagnostics.json";
const AI_CHAIN_URL = "data/ai_chain.json";
const REPORTS_INDEX_URL = "data/reports/index.json";
const MACRO_URL = "data/macro.json";
const POLL_INTERVAL_MS = 5 * 60 * 1000;
const HISTORY_DISPLAY_LIMIT = 40;
const AI_SEARCH_DEBOUNCE_MS = 250;

/** XRPS-X 网格参数（与 scripts/xrps_config.py 一致） */
const XRPS_ROLLING_SELL_LEVELS = [
  { key: "sell_15", pct: 0.15, label: "涨 15%" },
  { key: "sell_25", pct: 0.25, label: "涨 25%" },
  { key: "sell_40", pct: 0.4, label: "涨 40%" },
  { key: "sell_60", pct: 0.6, label: "涨 60%" },
];
const XRPS_ROLLING_BUY_LEVELS = [
  { key: "buy_10", pct: -0.1, label: "回撤 10%" },
  { key: "buy_20", pct: -0.2, label: "回撤 20%" },
  { key: "buy_30", pct: -0.3, label: "回撤 30%" },
];

let lastUpdatedAt = null;
let lastTradingUpdatedAt = null;
let historyFilter = "all";
let recoHistory = null;
let marketData = null;
let signalsData = null;
let backtestData = null;
let paperData = null;
let paperStrategyData = null;
let paperBacktestData = null;
let diagnosticsData = null;
let wencaiData = null;
let lastWencaiUpdatedAt = null;
let yahooNews = [];
let newsFilter = "all";
let aiChainData = null;
let aiChainFilter = "all";
let aiChainSearch = "";
let aiChainView = "list";
let reportsIndex = null;
let currentReportId = null;
let macroData = null;
let quoteMap = {};
let quoteChangeMap = {};
let activeTab = "cockpit";
let recoMode = "tactical";
let suppressTabRoute = false;
const tabBundles = { paper: false, ai: false, reports: false };
let historyDisplayLimit = HISTORY_DISPLAY_LIMIT;
let lastRecoHistoryStamp = null;
let aiSearchTimer = null;

const VALID_TABS = new Set(["cockpit", "reports", "market", "reco", "lab", "paper", "ai"]);
const TAB_ALIASES = { review: "paper", news: "cockpit" };
const DEFAULT_TAB = "cockpit";

function resolveTabId(tabId) {
  if (!tabId) return DEFAULT_TAB;
  if (VALID_TABS.has(tabId)) return tabId;
  return TAB_ALIASES[tabId] || DEFAULT_TAB;
}

let distributionChart;
let stocksChart;
let backtestChart;
let paperChart;
let paperBucketChart;
let paperModalChart;

function formatNumber(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(value)) return "--";
  return Number(value).toLocaleString("zh-CN", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function changeClass(value) {
  if (value === null || value === undefined) return "change--flat";
  if (value > 0) return "change--up";
  if (value < 0) return "change--down";
  return "change--flat";
}

function formatPct(value) {
  if (value === null || value === undefined) return "--";
  const prefix = value > 0 ? "+" : "";
  return `${prefix}${formatNumber(value)}%`;
}

function formatDateTime(iso) {
  if (!iso) return "未知";
  return new Date(iso).toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatFreshnessTime(iso) {
  if (!iso) return null;
  const text = formatDateTime(iso);
  return text.length > 11 ? text.slice(5) : text;
}

function updateHeaderFreshness() {
  const el = document.getElementById("updated-at");
  if (!el) return;
  const parts = [];
  const marketAt = formatFreshnessTime(lastUpdatedAt);
  const wencaiAt = formatFreshnessTime(lastWencaiUpdatedAt);
  const paperAt = formatFreshnessTime(paperData?.updatedAt);
  if (marketAt) parts.push(`行情 ${marketAt}`);
  if (wencaiAt) parts.push(`问财 ${wencaiAt}`);
  if (paperAt) parts.push(`模拟盘 ${paperAt}`);
  el.textContent = parts.length ? parts.join(" · ") : "数据更新中…";
}

function marketClass(market) {
  if (market === "A股") return "cn";
  if (market === "港股") return "hk";
  return "us";
}

function calcReturn(recoPrice, currentPrice) {
  if (!recoPrice || !currentPrice) return null;
  return Number((((currentPrice - recoPrice) / recoPrice) * 100).toFixed(2));
}

function tabFromLocation() {
  const raw = window.location.hash.replace(/^#\/?/, "").trim();
  if (raw) return resolveTabId(raw);
  if (history.state?.tab) return resolveTabId(history.state.tab);
  return DEFAULT_TAB;
}

function tabHash(tabId) {
  return `#${tabId}`;
}

function syncTabRoute(tabId, replace = false) {
  const hash = tabId === DEFAULT_TAB ? "" : tabHash(tabId);
  const url = `${window.location.pathname}${window.location.search}${hash}`;
  const current = `${window.location.pathname}${window.location.search}${window.location.hash}`;
  if (current === url) return;
  if (replace) {
    history.replaceState({ tab: tabId }, "", url);
  } else {
    history.pushState({ tab: tabId }, "", url);
  }
}

function switchTab(tabId, options = {}) {
  const { updateRoute = true, replaceRoute = false } = options;
  if (!VALID_TABS.has(tabId)) tabId = DEFAULT_TAB;

  activeTab = tabId;
  document.querySelectorAll(".tabs__btn").forEach((btn) => {
    const active = btn.dataset.tab === tabId;
    btn.classList.toggle("tabs__btn--active", active);
    btn.setAttribute("aria-selected", active ? "true" : "false");
  });
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    const show = panel.id === `panel-${tabId}`;
    panel.classList.toggle("tab-panel--active", show);
    panel.hidden = !show;
  });

  if (updateRoute && !suppressTabRoute) {
    syncTabRoute(tabId, replaceRoute);
  }

  if (tabId === "market" && marketData) {
    renderDistributionChart(marketData.summary);
    renderStocksChart(marketData.stocks);
  }
  if (tabId === "lab" && backtestData) {
    renderBacktestChart(backtestData.equityCurve);
  }
  if (tabId === "paper") {
    if (paperStrategyData) renderPaperStrategyCard(paperStrategyData);
    if (paperBacktestData) renderPaperBacktestCards(paperBacktestData);
    renderPaperPanel(paperData);
  }
  if (tabId === "market" && wencaiData) {
    renderWencaiPanels(wencaiData);
  }
  if (tabId === "market" && macroData) {
    renderMarketMacro(macroData);
  }
  if (tabId === "ai" && aiChainData) {
    renderAiChain(aiChainData);
    if (aiChainView === "mindmap") renderAiMindMap(aiChainData);
  }
  if (tabId === "reports" && reportsIndex) {
    renderReportsPanel();
  }
  ensureTabData(tabId);
}

function signalStatusLabel(status) {
  const map = {
    open: "持仓中",
    closed_stop: "止损平仓",
    closed_trail: "跟踪止损",
    closed_target: "止盈平仓",
    closed_expired: "到期平仓",
  };
  return map[status] || status || "--";
}

function signalStatusClass(status) {
  if (status === "open") return "signal-status--open";
  if (status === "closed_target" || status === "closed_trail") return "signal-status--win";
  if (status === "closed_stop") return "signal-status--loss";
  return "signal-status--neutral";
}

function reasonLabel(reason) {
  if (!reason) return "--";
  if (reason.includes("滚动卖出")) return reason;
  if (reason.includes("买回") || reason.includes("回撤")) return reason;
  if (reason.includes("连阴")) return reason;
  if (reason.includes("减滚动")) return reason;
  if (reason.includes("翻倍")) return reason;
  if (reason.includes("核心")) return reason;
  const map = { stop: "止损", trail: "跟踪止损", target: "止盈", expiry: "到期" };
  return map[reason] || reason;
}

function bucketLabel(bucket) {
  const map = { core: "核心仓", rolling: "滚动仓", cash: "现金" };
  return map[bucket] || bucket || "--";
}

function setupTabs() {
  const tabs = document.getElementById("main-tabs");
  tabs?.addEventListener("click", (e) => {
    const btn = e.target.closest(".tabs__btn");
    if (btn?.dataset.tab) switchTab(btn.dataset.tab);
  });
  document.querySelectorAll("[data-goto-tab]").forEach((el) => {
    el.addEventListener("click", () => switchTab(el.dataset.gotoTab));
  });

  document.getElementById("reco-mode-tabs")?.addEventListener("click", (e) => {
    const btn = e.target.closest(".reco-mode-btn");
    if (btn?.dataset.recoMode) switchRecoMode(btn.dataset.recoMode);
  });

  window.addEventListener("popstate", () => {
    suppressTabRoute = true;
    switchTab(tabFromLocation(), { updateRoute: false });
    suppressTabRoute = false;
  });

  window.addEventListener("hashchange", () => {
    if (suppressTabRoute) return;
    const tab = tabFromLocation();
    if (tab !== activeTab) {
      suppressTabRoute = true;
      switchTab(tab, { updateRoute: false });
      suppressTabRoute = false;
    }
  });
}

function formatMacroPrice(item) {
  if (!item) return "--";
  if (item.unit === "yield_pct") return `${formatNumber(item.price, 2)}%`;
  return formatNumber(item.price);
}

function formatFredValue(item) {
  if (!item) return "--";
  const unit = item.unit;
  if (unit === "pct" || unit === "spread") return `${formatNumber(item.price, item.unit === "spread" ? 2 : 2)}%`;
  if (unit === "rate") return formatNumber(item.price, 4);
  return formatNumber(item.price);
}

function renderMacroNewsList(news) {
  if (!news?.length) {
    return '<p class="empty">暂无 Finnhub 宏观资讯（配置 FINNHUB_API_KEY 后自动拉取）</p>';
  }
  return `<ul class="news-list news-list--compact">${news
    .map(
      (item) => `
      <li class="news-item news-item--compact">
        <div>
          <p class="news-item__title">
            ${item.link ? `<a href="${item.link}" target="_blank" rel="noopener noreferrer">${item.title}</a>` : item.title}
          </p>
          ${item.summary ? `<p class="news-item__summary">${item.summary}</p>` : ""}
          <p class="news-item__meta">
            <span class="news-source news-source--finnhub">${item.source || "Finnhub"}</span>
            ${item.category ? ` · ${item.category}` : ""}${item.related ? ` · ${item.related}` : ""}
          </p>
        </div>
        <span class="news-item__time">${formatDateTime(item.publishedAt)}</span>
      </li>
    `
    )
    .join("")}</ul>`;
}

function renderCockpitMacro(data) {
  const grid = document.getElementById("cockpit-macro-grid");
  const hintsEl = document.getElementById("cockpit-macro-hints");
  const hint = document.getElementById("cockpit-macro-hint");
  if (!grid) return;

  if (!data) {
    grid.innerHTML = '<p class="empty">宏观数据加载中…</p>';
    return;
  }

  const s = data.summary || {};
  if (hint) {
    const parts = [];
    if (s.vix != null) parts.push(`VIX ${formatNumber(s.vix, 1)}`);
    if (s.us10yYield != null) parts.push(`10Y ${formatNumber(s.us10yYield, 2)}%`);
    if (s.yieldSpread10y2y != null) parts.push(`10Y-2Y ${formatNumber(s.yieldSpread10y2y, 2)}%`);
    if (s.usdCnh != null) parts.push(`USDCNH ${formatNumber(s.usdCnh, 4)}`);
    hint.textContent = parts.length ? parts.join(" · ") : "VIX · 利率 · 汇率 · 商品 · 美股行业";
  }

  const vix = (data.risk || []).find((r) => r.symbol === "^VIX");
  const tnx = (data.rates || []).find((r) => r.symbol === "^TNX");
  const cnh = (data.fx || []).find((f) => f.symbol?.includes("CNH") || f.quote === "CNH");
  const gold = (data.commodities || []).find((c) => c.symbol === "GC=F");
  const oil = (data.commodities || []).find((c) => c.symbol === "CL=F");
  const topSector = (data.sectors || [])[0];

  const cards = [
    vix && { label: "VIX", value: formatNumber(vix.price, 1), chg: vix.changePct, hint: s.vixRegime === "high" ? "偏高" : s.vixRegime === "low" ? "偏低" : "正常" },
    tnx && { label: "美10Y", value: `${formatNumber(tnx.price, 2)}%`, chg: tnx.changePct, hint: "国债收益率" },
    cnh && { label: "USDCNH", value: formatNumber(cnh.price, 4), chg: cnh.changePct, hint: cnh.refSource || "汇率" },
    gold && { label: "黄金", value: formatMacroPrice(gold), chg: gold.changePct, hint: "GC=F" },
    oil && { label: "原油", value: formatMacroPrice(oil), chg: oil.changePct, hint: "WTI" },
    topSector && { label: `美股${topSector.sector}`, value: formatNumber(topSector.price), chg: topSector.changePct, hint: "行业ETF" },
  ].filter(Boolean);

  grid.innerHTML = cards
    .map(
      (c) => `
    <article class="macro-mini">
      <p class="macro-mini__label">${c.label}</p>
      <p class="macro-mini__value">${c.value}</p>
      <p class="macro-mini__chg change ${changeClass(c.chg)}">${formatPct(c.chg)}</p>
      <p class="macro-mini__hint">${c.hint}</p>
    </article>
  `
    )
    .join("");

  if (hintsEl) {
    const hints = s.hints || [];
    hintsEl.innerHTML = hints.length
      ? hints.map((h) => `<li>${h}</li>`).join("")
      : "";
    hintsEl.hidden = !hints.length;
  }
}

function renderMacroTable(title, subtitle, rows, columns) {
  if (!rows?.length) return "";
  const head = columns.map((c) => `<th>${c.label}</th>`).join("");
  const body = rows
    .map(
      (row) => `
    <tr>
      ${columns
        .map((c) => {
          const val = c.render ? c.render(row) : row[c.key];
          return `<td${c.class ? ` class="${c.class(row)}"` : ""}>${val ?? "--"}</td>`;
        })
        .join("")}
    </tr>
  `
    )
    .join("");
  return `
    <section class="macro-block">
      <div class="panel__head">
        <h3>${title}</h3>
        <p>${subtitle}</p>
      </div>
      <div class="table-wrap">
        <table class="data-table macro-table">
          <thead><tr>${head}</tr></thead>
          <tbody>${body}</tbody>
        </table>
      </div>
    </section>
  `;
}

function renderMarketMacro(data) {
  const el = document.getElementById("market-macro");
  if (!el) return;
  if (!data) {
    el.innerHTML = '<p class="empty">宏观数据加载中…</p>';
    return;
  }

  const sources = (data.sources || []).map((s) => `${s.name}(${s.status})`).join(" · ");

  el.innerHTML = `
    <div class="panel__head panel__head--row">
      <div>
        <h2>宏观与跨资产</h2>
        <p>更新 ${formatDateTime(data.updatedAt)} · ${sources}</p>
      </div>
    </div>
    <div class="macro-sections">
      ${renderMacroTable("风险与利率", "VIX · 美债收益率", [...(data.risk || []), ...(data.rates || [])], [
        { label: "指标", render: (r) => `<strong>${r.name}</strong>` },
        { label: "最新", render: (r) => formatMacroPrice(r) },
        { label: "日涨跌", render: (r) => `<span class="change ${changeClass(r.changePct)}">${formatPct(r.changePct)}</span>` },
        { label: "周涨跌", render: (r) => `<span class="change ${changeClass(r.weekChangePct)}">${formatPct(r.weekChangePct)}</span>` },
        { label: "来源", key: "source" },
      ])}
      ${renderMacroTable("汇率", "Yahoo 涨跌 + ECB/备用参考价", data.fx || [], [
        { label: "货币对", render: (r) => `<strong>${r.name}</strong>` },
        { label: "现价", render: (r) => formatNumber(r.price, 4) },
        { label: "日涨跌", render: (r) => `<span class="change ${changeClass(r.changePct)}">${formatPct(r.changePct)}</span>` },
        { label: "参考价", render: (r) => (r.refPrice != null ? formatNumber(r.refPrice, 4) : "—") },
        { label: "来源", render: (r) => r.refSource || r.source || "—" },
      ])}
      ${renderMacroTable("商品", "黄金 · 原油 · 铜", data.commodities || [], [
        { label: "品种", render: (r) => `<strong>${r.name}</strong>` },
        { label: "最新", render: (r) => formatMacroPrice(r) },
        { label: "日涨跌", render: (r) => `<span class="change ${changeClass(r.changePct)}">${formatPct(r.changePct)}</span>` },
        { label: "月涨跌", render: (r) => `<span class="change ${changeClass(r.monthChangePct)}">${formatPct(r.monthChangePct)}</span>` },
      ])}
      ${renderMacroTable("A股宽基", "沪深300 · 创业板 · 科创50", data.extraIndices || [], [
        { label: "指数", render: (r) => `<strong>${r.name}</strong>` },
        { label: "最新", render: (r) => formatNumber(r.price) },
        { label: "日涨跌", render: (r) => `<span class="change ${changeClass(r.changePct)}">${formatPct(r.changePct)}</span>` },
        { label: "月涨跌", render: (r) => `<span class="change ${changeClass(r.monthChangePct)}">${formatPct(r.monthChangePct)}</span>` },
      ])}
      ${renderMacroTable("美股行业 ETF", "SPDR 行业轮动（日涨跌排序）", data.sectors || [], [
        { label: "行业", render: (r) => `<strong>${r.sector}</strong> <span class="stock-card__symbol">${r.symbol}</span>` },
        { label: "价格", render: (r) => formatNumber(r.price) },
        { label: "日涨跌", render: (r) => `<span class="change ${changeClass(r.changePct)}">${formatPct(r.changePct)}</span>` },
        { label: "周涨跌", render: (r) => `<span class="change ${changeClass(r.weekChangePct)}">${formatPct(r.weekChangePct)}</span>` },
      ])}
      ${renderMacroTable("FRED 官方宏观", "圣路易斯联储 · 需 FRED_API_KEY", data.fred || [], [
        { label: "序列", render: (r) => `<strong>${r.name}</strong> <span class="stock-card__symbol">${r.seriesId}</span>` },
        { label: "最新", render: (r) => formatFredValue(r) },
        { label: "变动", render: (r) => `<span class="change ${changeClass(r.changePct)}">${formatPct(r.changePct)}</span>` },
        { label: "观测日", render: (r) => r.observedAt || "—" },
        { label: "来源", key: "source" },
      ])}
      <section class="macro-block">
        <div class="panel__head">
          <h3>Finnhub 宏观资讯</h3>
          <p>全球市场 · 外汇 · 免费层 API</p>
        </div>
        ${renderMacroNewsList(data.finnhubNews)}
      </section>
      ${renderMacroTable("财报日历（关注标的）", "AAPL · NVDA · 小米 · 腾讯 · 中芯", data.earningsCalendar || [], [
        { label: "代码", render: (r) => `<strong>${r.symbol || "—"}</strong>` },
        { label: "日期", render: (r) => r.date || "—" },
        { label: "时段", render: (r) => r.hour || "—" },
        { label: "EPS 预期", render: (r) => (r.epsEstimate != null ? formatNumber(r.epsEstimate, 2) : "—") },
        { label: "营收预期", render: (r) => (r.revenueEstimate != null ? formatNumber(r.revenueEstimate, 0) : "—") },
      ])}
    </div>
  `;
}

async function refreshMacroData() {
  const data = await fetchJson(MACRO_URL);
  if (!data) return;
  macroData = data;
  renderCockpitMacro(data);
  if (activeTab === "market") renderMarketMacro(data);
}

function renderCockpitMood(summary) {
  const el = document.getElementById("cockpit-mood");
  if (!el) return;
  const moodClass = summary.mood === "偏多" ? "up" : summary.mood === "偏空" ? "down" : "flat";
  el.innerHTML = `
    <div class="mood-gauge mood-gauge--${moodClass}">
      <p class="mood-gauge__label">市场情绪</p>
      <p class="mood-gauge__value">${summary.mood}</p>
      <p class="mood-gauge__hint">平均涨跌 ${formatPct(summary.avgChangePct)} · ${summary.up}涨 ${summary.down}跌</p>
    </div>
  `;
  document.getElementById("market-mood").textContent = `市场情绪：${summary.mood}`;
}

function renderCockpitMarkets(radar) {
  const el = document.getElementById("cockpit-markets");
  if (!el || !radar?.length) {
    if (el) el.innerHTML = '<p class="empty">市场雷达加载中…</p>';
    return;
  }
  el.innerHTML = radar
    .map(
      (m) => `
      <article class="market-radar market-radar--${m.status}">
        <span class="reco-market reco-market--${marketClass(m.market)}">${m.market}</span>
        <p class="market-radar__label">${m.label}</p>
        <p class="market-radar__chg change ${changeClass(m.changePct)}">${formatPct(m.changePct)}</p>
        <p class="market-radar__hint">${m.indices.join(" · ")}</p>
      </article>
    `
    )
    .join("");
}

function pickRiskLine(pick) {
  if (!pick) return "";
  const parts = [];
  if (pick.distToStopPct != null) parts.push(`止损缓冲 ${formatNumber(pick.distToStopPct)}%`);
  else if (pick.stopLossPrice != null) parts.push(`止损 ${formatNumber(pick.stopLossPrice)}`);
  if (pick.distToTargetPct != null) parts.push(`目标 +${formatNumber(pick.distToTargetPct)}%`);
  if (pick.breakout === true) parts.push("已突破");
  else if (pick.breakout === false) parts.push("待突破");
  if (pick.regimeOk === false) parts.push("趋势过滤未过");
  if (pick.relativeStrength != null) parts.push(`RS ${formatPct(pick.relativeStrength)}`);
  return parts.join(" · ");
}

function buildActionQueue() {
  const items = [];
  const openSymbols = new Set(
    (signalsData?.signals || []).filter((s) => s.status === "open").map((s) => s.symbol)
  );

  if (paperData) {
    const stage = analyzePaperStage(paperData);
    const triggers = computeNextTriggers(paperData);
    const plan = diagnosticsData?.xrpsActionPlan;
    const ms = paperData.monthlyState || plan?.monthly || {};

    items.push({
      priority: 2,
      system: "战役",
      title: stage.title,
      detail: stage.desc,
      type: stage.stage === "accumulate" ? "accumulate" : "hold",
    });

    const nextSell = triggers.sells[0] || plan?.nextSell;
    if (nextSell?.triggerPrice) {
      items.push({
        priority: 3,
        system: "战役",
        title: `滚动卖出 · ${nextSell.label}`,
        detail: `现价 ${formatNumber(triggers.price || plan?.price)} → 触发 ${formatNumber(nextSell.triggerPrice)}（还差 ${formatPct(nextSell.gapPct)}）`,
        type: "sell-watch",
      });
    }

    const nextBuy = triggers.buys[0] || plan?.nextBuy;
    if (nextBuy?.triggerPrice) {
      items.push({
        priority: 3,
        system: "战役",
        title: `回撤买回 · ${nextBuy.label}`,
        detail: `跌至 ${formatNumber(nextBuy.triggerPrice)} 触发网格买回（距现价 ${formatPct(nextBuy.gapPct)}）`,
        type: "buy-watch",
      });
    }

    if ((ms.consecutiveDownMonths || 0) >= 5) {
      items.push({
        priority: 2,
        system: "战役",
        title: `${ms.consecutiveDownMonths} 连阴月`,
        detail: `上月 ${formatPct(ms.lastMonthReturnPct)} · 按 XRPS 规则积累核心仓股数，勿因净值波动恐慌减仓`,
        type: "accumulate",
      });
    }
  }

  (signalsData?.signals || [])
    .filter((s) => s.status === "open")
    .forEach((sig) => {
      const distStop = sig.distToStopPct;
      const urgent = distStop != null && distStop < 5;
      items.push({
        priority: urgent ? 1 : 4,
        system: "战术",
        title: `${sig.name} · 持仓跟踪`,
        detail: `浮盈 ${formatPct(sig.returnPct)} · 距止损 ${distStop != null ? formatNumber(distStop) + "%" : "--"} · 距目标 ${sig.distToTargetPct != null ? "+" + sig.distToTargetPct + "%" : "--"} · ${sig.holdDays ?? 0} 天`,
        type: urgent ? "alert" : "hold",
      });
    });

  (marketData?.recommendations?.picks || []).forEach((pick) => {
    if (pick.signal !== "buy") return;
    if (openSymbols.has(pick.symbol)) return;
    items.push({
      priority: 5,
      system: "战术",
      title: `关注新信号 · ${pick.name}`,
      detail: `${pick.market} · 评分 ${pick.score} · ${pickRiskLine(pick)}`,
      type: "buy",
    });
  });

  const mood = marketData?.summary?.mood;
  if (mood === "偏空") {
    items.push({
      priority: 6,
      system: "市场",
      title: "整体偏空",
      detail: "战术新开仓宜轻仓或观望；战役仓按网格纪律执行，勿情绪化清仓",
      type: "caution",
    });
  } else if (mood === "偏多") {
    const weakMarkets = (marketData?.marketRadar || []).filter((r) => r.status === "weak").map((r) => r.market);
    if (weakMarkets.length) {
      items.push({
        priority: 6,
        system: "市场",
        title: "结构分化",
        detail: `${weakMarkets.join("、")}仍偏弱，注意分散配置与止损纪律`,
        type: "caution",
      });
    }
  }

  if (!items.length) {
    items.push({
      priority: 9,
      system: "系统",
      title: "空仓等待",
      detail: "当前无突破买入信号且无紧急触发，观察即是操作",
      type: "hold",
    });
  }

  return items.sort((a, b) => a.priority - b.priority);
}

function renderActionList(items) {
  const el = document.getElementById("action-list");
  if (!el) return;
  el.innerHTML = items
    .map(
      (item) => `
    <li class="action-item action-item--${item.type}">
      <span class="action-item__system">${item.system}</span>
      <div class="action-item__main">
        <strong>${item.title}</strong>
        <p>${item.detail}</p>
      </div>
    </li>
  `
    )
    .join("");
}

function renderDecisionBrief() {
  const body = document.getElementById("decision-brief-body");
  if (!body) return;

  const parts = [];
  const mood = marketData?.summary?.mood || "—";
  const wencaiMood = wencaiData?.sentiment?.mood;
  const limitUp = wencaiData?.sentiment?.limitUp;
  parts.push(
    `全球指数情绪 <strong>${mood}</strong>${wencaiMood ? `，A股问财 <strong>${wencaiMood}</strong>` : ""}${limitUp != null ? `（涨停 ${limitUp} 家）` : ""}。`
  );

  const radar = marketData?.marketRadar || [];
  const weak = radar.filter((r) => r.status === "weak").map((r) => r.market);
  const strong = radar.filter((r) => r.status === "strong").map((r) => r.market);
  if (strong.length) parts.push(`<strong>${strong.join("、")}</strong> 偏强，可多关注趋势突破。`);
  if (weak.length) parts.push(`<strong>${weak.join("、")}</strong> 偏弱，战术新开仓需更谨慎。`);

  const scan = marketData?.recommendations?.marketScan;
  if (scan) parts.push(`扫描：${scan}。`);

  if (paperData) {
    const stage = analyzePaperStage(paperData);
    parts.push(`战役仓 <strong>${stage.title}</strong>：${stage.desc}`);
  }

  const openCount = signalsData?.openCount || 0;
  const buyPicks = (marketData?.recommendations?.picks || []).filter((p) => p.signal === "buy");
  if (openCount) {
    parts.push(`战术实验 <strong>${openCount}</strong> 笔持仓跟踪中，请严守止损。`);
  } else if (!buyPicks.length) {
    parts.push(`战术 v1.3 暂无突破买入，<strong>空仓等待</strong> 亦是正确操作。`);
  }

  body.innerHTML = `<p class="decision-brief__text">${parts.join(" ")}</p>`;
  renderActionList(buildActionQueue());
  renderCockpitTacticalOpen(signalsData);
}

function renderCockpitTacticalOpen(data) {
  const panel = document.getElementById("cockpit-tactical-open");
  const tbody = document.querySelector("#cockpit-tactical-open-table tbody");
  if (!panel || !tbody) return;

  const open = (data?.signals || []).filter((s) => s.status === "open");
  if (!open.length) {
    panel.hidden = true;
    return;
  }

  panel.hidden = false;
  const hint = document.getElementById("cockpit-tactical-open-hint");
  if (hint) hint.textContent = `${open.length} 笔 open 信号 · 实验策略，非战役仓`;

  tbody.innerHTML = open
    .map((sig) => {
      const distStop = sig.distToStopPct;
      const stopClass = distStop != null && distStop < 5 ? "change--warn" : "";
      return `
      <tr>
        <td><strong>${sig.name}</strong><br><span class="stock-card__symbol">${sig.symbol}</span></td>
        <td class="change ${changeClass(sig.returnPct)}">${formatPct(sig.returnPct)}</td>
        <td class="change ${stopClass}">${distStop != null ? formatNumber(distStop) + "%" : "--"}</td>
        <td>${sig.distToTargetPct != null ? "+" + sig.distToTargetPct + "%" : "--"}</td>
        <td>${sig.holdDays ?? 0} 天</td>
      </tr>
    `;
    })
    .join("");
}

function renderCandidateScan(scan) {
  const wrap = document.getElementById("candidate-scan-wrap");
  const summary = document.getElementById("candidate-scan-summary");
  const tbody = document.querySelector("#candidate-scan-table tbody");
  if (!tbody) return;

  const rows = scan || [];
  if (summary) {
    summary.textContent = rows.length
      ? `全市场评分扫描（${rows.length} 只候选，按分数排序）`
      : "全市场评分扫描";
  }
  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="8" class="empty">暂无扫描数据</td></tr>';
    if (wrap) wrap.hidden = true;
    return;
  }
  if (wrap) wrap.hidden = false;

  tbody.innerHTML = rows
    .map(
      (row) => `
    <tr>
      <td><strong>${row.name}</strong><br><span class="stock-card__symbol">${row.symbol}</span></td>
      <td><span class="reco-market reco-market--${marketClass(row.market)}">${row.market}</span></td>
      <td>${row.score}</td>
      <td><span class="signal-${row.signal}">${row.signalLabel || row.signal}</span></td>
      <td>${row.rsi != null ? formatNumber(row.rsi, 1) : "--"}</td>
      <td>${row.relativeStrength != null ? formatPct(row.relativeStrength) : "--"}</td>
      <td>${row.breakout ? "是" : row.breakout === false ? "否" : "--"}</td>
      <td>${row.distToStopPct != null ? formatNumber(row.distToStopPct) + "%" : "--"}</td>
    </tr>
  `
    )
    .join("");
}

function renderPaperMonthlyDashboard(paper, diag) {
  if (!paper) return;
  const ms = paper.monthlyState || diag?.xrpsActionPlan?.monthly || {};
  renderStatCards("paper-monthly-stats", [
    {
      label: "连阴月数",
      value: ms.consecutiveDownMonths ?? "--",
      hint: (ms.consecutiveDownMonths || 0) >= 5 ? "核心仓加仓区间" : "正常跟踪",
    },
    {
      label: "上月涨跌",
      value: formatPct(ms.lastMonthReturnPct),
      valueClass: changeClass(ms.lastMonthReturnPct),
    },
    {
      label: "近两月累计",
      value: formatPct(ms.twoMonthReturnPct),
      valueClass: changeClass(ms.twoMonthReturnPct),
    },
    {
      label: "近三月累计",
      value: formatPct(ms.threeMonthReturnPct),
      valueClass: changeClass(ms.threeMonthReturnPct),
    },
  ]);

  const list = document.getElementById("paper-diagnostics-suggestions");
  if (!list) return;
  const suggestions = diag?.suggestions || [];
  list.innerHTML = suggestions.length
    ? suggestions.map((s) => `<li class="diagnostics-item">${s}</li>`).join("")
    : '<li class="diagnostics-item">XRPS 运行正常，按网格与月线纪律执行。</li>';
}

function renderPickCard(pick, compact = false) {
  const riskLine = pickRiskLine(pick);
  const riskHtml = riskLine
    ? `<p class="reco-card__risk${pick.distToStopPct != null && pick.distToStopPct < 8 ? " reco-card__risk--alert" : ""}">${riskLine}</p>`
    : "";
  const reasons = compact ? "" : `<ul class="reco-reasons">${pick.reasons.map((r) => `<li>${r}</li>`).join("")}</ul>`;
  const plan = compact
    ? ""
    : `<dl class="reco-plan">
        <div><dt>买入</dt><dd>${pick.plan.entry}</dd></div>
        <div><dt>止损</dt><dd>${pick.plan.stopLoss}</dd></div>
        <div><dt>止盈</dt><dd>${pick.plan.target}</dd></div>
        <div><dt>仓位</dt><dd>${pick.plan.position}</dd></div>
      </dl>`;
  return `
    <article class="reco-card reco-card--${pick.signal}${compact ? " reco-card--compact" : ""}">
      <div class="reco-card__top">
        <div>
          <div class="reco-card__tags">
            <span class="reco-market reco-market--${marketClass(pick.market)}">${pick.market}</span>
          </div>
          <h3>${pick.name}</h3>
          <p class="stock-card__symbol">${pick.symbol} · ${pick.sector || ""}</p>
        </div>
        <div class="reco-card__badge-box">
          <span class="reco-badge reco-badge--${pick.signal}">${pick.signalLabel}</span>
          <span class="reco-score">评分 ${pick.score}</span>
        </div>
      </div>
      <p class="stock-card__price">${formatNumber(pick.price)} <span>${pick.currency || ""}</span></p>
      ${riskHtml}
      ${reasons}
      ${plan}
    </article>
  `;
}

function formatMasterMetric(key, val) {
  if (val == null || val === "") return null;
  if (key === "pe" || key === "pb" || key === "peg") return formatNumber(val, 2);
  if (key === "roe" || key === "profitMargins" || key === "earningsGrowth") return `${formatNumber(val, 1)}%`;
  if (key === "monthChangePct" || key === "relativeStrength") return formatPct(val);
  if (key === "rangePosition") return `${Math.round(val * 100)}%`;
  if (key === "marketCapB") return `${formatNumber(val, 1)}B`;
  if (key === "bottleneckLayer") return String(val);
  return String(val);
}

function renderMasterPickCard(pick) {
  const metrics = pick.metrics || {};
  const metricLabels = {
    pe: "PE",
    pb: "PB",
    roe: "ROE",
    peg: "PEG",
    earningsGrowth: "盈利增速",
    profitMargins: "净利率",
    monthChangePct: "近一月",
    relativeStrength: "相对强度",
    rangePosition: "52周区间",
    marketCapB: "市值",
    bottleneckLayer: "瓶颈环节",
  };
  const metricHtml = Object.entries(metricLabels)
    .map(([key, label]) => {
      const val = formatMasterMetric(key, metrics[key]);
      return val != null ? `<span class="master-metric"><em>${label}</em> ${val}</span>` : "";
    })
    .filter(Boolean)
    .join("");

  return `
    <article class="master-pick reco-card reco-card--${pick.signal}">
      <div class="reco-card__top">
        <div>
          <div class="reco-card__tags">
            <span class="reco-market reco-market--${marketClass(pick.market)}">${pick.market}</span>
          </div>
          <h4>${pick.name}</h4>
          <p class="stock-card__symbol">${pick.symbol} · ${pick.sector || ""}</p>
        </div>
        <div class="reco-card__badge-box">
          <span class="reco-badge reco-badge--${pick.signal}">${pick.signalLabel}</span>
          <span class="reco-score">匹配 ${pick.matchScore}</span>
        </div>
      </div>
      <p class="stock-card__price">${formatNumber(pick.price)} <span>${pick.currency || ""}</span></p>
      ${metricHtml ? `<div class="master-metrics">${metricHtml}</div>` : ""}
      <ul class="reco-reasons">${(pick.reasons || []).map((r) => `<li>${r}</li>`).join("")}</ul>
      <dl class="reco-plan reco-plan--master">
        <div><dt>买入</dt><dd>${pick.plan?.entry || "—"}</dd></div>
        <div><dt>持有</dt><dd>${pick.plan?.holding || "—"}</dd></div>
        <div><dt>风控</dt><dd>${pick.plan?.risk || "—"}</dd></div>
        <div><dt>仓位</dt><dd>${pick.plan?.position || "—"}</dd></div>
      </dl>
    </article>
  `;
}

function renderMasterRecommendations(data) {
  const grid = document.getElementById("master-reco-grid");
  const strategyEl = document.getElementById("master-reco-strategy");
  const disclaimerEl = document.getElementById("master-reco-disclaimer");
  if (!grid) return;

  if (!data?.masters?.length) {
    grid.innerHTML = '<p class="empty">大师风格荐股数据加载中…</p>';
    return;
  }

  if (strategyEl && data.strategy) strategyEl.textContent = data.strategy;
  if (disclaimerEl) disclaimerEl.textContent = data.disclaimer || "";

  grid.innerHTML = data.masters
    .map((master) => {
      const picksHtml = master.picks?.length
        ? master.picks.map((p) => renderMasterPickCard(p)).join("")
        : '<p class="empty master-empty">当前候选池暂无符合该风格的标的</p>';
      return `
        <article class="master-card${master.id === "serenity" ? " master-card--serenity" : ""}" id="master-${master.id}">
          <header class="master-card__head">
            <div>
              <p class="master-card__style">${master.style}</p>
              <h3>${master.name}</h3>
              <p class="master-card__en">${master.nameEn || ""} · 持有 ${master.holdingHorizon || "—"}${master.xHandle ? ` · <a href="https://x.com/${master.xHandle.replace("@", "")}" target="_blank" rel="noopener noreferrer">${master.xHandle}</a>` : ""}</p>
            </div>
          </header>
          ${master.sourceNote ? `<p class="master-card__source-note">${master.sourceNote}</p>` : ""}
          <p class="master-card__philosophy">${master.philosophy || ""}</p>
          <ul class="master-principles">${(master.principles || []).map((p) => `<li>${p}</li>`).join("")}</ul>
          <div class="master-picks">${picksHtml}</div>
        </article>
      `;
    })
    .join("");
}

function switchRecoMode(mode) {
  recoMode = mode;
  document.querySelectorAll(".reco-mode-btn").forEach((btn) => {
    const active = btn.dataset.recoMode === mode;
    btn.classList.toggle("reco-mode-btn--active", active);
    btn.setAttribute("aria-selected", active ? "true" : "false");
  });
  const tactical = document.getElementById("reco-tactical-panel");
  const masters = document.getElementById("reco-masters-panel");
  const scan = document.getElementById("reco-scan-panel");
  if (tactical) tactical.hidden = mode !== "tactical";
  if (masters) masters.hidden = mode !== "masters";
  if (scan) scan.hidden = mode !== "tactical";
}

function renderRecommendations(reco, containerId = "reco-cards", compact = false) {
  const container = document.getElementById(containerId);
  const strategyEl = document.getElementById("reco-strategy");
  const disclaimerEl = document.getElementById("reco-disclaimer");
  if (!container) return;

  if (!reco?.picks?.length) {
    container.innerHTML = '<p class="empty">当前没有满足策略条件的标的，空仓等待也是一种操作。</p>';
    if (disclaimerEl && reco?.disclaimer) disclaimerEl.textContent = reco.disclaimer;
    if (compact) {
      const hint = document.getElementById("cockpit-reco-hint");
      if (hint) hint.textContent = reco?.marketScan || "暂无突破买入信号";
    }
    if (!compact) renderCandidateScan(reco?.candidateScan);
    return;
  }

  if (compact) {
    const hint = document.getElementById("cockpit-reco-hint");
    if (hint) hint.textContent = reco.marketScan || "A股 / 港股 / 美股 各 1 只";
  }

  if (!compact) {
    if (strategyEl && reco.strategy) {
      strategyEl.textContent = `${reco.strategy} · 实验策略，非 XRPS 战役持仓`;
    }
    if (disclaimerEl) {
      disclaimerEl.textContent =
        reco.disclaimer ||
        "战术荐股为实验室实验策略，仅供观察；小米 XRPS 模拟盘见「战役持仓」。";
    }
  }

  const scanHtml = !compact && reco.marketScan ? `<p class="reco-scan">${reco.marketScan}</p>` : "";
  container.innerHTML = scanHtml + reco.picks.map((p) => renderPickCard(p, compact)).join("");
  if (!compact) renderCandidateScan(reco.candidateScan);
}

function renderCockpitIndices(indices) {
  const el = document.getElementById("cockpit-indices");
  if (!el) return;
  el.innerHTML = indices
    .slice(0, 6)
    .map(
      (item) => `
      <article class="index-mini">
        <p class="index-mini__name">${item.name}</p>
        <p class="index-mini__price">${formatNumber(item.price)}</p>
        <p class="change ${changeClass(item.changePct)}">${formatPct(item.changePct)}</p>
      </article>
    `
    )
    .join("");
}

function newsSourceLabel(source) {
  if (source === "wencai") return "问财";
  if (source === "yahoo") return "Yahoo";
  return "资讯";
}

function mergeNews(yahoo = [], wencai = []) {
  const tagged = [
    ...yahoo.map((item) => ({ ...item, source: item.source || "yahoo" })),
    ...wencai.map((item) => ({ ...item, source: item.source || "wencai" })),
  ];
  const seen = new Set();
  const unique = [];
  tagged.forEach((item) => {
    const key = item.id || `${item.source}:${item.title}:${item.link || ""}`;
    if (seen.has(key)) return;
    seen.add(key);
    unique.push(item);
  });
  return unique.sort((a, b) => (b.publishedAt || "").localeCompare(a.publishedAt || ""));
}

function getFilteredNews() {
  const merged = mergeNews(yahooNews, wencaiData?.news || []);
  if (newsFilter === "all") return merged;
  return merged.filter((item) => item.source === newsFilter);
}

function renderMergedNews() {
  renderNews(getFilteredNews());
}

async function ensureTabData(tabId) {
  if (tabId === "paper" && !tabBundles.paper) {
    tabBundles.paper = true;
    await Promise.all([refreshPaperExtras(), refreshHistory()]);
    if (activeTab === "paper") {
      if (paperStrategyData) renderPaperStrategyCard(paperStrategyData);
      if (paperBacktestData) renderPaperBacktestCards(paperBacktestData);
      renderPaperPanel(paperData);
    }
  }
  if (tabId === "ai" && !tabBundles.ai) {
    tabBundles.ai = true;
    await loadAiChainData();
  }
  if (tabId === "reports" && !tabBundles.reports) {
    tabBundles.reports = true;
    await loadReportsIndex();
  }
}

function renderSummary(summary) {
  const container = document.getElementById("summary-cards");
  if (!container) return;
  const cards = [
    { label: "跟踪指数", value: summary.tracked, hint: "全球主要市场" },
    { label: "上涨", value: summary.up, hint: "当日收涨指数" },
    { label: "下跌", value: summary.down, hint: "当日收跌指数" },
    { label: "平均涨跌", value: formatPct(summary.avgChangePct), hint: `市场情绪：${summary.mood}` },
  ];
  container.innerHTML = cards
    .map(
      (card) => `
      <article class="summary-card">
        <p class="summary-card__label">${card.label}</p>
        <p class="summary-card__value">${card.value}</p>
        <p class="summary-card__hint">${card.hint}</p>
      </article>
    `
    )
    .join("");
}

function drawSparkline(canvas, values) {
  if (!canvas || !values || values.length < 2) return;
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const up = values[values.length - 1] >= values[0];
  ctx.clearRect(0, 0, width, height);
  ctx.strokeStyle = up ? "#f87171" : "#34d399";
  ctx.lineWidth = 2;
  ctx.beginPath();
  values.forEach((value, index) => {
    const x = (index / (values.length - 1)) * (width - 8) + 4;
    const y = height - 4 - ((value - min) / range) * (height - 8);
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
}

function renderIndices(indices) {
  const tbody = document.querySelector("#indices-table tbody");
  if (!tbody) return;
  tbody.innerHTML = indices
    .map((item, index) => {
      const canvasId = `spark-${index}`;
      return `
        <tr>
          <td><strong>${item.name}</strong><br><span class="stock-card__symbol">${item.symbol}</span></td>
          <td>${item.region || "--"}</td>
          <td>${formatNumber(item.price)} ${item.currency || ""}</td>
          <td class="change ${changeClass(item.changePct)}">${formatPct(item.changePct)}</td>
          <td class="change ${changeClass(item.weekChangePct)}">${formatPct(item.weekChangePct)}</td>
          <td class="change ${changeClass(item.monthChangePct)}">${formatPct(item.monthChangePct)}</td>
          <td><canvas id="${canvasId}" class="sparkline" width="110" height="34" aria-hidden="true"></canvas></td>
        </tr>
      `;
    })
    .join("");
  indices.forEach((item, index) => {
    drawSparkline(document.getElementById(`spark-${index}`), item.sparkline);
  });
}

function renderStocks(stocks) {
  const container = document.getElementById("stock-cards");
  if (!container) return;
  container.innerHTML = stocks
    .map(
      (stock) => `
      <article class="stock-card">
        <div class="stock-card__top">
          <div>
            <h3>${stock.name}</h3>
            <p class="stock-card__symbol">${stock.symbol} · ${stock.sector || ""}</p>
          </div>
          <span class="change ${changeClass(stock.changePct)}">${formatPct(stock.changePct)}</span>
        </div>
        <p class="stock-card__price">${formatNumber(stock.price)} <span>${stock.currency || ""}</span></p>
        <div class="stock-card__meta">
          <span>日涨跌 ${formatNumber(stock.change)}</span>
          <span>周涨跌 ${formatPct(stock.weekChangePct)}</span>
          <span>月涨跌 ${formatPct(stock.monthChangePct)}</span>
        </div>
      </article>
    `
    )
    .join("");
}

function renderNews(news) {
  const list = document.getElementById("news-list");
  if (!list) return;
  if (!news.length) {
    list.innerHTML = '<li class="empty">暂无资讯数据</li>';
    return;
  }
  list.innerHTML = news
    .map(
      (item) => `
      <li class="news-item">
        <div>
          <p class="news-item__title">
            ${item.link ? `<a href="${item.link}" target="_blank" rel="noopener noreferrer">${item.title}</a>` : item.title}
          </p>
          ${item.summary ? `<p class="news-item__summary">${item.summary}</p>` : ""}
          <p class="news-item__meta">
            <span class="news-source news-source--${item.source || "yahoo"}">${newsSourceLabel(item.source)}</span>
            ${item.publisher || ""} · ${item.related || ""}${item.category ? ` · ${item.category}` : ""}
          </p>
        </div>
        <span class="news-item__time">${formatDateTime(item.publishedAt)}</span>
      </li>
    `
    )
    .join("");
}

function buildReviewStats(history, prices) {
  const picks = [];
  (history?.records || []).forEach((record) => {
    record.picks.forEach((pick) => {
      picks.push({ ...pick, recordedAt: record.recordedAt });
    });
  });
  let wins = 0;
  let tracked = 0;
  let sumReturn = 0;
  picks.forEach((pick) => {
    const current = prices[pick.symbol];
    const ret = calcReturn(pick.price, current);
    if (ret === null) return;
    tracked += 1;
    if (ret > 0) wins += 1;
    sumReturn += ret;
  });
  return {
    totalRecords: history?.records?.length || 0,
    totalPicks: picks.length,
    tracked,
    winRate: tracked ? Number(((wins / tracked) * 100).toFixed(1)) : null,
    avgReturn: tracked ? Number((sumReturn / tracked).toFixed(2)) : null,
  };
}

function renderReviewStats(stats) {
  const el = document.getElementById("review-stats");
  if (!el) return;
  el.innerHTML = `
    <article class="stat-card">
      <p class="stat-card__label">存档批次</p>
      <p class="stat-card__value">${stats.totalRecords}</p>
    </article>
    <article class="stat-card">
      <p class="stat-card__label">推荐标的次</p>
      <p class="stat-card__value">${stats.totalPicks}</p>
    </article>
    <article class="stat-card">
      <p class="stat-card__label">胜率（现价 &gt; 推荐价）</p>
      <p class="stat-card__value">${stats.winRate !== null ? `${stats.winRate}%` : "--"}</p>
      <p class="stat-card__hint">可追踪 ${stats.tracked} 只</p>
    </article>
    <article class="stat-card">
      <p class="stat-card__label">平均收益率</p>
      <p class="stat-card__value change ${changeClass(stats.avgReturn)}">${formatPct(stats.avgReturn)}</p>
      <p class="stat-card__hint">自推荐价至现价</p>
    </article>
  `;
}

function renderRecoHistory(history) {
  const container = document.getElementById("history-timeline");
  const summaryEl = document.getElementById("history-summary");
  if (!container) return;

  recoHistory = history;
  const records = history?.records || [];
  const stats = buildReviewStats(history, quoteMap);
  renderReviewStats(stats);

  if (summaryEl) {
    summaryEl.textContent = records.length
      ? `共 ${records.length} 条荐股快照 · 胜率 ${stats.winRate ?? "--"}% · 均收益 ${formatPct(stats.avgReturn)}`
      : "暂无历史记录，系统将在每次更新时自动存档";
  }

  if (!records.length) {
    container.innerHTML = '<p class="empty">暂无历史荐股记录…</p>';
    return;
  }

  const filtered = [...records]
    .reverse()
    .map((record) => {
      const picks = historyFilter === "all"
        ? record.picks
        : record.picks.filter((p) => p.market === historyFilter);
      return { ...record, picks };
    })
    .filter((record) => record.picks.length > 0)
    .slice(0, historyDisplayLimit);

  if (!filtered.length) {
    container.innerHTML = '<p class="empty">当前筛选市场下暂无记录。</p>';
    return;
  }

  const grouped = new Map();
  filtered.forEach((record) => {
    const dateKey = formatDateTime(record.recordedAt).slice(0, 10);
    if (!grouped.has(dateKey)) grouped.set(dateKey, []);
    grouped.get(dateKey).push(record);
  });

  container.innerHTML = [...grouped.entries()]
    .map(
      ([date, dayRecords]) => `
      <section class="history-day">
        <h3 class="history-day__title">${date}</h3>
        <div class="history-day__list">
          ${dayRecords
            .map((record) => `
            <article class="history-record">
              <header class="history-record__head">
                <time datetime="${record.recordedAt}">${formatDateTime(record.recordedAt).slice(11)}</time>
                <span class="history-record__count">${record.picks.length} 只标的</span>
              </header>
              <div class="history-record__picks">
                ${record.picks
                  .map((pick) => {
                    const current = quoteMap[pick.symbol];
                    const ret = calcReturn(pick.price, current);
                    const retHtml =
                      ret !== null
                        ? `<span class="history-pick__return change ${changeClass(ret)}">至今 ${formatPct(ret)}</span>`
                        : "";
                    return `
                  <details class="history-pick">
                    <summary>
                      <span class="reco-market reco-market--${marketClass(pick.market)}">${pick.market}</span>
                      <strong>${pick.name}</strong>
                      <span class="stock-card__symbol">${pick.symbol}</span>
                      <span class="reco-badge reco-badge--${pick.signal}">${pick.signalLabel}</span>
                      <span class="history-pick__meta">推荐 ${formatNumber(pick.price)} → 现价 ${formatNumber(current)}</span>
                      ${retHtml}
                    </summary>
                    <div class="history-pick__body">
                      <p class="history-pick__price">推荐价 ${formatNumber(pick.price)} ${pick.currency || ""} · 评分 ${pick.score}</p>
                      ${pick.relativeStrength != null ? `<p class="history-pick__rs">相对强弱 ${formatPct(pick.relativeStrength)}</p>` : ""}
                      <dl class="reco-plan">
                        <div><dt>买入</dt><dd>${pick.plan?.entry || "--"}</dd></div>
                        <div><dt>止损</dt><dd>${pick.plan?.stopLoss || "--"}</dd></div>
                        <div><dt>止盈</dt><dd>${pick.plan?.target || "--"}</dd></div>
                        <div><dt>仓位</dt><dd>${pick.plan?.position || "--"}</dd></div>
                      </dl>
                    </div>
                  </details>`;
                  })
                  .join("")}
              </div>
            </article>
          `)
            .join("")}
        </div>
      </section>
    `
    )
    .join("");

  const totalShown = filtered.length;
  const hasMore = records.length > historyDisplayLimit;
  if (hasMore) {
    container.insertAdjacentHTML(
      "beforeend",
      `<p class="history-load-more"><button type="button" class="link-btn" id="history-load-more-btn">加载更多（已显示 ${totalShown} / ${records.length} 条）</button></p>`
    );
    document.getElementById("history-load-more-btn")?.addEventListener("click", () => {
      historyDisplayLimit += HISTORY_DISPLAY_LIMIT;
      renderRecoHistory(history);
    }, { once: true });
  }
}

function setupHistoryFilters() {
  const filters = document.getElementById("history-filters");
  if (!filters) return;
  filters.addEventListener("click", (event) => {
    const btn = event.target.closest(".history-filter");
    if (!btn) return;
    historyFilter = btn.dataset.market || "all";
    filters.querySelectorAll(".history-filter").forEach((el) => {
      el.classList.toggle("history-filter--active", el === btn);
    });
    if (recoHistory) renderRecoHistory(recoHistory);
  });
}

function normalizeSeries(values) {
  if (!values || values.length < 2) return [];
  const base = values[0] || 1;
  return values.map((value) => Number((((value - base) / base) * 100).toFixed(2)));
}

function renderDistributionChart(summary) {
  const canvas = document.getElementById("distribution-chart");
  if (!canvas || !summary) return;
  const chartData = [summary.up, summary.down, summary.flat];
  if (distributionChart) {
    distributionChart.data.datasets[0].data = chartData;
    distributionChart.update("none");
    return;
  }
  distributionChart = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: ["上涨", "下跌", "持平"],
      datasets: [{ data: chartData, backgroundColor: ["#f87171", "#34d399", "#fbbf24"], borderWidth: 0 }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom", labels: { color: "#cbd5e1" } } },
    },
  });
}

function renderStocksChart(stocks) {
  const canvas = document.getElementById("stocks-chart");
  if (!canvas || !stocks?.length) return;
  const colors = ["#38bdf8", "#34d399", "#f472b6"];
  const labels = stocks[0]?.sparkline?.map((_, i) => `T-${stocks[0].sparkline.length - i - 1}`) || [];
  const datasets = stocks.map((stock, index) => ({
    label: stock.name,
    data: normalizeSeries(stock.sparkline),
    borderColor: colors[index % colors.length],
    backgroundColor: "transparent",
    tension: 0.3,
    pointRadius: 0,
    borderWidth: 2,
  }));
  if (stocksChart) {
    stocksChart.data.labels = labels;
    stocksChart.data.datasets = datasets;
    stocksChart.update("none");
    return;
  }
  stocksChart = new Chart(canvas, {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: "#94a3b8", maxTicksLimit: 8 }, grid: { color: "rgba(148,163,184,0.08)" } },
        y: {
          ticks: { color: "#94a3b8", callback: (v) => `${v}%` },
          grid: { color: "rgba(148,163,184,0.08)" },
        },
      },
      plugins: {
        legend: { labels: { color: "#cbd5e1" } },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y}%` } },
      },
    },
  });
}

function renderStatCards(containerId, cards) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = cards
    .map(
      (card) => `
    <article class="stat-card">
      <p class="stat-card__label">${card.label}</p>
      <p class="stat-card__value ${card.valueClass || ""}">${card.value}</p>
      ${card.hint ? `<p class="stat-card__hint">${card.hint}</p>` : ""}
    </article>
  `
    )
    .join("");
}

function filterTradesByPeriod(trades, startDate, endDate) {
  if (!trades?.length || !startDate || !endDate) return [];
  return trades.filter((t) => {
    const day = (t.time || "").slice(0, 10);
    return day >= startDate && day <= endDate;
  });
}

function renderTacticalSignals(data) {
  const tbody = document.querySelector("#tactical-signals-table tbody");
  const summaryEl = document.getElementById("tactical-signals-summary");
  if (!tbody) return;

  const signals = data?.signals || [];
  const summary = data?.summary || {};
  if (summaryEl) {
    summaryEl.textContent = signals.length
      ? `v1.3 实验策略 · 持仓 ${data.openCount ?? 0} · 已平仓 ${data.closedCount ?? 0} · 胜率 ${summary.winRate ?? "--"}%`
      : "v1.3 实验策略 · 出现 buy 信号后自动跟踪";
  }

  if (!signals.length) {
    tbody.innerHTML = '<tr><td colspan="13" class="empty">暂无战术信号，等待荐股出现 buy 信号</td></tr>';
    return;
  }

  const sorted = [...signals].sort((a, b) => (b.openedAt || "").localeCompare(a.openedAt || ""));
  tbody.innerHTML = sorted
    .map((sig) => {
      const ret = sig.returnPct;
      const hold =
        sig.status === "open" ? `${sig.holdDays ?? 0} 天` : sig.closeReason || reasonLabel(sig.closeReason) || "--";
      const distStop = sig.distToStopPct;
      const stopAlert = distStop != null && distStop < 5 ? "change--warn" : "";
      return `
      <tr>
        <td><strong>${sig.name}</strong><br><span class="stock-card__symbol">${sig.symbol}</span></td>
        <td><span class="reco-market reco-market--${marketClass(sig.market)}">${sig.market}</span></td>
        <td><span class="signal-status ${signalStatusClass(sig.status)}">${signalStatusLabel(sig.status)}</span></td>
        <td>${formatNumber(sig.entryPrice)}</td>
        <td>${formatNumber(sig.currentPrice ?? sig.exitPrice)}</td>
        <td class="change ${changeClass(ret)}">${formatPct(ret)}</td>
        <td>${formatNumber(sig.stopLossPrice)}</td>
        <td class="change ${stopAlert}">${distStop != null ? formatNumber(distStop) + "%" : "--"}</td>
        <td>${formatNumber(sig.targetPrice)}</td>
        <td>${sig.distToTargetPct != null ? "+" + sig.distToTargetPct + "%" : "--"}</td>
        <td class="change change--up">${formatPct(sig.maxGainPct)}</td>
        <td class="change change--down">${formatPct(sig.maxDrawdownPct)}</td>
        <td>${hold}</td>
      </tr>
    `;
    })
    .join("");
}

function analyzePaperStage(paper) {
  if (!paper) {
    return { stage: "loading", title: "加载中", desc: "正在读取模拟盘数据…" };
  }

  const sells = (paper.trades || []).filter((t) => t.type === "sell");
  const streak = paper.monthlyState?.consecutiveDownMonths || 0;
  const positionPct = paper.positionPct || 0;

  if (!paper.coreShares && !paper.rollingShares) {
    return {
      stage: "bootstrap",
      title: "待建仓",
      desc: "等待首次核心仓建仓信号，目标：股数优先、成本优先。",
    };
  }

  if (sells.length === 0 && streak >= 5) {
    return {
      stage: "accumulate",
      title: "建仓积累期",
      desc: `${streak} 连阴月加仓阶段：侧重积累股数与摊低成本，短期净值波动属正常。`,
    };
  }

  if (sells.length > 0 || (paper.rollingShares && paper.triggeredSellLevels?.length)) {
    return {
      stage: "rolling",
      title: "滚动做 T 期",
      desc: "滚动仓网格已激活，上涨分批卖、回撤分批买，锁定波动利润。",
    };
  }

  if (positionPct >= 75) {
    return {
      stage: "high-position",
      title: "高仓位待机",
      desc: `仓位 ${positionPct}% 接近上限，等待滚动减仓或回撤补仓触发。`,
    };
  }

  return {
    stage: "normal",
    title: "正常运行",
    desc: "核心仓保留 + 滚动网格待命，关注下一档买卖触发位。",
  };
}

function computeNextTriggers(paper) {
  if (!paper) return { sells: [], buys: [] };

  const price = quoteMap[paper.focusSymbol] || paper.lastPrice || 0;
  const peak = paper.peakPrice || price;
  const rollingCost = paper.rollingAvgCost || paper.avgCost || 0;
  const triggeredSell = new Set(paper.triggeredSellLevels || []);
  const triggeredBuy = new Set(paper.triggeredBuyLevels || []);

  const sells = XRPS_ROLLING_SELL_LEVELS.filter((lv) => !triggeredSell.has(lv.key)).map((lv) => {
    const triggerPrice = rollingCost > 0 ? rollingCost * (1 + lv.pct) : null;
    const gap =
      triggerPrice && price
        ? Number((((triggerPrice - price) / price) * 100).toFixed(1))
        : null;
    return { ...lv, triggerPrice, gapPct: gap };
  });

  const buys = XRPS_ROLLING_BUY_LEVELS.filter((lv) => !triggeredBuy.has(lv.key)).map((lv) => {
    const triggerPrice = peak > 0 ? peak * (1 + lv.pct) : null;
    const gap =
      triggerPrice && price
        ? Number((((price - triggerPrice) / price) * 100).toFixed(1))
        : null;
    return { ...lv, triggerPrice, gapPct: gap };
  });

  return { sells: sells.slice(0, 2), buys: buys.slice(0, 2), price, peak, rollingCost };
}

function renderPaperStageBanner(paper) {
  const el = document.getElementById("paper-stage-banner");
  if (!el) return;

  if (!paper) {
    el.hidden = true;
    return;
  }

  const stage = analyzePaperStage(paper);
  const triggers = computeNextTriggers(paper);
  const nextSell = triggers.sells[0];
  const nextBuy = triggers.buys[0];

  const triggerHtml = [
    nextSell?.triggerPrice
      ? `<span class="paper-stage-banner__trigger">下一卖出 <strong>${formatNumber(nextSell.triggerPrice)}</strong>（${nextSell.label}，${nextSell.gapPct > 0 ? `还需涨 ${nextSell.gapPct}%` : "已到触发区"}）</span>`
      : "",
    nextBuy?.triggerPrice
      ? `<span class="paper-stage-banner__trigger">下一买回 <strong>${formatNumber(nextBuy.triggerPrice)}</strong>（${nextBuy.label}，${nextBuy.gapPct > 0 ? `还需跌 ${nextBuy.gapPct}%` : "已到触发区"}）</span>`
      : "",
  ]
    .filter(Boolean)
    .join("");

  el.hidden = false;
  el.innerHTML = `
    <div class="paper-stage-banner__main">
      <span class="paper-stage-banner__badge paper-stage-banner__badge--${stage.stage}">${stage.title}</span>
      <p class="paper-stage-banner__desc">${stage.desc}</p>
    </div>
    ${triggerHtml ? `<div class="paper-stage-banner__triggers">${triggerHtml}</div>` : ""}
  `;
}

function renderReviewXrpsStats(paper, diagnostics) {
  const el = document.getElementById("review-xrps-stats");
  if (!el) return;

  if (!paper) {
    el.innerHTML = '<article class="stat-card"><p class="stat-card__label">XRPS-X</p><p class="stat-card__value">加载中…</p></article>';
    return;
  }

  const summary = diagnostics?.summary || {};
  const trades = paper.trades || [];
  const sells = trades.filter((t) => t.type === "sell");
  const wins = sells.filter((t) => (t.pnl || 0) > 0).length;
  const rollingWinRate = sells.length ? Number(((wins / sells.length) * 100).toFixed(1)) : null;

  renderStatCards("review-xrps-stats", [
    { label: "持股数量", value: formatNumber(paper.totalShares, 0) },
    { label: "持仓成本", value: formatNumber(paper.avgCost) },
    {
      label: "模拟收益",
      value: formatPct(paper.returnPct),
      valueClass: changeClass(paper.returnPct),
      hint: `仓位 ${paper.positionPct ?? "--"}%`,
    },
    {
      label: "回测对照",
      value: formatPct(summary.backtestReturn),
      valueClass: changeClass(summary.backtestReturn),
      hint: rollingWinRate !== null ? `滚动胜率 ${rollingWinRate}%` : "尚无滚动卖出",
    },
  ]);
}

function renderXrpsTradesLog(paper) {
  const tbody = document.querySelector("#xrps-trades-table tbody");
  const summaryEl = document.getElementById("xrps-trades-summary");
  if (!tbody) return;

  const trades = paper?.trades || [];
  if (summaryEl) {
    summaryEl.textContent = trades.length
      ? `共 ${trades.length} 笔成交 · 核心仓永不卖 · 滚动仓做 T`
      : "暂无 XRPS-X 成交记录";
  }

  if (!trades.length) {
    tbody.innerHTML = '<tr><td colspan="8" class="empty">暂无成交记录</td></tr>';
    return;
  }

  const sorted = [...trades].reverse();
  tbody.innerHTML = sorted
    .map((t) => {
      const typeLabel = t.type === "buy" ? "买入" : "卖出";
      const typeClass = t.type === "buy" ? "trade-type--buy" : "trade-type--sell";
      const pnlHtml =
        t.type === "sell"
          ? `<span class="change ${changeClass(t.pnlPct)}">${formatNumber(t.pnl)} (${formatPct(t.pnlPct)})</span>`
          : "--";
      return `
      <tr>
        <td>${bucketLabel(t.bucket)}</td>
        <td><span class="trade-type ${typeClass}">${typeLabel}</span></td>
        <td>${formatNumber(t.price)}</td>
        <td>${formatNumber(t.shares, 2)}</td>
        <td>${formatNumber(t.amount)}</td>
        <td>${pnlHtml}</td>
        <td>${reasonLabel(t.reason)}</td>
        <td>${formatDateTime(t.time)}</td>
      </tr>
    `;
    })
    .join("");
}

function renderCockpitTactical(backtest) {
  const hintEl = document.getElementById("cockpit-tactical-hint");
  const bt = backtest?.metrics || {};
  const openCount = signalsData?.openCount || 0;
  if (hintEl) {
    hintEl.textContent = openCount
      ? `v1.3 实验 · ${openCount} 笔 open 持仓跟踪中`
      : backtest?.strategyVersion
        ? `${backtest.strategyVersion} · 近 ${backtest.period || "1y"} · 等待突破信号`
        : "荐股 v1.3 · 强趋势+突破（实验室回测）";
  }

  renderStatCards("cockpit-tactical", [
    { label: "战术策略", value: backtest?.strategyVersion || "v1.3.0" },
    {
      label: "持仓跟踪",
      value: openCount || "0",
      hint: openCount ? "实验策略 open" : "暂无 buy 信号",
    },
    {
      label: "回测胜率",
      value: bt.winRate !== undefined && bt.totalTrades ? `${bt.winRate}%` : "--",
      hint: bt.totalTrades ? `${bt.totalTrades} 笔` : "当前无成交",
    },
    {
      label: "信号胜率",
      value: signalsData?.summary?.winRate != null ? `${signalsData.summary.winRate}%` : "--",
      hint: signalsData?.closedCount ? `已平 ${signalsData.closedCount} 笔` : "跟踪中",
    },
  ]);
}

function renderCockpitPaper(paper, diagnostics) {
  const hintEl = document.getElementById("cockpit-paper-hint");
  if (!paper) {
    renderStatCards("cockpit-paper", [{ label: "战役持仓", value: "加载中…" }]);
    if (hintEl) hintEl.textContent = "XRPS-X 小米滚动仓";
    return;
  }

  const stage = analyzePaperStage(paper);
  const summary = diagnostics?.summary || {};
  const focusName = paper.focusName || "小米集团";

  if (hintEl) {
    hintEl.textContent = `${focusName} · ${stage.title} · ${formatNumber(paper.totalShares, 0)} 股`;
  }

  renderStatCards("cockpit-paper", [
    { label: "持股数量", value: formatNumber(paper.totalShares, 0) },
    { label: "持仓成本", value: formatNumber(paper.avgCost) },
    {
      label: "模拟收益",
      value: formatPct(paper.returnPct),
      valueClass: changeClass(paper.returnPct),
      hint: `仓位 ${paper.positionPct ?? "--"}%`,
    },
    {
      label: "回测对照",
      value: formatPct(summary.backtestReturn),
      valueClass: changeClass(summary.backtestReturn),
      hint: diagnostics?.strategyVersion || "XRPS-X",
    },
  ]);
}

function renderLabMetrics(backtest) {
  const m = backtest?.metrics || {};
  const periodEl = document.getElementById("lab-backtest-period");
  const versionEl = document.getElementById("lab-strategy-version");
  if (periodEl) periodEl.textContent = `历史 K 线 ${backtest?.period || "1y"} · ${backtest?.universe?.length || 0} 只标的`;
  if (versionEl) versionEl.textContent = `实验策略 ${backtest?.strategyVersion || "--"} · 非 XRPS`;

  renderStatCards("lab-metrics", [
    { label: "总交易", value: m.totalTrades ?? "--" },
    { label: "胜率", value: m.winRate !== undefined ? `${m.winRate}%` : "--" },
    {
      label: "期望值",
      value: m.expectancy !== undefined ? `${formatNumber(m.expectancy)}%` : "--",
      valueClass: changeClass(m.expectancy),
    },
    { label: "夏普比率", value: m.sharpe ?? "--" },
    { label: "盈亏比", value: m.profitFactor ?? "--" },
    { label: "最大回撤", value: m.maxDrawdown !== undefined ? `${m.maxDrawdown}%` : "--" },
    { label: "年化收益", value: formatPct(m.annualReturn) },
    { label: "均盈/均亏", value: `${formatPct(m.avgWin)} / ${formatPct(m.avgLoss)}` },
  ]);
}

function renderEquityChart(canvasId, curve, chartRef, label, forceRecreate = false) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || !curve?.length) return chartRef;

  const labels = curve.map((p) => (p.date || p.time || "").slice(0, 10));
  const values = curve.map((p) => p.value ?? p.equity);

  if (chartRef && !forceRecreate) {
    chartRef.data.labels = labels;
    chartRef.data.datasets[0].data = values;
    chartRef.update("none");
    if (typeof chartRef.resize === "function") chartRef.resize();
    return chartRef;
  }

  if (chartRef) {
    chartRef.destroy();
  }

  const chart = new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label,
          data: values,
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.08)",
          fill: true,
          tension: 0.25,
          pointRadius: 0,
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: "#94a3b8", maxTicksLimit: 6 }, grid: { color: "rgba(148,163,184,0.08)" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.08)" } },
      },
      plugins: { legend: { labels: { color: "#cbd5e1" } } },
    },
  });

  if (canvasId === "backtest-chart") backtestChart = chart;
  if (canvasId === "paper-chart") paperChart = chart;
  return chart;
}

function renderBacktestChart(curve) {
  const emptyEl = document.getElementById("backtest-chart-empty");
  const canvas = document.getElementById("backtest-chart");
  if (!curve?.length) {
    if (emptyEl) emptyEl.hidden = false;
    if (canvas) canvas.hidden = true;
    if (backtestChart) {
      backtestChart.destroy();
      backtestChart = null;
    }
    return;
  }
  if (emptyEl) emptyEl.hidden = true;
  if (canvas) canvas.hidden = false;
  backtestChart = renderEquityChart("backtest-chart", curve, backtestChart, "回测净值");
}

function renderPaperChart(curve, forceRecreate = false) {
  paperChart = renderEquityChart("paper-chart", curve, paperChart, "账户净值", forceRecreate);
}

function renderPaperStrategyCard(data) {
  if (!data) return;
  const versionEl = document.getElementById("paper-card-version");
  const summaryEl = document.getElementById("paper-strategy-summary");
  if (versionEl) versionEl.textContent = data.strategyCode || data.strategyVersion || "--";

  const acct = data.account || {};
  const risk = data.riskParams || {};
  if (summaryEl) {
    summaryEl.innerHTML = [
      { label: "系统", value: data.strategyName || "XRPS-X" },
      { label: "核心/滚动/现金", value: `${acct.corePct ?? 40}/${acct.rollingPct ?? 40}/${acct.cashPct ?? 20}%` },
      { label: "最大仓位", value: `${acct.maxPositionPct ?? 80}%` },
      { label: "口诀", value: risk.motto ? risk.motto.slice(0, 12) + "…" : "滚动做T" },
    ]
      .map(
        (item) => `
        <div class="paper-strategy-card__item">
          <span class="paper-strategy-card__label">${item.label}</span>
          <span class="paper-strategy-card__value">${item.value}</span>
        </div>
      `
      )
      .join("");
  }
}

function renderPaperStrategyDetail(data) {
  if (!data) return "";

  const renderRules = (rules) =>
    (rules || [])
      .map(
        (rule) => `
        <li>
          <span class="paper-strategy-rules__label">${rule.label}</span>
          <span class="paper-strategy-rules__value">${rule.value}</span>
          ${rule.detail ? `<span class="paper-strategy-rules__detail">${rule.detail}</span>` : ""}
        </li>
      `
      )
      .join("");

  const ps = data.positionSizing || {};
  const risk = data.riskParams || {};
  const acct = data.account || {};

  const paramsHtml = [
    { label: "初始资金", value: formatNumber(acct.initialCash) },
    { label: "最大持仓", value: `${acct.maxPositions ?? 1} 只` },
    { label: "开仓模式", value: acct.buyOnlyLabel || "--" },
    { label: "仓位上限", value: `${ps.maxPct ?? 25}%` },
    { label: "盈亏比", value: `${risk.rewardRiskRatio ?? 2} : 1` },
    { label: "最长持有", value: `${risk.maxHoldDays ?? 25} 天` },
  ]
    .map(
      (p) => `
      <div class="paper-strategy-param">
        <span class="paper-strategy-param__label">${p.label}</span>
        <span class="paper-strategy-param__value">${p.value}</span>
      </div>
    `
    )
    .join("");

  const filtersHtml = (data.signalFilters || [])
    .map(
      (f) => `
      <span class="paper-strategy-filter ${f.enabled ? "" : "paper-strategy-filter--off"}">
        ${f.label} <strong>${f.value}</strong>
      </span>
    `
    )
    .join("");

  const flowHtml = (data.flow || [])
    .map(
      (step) => `
      <article class="paper-strategy-flow__step">
        <span class="paper-strategy-flow__num">${step.step}</span>
        <p class="paper-strategy-flow__title">${step.title}</p>
        <p class="paper-strategy-flow__desc">${step.desc || ""}</p>
      </article>
    `
    )
    .join("");

  return `
    <section class="paper-strategy">
      <div class="paper-strategy__head">
        <p class="paper-strategy__summary">${data.strategyName || ""} · ${data.summary || ""}</p>
        <p class="paper-strategy__schedule">${data.schedule ? `执行频率：${data.schedule}` : ""}</p>
      </div>
      <div class="paper-strategy-flow">${flowHtml}</div>
      <div class="paper-strategy-grid">
        <div class="paper-strategy-block paper-strategy-block--buy">
          <h3 class="paper-strategy-block__title">买入条件</h3>
          <ul class="paper-strategy-rules">${renderRules(data.buyRules)}</ul>
        </div>
        <div class="paper-strategy-block paper-strategy-block--sell">
          <h3 class="paper-strategy-block__title">卖出条件</h3>
          <ul class="paper-strategy-rules">${renderRules(data.sellRules)}</ul>
        </div>
        <div class="paper-strategy-block paper-strategy-block--params">
          <h3 class="paper-strategy-block__title">仓位计算</h3>
          <p class="paper-strategy-formula">${ps.formula || ""}${ps.note ? `\n${ps.note}` : ""}</p>
          <div class="paper-strategy-params">${paramsHtml}</div>
        </div>
        <div class="paper-strategy-block paper-strategy-block--params">
          <h3 class="paper-strategy-block__title">buy 信号硬过滤</h3>
          <div class="paper-strategy-filters">${filtersHtml}</div>
        </div>
      </div>
    </section>
  `;
}

function renderPaperBacktestCards(data) {
  const rollingEl = document.getElementById("paper-backtest-rolling");
  const yearsEl = document.getElementById("paper-backtest-years");
  if (!rollingEl && !yearsEl) return;

  if (!data?.periods) {
    const loading = '<p class="empty">回测数据加载中…</p>';
    if (rollingEl) rollingEl.innerHTML = loading;
    if (yearsEl) yearsEl.innerHTML = loading;
    return;
  }

  const renderGroup = (el, keys) => {
    if (!el) return;
    if (!keys?.length) {
      el.innerHTML = '<p class="empty">暂无数据</p>';
      return;
    }
    el.innerHTML = keys
      .filter((p) => data.periods[p])
      .map((period) => {
        const block = data.periods[period];
        const m = block.metrics || {};
        const rangeHint =
          block.startDate && block.endDate
            ? `${block.startDate} ~ ${block.endDate}`
            : "";
        return `
        <article class="paper-backtest-card" data-paper-backtest="${period}" role="button" tabindex="0">
          <p class="paper-backtest-card__period">${block.label || period}</p>
          <p class="paper-backtest-card__return change ${changeClass(m.totalReturnPct)}">${formatPct(m.totalReturnPct)}</p>
          <div class="paper-backtest-card__meta">
            <span>期末净值 ${formatNumber(m.finalEquity)}</span>
            <span>股数 ${formatNumber(m.initialShares, 0)} → ${formatNumber(m.finalShares, 0)}</span>
            <span>${m.totalTrades ?? 0} 笔 · 股数增长 ${formatPct(m.shareGrowthPct)}</span>
          </div>
          <p class="paper-backtest-card__hint">点击查看交易明细 →</p>
        </article>
      `;
      })
      .join("");
  };

  const groups = data.periodGroups || {};
  const rollingKeys = groups.rolling || data.periodOrder?.filter((k) => k === "all" || k.endsWith("y")) || [];
  const calendarKeys = groups.calendar || data.periodOrder?.filter((k) => /^\d{4}$/.test(k)) || [];

  renderGroup(rollingEl, rollingKeys);
  renderGroup(yearsEl, calendarKeys);
}

function renderPaperBacktestModal(period, trades, curve) {
  const data = paperBacktestData;
  if (!data?.periods?.[period]) return "";
  const block = data.periods[period];
  const m = block.metrics || {};
  const periodTrades = trades ?? filterTradesByPeriod(data.trades, block.startDate, block.endDate);
  const rows = periodTrades.length
    ? periodTrades
        .map(
          (t) => `
        <tr>
          <td>${bucketLabel(t.bucket)}</td>
          <td>${t.type === "buy" ? "买入" : "卖出"}</td>
          <td>${formatNumber(t.price)}</td>
          <td>${formatNumber(t.shares, 2)}</td>
          <td>${formatNumber(t.amount)}</td>
          <td>${t.type === "sell" ? `<span class="change ${changeClass(t.pnlPct)}">${formatNumber(t.pnl)}</span>` : "--"}</td>
          <td>${reasonLabel(t.reason)}</td>
          <td>${(t.time || "").slice(0, 10)}</td>
        </tr>
      `
        )
        .join("")
    : '<tr><td colspan="8" class="empty">该周期暂无交易</td></tr>';

  return `
    <p class="paper-modal-summary">股数 ${formatNumber(m.initialShares, 0)} → ${formatNumber(m.finalShares, 0)} · 成本 ${formatNumber(m.finalAvgCost)} · 回撤 ${m.maxDrawdown ?? 0}%</p>
    <div class="paper-modal__chart">
      <canvas id="paper-modal-chart" aria-label="回测净值曲线"></canvas>
    </div>
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>仓位</th>
            <th>类型</th>
            <th>价格</th>
            <th>数量</th>
            <th>金额</th>
            <th>盈亏</th>
            <th>原因</th>
            <th>日期</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function openPaperModal(type, payload) {
  const modal = document.getElementById("paper-modal");
  const titleEl = document.getElementById("paper-modal-title");
  const bodyEl = document.getElementById("paper-modal-body");
  if (!modal || !titleEl || !bodyEl) return;

  if (paperModalChart) {
    paperModalChart.destroy();
    paperModalChart = null;
  }

  if (type === "strategy") {
    titleEl.textContent = "策略详情";
    bodyEl.innerHTML = renderPaperStrategyDetail(paperStrategyData);
    modal.hidden = false;
    document.body.classList.add("modal-open");
    return;
  }

  if (type === "backtest-trades") {
    const period = payload?.period;
    const label = paperBacktestData?.periods?.[period]?.label || period;
    const block = paperBacktestData?.periods?.[period];
    titleEl.textContent = `${label} 交易明细`;
    bodyEl.innerHTML = '<p class="empty">加载交易明细…</p>';
    modal.hidden = false;
    document.body.classList.add("modal-open");

    const trades = filterTradesByPeriod(paperBacktestData?.trades, block?.startDate, block?.endDate);
    const curvePath = block?.curveFile ? `data/${block.curveFile}` : null;

    const loadCurve = curvePath
      ? fetchJson(curvePath).then((file) => file?.equityCurve || [])
      : Promise.resolve(block?.equityCurve || []);

    loadCurve
      .then((curve) => {
        bodyEl.innerHTML = renderPaperBacktestModal(period, trades, curve);
        requestAnimationFrame(() => {
          if (curve?.length) {
            paperModalChart = renderEquityChart(
              "paper-modal-chart",
              curve,
              paperModalChart,
              "回测净值",
              true
            );
          }
        });
      })
      .catch(() => {
        bodyEl.innerHTML = renderPaperBacktestModal(period, trades, []);
      });
    return;
  }

  modal.hidden = false;
  document.body.classList.add("modal-open");
}

function closePaperModal() {
  const modal = document.getElementById("paper-modal");
  if (!modal) return;
  modal.hidden = true;
  document.body.classList.remove("modal-open");
  if (paperModalChart) {
    paperModalChart.destroy();
    paperModalChart = null;
  }
}

function onPaperBacktestClick(e) {
  const target = e.target.closest("[data-paper-backtest]");
  if (target?.dataset.paperBacktest) {
    openPaperModal("backtest-trades", { period: target.dataset.paperBacktest });
  }
}

function setupPaperModal() {
  const card = document.getElementById("paper-strategy-card");
  card?.addEventListener("click", () => openPaperModal("strategy"));
  card?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openPaperModal("strategy");
    }
  });

  document.getElementById("paper-backtest-rolling")?.addEventListener("click", onPaperBacktestClick);
  document.getElementById("paper-backtest-years")?.addEventListener("click", onPaperBacktestClick);

  document.querySelectorAll("[data-paper-modal-close]").forEach((el) => {
    el.addEventListener("click", closePaperModal);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closePaperModal();
  });
}

function renderPaperPanel(paper, loadState = "ready") {
  if (!paper) {
    const isError = loadState === "error";
    renderStatCards("paper-stats", [
      {
        label: "模拟盘",
        value: isError ? "加载失败" : "加载中…",
        hint: isError ? "无法读取 paper_account.json，请刷新重试" : "正在读取 paper_account.json",
      },
    ]);
    renderCockpitPaper(null);
    renderPaperStageBanner(null);
    const positionsEl = document.getElementById("paper-positions");
    if (positionsEl) positionsEl.innerHTML = '<p class="empty">数据加载中…</p>';
    const tbody = document.querySelector("#paper-trades-table tbody");
    if (tbody) tbody.innerHTML = '<tr><td colspan="8" class="empty">数据加载中…</td></tr>';
    return;
  }
  renderPaperStats(paper);
  renderPaperPositions(paper);
  renderPaperTrades(paper.trades);
  renderPaperStageBanner(paper);
  renderPaperCompare(paper);
  renderCockpitPaper(paper, diagnosticsData);
  renderPaperMonthlyDashboard(paper, diagnosticsData);
  renderXrpsTradesLog(paper);
  renderReviewXrpsStats(paper, diagnosticsData);
  renderPaperBucketChart(paper, true);
  requestAnimationFrame(() => {
    try {
      renderPaperChart(paper.equityCurve, true);
    } catch (error) {
      console.error("paper chart render failed", error);
    }
  });
}

function renderLabVersionCompare(backtest) {
  const el = document.getElementById("lab-version-compare");
  if (!el || !backtest?.compareWith) {
    if (el) el.innerHTML = "";
    return;
  }
  const prev = backtest.compareWith;
  const cur = backtest.metrics || {};
  const delta = prev.delta || {};
  const fmtDelta = (v, suffix = "") => {
    if (v === null || v === undefined) return "--";
    const prefix = v > 0 ? "+" : "";
    return `${prefix}${v}${suffix}`;
  };
  el.innerHTML = `
    <div class="version-compare__grid">
      <article class="version-compare__card">
        <p class="version-compare__label">${backtest.strategyVersion || "当前"}</p>
        <p>胜率 ${cur.winRate ?? "--"}% · 期望 ${cur.expectancy ?? "--"}%</p>
      </article>
      <article class="version-compare__card version-compare__card--muted">
        <p class="version-compare__label">${prev.version}</p>
        <p>胜率 ${prev.metrics?.winRate ?? "--"}% · 期望 ${prev.metrics?.expectancy ?? "--"}%</p>
      </article>
      <article class="version-compare__card version-compare__card--delta">
        <p class="version-compare__label">变化</p>
        <p class="change ${changeClass(delta.expectancy)}">期望 ${fmtDelta(delta.expectancy, "%")}</p>
        <p>胜率 ${fmtDelta(delta.winRate, "pp")}</p>
      </article>
    </div>
  `;
}

function formatFlow(value) {
  if (value === null || value === undefined) return "--";
  const abs = Math.abs(value);
  if (abs >= 1e8) return `${(value / 1e8).toFixed(2)}亿`;
  if (abs >= 1e4) return `${(value / 1e4).toFixed(0)}万`;
  return String(value);
}

function renderWencaiBanner(data, containerId = "cockpit-wencai") {
  const el = document.getElementById(containerId);
  if (!el) return;

  if (!data || data.status === "error") {
    el.innerHTML = data?.message
      ? `<p class="wencai-hint">${data.message}</p>`
      : "";
    return;
  }

  const staleNote = data.newsStale || data.screens?.some((s) => s.stale) ? " · 部分缓存" : "";
  const cookieHint = data.cookieHint && !data.cookieUsed
    ? `<p class="wencai-hint wencai-hint--stale">${data.cookieHint}</p>`
    : "";

  const s = data.sentiment || {};
  const up = s.limitUp != null ? `${s.limitUp}${s.limitUpNote ? "+" : ""}` : "--";
  const down = s.limitDown != null ? `${s.limitDown}${s.limitDownNote ? "+" : ""}` : "--";
  const moodClass = s.mood === "偏多" ? "up" : s.mood === "偏空" ? "down" : "flat";

  el.innerHTML = `
    ${cookieHint}
    <div class="wencai-banner__inner">
      <div class="wencai-banner__brand">
        <span class="wencai-badge">问财</span>
        <span class="wencai-banner__title">A股情绪 · ${s.mood || "—"}</span>
      </div>
      <div class="wencai-banner__stats">
        <span>涨停 <strong class="change change--up">${up}</strong></span>
        <span>跌停 <strong class="change change--down">${down}</strong></span>
        <span class="wencai-banner__time">${formatDateTime(data.updatedAt)}${staleNote}</span>
      </div>
      <button type="button" class="link-btn" data-goto-tab="market">详情 →</button>
    </div>
  `;
}

function renderWencaiPanels(data, containerId = "market-wencai") {
  const el = document.getElementById(containerId);
  if (!el) return;

  if (!data || (data.status !== "ok" && data.status !== "empty")) {
    el.innerHTML = `<p class="empty">${data?.message || "问财数据加载中…"}</p>`;
    return;
  }

  const screens = data.screens || [];
  if (!screens.length) {
    el.innerHTML = '<p class="empty">暂无问财数据</p>';
    return;
  }

  const staleBanner = data.screens?.some((s) => s.stale)
    ? '<p class="wencai-hint wencai-hint--stale">部分问句拉取失败，已展示上次成功数据</p>'
    : "";

  el.innerHTML = `
    ${staleBanner}
    <div class="panel__head">
      <h2>问财 A股洞察</h2>
      <p>同花顺问财自然语言筛选 · ${formatDateTime(data.updatedAt)}</p>
    </div>
    <div class="wencai-grid">
      ${screens
        .map((screen) => {
          const countHtml =
            screen.count != null
              ? `<span class="wencai-screen__count">共 ${screen.count}${screen.countNote ? "+" : ""} 只</span>`
              : "";
          const statusNote =
            screen.status === "error"
              ? `<span class="wencai-screen__error">${screen.error || "拉取失败"}</span>`
              : screen.stale
                ? `<span class="wencai-screen__stale">${screen.staleMessage || "缓存"}</span>`
                : "";
          const rows =
            screen.items?.length > 0
              ? screen.items
                  .map(
                    (item) => `
              <tr>
                <td><strong>${item.name}</strong><br><span class="stock-card__symbol">${item.code}</span></td>
                <td>${formatNumber(item.price)}</td>
                <td class="change ${changeClass(item.changePct)}">${formatPct(item.changePct)}</td>
                <td>${item.rank || (item.flow != null ? formatFlow(item.flow) : "--")}</td>
              </tr>
            `
                  )
                  .join("")
              : screen.status === "error"
                ? `<tr><td colspan="4" class="empty">${screen.error || "拉取失败"}</td></tr>`
                : '<tr><td colspan="4" class="empty">暂无结果</td></tr>';
          return `
          <article class="wencai-screen ${screen.stale ? "wencai-screen--stale" : ""}">
            <header class="wencai-screen__head">
              <h3>${screen.title}</h3>
              ${countHtml}
              ${statusNote}
              <span class="wencai-screen__query">${screen.query}</span>
            </header>
            <div class="table-wrap">
              <table class="data-table data-table--compact">
                <thead>
                  <tr>
                    <th>标的</th>
                    <th>现价</th>
                    <th>涨跌</th>
                    <th>${screen.id === "main_flow" ? "主力流向" : "排名/流向"}</th>
                  </tr>
                </thead>
                <tbody>${rows}</tbody>
              </table>
            </div>
          </article>
        `;
        })
        .join("")}
    </div>
  `;
}

function enrichAiStocksWithQuotes(stocks) {
  return (stocks || []).map((stock) => {
    const price = quoteMap[stock.symbol];
    const changePct = quoteChangeMap[stock.symbol];
    if (price == null) return stock;
    return { ...stock, price, changePct };
  });
}

function filterAiStocks(stocks) {
  if (!stocks?.length) return [];
  let result = enrichAiStocksWithQuotes(stocks);
  if (aiChainFilter !== "all") {
    result = result.filter((s) => s.market === aiChainFilter);
  }
  const query = aiChainSearch.trim().toLowerCase();
  if (query) {
    result = result.filter((s) => {
      const haystack = [s.name, s.symbol, s.role, s.market, ...(s.tags || [])]
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    });
  }
  return result;
}

function buildAiSegmentGroups(segments) {
  const groups = [];
  const index = new Map();
  for (const seg of segments || []) {
    const stocks = filterAiStocks(seg.stocks);
    if (!stocks.length) continue;
    const groupName = seg.group || "其他";
    if (!index.has(groupName)) {
      const group = { name: groupName, segments: [] };
      index.set(groupName, group);
      groups.push(group);
    }
    index.get(groupName).segments.push({ ...seg, stocks });
  }
  return groups;
}

function renderAiStockCard(stock) {
  const tags = (stock.tags || [])
    .map((tag) => `<span class="ai-stock__tag">${tag}</span>`)
    .join("");
  const price = quoteMap[stock.symbol];
  const quoteHtml =
    price != null
      ? `<span class="ai-stock__quote change ${changeClass(stock.changePct)}">${formatNumber(price)}${stock.changePct != null ? ` (${formatPct(stock.changePct)})` : ""}</span>`
      : `<span class="ai-stock__quote ai-stock__quote--na">行情未收录</span>`;
  return `
    <article class="ai-stock">
      <div class="ai-stock__row">
        <span class="ai-stock__name">${stock.name}</span>
        <span class="reco-market reco-market--${marketClass(stock.market)}">${stock.market}</span>
      </div>
      <div class="ai-stock__row ai-stock__row--quote">
        <span class="ai-stock__symbol">${stock.symbol}</span>
        ${quoteHtml}
      </div>
      <p class="ai-stock__role">${stock.role || ""}</p>
      ${tags ? `<div class="ai-stock__tags">${tags}</div>` : ""}
    </article>
  `;
}

function renderAiSegment(seg) {
  return `
    <article class="ai-segment">
      <div class="ai-segment__head">
        <div class="ai-segment__title-row">
          <h4 class="ai-segment__name">${seg.name}</h4>
          <span class="ai-segment__count">${seg.stocks.length} 只</span>
        </div>
        <p class="ai-segment__desc">${seg.desc || ""}</p>
      </div>
      <div class="ai-stocks">
        ${seg.stocks.map((stock) => renderAiStockCard(stock)).join("")}
      </div>
    </article>
  `;
}

function renderAiChainIntro(data) {
  const el = document.getElementById("ai-chain-intro");
  if (!el) return;
  el.innerHTML = `
    <div class="ai-chain-intro__inner">
      <h2 class="ai-chain-intro__title">${data.title || "AI 产业链"}</h2>
      <p class="ai-chain-intro__subtitle">${data.subtitle || ""}</p>
      <p class="ai-chain-intro__disclaimer">${data.disclaimer || ""}</p>
    </div>
  `;
}

function renderAiChainPipeline(data) {
  const el = document.getElementById("ai-chain-pipeline");
  if (!el) return;
  const steps = data.pipeline || [];
  el.innerHTML = steps
    .map(
      (step) => `
      <article class="ai-pipeline__step">
        <p class="ai-pipeline__label">${step.label}</p>
        <p class="ai-pipeline__hint">${step.hint || ""}</p>
      </article>
    `
    )
    .join("");
}

function renderAiChainLayers(data) {
  const el = document.getElementById("ai-chain-layers");
  const summaryEl = document.getElementById("ai-chain-summary");
  if (!el) return;

  const layers = data.layers || [];
  let segmentCount = 0;
  let stockCount = 0;

  const html = layers
    .map((layer) => {
      const groups = buildAiSegmentGroups(layer.segments);
      if (!groups.length) return "";

      const segmentsHtml = groups
        .map((group) => {
          segmentCount += group.segments.length;
          stockCount += group.segments.reduce((sum, seg) => sum + seg.stocks.length, 0);
          return `
          <section class="ai-segment-group">
            <h4 class="ai-segment-group__title">${group.name}</h4>
            <div class="ai-segment-group__list">
              ${group.segments.map((seg) => renderAiSegment(seg)).join("")}
            </div>
          </section>
        `;
        })
        .join("");

      return `
      <section class="ai-layer">
        <header class="ai-layer__head ai-layer__head--${layer.id}">
          <h3 class="ai-layer__title">${layer.name}</h3>
          <p class="ai-layer__summary">${layer.summary || ""}</p>
        </header>
        <div class="ai-segments">${segmentsHtml}</div>
      </section>
    `;
    })
    .filter(Boolean)
    .join("");

  if (summaryEl) {
    const filterLabel = aiChainFilter === "all" ? "全市场" : aiChainFilter;
    const version = data.version ? ` v${data.version}` : "";
    const searchHint = aiChainSearch.trim() ? ` · 搜索「${aiChainSearch.trim()}」` : "";
    summaryEl.textContent = `${filterLabel}${searchHint} · ${segmentCount} 个环节 · ${stockCount} 只标的${version}`;
  }

  el.innerHTML = html || '<p class="ai-chain-empty">当前筛选市场下暂无标的，请切换「全部」查看。</p>';
}

function renderAiChainThemes(data) {
  const el = document.getElementById("ai-chain-themes");
  if (!el) return;
  const themes = data.themes || [];
  if (!themes.length) {
    el.innerHTML = "";
    return;
  }
  el.innerHTML = themes
    .map(
      (theme) => `
      <article class="ai-theme">
        <h4 class="ai-theme__name">${theme.name}</h4>
        <p class="ai-theme__logic">${theme.logic || ""}</p>
        <p class="ai-theme__leaders">代表方向：${theme.leaders || ""}</p>
      </article>
    `
    )
    .join("");
}

function setAiChainView(view) {
  aiChainView = view === "mindmap" ? "mindmap" : "list";
  const listEl = document.getElementById("ai-chain-list-view");
  const mindEl = document.getElementById("ai-chain-mindmap-view");
  const toggle = document.getElementById("ai-chain-view-toggle");
  if (listEl) listEl.hidden = aiChainView !== "list";
  if (mindEl) mindEl.hidden = aiChainView !== "mindmap";
  toggle?.querySelectorAll(".ai-view-btn").forEach((btn) => {
    btn.classList.toggle("ai-view-btn--active", btn.dataset.view === aiChainView);
  });
  if (aiChainView === "mindmap" && aiChainData) {
    renderAiMindMap(aiChainData);
  }
}

function renderAiMindMap(data) {
  if (!window.AiMindMap?.render) return;
  const ok = window.AiMindMap.render(data, filterAiStocks);
  if (!ok) {
    const detail = document.getElementById("ai-mindmap-detail");
    if (detail) {
      detail.innerHTML = '<p class="ai-mindmap-detail__empty">思维导图加载中，请稍后刷新…</p>';
    }
  }
}

function renderAiChain(data) {
  if (!data) return;
  renderAiChainIntro(data);
  renderAiChainPipeline(data);
  renderAiChainLayers(data);
  if (aiChainView === "mindmap") {
    renderAiMindMap(data);
  }
  renderAiChainThemes(data);
}

function setupAiChainFilters() {
  const toggle = document.getElementById("ai-chain-view-toggle");
  if (toggle) {
    toggle.addEventListener("click", (event) => {
      const btn = event.target.closest(".ai-view-btn");
      if (!btn?.dataset.view) return;
      setAiChainView(btn.dataset.view);
    });
  }

  const filters = document.getElementById("ai-chain-filters");
  if (filters) {
    filters.addEventListener("click", (event) => {
      const btn = event.target.closest(".history-filter");
      if (!btn) return;
      aiChainFilter = btn.dataset.market || "all";
      filters.querySelectorAll(".history-filter").forEach((el) => {
        el.classList.toggle("history-filter--active", el === btn);
      });
      if (aiChainData) renderAiChain(aiChainData);
    });
  }

  const searchInput = document.getElementById("ai-chain-search");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      aiChainSearch = searchInput.value || "";
      clearTimeout(aiSearchTimer);
      aiSearchTimer = setTimeout(() => {
        if (aiChainData) renderAiChain(aiChainData);
      }, AI_SEARCH_DEBOUNCE_MS);
    });
  }
}

function renderCockpitAiTeaser(data) {
  const el = document.getElementById("ai-cockpit-teaser");
  if (!el) return;
  if (!data?.layers?.length) {
    el.textContent = "算力 · 模型 · 应用全景拆解，支持列表与思维导图双视图。";
    return;
  }
  const layers = data.layers.length;
  const symbols = data.layers.reduce(
    (sum, layer) => sum + (layer.segments || []).reduce((n, seg) => n + (seg.symbols?.length || 0), 0),
    0
  );
  el.textContent = `${layers} 环节 · ${symbols} 只标的 · 支持列表与思维导图双视图，可搜索筛选。`;
}

async function loadAiChainData() {
  const data = await fetchJson(AI_CHAIN_URL);
  if (!data) return;
  aiChainData = data;
  renderCockpitAiTeaser(data);
  if (activeTab === "ai") renderAiChain(data);
}

async function loadAiChainData() {
  const data = await fetchJson(AI_CHAIN_URL);
  if (!data) return;
  aiChainData = data;
  renderCockpitAiTeaser(data);
  if (activeTab === "ai") renderAiChain(data);
}

function slotBadgeClass(slot) {
  if (slot === "morning") return "report-slot--morning";
  if (slot === "noon") return "report-slot--noon";
  return "report-slot--afternoon";
}

async function loadReportsIndex() {
  const data = await fetchJson(REPORTS_INDEX_URL);
  if (!data) return;
  reportsIndex = data;
  if (!currentReportId && data.latest?.id) {
    currentReportId = data.latest.id;
    await loadReportContent(currentReportId);
  }
  if (activeTab === "reports") renderReportsPanel();
}

async function loadReportContent(reportId) {
  const entry = reportsIndex?.reports?.find((r) => r.id === reportId);
  if (!entry?.path) return;
  try {
    const response = await fetch(`${entry.path}?t=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const markdown = await response.text();
    currentReportId = reportId;
    renderReportMarkdown(entry, markdown);
    renderReportsPanel();
  } catch (error) {
    console.error("report load failed", error);
    const el = document.getElementById("report-markdown");
    if (el) el.innerHTML = '<p class="empty">报告加载失败，请稍后重试。</p>';
  }
}

function renderReportMarkdown(entry, markdown) {
  const head = document.getElementById("report-body-head");
  const body = document.getElementById("report-markdown");
  if (!body) return;

  if (head) {
    head.innerHTML = `
      <h3>${entry.title || entry.slotLabel || "投资决策日报"}</h3>
      <p>${formatDateTime(entry.generatedAt)} · ${entry.subtitle || ""}</p>
      <p class="report-excerpt">${entry.excerpt || ""}</p>
    `;
  }

  if (typeof marked !== "undefined" && marked.parse) {
    body.innerHTML = marked.parse(markdown, { gfm: true, breaks: false });
  } else {
    body.innerHTML = `<pre class="report-fallback">${markdown.replace(/</g, "&lt;")}</pre>`;
  }
}

function renderReportsPanel() {
  const list = document.getElementById("report-list");
  const subtitle = document.getElementById("report-panel-subtitle");
  if (!list) return;

  const reports = reportsIndex?.reports || [];
  if (subtitle) {
    subtitle.textContent = reportsIndex?.updatedAt
      ? `最近更新 ${formatDateTime(reportsIndex.updatedAt)} · 每日 09:00 / 12:00 / 16:00`
      : "每日 09:00 / 12:00 / 16:00（北京时间）自动生成";
  }

  if (!reports.length) {
    list.innerHTML = '<li class="empty">暂无研报，等待定时任务生成。</li>';
    return;
  }

  list.innerHTML = reports
    .map(
      (r) => `
    <li>
      <button type="button" class="report-list__btn ${r.id === currentReportId ? "report-list__btn--active" : ""}" data-report-id="${r.id}">
        <time datetime="${r.generatedAt}">${r.date} ${r.slotLabel}</time>
        <strong>${r.title}</strong>
      </button>
    </li>
  `
    )
    .join("");

  list.querySelectorAll("[data-report-id]").forEach((btn) => {
    btn.addEventListener("click", () => loadReportContent(btn.dataset.reportId));
  });
}

function setupNewsFilters() {
  const filters = document.getElementById("news-filters");
  if (!filters) return;
  filters.addEventListener("click", (event) => {
    const btn = event.target.closest(".news-filter");
    if (!btn) return;
    newsFilter = btn.dataset.source || "all";
    filters.querySelectorAll(".news-filter").forEach((el) => {
      el.classList.toggle("news-filter--active", el === btn);
    });
    renderMergedNews();
  });
}

function applyWencaiData(data) {
  if (!data) return;
  wencaiData = data;
  renderWencaiBanner(data);
  if (activeTab === "market") renderWencaiPanels(data);
  renderMergedNews();
  lastWencaiUpdatedAt = data.updatedAt;
  updateHeaderFreshness();
  renderDecisionBrief();
}

async function refreshWencaiData() {
  try {
    const data = await fetchJson(WENCAI_URL);
    if (!data) return;
    if (data.updatedAt && data.updatedAt === lastWencaiUpdatedAt) return;
    applyWencaiData(data);
  } catch (error) {
    console.error("wencai load failed", error);
  }
}

function renderDiagnostics(diag) {
  const list = document.getElementById("diagnostics-suggestions");
  if (!list) return;
  const suggestions = diag?.suggestions || [];
  if (!suggestions.length) {
    list.innerHTML = '<li class="empty">暂无诊断建议</li>';
    return;
  }
  list.innerHTML = suggestions.map((s) => `<li class="diagnostics-item">${s}</li>`).join("");
}

function renderLabByMarket(backtest) {
  const el = document.getElementById("lab-by-market");
  if (!el) return;
  const byMarket = backtest?.byMarket || {};
  const entries = Object.entries(byMarket);
  if (!entries.length) {
    el.innerHTML = "";
    return;
  }
  el.innerHTML = `
    <div class="market-metrics">
      <p class="market-metrics__title">分市场回测</p>
      <div class="market-metrics__grid">
        ${entries
          .map(
            ([market, m]) => `
          <article class="market-metric">
            <span class="reco-market reco-market--${marketClass(market)}">${market}</span>
            <p>交易 ${m.totalTrades} · 胜率 ${m.winRate}%</p>
            <p class="change ${changeClass(m.expectancy)}">期望 ${formatPct(m.expectancy)}</p>
          </article>
        `
          )
          .join("")}
      </div>
    </div>
  `;
}

function renderBacktestTrades(trades) {
  const tbody = document.querySelector("#backtest-trades-table tbody");
  if (!tbody) return;
  if (!trades?.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty">暂无回测交易</td></tr>';
    return;
  }
  tbody.innerHTML = trades
    .map(
      (t) => `
    <tr>
      <td><strong>${t.symbol}</strong></td>
      <td><span class="reco-market reco-market--${marketClass(t.market)}">${t.market}</span></td>
      <td>${t.entryDate}<br>${formatNumber(t.entryPrice)}</td>
      <td>${t.exitDate}<br>${formatNumber(t.exitPrice)}</td>
      <td class="change ${changeClass(t.returnPct)}">${formatPct(t.returnPct)}</td>
      <td>${reasonLabel(t.reason)}</td>
    </tr>
  `
    )
    .join("");
}

function renderPaperBucketChart(paper, forceRecreate = false) {
  const canvas = document.getElementById("paper-bucket-chart");
  if (!canvas || !paper || typeof Chart === "undefined") return;

  const values = [
    paper.coreValue || 0,
    paper.rollingValue || 0,
    paper.cash || 0,
  ];
  const total = values.reduce((a, b) => a + b, 0);
  if (!total) return;

  if (paperBucketChart && !forceRecreate) {
    paperBucketChart.data.datasets[0].data = values;
    paperBucketChart.update();
    return;
  }

  if (paperBucketChart) {
    paperBucketChart.destroy();
    paperBucketChart = null;
  }

  paperBucketChart = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: ["核心仓", "滚动仓", "现金"],
      datasets: [
        {
          data: values,
          backgroundColor: ["#38bdf8", "#34d399", "#94a3b8"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      cutout: "62%",
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#cbd5e1", boxWidth: 12, padding: 14 },
        },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const pct = ((ctx.raw / total) * 100).toFixed(1);
              return ` ${ctx.label}: ${formatNumber(ctx.raw)} (${pct}%)`;
            },
          },
        },
      },
    },
  });
}

function renderPaperCompare(paper) {
  const section = document.getElementById("paper-compare");
  const grid = document.getElementById("paper-compare-grid");
  const hint = document.getElementById("paper-compare-hint");
  if (!section || !grid) return;

  const bt = paperBacktestData?.periods?.all?.metrics;
  if (!paper || !bt) {
    section.hidden = true;
    return;
  }

  section.hidden = false;
  if (hint) {
    hint.textContent = `实时模拟（${paper.updatedAt?.slice(0, 10) || "今日"}）vs 上市以来回测（${paperBacktestData.periods.all.startDate} ~ ${paperBacktestData.periods.all.endDate}）`;
  }

  const rows = [
    { label: "总收益率", live: formatPct(paper.returnPct), bt: formatPct(bt.totalReturnPct), liveClass: changeClass(paper.returnPct), btClass: changeClass(bt.totalReturnPct) },
    { label: "持股数量", live: formatNumber(paper.totalShares, 0), bt: formatNumber(bt.finalShares, 0) },
    { label: "持仓成本", live: formatNumber(paper.avgCost), bt: formatNumber(bt.finalAvgCost) },
    { label: "股数增长", live: "—", bt: formatPct(bt.shareGrowthPct), btClass: changeClass(bt.shareGrowthPct) },
    { label: "胜率", live: "—", bt: bt.winRate != null ? `${bt.winRate}%` : "—" },
    { label: "最大回撤", live: "—", bt: bt.maxDrawdown != null ? `${bt.maxDrawdown}%` : "—", btClass: "change--down" },
  ];

  grid.innerHTML = `
    <div class="paper-compare-table-wrap">
      <table class="data-table paper-compare-table">
        <thead>
          <tr>
            <th>指标</th>
            <th>实时模拟</th>
            <th>回测（上市以来）</th>
          </tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (row) => `
            <tr>
              <td>${row.label}</td>
              <td class="${row.liveClass || ""}">${row.live}</td>
              <td class="${row.btClass || ""}">${row.bt}</td>
            </tr>
          `
            )
            .join("")}
        </tbody>
      </table>
    </div>
    <p class="paper-compare-note">模拟盘刚建仓时收益率接近 0% 属正常；回测验证的是长期「股数↑成本↓」路径。</p>
  `;
}

function renderPaperStats(paper) {
  const hintEl = document.getElementById("paper-positions-hint");
  if (hintEl) {
    hintEl.textContent = `仓位 ${paper?.positionPct ?? 0}% · 成本 ${formatNumber(paper?.avgCost)}`;
  }

  renderStatCards("paper-stats", [
    { label: "账户净值", value: formatNumber(paper?.equity) },
    { label: "持股数量", value: formatNumber(paper?.totalShares, 0) },
    { label: "持仓成本", value: formatNumber(paper?.avgCost) },
    {
      label: "总收益率",
      value: formatPct(paper?.returnPct),
      valueClass: changeClass(paper?.returnPct),
    },
  ]);
}

function renderPaperPositions(paper) {
  const el = document.getElementById("paper-positions");
  if (!el) return;
  if (!paper) {
    el.innerHTML = '<p class="empty">数据加载中…</p>';
    return;
  }
  const price = quoteMap[paper.focusSymbol] || paper.lastPrice || 0;
  const buckets = [
    {
      name: "核心仓",
      className: "paper-bucket--core",
      shares: paper.coreShares,
      value: paper.coreValue,
      note: "永不卖出",
    },
    {
      name: "滚动仓",
      className: "paper-bucket--rolling",
      shares: paper.rollingShares,
      value: paper.rollingValue,
      note: `成本 ${formatNumber(paper.rollingAvgCost)}`,
    },
    {
      name: "现金仓",
      className: "paper-bucket--cash",
      shares: null,
      value: paper.cash,
      note: "恐慌备用",
    },
  ];
  el.innerHTML = buckets
    .map(
      (b) => `
      <article class="paper-bucket ${b.className}">
        <div class="paper-bucket__head">
          <strong>${b.name}</strong>
          <span class="paper-bucket__note">${b.note}</span>
        </div>
        <div class="paper-bucket__meta">
          ${b.shares != null ? `<span>${formatNumber(b.shares, 0)} 股</span>` : ""}
          <span>${formatNumber(b.value)}</span>
          ${price && b.shares ? `<span>现价 ${formatNumber(price)}</span>` : ""}
        </div>
      </article>
    `
    )
    .join("");
}

function renderPaperTrades(trades) {
  const tbody = document.querySelector("#paper-trades-table tbody");
  if (!tbody) return;
  if (!trades?.length) {
    tbody.innerHTML = '<tr><td colspan="8" class="empty">暂无模拟交易</td></tr>';
    return;
  }
  const sorted = [...trades].reverse().slice(0, 50);
  tbody.innerHTML = sorted
    .map((t) => {
      const typeLabel = t.type === "buy" ? "买入" : "卖出";
      const typeClass = t.type === "buy" ? "trade-type--buy" : "trade-type--sell";
      const pnlHtml =
        t.type === "sell"
          ? `<span class="change ${changeClass(t.pnlPct)}">${formatNumber(t.pnl)} (${formatPct(t.pnlPct)})</span>`
          : "--";
      return `
      <tr>
        <td>${bucketLabel(t.bucket)}</td>
        <td><span class="trade-type ${typeClass}">${typeLabel}</span></td>
        <td><strong>${t.name || "小米集团"}</strong><br><span class="stock-card__symbol">${t.symbol || "1810.HK"}</span></td>
        <td>${formatNumber(t.price)}</td>
        <td>${formatNumber(t.shares, 2)}</td>
        <td>${formatNumber(t.amount)}</td>
        <td>${pnlHtml}</td>
        <td>${formatDateTime(t.time)}</td>
      </tr>
    `;
    })
    .join("");
}

function applyTradingData(payload) {
  const { signals, backtest, paper, diagnostics } = payload;
  // 优先应用模拟盘，避免其他面板渲染异常阻塞 paper 展示
  if (paper) {
    paperData = paper;
    renderPaperPanel(paper);
  }
  if (backtest) {
    backtestData = backtest;
    renderLabMetrics(backtest);
    renderLabVersionCompare(backtest);
    renderLabByMarket(backtest);
    renderBacktestTrades(backtest.recentTrades);
    renderCockpitTactical(backtest);
    if (activeTab === "lab") renderBacktestChart(backtest.equityCurve);
  }
  if (signals) {
    signalsData = signals;
    renderTacticalSignals(signals);
    if (backtestData) renderCockpitTactical(backtestData);
  }
  if (diagnostics) {
    diagnosticsData = diagnostics;
    renderDiagnostics(diagnostics);
    if (paperData) {
      renderCockpitPaper(paperData, diagnostics);
      renderPaperMonthlyDashboard(paperData, diagnostics);
      renderReviewXrpsStats(paperData, diagnostics);
    }
  }
  renderDecisionBrief();
  updateHeaderFreshness();
}

async function refreshPaperExtras() {
  const [strategy, backtest] = await Promise.all([
    fetchJson(PAPER_STRATEGY_URL),
    fetchJson(PAPER_BACKTEST_URL),
  ]);
  if (strategy) {
    paperStrategyData = strategy;
    if (activeTab === "paper") renderPaperStrategyCard(strategy);
  }
  if (backtest) {
    paperBacktestData = backtest;
    if (activeTab === "paper") {
      renderPaperBacktestCards(backtest);
      if (paperData) renderPaperCompare(paperData);
    }
  }
}

async function refreshPaperData() {
  await refreshPaperExtras();
  if (paperData && activeTab === "paper") {
    renderPaperPanel(paperData);
    return true;
  }
  if (activeTab === "paper" && !paperData) {
    renderPaperPanel(null, "error");
  }
  return Boolean(paperData);
}

async function fetchJson(url) {
  try {
    const response = await fetch(`${url}?t=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error(`fetch failed: ${url}`, error);
    return null;
  }
}

function tradingDataStamp(signals, backtest, paper, diagnostics) {
  return [signals?.updatedAt, backtest?.updatedAt, paper?.updatedAt, diagnostics?.updatedAt].join("|");
}

async function refreshTradingData() {
  try {
    const [signals, backtest, paper, diagnostics] = await Promise.all([
      fetchJson(SIGNALS_URL),
      fetchJson(BACKTEST_URL),
      fetchJson(PAPER_URL),
      fetchJson(DIAGNOSTICS_URL),
    ]);
    const stamp = tradingDataStamp(signals, backtest, paper, diagnostics);
    const needsPaper = !paperData && paper;
    if (stamp && stamp === lastTradingUpdatedAt && !needsPaper) return;
    applyTradingData({ signals, backtest, paper, diagnostics });
    lastTradingUpdatedAt = stamp;
  } catch (error) {
    console.error("trading data load failed", error);
    if (activeTab === "paper" && !paperData) renderPaperPanel(null);
  }
}

async function fetchRecoHistory() {
  try {
    const response = await fetch(`${HISTORY_URL}?t=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error("fetch reco history failed", error);
    return null;
  }
}

async function refreshHistory() {
  try {
    const history = await fetchRecoHistory();
    if (!history) return;
    const stamp = history.updatedAt || String(history.records?.length || 0);
    if (stamp === lastRecoHistoryStamp && recoHistory) return;
    lastRecoHistoryStamp = stamp;
    renderRecoHistory(history);
  } catch (error) {
    console.error("history load failed", error);
  }
}

function buildQuoteMap(data) {
  const map = { ...(data.quoteMap || {}) };
  quoteChangeMap = { ...(data.changeMap || {}) };
  data.stocks?.forEach((s) => {
    if (s.symbol && s.price) map[s.symbol] = s.price;
    if (s.symbol && s.changePct != null) quoteChangeMap[s.symbol] = s.changePct;
  });
  data.recommendations?.picks?.forEach((p) => {
    if (p.symbol && p.price) map[p.symbol] = p.price;
    if (p.symbol && p.monthChangePct != null) quoteChangeMap[p.symbol] = p.monthChangePct;
  });
  return map;
}

function applyData(data) {
  marketData = data;
  quoteMap = buildQuoteMap(data);

  updateHeaderFreshness();

  renderCockpitMood(data.summary);
  renderCockpitMarkets(data.marketRadar);
  renderRecommendations(data.recommendations, "cockpit-picks", true);
  renderRecommendations(data.recommendations, "reco-cards", false);
  renderMasterRecommendations(data.masterRecommendations);
  switchRecoMode(recoMode);
  renderCockpitIndices(data.indices);

  yahooNews = data.news || [];
  renderMergedNews();

  renderSummary(data.summary);
  renderIndices(data.indices);
  renderStocks(data.stocks);

  if (activeTab === "market") {
    renderDistributionChart(data.summary);
    renderStocksChart(data.stocks);
  }

  if (activeTab === "paper" && recoHistory) renderRecoHistory(recoHistory);
  if (paperData && activeTab === "paper") {
    renderPaperPositions(paperData);
    renderPaperBucketChart(paperData);
    renderPaperPanel(paperData);
  }
  renderDecisionBrief();
  lastUpdatedAt = data.updatedAt;
}

async function fetchMarketData() {
  const response = await fetch(`${DATA_URL}?t=${Date.now()}`, { cache: "no-store" });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function refreshData() {
  try {
    const data = await fetchMarketData();
    if (data.updatedAt === lastUpdatedAt) return;
    applyData(data);
  } catch (error) {
    if (lastUpdatedAt === null) {
      updateHeaderFreshness();
      const moodEl = document.getElementById("market-mood");
      if (moodEl) moodEl.textContent = "离线";
      const el = document.getElementById("updated-at");
      if (el) el.textContent = "数据加载失败，请稍后重试";
    }
    console.error(error);
  }
}

async function init() {
  setupTabs();
  setupHistoryFilters();
  setupNewsFilters();
  setupAiChainFilters();
  setupPaperModal();

  const initialTab = tabFromLocation();
  suppressTabRoute = true;
  switchTab(initialTab, { updateRoute: false });
  suppressTabRoute = false;

  await Promise.all([
    refreshData(),
    refreshMacroData(),
    refreshWencaiData(),
    refreshTradingData(),
  ]);

  await ensureTabData(initialTab);

  setInterval(refreshData, POLL_INTERVAL_MS);
  setInterval(refreshMacroData, POLL_INTERVAL_MS);
  setInterval(refreshWencaiData, POLL_INTERVAL_MS);
  setInterval(refreshTradingData, POLL_INTERVAL_MS);
  setInterval(() => {
    if (tabBundles.paper) {
      refreshPaperExtras();
      refreshHistory();
    }
  }, POLL_INTERVAL_MS);

  const scheduleIdle = window.requestIdleCallback || ((cb) => setTimeout(cb, 2500));
  scheduleIdle(() => {
    ensureTabData("ai");
    ensureTabData("reports");
  });
}

document.addEventListener("DOMContentLoaded", init);
