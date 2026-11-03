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

function xmShort(text, limit) {
  const clean = String(text || "").replace(/\s+/g, " ").trim();
  if (!clean) return "";
  if (clean.length <= limit) return clean;
  return `${clean.slice(0, limit)}…`;
}

function xmStep(value, max) {
  if (value == null || !max || Number.isNaN(Number(value)) || Number(max) <= 0) return 0;
  return Math.max(0, Math.min(20, Math.round((Number(value) / Number(max)) * 20))) * 5;
}

function xmChangeClass(value) {
  if (value == null || Number.isNaN(Number(value)) || Number(value) === 0) return "";
  return Number(value) > 0 ? "change change--up" : "change change--down";
}

function xmGateGlance(gate) {
  const note = String(gate.humanNote || "").trim();
  if (note) return xmShort(note.split("。")[0], 78);
  return xmShort(String(gate.summary || "").split("。")[0], 56);
}

function xmRadarCluster(cluster, { folded }) {
  const conf = ["high", "medium", "low"].includes(cluster.confidence) ? cluster.confidence : "low";
  const head = `
    <div class="xm-cluster__head">
      <h3 class="xm-cluster__title">${xmEscape(cluster.title || cluster.pillar || "簇")}</h3>
      <p class="xm-conf--${conf}">置信 ${xmEscape(cluster.confidenceLabel || conf)} · ${cluster.staleCount ? `${cluster.staleCount} 条过期` : "在窗口内"}</p>
    </div>
    <p class="xm-note">${xmEscape(cluster.summary || "")}</p>
    <ul class="xm-radar">${(cluster.items || []).map(xmRadarItem).join("")}</ul>`;
  if (!folded) return `<section class="xm-cluster">${head}</section>`;
  const count = (cluster.items || []).length;
  return `
    <details class="xm-cluster xm-cluster--gap">
      <summary>${xmEscape(cluster.title || "数据缺口")} · ${count} 条 · 默认收起</summary>
      ${head}
    </details>`;
}

function xmRadarClusters(radar) {
  const clusters = (radar && radar.clusters) || [];
  if (!clusters.length) {
    const items = (radar && radar.items) || [];
    if (!items.length) return "";
    return `<ul class="xm-radar">${items.map(xmRadarItem).join("")}</ul>`;
  }
  const ordered = [...clusters].sort((a, b) => {
    const ag = a.id === "data-gaps" ? 1 : 0;
    const bg = b.id === "data-gaps" ? 1 : 0;
    if (ag !== bg) return ag - bg;
    return String(b.latestDate || "").localeCompare(String(a.latestDate || ""));
  });
  return ordered.map((cluster) => xmRadarCluster(cluster, { folded: cluster.id === "data-gaps" })).join("");
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

const XM_PIP = { pass: "过", caution: "核", block: "拦", open: "空" };
const XM_TICK = "#94a3b8";
const XM_GRID = "rgba(148,163,184,0.12)";
let xmChartBag = [];

function xmDropCharts() {
  xmChartBag.forEach((chart) => {
    try {
      chart.destroy();
    } catch (err) {
      /* 画布已经卸掉 */
    }
  });
  xmChartBag = [];
}

function xmMountChart(canvasId, config) {
  if (typeof Chart !== "function") return false;
  const canvas = document.getElementById(canvasId);
  if (!canvas) return false;
  xmChartBag.push(new Chart(canvas, config));
  return true;
}

function xmAxis(indexAxis) {
  const value = {
    beginAtZero: true,
    ticks: { color: XM_TICK },
    grid: { color: XM_GRID },
  };
  const category = { ticks: { color: XM_TICK }, grid: { display: false } };
  return indexAxis === "y" ? { x: value, y: category } : { x: category, y: value };
}

function xmChartBase(indexAxis) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis,
    scales: xmAxis(indexAxis),
    plugins: {
      legend: { display: false },
    },
  };
}

