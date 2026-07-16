/** 驾驶舱 · 持续进化面板 */

function pipelineStatusLabel(status) {
  const map = { ok: "运行中", stale: "数据过期", missing: "未就绪", empty: "暂无数据" };
  return map[status] || status || "—";
}

function workflowUrl(workflowFile) {
  if (!workflowFile) return null;
  return `https://github.com/shixiaoquan/shixiaoquan.github.io/actions/workflows/${workflowFile}`;
}

function renderEvolutionPanel(data) {
  const summaryEl = document.getElementById("cockpit-evolution-summary");
  const pipesEl = document.getElementById("cockpit-evolution-pipelines");
  const hintEl = document.getElementById("cockpit-evolution-hint");
  if (!summaryEl || !pipesEl) return;

  if (!data) {
    summaryEl.innerHTML = '<p class="empty">自动化状态加载中…</p>';
    pipesEl.innerHTML = "";
    return;
  }

  const ev = data.evolution || {};
  const sum = data.summary || {};
  if (hintEl) {
    const staleNote = sum.pipelinesStale ? ` · ${sum.pipelinesStale} 条过期` : "";
    hintEl.textContent = `GitHub Actions · ${sum.pipelinesHealthy ?? 0}/${sum.pipelinesTotal ?? 0} 条活跃${staleNote} · Cursor PR 审阅策略升级`;
  }

  const attrT5 =
    ev.recoWinRateT5 != null
      ? `生产 ${ev.recoWinRateT5}%${ev.shadowWinRateT5 != null ? ` · 影子 ${ev.shadowWinRateT5}%` : ""}${ev.pairedShadowWinRate != null ? ` · 配对 ${ev.pairedShadowWinRate}%` : ""}`
      : null;
  const upgradeNote = ev.strategyUpgradePending ? "待 Cursor 审阅升级" : null;
  const tuneNote =
    typeof window.marketData?.tacticTune?.buyScoreAdjust === "number" &&
    window.marketData.tacticTune.buyScoreAdjust !== 0
      ? `门槛 ${window.marketData.tacticTune.buyScoreAdjust > 0 ? "+" : ""}${window.marketData.tacticTune.buyScoreAdjust}`
      : null;

  summaryEl.innerHTML = [
    { label: "战术策略", value: ev.strategyVersion || "—" },
    { label: "大师学习迭代", value: ev.masterLearnRevision != null ? `#${ev.masterLearnRevision}` : "—" },
    { label: "荐股 T+5", value: attrT5 || "累计中" },
    { label: "自适应门槛", value: tuneNote || upgradeNote || "持有当前" },
  ]
    .map(
      (item) => `
      <div class="evolution-stat">
        <p class="evolution-stat__label">${item.label}</p>
        <p class="evolution-stat__value">${item.value}</p>
      </div>`
    )
    .join("");

  renderShadowTrack(ev);
  renderEvolutionBuckets(ev);

  const log = data.recentLog || [];
  const logHtml = log.length
    ? `<ul class="evolution-log">${log
        .map((e) => {
          const when = typeof formatFreshnessTime === "function" ? formatFreshnessTime(e.at) : e.at;
          const detail =
            e.type === "master_learn"
              ? `大师学习 #${e.revision} · ${e.regime || ""}`
              : e.type === "param_sweep"
                ? `参数搜索 · ${e.reason || ""}`
                : e.type === "reco_attribution"
                  ? `荐股归因 +${e.newItems || 0}`
                  : e.type || "event";
          return `<li><span class="evolution-log__time">${when || "—"}</span> ${detail}</li>`;
        })
        .join("")}</ul>`
    : "";

  const pipelines = data.pipelines || [];
  pipesEl.innerHTML =
    logHtml +
    pipelines
      .map((pipe) => {
        const status = pipe.status || "empty";
        const updated =
          pipe.updatedAt && typeof formatFreshnessTime === "function"
            ? formatFreshnessTime(pipe.updatedAt)
            : "—";
        const wf = workflowUrl(pipe.workflow);
        const nameHtml = wf
          ? `<a href="${wf}" target="_blank" rel="noopener noreferrer" class="evolution-pipe__link">${pipe.name}</a>`
          : pipe.name;
        return `
        <div class="evolution-pipe">
          <p class="evolution-pipe__name">${nameHtml}</p>
          <p class="evolution-pipe__meta">${pipe.schedule} · 更新 ${updated}</p>
          <span class="evolution-pipe__status evolution-pipe__status--${status}">${pipelineStatusLabel(status)}</span>
        </div>`;
      })
      .join("");

  const queueEl = document.getElementById("cockpit-evolution-queue");
  const queue = data.evolutionQueue || window.evolutionQueueData;
  if (queueEl) {
    const tasks = queue?.tasks || [];
    if (!tasks.length) {
      queueEl.innerHTML = '<p class="evolution-queue__empty">进化队列空闲 · 系统正常运转</p>';
    } else {
      queueEl.innerHTML = `
        <h3 class="evolution-queue__title">进化指令队列 <span>${tasks.length}</span></h3>
        <ul class="evolution-queue__list">${tasks
          .slice(0, 5)
          .map(
            (t) => `
          <li class="evolution-queue__item evolution-queue__item--${t.priority || "low"}">
            <strong>${t.title || t.type}</strong>
            <p>${t.reason || ""}</p>
            <code class="evolution-queue__prompt">${t.cursorPrompt || ""}</code>
          </li>`
          )
          .join("")}</ul>`;
    }
  }
}

function renderShadowTrack(ev) {
  const el = document.getElementById("cockpit-evolution-shadow");
  if (!el) return;
  const params = ev.shadowCandidateParams || {};
  const ready = ev.shadowReadyForPR;
  const stalled = ev.attributionStalled;
  const days = ev.shadowTradingDays != null ? `${ev.shadowTradingDays} 日` : "—";
  const weeks = ev.shadowWeeks != null ? `${ev.shadowWeeks} 周` : "—";
  const matured = ev.shadowMaturedT5 != null ? ev.shadowMaturedT5 : "—";
  const paired =
    ev.pairedCount != null
      ? `${ev.pairedCount} 标的${ev.marketPairedCount != null ? ` · ${ev.marketPairedCount} 市场日` : ""}`
      : "—";
  const statusClass = ready ? "ready" : stalled ? "stalled" : "tracking";
  const statusText = ready ? "可申请升级 PR" : stalled ? "归因停滞" : "积累中";
  el.innerHTML = `
    <div class="evolution-shadow__card evolution-shadow__card--${statusClass}">
      <div class="evolution-shadow__head">
        <h3>影子荐股轨</h3>
        <span class="evolution-shadow__status">${statusText}</span>
      </div>
      <p class="evolution-shadow__reason">${ev.shadowReason || "等待影子轨数据"}</p>
      <ul class="evolution-shadow__meta">
        <li>候选 buy≥${params.buyScore ?? "—"} / breakout≥${params.breakoutScoreMin ?? "—"}</li>
        <li>日历 ${weeks} · 交易日 ${days} · 成熟 ${matured}</li>
        <li>配对 ${paired}${ev.daysUntilFirstMature > 0 ? ` · 距首批成熟 ${ev.daysUntilFirstMature} 天` : ""}</li>
      </ul>
    </div>`;
}

function renderEvolutionBuckets(ev) {
  const el = document.getElementById("cockpit-evolution-buckets");
  if (!el) return;
  const decision = ev.recoDecisionBuckets || {};
  const market = ev.recoMarketBuckets || {};
  const tuneByM = ev.tacticTuneByMarket || {};

  const decisionHtml = ["高", "中", "低"]
    .map((k) => {
      const b = decision[k] || {};
      if (!b.count) return "";
      return `<span class="evo-bucket evo-bucket--dec-${k === "高" ? "high" : k === "低" ? "low" : "mid"}">决策${k} ${b.winRate ?? "—"}% <small>n=${b.count}</small></span>`;
    })
    .filter(Boolean)
    .join("");

  const marketHtml = ["A股", "港股", "美股"]
    .map((k) => {
      const b = market[k] || {};
      if (!b.count) return "";
      const adj = tuneByM[k];
      const adjText = typeof adj === "number" && adj !== 0 ? ` · 门槛${adj > 0 ? "+" : ""}${adj}` : "";
      return `<span class="evo-bucket evo-bucket--mkt">${k} ${b.winRate ?? "—"}%${adjText} <small>n=${b.count}</small></span>`;
    })
    .filter(Boolean)
    .join("");

  if (!decisionHtml && !marketHtml) {
    el.innerHTML = "";
    return;
  }
  el.innerHTML = `
    <div class="evolution-buckets__row">
      ${decisionHtml}
      ${marketHtml}
    </div>`;
}

function updateEvolutionBadge(data) {
  const evoBadge = document.getElementById("evolution-badge");
  if (!evoBadge || !data?.evolution) return;
  const rev = data.evolution.masterLearnRevision;
  const ver = data.evolution.strategyVersion;
  evoBadge.hidden = false;
  evoBadge.textContent = rev != null ? `${ver} · 学习 #${rev}` : `${ver} · 自动进化`;
}

