/** Truth Social @realDonaldTrump 镜像 — 默认中文，可切换原文 */

const TRUTH_URL = "data/trump_truth.json";
const TRUTH_POLL_MS = 5 * 60 * 1000;

let truthData = null;
let lastTruthUpdatedAt = null;
let truthToggleBound = false;

function escapeHtml(text) {
  return String(text || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatTruthTime(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return iso;
  }
}

function truthStatusLabel(status) {
  const map = {
    ok: "已同步",
    stale: "缓存数据",
    error: "拉取失败",
    missing_credentials: "拉取失败",
    empty: "暂无数据",
  };
  return map[status] || status || "—";
}

function truthLinkLabel(data) {
  const src = data?.source?.dataSource;
  if (src === "telegram_mirror") return "在 Telegram 查看";
  return "在 Truth Social 查看";
}

function truthBannerSub(data) {
  const src = data?.source;
  if (src?.dataSource === "telegram_mirror") {
    return "非官方阅读副本 · 正文默认中文 · 来源 Telegram 官方频道镜像";
  }
  return "非官方阅读副本 · 正文默认中文 · 来源 truthsocial.com";
}

function renderTruthMedia(media) {
  if (!media?.length) return "";
  return `<div class="truth-post__media">${media
    .filter((m) => m.url || m.previewUrl)
    .map(
      (m) =>
        `<a href="${escapeHtml(m.url || m.previewUrl)}" target="_blank" rel="noopener noreferrer"><img src="${escapeHtml(m.previewUrl || m.url)}" alt="${escapeHtml(m.description || "media")}" loading="lazy"></a>`
    )
    .join("")}</div>`;
}

function renderTruthTags(tags) {
  if (!tags?.length) return "";
  return `<div class="truth-post__tags">${tags
    .map((t) => `<span class="truth-tag">${escapeHtml(t.label || t.id)}</span>`)
    .join("")}</div>`;
}

function renderTruthPost(post, account, linkLabel) {
  const id = escapeHtml(post.id);
  const zh = post.contentZh || post.content || "";
  const original = post.content || "";
  const showOriginal = false;
  const avatar = account?.avatar || "";
  const name = escapeHtml(account?.displayName || "Donald J. Trump");
  const handle = escapeHtml(account?.username || "realDonaldTrump");

  return `
    <article class="truth-post" data-post-id="${id}" data-show-original="${showOriginal}">
      <div class="truth-post__head">
        ${avatar ? `<img class="truth-post__avatar" src="${escapeHtml(avatar)}" alt="${name}" loading="lazy">` : '<div class="truth-post__avatar"></div>'}
        <div class="truth-post__who">
          <p class="truth-post__name">${name}</p>
          <p class="truth-post__meta">@${handle} · ${formatTruthTime(post.publishedAt)}</p>
        </div>
      </div>
      <p class="truth-post__body truth-post__body--zh">${escapeHtml(zh)}</p>
      <p class="truth-post__body truth-post__body--original" hidden>${escapeHtml(original)}</p>
      ${renderTruthTags(post.tags)}
      ${renderTruthMedia(post.media)}
      <div class="truth-post__actions">
        <button type="button" class="truth-post__toggle" data-post-id="${id}" aria-pressed="false">显示原文</button>
        <a class="truth-post__link" href="${escapeHtml(post.url || "#")}" target="_blank" rel="noopener noreferrer">${escapeHtml(linkLabel)}</a>
        <div class="truth-post__stats">
          <span>💬 ${post.repliesCount ?? 0}</span>
          <span>🔁 ${post.reblogsCount ?? 0}</span>
          <span>❤️ ${post.favouritesCount ?? 0}</span>
        </div>
      </div>
    </article>
  `;
}

function bindTruthToggles() {
  if (truthToggleBound) return;
  const feed = document.getElementById("truth-feed");
  if (!feed) return;
  feed.addEventListener("click", (e) => {
    const btn = e.target.closest(".truth-post__toggle");
    if (!btn) return;
    const post = btn.closest(".truth-post");
    if (!post) return;
    const showOriginal = post.dataset.showOriginal !== "true";
    post.dataset.showOriginal = showOriginal ? "true" : "false";
    const zhEl = post.querySelector(".truth-post__body--zh");
    const origEl = post.querySelector(".truth-post__body--original");
    if (zhEl) zhEl.hidden = showOriginal;
    if (origEl) origEl.hidden = !showOriginal;
    btn.textContent = showOriginal ? "显示中文" : "显示原文";
    btn.classList.toggle("truth-post__toggle--active", showOriginal);
    btn.setAttribute("aria-pressed", showOriginal ? "true" : "false");
  });
  truthToggleBound = true;
}

function renderTruthPanel(data) {
  const root = document.getElementById("truth-root");
  if (!root) return;

  if (!data) {
    root.innerHTML = '<p class="truth-empty">Truth Social 数据加载中…</p>';
    return;
  }

  truthData = data;
  const account = data.account || {};
  const posts = data.posts || [];
  const status = data.status || "empty";
  const updated = data.updatedAt ? formatTruthTime(data.updatedAt) : "—";

  const linkLabel = truthLinkLabel(data);
  const topicLine = (data.topicSummary || []).length
    ? `舆情主题：${data.topicSummary
        .slice(0, 4)
        .map((t) => `${t.label}(${t.count})`)
        .join(" · ")}`
    : "";

  const emptyHtml =
  posts.length === 0
    ? `<div class="truth-empty"><p>暂无帖子数据。</p>${data.setupHint ? `<p>${escapeHtml(data.setupHint)}</p>` : ""}</div>`
    : "";

  root.innerHTML = `
    <div class="truth-app">
      <div class="truth-banner">
        <p class="truth-banner__title">Truth Social 镜像 · @realDonaldTrump</p>
        <p class="truth-banner__sub">${truthBannerSub(data)}${topicLine ? ` · ${topicLine}` : ""}</p>
      </div>
      <section class="truth-profile">
        <div class="truth-profile__header"${account.header ? ` style="background-image:url('${escapeHtml(account.header)}')"` : ""}></div>
        <div class="truth-profile__body">
          ${account.avatar ? `<img class="truth-profile__avatar" src="${escapeHtml(account.avatar)}" alt="${escapeHtml(account.displayName || "")}" loading="lazy">` : '<div class="truth-profile__avatar"></div>'}
          <h2 class="truth-profile__name">${escapeHtml(account.displayName || "Donald J. Trump")}</h2>
          <p class="truth-profile__handle">@${escapeHtml(account.username || "realDonaldTrump")}</p>
          ${account.note ? `<p class="truth-profile__handle">${escapeHtml(account.note)}</p>` : ""}
          <div class="truth-profile__stats">
            <span><strong>${account.statusesCount ?? "—"}</strong> 帖子</span>
            <span><strong>${account.followersCount ?? "—"}</strong> 粉丝</span>
          </div>
        </div>
      </section>
      <div class="truth-meta">
        <span>更新 ${updated}</span>
        <span class="truth-meta__status truth-meta__status--${status}">${truthStatusLabel(status)}</span>
      </div>
      <div class="truth-feed" id="truth-feed">
        ${posts.length ? posts.map((p) => renderTruthPost(p, account, linkLabel)).join("") : emptyHtml}
      </div>
      <p class="truth-disclaimer">${escapeHtml(data.disclaimer || "")}</p>
    </div>
  `;

  bindTruthToggles();
}

async function refreshTruthData() {
  try {
    const res = await fetch(`${TRUTH_URL}?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data.updatedAt === lastTruthUpdatedAt && truthData) return;
    lastTruthUpdatedAt = data.updatedAt;
    renderTruthPanel(data);
  } catch (err) {
    const root = document.getElementById("truth-root");
    if (root && !truthData) {
      root.innerHTML = '<p class="truth-empty">Truth Social 数据加载失败，请稍后重试。</p>';
    }
    console.warn("truth refresh failed", err);
  }
}

function initTruthModule() {
  refreshTruthData();
  setInterval(refreshTruthData, TRUTH_POLL_MS);
}
