const DATA_URL = "data/market.json";
const HISTORY_URL = "data/reco_history.json";
const POLL_INTERVAL_MS = 5 * 60 * 1000;

let lastUpdatedAt = null;
let historyFilter = "all";
let recoHistory = null;
let distributionChart;
let stocksChart;

function formatNumber(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "--";
  }
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
  const date = new Date(iso);
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function renderSummary(summary) {
  const container = document.getElementById("summary-cards");
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

  document.getElementById("market-mood").textContent = `市场情绪：${summary.mood}`;
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
  tbody.innerHTML = indices
    .map((item, index) => {
      const canvasId = `spark-${index}`;
      return `
        <tr>
          <td>
            <strong>${item.name}</strong><br>
            <span class="stock-card__symbol">${item.symbol}</span>
          </td>
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
    const canvas = document.getElementById(`spark-${index}`);
    drawSparkline(canvas, item.sparkline);
  });
}

function renderStocks(stocks) {
  const container = document.getElementById("stock-cards");
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
              <a href="${item.link}" target="_blank" rel="noopener noreferrer">${item.title}</a>
            </p>
            <p class="news-item__meta">${item.publisher} · 关联 ${item.related}</p>
          </div>
          <span class="news-item__time">${formatDateTime(item.publishedAt)}</span>
        </li>
      `
    )
    .join("");
}

function renderRecommendations(reco) {
  const container = document.getElementById("reco-cards");
  const strategyEl = document.getElementById("reco-strategy");
  const disclaimerEl = document.getElementById("reco-disclaimer");
  if (!container) return;

  if (!reco || !reco.picks || !reco.picks.length) {
    container.innerHTML = '<p class="empty">当前没有满足策略条件的标的，空仓等待也是一种操作。</p>';
    if (disclaimerEl && reco?.disclaimer) disclaimerEl.textContent = reco.disclaimer;
    return;
  }

  if (strategyEl && reco.strategy) strategyEl.textContent = reco.strategy;
  if (disclaimerEl && reco.disclaimer) disclaimerEl.textContent = reco.disclaimer;

  const scanHtml = reco.marketScan
    ? `<p class="reco-scan">${reco.marketScan}</p>`
    : "";

  container.innerHTML = scanHtml + reco.picks
    .map(
      (pick) => `
        <article class="reco-card reco-card--${pick.signal}">
          <div class="reco-card__top">
            <div>
              <div class="reco-card__tags">
                <span class="reco-market reco-market--${pick.market === "A股" ? "cn" : pick.market === "港股" ? "hk" : "us"}">${pick.market || ""}</span>
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
          <ul class="reco-reasons">
            ${pick.reasons.map((r) => `<li>${r}</li>`).join("")}
          </ul>
          <dl class="reco-plan">
            <div><dt>买入</dt><dd>${pick.plan.entry}</dd></div>
            <div><dt>止损</dt><dd>${pick.plan.stopLoss}</dd></div>
            <div><dt>止盈</dt><dd>${pick.plan.target}</dd></div>
            <div><dt>仓位</dt><dd>${pick.plan.position}</dd></div>
          </dl>
        </article>
      `
    )
    .join("");
}

function marketClass(market) {
  if (market === "A股") return "cn";
  if (market === "港股") return "hk";
  return "us";
}

function renderRecoHistory(history) {
  const container = document.getElementById("history-timeline");
  const summaryEl = document.getElementById("history-summary");
  if (!container) return;

  recoHistory = history;
  const records = history?.records || [];

  if (summaryEl) {
    summaryEl.textContent = records.length
      ? `共 ${records.length} 条荐股快照，最新 ${formatDateTime(history.updatedAt || records[records.length - 1]?.recordedAt)}`
      : "暂无历史记录，系统将在每次更新时自动存档";
  }

  if (!records.length) {
    container.innerHTML = '<p class="empty">暂无历史荐股记录，等待下一次自动更新…</p>';
    return;
  }

  const filtered = [...records].reverse().map((record) => {
    const picks = historyFilter === "all"
      ? record.picks
      : record.picks.filter((p) => p.market === historyFilter);
    return { ...record, picks };
  }).filter((record) => record.picks.length > 0);

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
    .map(([date, dayRecords]) => `
      <section class="history-day">
        <h3 class="history-day__title">${date}</h3>
        <div class="history-day__list">
          ${dayRecords.map((record) => `
            <article class="history-record">
              <header class="history-record__head">
                <time datetime="${record.recordedAt}">${formatDateTime(record.recordedAt).slice(11)}</time>
                <span class="history-record__count">${record.picks.length} 只标的</span>
              </header>
              <div class="history-record__picks">
                ${record.picks.map((pick) => `
                  <details class="history-pick">
                    <summary>
                      <span class="reco-market reco-market--${marketClass(pick.market)}">${pick.market}</span>
                      <strong>${pick.name}</strong>
                      <span class="stock-card__symbol">${pick.symbol}</span>
                      <span class="reco-badge reco-badge--${pick.signal}">${pick.signalLabel}</span>
                      <span class="history-pick__meta">${formatNumber(pick.price)} ${pick.currency || ""} · 评分 ${pick.score}</span>
                    </summary>
                    <div class="history-pick__body">
                      <p class="history-pick__price">推荐价：${formatNumber(pick.price)} ${pick.currency || ""}</p>
                      ${pick.relativeStrength != null ? `<p class="history-pick__rs">相对强弱：${formatPct(pick.relativeStrength)}</p>` : ""}
                      <dl class="reco-plan">
                        <div><dt>买入</dt><dd>${pick.plan?.entry || "--"}</dd></div>
                        <div><dt>止损</dt><dd>${pick.plan?.stopLoss || "--"}</dd></div>
                        <div><dt>止盈</dt><dd>${pick.plan?.target || "--"}</dd></div>
                        <div><dt>仓位</dt><dd>${pick.plan?.position || "--"}</dd></div>
                      </dl>
                    </div>
                  </details>
                `).join("")}
              </div>
            </article>
          `).join("")}
        </div>
      </section>
    `)
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
      datasets: [
        {
          data: chartData,
          backgroundColor: ["#34d399", "#f87171", "#fbbf24"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#cbd5e1" },
        },
      },
    },
  });
}

