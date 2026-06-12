const DATA_URL = "data/market.json";
const POLL_INTERVAL_MS = 5 * 60 * 1000;

let lastUpdatedAt = null;
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

function applyData(data) {
  document.getElementById("updated-at").textContent = `最近更新：${formatDateTime(data.updatedAt)}`;
  renderSummary(data.summary);
  renderIndices(data.indices);
  renderStocks(data.stocks);
  renderNews(data.news);
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
  await refreshData();
  setInterval(refreshData, POLL_INTERVAL_MS);
}

document.addEventListener("DOMContentLoaded", init);
