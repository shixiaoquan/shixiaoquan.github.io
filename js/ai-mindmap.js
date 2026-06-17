/**
 * AI 产业链思维导图 — 基于 jsMind，由 app.js 调用。
 */
(function () {
  const LAYER_COLORS = {
    upstream: { bg: "#0c4a6e", fg: "#e0f2fe" },
    midstream: { bg: "#4c1d95", fg: "#ede9fe" },
    downstream: { bg: "#064e3b", fg: "#d1fae5" },
    support: { bg: "#78350f", fg: "#fef3c7" },
  };

  const MARKET_COLORS = {
    A股: { bg: "#1e3a5f", fg: "#bae6fd" },
    港股: { bg: "#3b1f4f", fg: "#e9d5ff" },
    美股: { bg: "#1a3d2e", fg: "#bbf7d0" },
  };

  let jmInstance = null;
  let metaMap = new Map();
  let stockFilter = () => [];

  function slug(text) {
    return String(text).replace(/\s+/g, "-").replace(/[^\w\u4e00-\u9fff-]/g, "");
  }

  function buildTree(chainData, filterStocks) {
    metaMap = new Map();
    stockFilter = filterStocks;

    const root = {
      id: "ai-root",
      topic: chainData.title || "AI 产业链",
      children: [],
    };
    metaMap.set("ai-root", { type: "root" });

    for (const layer of chainData.layers || []) {
      const layerShort = (layer.name || "").split("：").pop() || layer.id;
      const layerId = `layer-${layer.id}`;
      const colors = LAYER_COLORS[layer.id] || { bg: "#334155", fg: "#f1f5f9" };
      const layerNode = {
        id: layerId,
        topic: layerShort,
        "background-color": colors.bg,
        "foreground-color": colors.fg,
        children: [],
      };
      metaMap.set(layerId, { type: "layer", layer });

      const groupIndex = new Map();
      const groupOrder = [];

      for (const seg of layer.segments || []) {
        const stocks = filterStocks(seg.stocks || []);
        if (!stocks.length) continue;

        const gName = seg.group || "其他";
        if (!groupIndex.has(gName)) {
          const gId = `${layerId}-g-${slug(gName)}`;
          const gNode = { id: gId, topic: gName, children: [] };
          groupIndex.set(gName, gNode);
          groupOrder.push(gName);
          metaMap.set(gId, { type: "group", name: gName, layerId: layer.id });
        }
        const groupNode = groupIndex.get(gName);

        const segId = `${layerId}-s-${slug(seg.name)}`;
        const maxStocks = 8;
        const visible = stocks.slice(0, maxStocks);
        const stockNodes = visible.map((stock, i) => {
          const sid = `${segId}-st-${i}`;
          const mc = MARKET_COLORS[stock.market] || { bg: "#1e293b", fg: "#cbd5e1" };
          metaMap.set(sid, { type: "stock", stock, segment: seg });
          return {
            id: sid,
            topic: stock.name,
            "background-color": mc.bg,
            "foreground-color": mc.fg,
          };
        });

        if (stocks.length > maxStocks) {
          const moreId = `${segId}-more`;
          metaMap.set(moreId, { type: "more", segment: seg, stocks, hidden: stocks.slice(maxStocks) });
          stockNodes.push({
            id: moreId,
            topic: `+${stocks.length - maxStocks} 只…`,
            "background-color": "#334155",
            "foreground-color": "#94a3b8",
          });
        }

        metaMap.set(segId, { type: "segment", segment: seg, stocks });
        groupNode.children.push({
          id: segId,
          topic: `${seg.name} (${stocks.length})`,
          children: stockNodes,
        });
      }

      for (const gName of groupOrder) {
        const gNode = groupIndex.get(gName);
        if (gNode.children.length) layerNode.children.push(gNode);
      }
      if (layerNode.children.length) root.children.push(layerNode);
    }

    return {
      meta: { name: chainData.title || "ai-chain", author: "shixiaoquan" },
      format: "node_tree",
      data: root,
    };
  }

  function renderDetail(meta, detailEl) {
    if (!detailEl) return;
    if (!meta) {
      detailEl.innerHTML = '<p class="ai-mindmap-detail__empty">点击节点查看环节说明与标的详情</p>';
      return;
    }

    if (meta.type === "stock") {
      const s = meta.stock;
      detailEl.innerHTML = `
        <h4 class="ai-mindmap-detail__title">${s.name}</h4>
        <p class="ai-mindmap-detail__meta"><span class="reco-market reco-market--${s.market === "A股" ? "cn" : s.market === "港股" ? "hk" : "us"}">${s.market}</span> · ${s.symbol}</p>
        <p class="ai-mindmap-detail__desc">${s.role || ""}</p>
        <p class="ai-mindmap-detail__seg">所属环节：${meta.segment?.name || ""}</p>
      `;
      return;
    }

    if (meta.type === "segment" || meta.type === "more") {
      const seg = meta.segment;
      const stocks = meta.stocks || meta.segment?.stocks || [];
      const filtered = stockFilter(stocks);
      detailEl.innerHTML = `
        <h4 class="ai-mindmap-detail__title">${seg.name}</h4>
        <p class="ai-mindmap-detail__desc">${seg.desc || ""}</p>
        <p class="ai-mindmap-detail__meta">${seg.group || ""} · ${filtered.length} 只标的</p>
        <ul class="ai-mindmap-detail__list">
          ${filtered
            .map(
              (s) => `
            <li>
              <strong>${s.name}</strong>
              <span class="ai-mindmap-detail__sym">${s.symbol}</span>
              <span class="reco-market reco-market--${s.market === "A股" ? "cn" : s.market === "港股" ? "hk" : "us"}">${s.market}</span>
              <span class="ai-mindmap-detail__role">${s.role || ""}</span>
            </li>
          `
            )
            .join("")}
        </ul>
      `;
      return;
    }

    if (meta.type === "layer") {
      detailEl.innerHTML = `
        <h4 class="ai-mindmap-detail__title">${meta.layer.name}</h4>
        <p class="ai-mindmap-detail__desc">${meta.layer.summary || ""}</p>
      `;
      return;
    }

    if (meta.type === "group") {
      detailEl.innerHTML = `
        <h4 class="ai-mindmap-detail__title">${meta.name}</h4>
        <p class="ai-mindmap-detail__desc">点击子环节查看具体标的</p>
      `;
      return;
    }

    detailEl.innerHTML = `
      <h4 class="ai-mindmap-detail__title">AI 产业链</h4>
      <p class="ai-mindmap-detail__desc">从中心向四周展开：上游算力 → 中游模型 → 下游应用 → 配套生态。可缩放、拖拽画布，点击节点查看详情。</p>
    `;
  }

  function onSelect(node) {
    const detailEl = document.getElementById("ai-mindmap-detail");
    if (!node) {
      renderDetail(null, detailEl);
      return;
    }
    const meta = metaMap.get(node.id);
    renderDetail(meta, detailEl);
  }

  function render(chainData, filterStocks) {
    const container = document.getElementById("ai-mindmap-container");
    if (!container || !window.jsMind) return false;

    const mind = buildTree(chainData, filterStocks);

    if (!jmInstance) {
      const options = {
        container: "ai-mindmap-container",
        editable: false,
        theme: "primary",
        mode: "full",
        support_html: false,
        view: {
          engine: "canvas",
          hmargin: 140,
          vmargin: 80,
          line_width: 2,
          line_color: "#475569",
          draggable: true,
          hide_scrollbars_when_draggable: true,
        },
        layout: {
          hspace: 36,
          vspace: 18,
          pspace: 14,
        },
      };
      jmInstance = new jsMind(options);
      jmInstance.add_event_listener((type, data) => {
        if (type === jsMind.event_type.select) {
          onSelect(data.node);
        }
      });
    }

    jmInstance.show(mind);
    jmInstance.expand_all();
    onSelect(null);
    return true;
  }

  function destroy() {
    jmInstance = null;
    metaMap = new Map();
    const container = document.getElementById("ai-mindmap-container");
    if (container) container.innerHTML = "";
  }

  window.AiMindMap = { render, destroy, renderDetail };
})();