function xmPeRows(scenarios, valuation) {
  const rows = [];
  (scenarios.items || []).forEach((row) => {
    if (row.impliedPe == null) return;
    rows.push({ label: row.label || row.id, pe: Number(row.impliedPe), kind: row.id });
  });
  if (valuation.h1RunRatePe != null) {
    rows.push({ label: "上半年年化", pe: Number(valuation.h1RunRatePe), kind: "history" });
  }
  if (valuation.maxBasePeToAdd != null) {
    rows.push({ label: "加仓线", pe: Number(valuation.maxBasePeToAdd), kind: "add" });
  }
  if (valuation.richBasePe != null) {
    rows.push({ label: "贵价线", pe: Number(valuation.richBasePe), kind: "rich" });
  }
  return rows;
}

function xmPeColor(kind) {
  if (kind === "bull") return "#34d399";
  if (kind === "base") return "#38bdf8";
  if (kind === "bear") return "#f87171";
  if (kind === "add") return "#fbbf24";
  if (kind === "rich") return "#fb7185";
  return "#94a3b8";
}

function xmMountDeskCharts(trader) {
  const indicators = trader.indicators || {};
  const points = (indicators.autoMonthly && indicators.autoMonthly.points) || [];
  if (points.length) {
    xmMountChart("xm-delivery-chart", {
      type: "bar",
      data: {
        labels: points.map((point) => String(point.period || "").slice(5)),
        datasets: [
          {
            data: points.map((point) => point.value),
            backgroundColor: points.map((point) =>
              point.quality === "lower_bound" ? "#fbbf24" : "#38bdf8"
            ),
            borderWidth: 0,
            borderRadius: 4,
          },
        ],
      },
      options: {
        ...xmChartBase("x"),
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => {
                const point = points[ctx.dataIndex] || {};
                const bound = point.quality === "lower_bound" ? "（下限）" : "";
                return `${xmInt(ctx.parsed.y)} 辆${bound}`;
              },
            },
          },
        },
      },
    });
  }

  const peRows = xmPeRows(trader.scenarios || {}, trader.valuation || {});
  if (peRows.length) {
    xmMountChart("xm-pe-chart", {
      type: "bar",
      data: {
        labels: peRows.map((row) => row.label),
        datasets: [
          {
            data: peRows.map((row) => row.pe),
            backgroundColor: peRows.map((row) => xmPeColor(row.kind)),
            borderWidth: 0,
            borderRadius: 4,
          },
        ],
      },
      options: {
        ...xmChartBase("y"),
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: { label: (ctx) => `${xmNum(ctx.parsed.x, 1)} 倍` },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            suggestedMax: 35,
            ticks: { color: XM_TICK, callback: (value) => `${value}x` },
            grid: { color: XM_GRID },
          },
          y: { ticks: { color: XM_TICK }, grid: { display: false } },
        },
      },
    });
  }

  const limits = trader.riskLimits || {};
  const sim = trader.publicSim;
  const bars = [];
  if (sim && sim.positionPct != null) {
    const hot = limits.addCeilingPct != null && sim.positionPct >= limits.addCeilingPct;
    bars.push({ label: "模拟仓", value: sim.positionPct, color: hot ? "#f87171" : "#34d399" });
  }
  if (limits.addCeilingPct != null) {
    bars.push({ label: "加仓线", value: limits.addCeilingPct, color: "#fbbf24" });
  }
  if (limits.maxPositionPct != null) {
    bars.push({ label: "总仓上限", value: limits.maxPositionPct, color: "#64748b" });
  }
  if (bars.length) {
    xmMountChart("xm-position-chart", {
      type: "bar",
      data: {
        labels: bars.map((row) => row.label),
        datasets: [
          {
            data: bars.map((row) => row.value),
            backgroundColor: bars.map((row) => row.color),
            borderWidth: 0,
            borderRadius: 4,
          },
        ],
      },
      options: {
        ...xmChartBase("y"),
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: { label: (ctx) => `${xmNum(ctx.parsed.x, 1)}%` },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            suggestedMax: limits.maxPositionPct || 100,
            ticks: { color: XM_TICK, callback: (value) => `${value}%` },
            grid: { color: XM_GRID },
          },
          y: { ticks: { color: XM_TICK }, grid: { display: false } },
        },
      },
    });
  }

  requestAnimationFrame(() => {
    xmChartBag.forEach((chart) => {
      try {
        chart.resize();
      } catch (err) {
        /* 隐藏页签里先画，切过来再量一次 */
      }
    });
  });
}

