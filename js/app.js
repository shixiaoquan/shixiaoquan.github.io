const DATA_URL = "data/market.json";
const HISTORY_URL = "data/reco_history.json";
const POLL_INTERVAL_MS = 5 * 60 * 1000;

let lastUpdatedAt = null;
let historyFilter = "all";
let recoHistory = null;
let marketData = null;
let quoteMap = {};
let activeTab = "cockpit";
let distributionChart;
let stocksChart;

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

function marketClass(market) {
  if (market === "A股") return "cn";
  if (market === "港股") return "hk";
  return "us";
}

function calcReturn(recoPrice, currentPrice) {
  if (!recoPrice || !currentPrice) return null;
  return Number((((currentPrice - recoPrice) / recoPrice) * 100).toFixed(2));
}

function switchTab(tabId) {
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
  if (tabId === "market" && marketData) {
    renderDistributionChart(marketData.summary);
    renderStocksChart(marketData.stocks);
  }
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

function renderPickCard(pick, compact = false) {
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
      ${reasons}
      ${plan}
    </article>
  `;
}

function renderRecommendations(reco, containerId = "reco-cards", compact = false) {
  const container = document.getElementById(containerId);
  const strategyEl = document.getElementById("reco-strategy");
  const disclaimerEl = document.getElementById("reco-disclaimer");
  if (!container) return;

  if (!reco?.picks?.length) {
    container.innerHTML = '<p class="empty">当前没有满足策略条件的标的，空仓等待也是一种操作。</p>';
    if (disclaimerEl && reco?.disclaimer) disclaimerEl.textContent = reco.disclaimer;
    return;
  }

  if (!compact) {
    if (strategyEl && reco.strategy) strategyEl.textContent = reco.strategy;
    if (disclaimerEl && reco.disclaimer) disclaimerEl.textContent = reco.disclaimer;
  }

  const scanHtml = !compact && reco.marketScan ? `<p class="reco-scan">${reco.marketScan}</p>` : "";
  container.innerHTML = scanHtml + reco.picks.map((p) => renderPickCard(p, compact)).join("");
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

function renderCockpitNews(news) {
  const el = document.getElementById("cockpit-news");
  if (!el) return;
  if (!news.length) {
    el.innerHTML = '<li class="empty">暂无资讯</li>';
    return;
  }
  el.innerHTML = news
    .slice(0, 4)
    .map(
      (item) => `
      <li class="news-item news-item--compact">
        <p class="news-item__title">
          ${item.link ? `<a href="${item.link}" target="_blank" rel="noopener noreferrer">${item.title}</a>` : item.title}
        </p>
        ${item.summary ? `<p class="news-item__summary">${item.summary}</p>` : ""}
        <span class="news-item__time">${item.publisher || ""} · ${formatDateTime(item.publishedAt)}</span>
      </li>
    `
    )
    .join("");
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
  ctx.strokeStyle = up ? "#34d399" : "#f87171";
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
          <p class="news-item__meta">${item.publisher} · 关联 ${item.related}</p>
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
    .filter((record) => record.picks.length > 0);

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
      datasets: [{ data: chartData, backgroundColor: ["#34d399", "#f87171", "#fbbf24"], borderWidth: 0 }],
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

async function fetchRecoHistory() {
  const response = await fetch(`${HISTORY_URL}?t=${Date.now()}`, { cache: "no-store" });
  if (!response.ok) return null;
  return response.json();
}

async function refreshHistory() {
  try {
    const history = await fetchRecoHistory();
    if (history) renderRecoHistory(history);
  } catch (error) {
    console.error("history load failed", error);
  }
}

function buildQuoteMap(data) {
  const map = { ...(data.quoteMap || {}) };
  data.stocks?.forEach((s) => {
    if (s.symbol && s.price) map[s.symbol] = s.price;
  });
  data.recommendations?.picks?.forEach((p) => {
    if (p.symbol && p.price) map[p.symbol] = p.price;
  });
  return map;
}

function applyData(data) {
  marketData = data;
  quoteMap = buildQuoteMap(data);

  document.getElementById("updated-at").textContent = `最近更新：${formatDateTime(data.updatedAt)}`;

  renderCockpitMood(data.summary);
  renderCockpitMarkets(data.marketRadar);
  renderRecommendations(data.recommendations, "cockpit-picks", true);
  renderRecommendations(data.recommendations, "reco-cards", false);
  renderCockpitIndices(data.indices);
  renderCockpitNews(data.news);

  renderSummary(data.summary);
  renderIndices(data.indices);
  renderStocks(data.stocks);
  renderNews(data.news);

  if (activeTab === "market") {
    renderDistributionChart(data.summary);
    renderStocksChart(data.stocks);
  }

  if (recoHistory) renderRecoHistory(recoHistory);
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
      document.getElementById("updated-at").textContent = "数据加载失败，请稍后重试";
      document.getElementById("market-mood").textContent = "离线";
    }
    console.error(error);
  }
}

async function init() {
  setupTabs();
  setupHistoryFilters();
  await Promise.all([refreshData(), refreshHistory()]);
  setInterval(refreshData, POLL_INTERVAL_MS);
  setInterval(refreshHistory, POLL_INTERVAL_MS);
}

document.addEventListener("DOMContentLoaded", init);