async function refreshSiteStatus() {
  if (typeof SITE_STATUS_URL === "undefined") return;
  try {
    let data;
    if (typeof DataCache !== "undefined") {
      data = await DataCache.fetchJson(SITE_STATUS_URL, {
        onStale: (d) => {
          window.siteStatusData = d;
          renderEvolutionPanel(d);
        },
      });
    } else {
      const res = await fetch(`${SITE_STATUS_URL}?t=${Date.now()}`, { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      data = await res.json();
    }
    if (data.updatedAt === window.lastSiteStatusAt && window.siteStatusData) return;
    window.lastSiteStatusAt = data.updatedAt;
    window.siteStatusData = data;
    if (typeof EVOLUTION_QUEUE_URL !== "undefined") {
      window.evolutionQueueData = await fetch(
        `${EVOLUTION_QUEUE_URL}?t=${Date.now()}`,
        { cache: "no-store" }
      )
        .then((r) => (r.ok ? r.json() : null))
        .catch(() => null);
    }
    renderEvolutionPanel(data);
    updateEvolutionBadge(data);
    if (typeof updateHeaderFreshness === "function") updateHeaderFreshness();
  } catch (err) {
    console.warn("site status refresh failed", err);
  }
}

function initEvolutionPolling() {
  if (typeof PollScheduler === "undefined") return;
  PollScheduler.register(refreshSiteStatus);
}