function xmMissChip(label) {
  return `<span class="xm-miss">${xmEscape(label)}<span class="xm-miss__tag">未接入</span></span>`;
}

function xmMeter(value, max, hot, markValue) {
  const step = xmStep(value, max);
  const tone = hot ? "xm-meter--hot" : "xm-meter--ok";
  const mark =
    markValue == null ? "" : `<div class="xm-meter__mark xm-mark-${xmStep(markValue, max)}"></div>`;
  return `<div class="xm-meter ${tone}" aria-hidden="true"><div class="xm-meter__fill xm-fill-${step}"></div>${mark}</div>`;
}

function renderXiaomiTrader(trader, radar, marketData) {
  const root = document.getElementById("xiaomi-trader-root");
  if (!root) return;
  xmDropCharts();
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
  const boxPct = box.positionInBox == null ? null : Math.round(Number(box.positionInBox) * 100);
  const posPct = sim && sim.positionPct != null ? Number(sim.positionPct) : null;
  const addPct = limits.addCeilingPct != null ? Number(limits.addCeilingPct) : null;
  const maxPct = limits.maxPositionPct != null ? Number(limits.maxPositionPct) : null;
  const aboveAdd = posPct != null && addPct != null && posPct >= addPct;
  const next = calendar.next || null;
  const chartsOn = typeof Chart === "function";
  const boxLevels = box.levels || {};
  const changePct = box.changePct;
  const missChips = [
    !phone.available ? xmMissChip(phone.label || "手机出货 / ASP") : "",
    memory.value == null ? xmMissChip("存储价格指数") : "",
    iot.placeholder || iot.value == null ? xmMissChip(iot.label || "IoT 毛利率") : "",
  ]
    .filter(Boolean)
    .join("");
  const grossChip =
    gross.valuePct == null
      ? xmMissChip(gross.label || "集团毛利率")
      : `<span class="xm-live">${xmEscape(gross.label || "集团毛利率")}<strong>${xmNum(gross.valuePct, 1)}%</strong><span class="xm-miss__tag">上年 ${xmNum(gross.priorValuePct, 1)}%</span></span>`;
  const narratives = (scenarios.items || [])
    .map((row) => `<li><strong>${xmEscape(row.label)}</strong> ${xmEscape(row.narrative || "")}</li>`)
    .join("");
  const matrix = gates
    .map((gate) => {
      const status = XM_STATUSES.has(gate.status) ? gate.status : "open";
      return `
        <article class="xm-matrix__row ${xmStatusClass(gate.status)}">
          <span class="xm-pip">${XM_PIP[status] || "空"}</span>
          <div>
            <p class="xm-matrix__line"><strong>${xmEscape(gate.label)}</strong> <span>${xmEscape(gate.statusLabel || "")}</span> ${xmEscape(xmGateGlance(gate))}</p>
            <details>
              <summary>依据</summary>
              <p>${xmEscape(gate.summary || "")}</p>
              <p class="xm-note">要写的判断：${xmEscape(gate.humanPrompt || "")}</p>
              <p class="xm-note">${gate.humanNote ? `交易员：${xmEscape(gate.humanNote)}` : "备注仍空。空备注不能把拦住改成通过。"}</p>
            </details>
          </div>
        </article>`;
    })
    .join("");
  const basePe = ((scenarios.items || []).find((row) => row.id === "base") || {}).impliedPe;

  const deliveryFallback = points
    .map((point) => `${xmEscape(String(point.period || "").slice(5))} ${xmInt(point.value)}${point.quality === "lower_bound" ? " 下限" : ""}`)
    .join(" · ");
  const peFallback = xmPeRows(scenarios, valuation)
    .map((row) => `${xmEscape(row.label)} ${xmNum(row.pe, 1)} 倍`)
    .join(" · ");

  root.innerHTML = `
    <header class="xm-desk">
      <div class="xm-desk__top">
        <div>
          <p class="xm-hero__eyebrow">Xiaomi desk · 1810.HK</p>
          <h2 class="xm-hero__title">${xmEscape(trader.name || "小米集团")}</h2>
          <p class="xm-desk-links">${xmHashLinks(trader.links)}</p>
        </div>
        <p class="xm-stance-badge xm-stance-badge--${tone}" aria-live="polite">${xmEscape(stance.headline || "四门未计算")}</p>
      </div>
      <div class="xm-kpis">
        <article class="xm-kpi">
          <p class="xm-kpi__label">最新价</p>
          <p class="xm-kpi__value">${xmNum(price, 2)} <span>港元</span></p>
          <p class="xm-kpi__sub"><span class="${xmChangeClass(changePct)}">${changePct == null ? "—" : xmPct(changePct)}</span> · ${xmEscape((box.advice || {}).actionLabel || "—")}</p>
          ${drift}
        </article>
        <article class="xm-kpi">
          <p class="xm-kpi__label">箱体位置</p>
          <p class="xm-kpi__value">${boxPct == null ? "—" : `${boxPct}%`}</p>
          ${xmMeter(box.positionInBox, 1, false)}
          <p class="xm-kpi__sub">${xmNum(boxLevels.boxLow, 2)} – ${xmNum(boxLevels.boxHigh, 2)}</p>
        </article>
        <article class="xm-kpi">
          <p class="xm-kpi__label">模拟仓 / 加仓线</p>
          <p class="xm-kpi__value">${posPct == null ? "—" : `${xmNum(posPct, 1)}%`} <span>/ ${addPct == null ? "—" : `${xmNum(addPct, 0)}%`}</span></p>
          ${xmMeter(posPct, maxPct || 100, aboveAdd, addPct)}
          <p class="xm-kpi__sub">${aboveAdd ? "已过加仓线" : posPct == null ? "模拟盘未接入" : "低于加仓线"} · 上限 ${maxPct == null ? "—" : `${xmNum(maxPct, 0)}%`}</p>
        </article>
        <article class="xm-kpi">
          <p class="xm-kpi__label">下一催化</p>
          <p class="xm-kpi__value">${next ? xmEscape(next.countdownLabel || "—") : "—"}</p>
          <p class="xm-kpi__sub">${next ? `${xmEscape(next.title)} · ${xmEscape(next.date || "")}` : "60 天内无已写窗口"}</p>
        </article>
      </div>
      <p class="xm-hero__asof">快照 ${xmEscape(updated)}</p>
      <details class="xm-fold">
        <summary>允许与不许写进行动</summary>
        <div class="xm-fold__body">
          <p class="xm-kicker">允许</p>
          ${xmList(stance.allowed)}
          <p class="xm-kicker">不许写进行动</p>
          ${xmList(stance.forbidden)}
        </div>
      </details>
    </header>
    <p class="xm-disclaimer xm-disclaimer--desk">${xmEscape(trader.disclaimer || "仅供研究参考，不构成投资建议。")} 情景是假设，不是预测。XRPS 模拟盘不是真实持仓。</p>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>估值与仓位</h2>
        <p>加仓线 ${xmNum(valuation.maxBasePeToAdd, 0)} 倍 · 基准 ${basePe == null ? "—" : `${xmNum(basePe, 1)} 倍`} · 贵价线 ${xmNum(valuation.richBasePe, 0)} 倍 · ${xmEscape(scenarios.assumptionLabel || "情景假设")}</p>
      </div>
      <div class="xm-charts">
        <div>
          <p class="xm-kicker">情景倍数对照</p>
          ${chartsOn ? `<div class="xm-chart xm-chart--pe"><canvas id="xm-pe-chart" aria-label="情景市盈率对照"></canvas></div>` : `<p class="xm-table-note">${peFallback}</p>`}
          <p class="xm-legend"><span class="xm-swatch xm-swatch--bull"></span>乐观 <span class="xm-swatch xm-swatch--base"></span>基准 <span class="xm-swatch xm-swatch--bear"></span>悲观 <span class="xm-swatch xm-swatch--add"></span>加仓线 <span class="xm-swatch xm-swatch--rich"></span>贵价线 <span class="xm-swatch xm-swatch--history"></span>上半年年化</p>
        </div>
        <div>
          <p class="xm-kicker">仓位进度</p>
          ${chartsOn ? `<div class="xm-chart xm-chart--pe"><canvas id="xm-position-chart" aria-label="模拟仓位相对加仓线"></canvas></div>` : `<p class="xm-table-note">模拟仓 ${posPct == null ? "—" : `${xmNum(posPct, 1)}%`} · 加仓线 ${addPct == null ? "—" : `${xmNum(addPct, 0)}%`} · 上限 ${maxPct == null ? "—" : `${xmNum(maxPct, 0)}%`}</p>`}
          <p class="xm-table-note">${aboveAdd ? "红条表示模拟仓已经不低于加仓线。" : "绿条表示模拟仓还在加仓线下方。"}这不是真实持仓。</p>
        </div>
      </div>
      <p class="xm-statline">
        <span>上半年年化 <strong>${valuation.h1RunRatePe == null ? "—" : `${xmNum(valuation.h1RunRatePe, 1)} 倍`}</strong></span>
        <span>年化利润 <strong>${xmNum(valuation.h1RunRateProfitYi, 1)}</strong> 亿元</span>
        <span>市值 <strong>${xmNum(valuation.marketCapCnyYi, 0)}</strong> 亿元</span>
        <span>现金底线 <strong>${xmNum(limits.minCashPct, 0)}%</strong></span>
      </p>
      <div class="table-wrap">
        <table class="data-table xm-scenarios">
          <thead>
            <tr>
              <th>情景</th>
              <th>收入（亿元）</th>
              <th>经调整净利润（亿元）</th>
              <th>现价倍数</th>
              <th>相对加仓线</th>
            </tr>
          </thead>
          <tbody>${scenarioRows}</tbody>
        </table>
      </div>
      <details class="xm-fold">
        <summary>情景假设全文</summary>
        <ul class="xm-rule-list">${narratives}</ul>
      </details>
      <details class="xm-fold">
        <summary>风险限度与已披露锚</summary>
        <ul class="xm-rule-list">${stops}</ul>
        <p class="xm-table-note">${xmEscape(valuation.historyNote || "")} ${xmEscape(limits.limitsNote || "")} ${xmEscape(valuation.fxNote || "")}</p>
        <p class="xm-table-note">已披露：收入 ${xmNum(anchor.revenueYi, 1)} 亿元（${xmPct(anchor.revenueYoyPct)}），经调整净利润 ${xmNum(anchor.adjustedNetProfitYi, 1)} 亿元（${xmPct(anchor.adjustedNetProfitYoyPct)}），IFRS 净利润 ${xmNum(anchor.ifrsNetProfitYi, 1)} 亿元。${anchorUrl}</p>
        <p class="xm-table-note">${xmEscape(valuation.multipleNote || "")}</p>
      </details>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>开仓四门</h2>
        <p>通过 ${counts.pass || 0} · 需人工 ${(counts.caution || 0) + (counts.open || 0)} · 拦住 ${counts.block || 0}。拦住的门改写页首立场。</p>
      </div>
      <div class="xm-chips xm-chips--desk">${chips}</div>
      <div class="xm-matrix">${matrix}</div>
      <details class="xm-fold">
        <summary>备注写在种子文件</summary>
        <p class="xm-table-note">${xmEscape(checklist.editHint || "")}</p>
      </details>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>领先指标</h2>
        <p>有数才进图。没接入的指标只留一枚芯片。</p>
      </div>
      <h3 class="xm-subtitle">${xmEscape((indicators.autoMonthly || {}).label || "汽车月交付")}</h3>
      ${chartsOn ? `<div class="xm-chart"><canvas id="xm-delivery-chart" aria-label="汽车月交付"></canvas></div>` : `<p class="xm-table-note">${deliveryFallback}</p>`}
      <p class="xm-table-note">${xmEscape((indicators.autoMonthly || {}).source || "")} 黄柱是下限，不是精确值。已公布月份均值 ${xmInt((indicators.autoMonthly || {}).reportedAverage)} 辆。</p>
      <div class="xm-chip-row">${missChips}${grossChip}</div>
      <p class="xm-table-note">${phone.relatedRevenueYi != null ? `${xmEscape(phone.relatedLabel || "手机 × AIoT")} ${xmNum(phone.relatedRevenueYi, 1)} 亿元，不是出货量。` : ""} ${memory.value == null ? xmEscape(memory.note || "") : ""}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>业务雷达</h2>
        <p>策展条目，带来源和日期。数据缺口默认收起。没有爬虫。</p>
      </div>
      ${radarBody || `<p class="empty">${xmEscape((trader.radar || {}).error || "雷达还没生成。")}</p>`}
      <p class="xm-table-note">${xmEscape((radar && radar.disclaimer) || "仅供研究参考，不构成投资建议。")}</p>
    </section>

    <section class="panel panel--wide xm-section">
      <div class="panel__head">
        <h2>日历</h2>
        <p>未来 ${calendar.horizonDays || 60} 天 · 基准日 ${xmEscape(calendar.asOf || "—")}</p>
      </div>
      <ul class="xm-list">${upcoming}</ul>
      ${undated ? `<h3 class="xm-subtitle">日期未定</h3><ul class="xm-list">${undated}</ul>` : ""}
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

    <details class="xm-fold xm-fold--research">
      <summary>研究叙事 · ${xmEscape(stance.researchHeadline || "展开")}</summary>
      <div class="xm-fold__body">
        <p class="xm-note">${xmEscape(stance.researchLabel || "")}</p>
        <p class="xm-note">${xmEscape(stance.researchBody || "")}</p>
      </div>
    </details>
  `;
  xmMountDeskCharts(trader);
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
  const price = trader.valuation?.priceHkd;
  const pos = trader.publicSim?.positionPct;
  const change = trader.box?.changePct;
  const next = trader.calendar?.next;
  const gates = trader.checklist?.gates || [];
  const chips = gates
    .map((gate) => {
      const status = XM_STATUSES.has(gate.status) ? gate.status : "open";
      return `<span class="xm-chip xm-chip--${status}">${xmEscape(gate.label)} ${xmEscape(gate.statusLabel || "")}</span>`;
    })
    .join("");
  el.innerHTML = `
    <div class="xm-cockpit__top">
      <p class="xm-cockpit__price">${xmNum(price, 2)} <span>港元</span></p>
      <p class="xm-cockpit__pos">模拟仓 ${pos == null ? "—" : `${xmNum(pos, 1)}%`}</p>
    </div>
    ${change == null ? "" : `<p class="xm-cockpit__change ${xmChangeClass(change)}">${xmPct(change)}</p>`}
    <div class="xm-chips">${chips}</div>
    <p class="xm-cockpit__title">${next ? `${xmEscape(next.countdownLabel)} · ${xmEscape(next.title)}` : "未来 60 天无已写窗口"}</p>
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