function renderStocksChart(stocks) {
  const canvas = document.getElementById("stocks-chart");
  const colors = ["#38bdf8", "#34d399", "#f472b6"];
  const labels = stocks[0]?.sparkline?.map((_, index) => `T-${stocks[0].sparkline.length - index - 1}`) || [];
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
    data: {
      labels,
      datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: "#94a3b8", maxTicksLimit: 8 },
          grid: { color: "rgba(148,163,184,0.08)" },
        },
        y: {
          ticks: {
            color: "#94a3b8",
            callback: (value) => `${value}%`,
          },
          grid: { color: "rgba(148,163,184,0.08)" },
        },
      },
      plugins: {
        legend: {
          labels: { color: "#cbd5e1" },
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${context.parsed.y}%`,
          },
        },
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

function applyData(data) {
  document.getElementById("updated-at").textContent = `最近更新：${formatDateTime(data.updatedAt)}`;
  renderSummary(data.summary);
  renderIndices(data.indices);
  renderStocks(data.stocks);
  renderNews(data.news);
  renderRecommendations(data.recommendations);
  renderDistributionChart(data.summary);
  renderStocksChart(data.stocks);
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
  setupHistoryFilters();
  await Promise.all([refreshData(), refreshHistory()]);
  setInterval(refreshData, POLL_INTERVAL_MS);
  setInterval(refreshHistory, POLL_INTERVAL_MS);
}

document.addEventListener("DOMContentLoaded", init);
