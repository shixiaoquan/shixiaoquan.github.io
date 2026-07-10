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

  const attrT5 = ev.recoWinRateT5 != null ? `T+5 胜率 ${ev.recoWinRateT5}%` : null;
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
    const res = await fetch(`${SITE_STATUS_URL}?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data.updatedAt === window.lastSiteStatusAt && window.siteStatusData) return;
    window.lastSiteStatusAt = data.updatedAt;
    window.siteStatusData = data;
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
