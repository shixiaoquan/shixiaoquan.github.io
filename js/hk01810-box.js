/** HK01810 箱体短线 — 规则与渲染（页面刷新时用最新报价重算建议） */

const HK01810_BOX_URL = "data/hk01810_box.json";

const HK01810_DEFAULT_LEVELS = {
  boxLow: 25.44,
  boxHigh: 29.1,
  bottom: 21.3,
  boxHeight: 3.66,
  breakoutTarget: 32.76,
  breakdownTarget: 21.78,
  fakeBreakoutBack: 28.5,
  shortCover: 26.2,
};

const HK01810_DEFAULT_BUY = [
  { id: "t1", label: "第1份", low: 25.44, high: 26.0, weight: "1/3" },
  { id: "t2", label: "第2份", low: 23.0, high: 24.0, weight: "1/3" },
  { id: "t3", label: "第3份", low: 21.5, high: 22.3, weight: "1/3" },
];

const HK01810_DEFAULT_SELL = [
  { id: "s1", label: "卖出2份", low: 28.2, high: 28.8, weight: "2/3" },
  { id: "s2", label: "卖出尾仓", low: 29.0, high: 29.1, weight: "1/3" },
];

let hk01810BoxData = null;

function hk01810Decide(
  price,
  levels = HK01810_DEFAULT_LEVELS,
  buyZones = HK01810_DEFAULT_BUY,
  sellZones = HK01810_DEFAULT_SELL,
  lotSize = 200
) {
  const boxLow = levels.boxLow;
  const boxHigh = levels.boxHigh;
  const bottom = levels.bottom;
  const boxHeight = levels.boxHeight ?? boxHigh - boxLow;

  if (price == null || Number.isNaN(Number(price))) {
    return {
      action: "unavailable",
      actionLabel: "行情不可用",
      tone: "neutral",
      operate: false,
      title: "暂无可用报价",
      detail: "刷新后重试，或等待行情流水线更新。",
      emptyAdvice: "暂不操作",
      holdingAdvice: "暂不操作",
      zoneId: null,
    };
  }

  const p = Number(price);

  if (p < bottom) {
    return {
      action: "exit",
      actionLabel: "清仓离场",
      tone: "danger",
      operate: true,
      title: `收盘价 ${p.toFixed(2)} 跌破底部 ${bottom.toFixed(2)}`,
      detail: "底部判断失效。持仓全部卖出；空仓不再抄底，等待新结构。",
      emptyAdvice: "空仓观望，停止箱体内买点",
      holdingAdvice: "清仓离场",
      zoneId: "bottom",
    };
  }

  if (p > boxHigh) {
    const target = Number((boxHigh + boxHeight).toFixed(2));
    return {
      action: "breakout_up",
      actionLabel: "向上突破 · 不追",
      tone: "warn",
      operate: false,
      title: `收盘价 ${p.toFixed(2)} 站上箱顶 ${boxHigh.toFixed(2)}`,
      detail: `日常箱子向上打开。按规则空仓不追高。测量目标约 ${target.toFixed(2)}；若跌回 28.50 下方视为假突破。`,
      emptyAdvice: "继续空仓，不在更高位置追",
      holdingAdvice: "按突破规则另议；本策略默认已在上沿卖完",
      zoneId: "breakout",
    };
  }

  for (const zone of sellZones) {
    if (p >= zone.low && p <= zone.high) {
      return {
        action: "sell",
        actionLabel: zone.label,
        tone: "sell",
        operate: true,
        title: `进入卖区 ${zone.low.toFixed(2)}–${zone.high.toFixed(2)}`,
        detail: `现价 ${p.toFixed(2)}。只卖已持有股份；卖完空仓，等下一次买区。`,
        emptyAdvice: "空仓不新开多单",
        holdingAdvice: `${zone.label}（${zone.weight}）`,
        zoneId: zone.id,
      };
    }
  }

  for (const zone of buyZones) {
    if (p >= zone.low && p <= zone.high) {
      return {
        action: "buy",
        actionLabel: `买入${zone.label}`,
        tone: "buy",
        operate: true,
        title: `进入买区 ${zone.low.toFixed(2)}–${zone.high.toFixed(2)}`,
        detail: `现价 ${p.toFixed(2)}。按收盘价确认后买入${zone.label}（${zone.weight}）。每手 ${lotSize} 股。收盘跌破 ${bottom.toFixed(2)} 全部止损。`,
        emptyAdvice: `买入${zone.label}（${zone.weight}）`,
        holdingAdvice: `若尚未买过该档，可加${zone.label}`,
        zoneId: zone.id,
      };
    }
  }

  if (p > boxLow && p < 28.2) {
    return {
      action: "wait",
      actionLabel: "箱体中部 · 观望",
      tone: "neutral",
      operate: false,
      title: `现价 ${p.toFixed(2)} 在箱子中部`,
      detail: `买区在 ${buyZones[0].low.toFixed(2)}–${buyZones[0].high.toFixed(2)} 及以下更深档；卖区在 ${sellZones[0].low.toFixed(2)} 以上。两边都不到，今天不操作。`,
      emptyAdvice: "继续空仓等待买区",
      holdingAdvice: "持有不动，不加不减",
      zoneId: "mid",
    };
  }

  if (p > 24 && p < boxLow) {
    return {
      action: "wait",
      actionLabel: "等待买区",
      tone: "neutral",
      operate: false,
      title: `现价 ${p.toFixed(2)} 低于日常箱下沿`,
      detail: `尚未进入第2份买区 23.00–24.00。收盘跌破 ${bottom.toFixed(2)} 则清仓逻辑启动。`,
      emptyAdvice: "等待进入 23.00–24.00",
      holdingAdvice: "持有观察；不在空白区加仓",
      zoneId: "gap_t1_t2",
    };
  }

  if (p > 22.3 && p < 23) {
    return {
      action: "wait",
      actionLabel: "买区之间 · 观望",
      tone: "neutral",
      operate: false,
      title: `现价 ${p.toFixed(2)} 在第2/第3份买区之间`,
      detail: "不在规则买区内，等收盘落入 23.00–24.00 或 21.50–22.30。",
      emptyAdvice: "观望",
      holdingAdvice: "持有观察",
      zoneId: "gap_t2_t3",
    };
  }

  if (p >= bottom && p < 21.5) {
    return {
      action: "watch",
      actionLabel: "贴近失效线",
      tone: "warn",
      operate: false,
      title: `现价 ${p.toFixed(2)} 贴近底部 ${bottom.toFixed(2)}`,
      detail: `尚未进入第3份买区 21.50–22.30。回到该区间再买第3份；收盘跌破 ${bottom.toFixed(2)} 则清仓。`,
      emptyAdvice: "只观察，等 21.50–22.30",
      holdingAdvice: "高度警戒；跌破清仓",
      zoneId: "near_bottom",
    };
  }

  return {
    action: "wait",
    actionLabel: "观望",
    tone: "neutral",
    operate: false,
    title: `现价 ${p.toFixed(2)}`,
    detail: "未落入买卖区。",
    emptyAdvice: "观望",
    holdingAdvice: "持有观察",
    zoneId: null,
  };
}

function hk01810ResolvePrice(boxData, marketData) {
  const fromBox = boxData?.quote?.price;
  const stock = marketData?.stocks?.find((s) => s.symbol === "1810.HK");
  const fromMarket = stock?.price ?? marketData?.quoteMap?.["1810.HK"];
  if (typeof fromMarket === "number") return { price: fromMarket, source: "market" };
  if (typeof fromBox === "number") return { price: fromBox, source: "box" };
  return { price: null, source: null };
}

function hk01810Enrich(boxData, marketData) {
  const base = boxData || {
    levels: HK01810_DEFAULT_LEVELS,
    buyZones: HK01810_DEFAULT_BUY,
    sellZones: HK01810_DEFAULT_SELL,
    lotSize: 200,
    symbol: "1810.HK",
    name: "小米集团-W",
  };
  const { price, source } = hk01810ResolvePrice(base, marketData);
  const advice = hk01810Decide(
    price,
    base.levels || HK01810_DEFAULT_LEVELS,
    base.buyZones || HK01810_DEFAULT_BUY,
    base.sellZones || HK01810_DEFAULT_SELL,
    base.lotSize || 200
  );
  const levels = base.levels || HK01810_DEFAULT_LEVELS;
  let positionInBox = null;
  if (price != null && levels.boxHigh !== levels.boxLow) {
    positionInBox = Math.max(0, Math.min(1, (price - levels.boxLow) / (levels.boxHigh - levels.boxLow)));
  }
  return {
    ...base,
    livePrice: price,
    livePriceSource: source,
    positionInBox,
    advice,
  };
}

function hk01810ToneClass(tone) {
  const map = {
    buy: "hkbox-advice--buy",
    sell: "hkbox-advice--sell",
    danger: "hkbox-advice--danger",
    warn: "hkbox-advice--warn",
    neutral: "hkbox-advice--neutral",
  };
  return map[tone] || map.neutral;
}

function hk01810FormatPct(value) {
  if (value == null || Number.isNaN(Number(value))) return "—";
  const n = Number(value);
  const sign = n > 0 ? "+" : "";
  return `${sign}${n.toFixed(2)}%`;
}

function hk01810FormatPrice(value) {
  if (value == null || Number.isNaN(Number(value))) return "—";
  return Number(value).toFixed(2);
}

function hk01810MarkerClass(pct) {
  const clamped = Math.max(0, Math.min(100, Math.round(pct / 5) * 5));
  return `hkbox-ruler__marker--p${clamped}`;
}

function renderHk01810Box(boxData, marketData) {
  const root = document.getElementById("hk01810-root");
  if (!root) return;
  const data = hk01810Enrich(boxData, marketData);
  hk01810BoxData = data;
  const advice = data.advice || {};
  const levels = data.levels || HK01810_DEFAULT_LEVELS;
  const quote = data.quote || {};
  const price = data.livePrice;
  const changePct = quote.changePct;
  const updated =
    typeof formatDateTime === "function" ? formatDateTime(data.updatedAt) : data.updatedAt || "—";

  const markerPct = data.positionInBox == null ? 50 : Math.round(data.positionInBox * 100);
  const markerClass = hk01810MarkerClass(markerPct);

  const buyRows = (data.buyZones || HK01810_DEFAULT_BUY)
    .map(
      (z) => `<tr class="${advice.zoneId === z.id ? "hkbox-row--active" : ""}">
        <td>${z.label}</td>
        <td>${z.low.toFixed(2)}–${z.high.toFixed(2)}</td>
        <td>${z.weight}</td>
      </tr>`
    )
    .join("");
  const sellRows = (data.sellZones || HK01810_DEFAULT_SELL)
    .map(
      (z) => `<tr class="${advice.zoneId === z.id ? "hkbox-row--active" : ""}">
        <td>${z.label}</td>
        <td>${z.low.toFixed(2)}–${z.high.toFixed(2)}</td>
        <td>${z.weight}</td>
      </tr>`
    )
    .join("");

  const recent = (quote.recentBars || []).slice(-8).reverse();
  const recentRows = recent.length
    ? recent
        .map(
          (b) => `<tr>
            <td>${b.date || "—"}</td>
            <td>${hk01810FormatPrice(b.close)}</td>
            <td>${hk01810FormatPrice(b.high)}</td>
            <td>${hk01810FormatPrice(b.low)}</td>
          </tr>`
        )
        .join("")
    : `<tr><td colspan="4">暂无近期 K 线</td></tr>`;

  const operateText = advice.operate ? "今日有操作信号" : "今日不操作";
  const breakoutTarget = levels.breakoutTarget ?? levels.boxHigh + levels.boxHeight;

  root.innerHTML = `
    <header class="hkbox-hero">
      <div>
        <p class="hkbox-hero__eyebrow">Box Swing · 高抛低吸</p>
        <h2 class="hkbox-hero__title">${data.name || "小米集团-W"}</h2>
        <p class="hkbox-hero__meta">${data.symbolAlias || "HK01810"} · ${data.symbol || "1810.HK"} · 每手 ${data.lotSize || 200} 股</p>
      </div>
      <div class="hkbox-hero__quote">
        <p class="hkbox-hero__price">${hk01810FormatPrice(price)} <span>港元</span></p>
        <p class="hkbox-hero__change ${Number(changePct) >= 0 ? "change--up" : "change--down"}">${hk01810FormatPct(changePct)}</p>
        <p class="hkbox-hero__asof">参考价来源 ${data.livePriceSource || "—"} · 策略更新 ${updated}</p>
      </div>
    </header>

    <section class="hkbox-advice ${hk01810ToneClass(advice.tone)}" aria-live="polite">
      <div class="hkbox-advice__head">
        <p class="hkbox-advice__kicker">${operateText}</p>
        <h3 class="hkbox-advice__label">${advice.actionLabel || "观望"}</h3>
      </div>
      <p class="hkbox-advice__title">${advice.title || ""}</p>
      <p class="hkbox-advice__detail">${advice.detail || ""}</p>
      <div class="hkbox-advice__split">
        <article>
          <h4>空仓</h4>
          <p>${advice.emptyAdvice || "—"}</p>
        </article>
        <article>
          <h4>已有持仓</h4>
          <p>${advice.holdingAdvice || "—"}</p>
        </article>
      </div>
    </section>

    <section class="panel panel--wide hkbox-panel">
      <div class="panel__head">
        <h2>箱体标尺</h2>
        <p>日常箱子 ${levels.boxLow.toFixed(2)}–${levels.boxHigh.toFixed(2)} · 底部失效 ${levels.bottom.toFixed(2)}</p>
      </div>
      <div class="hkbox-ruler" aria-hidden="true">
        <div class="hkbox-ruler__track">
          <span class="hkbox-ruler__buy"></span>
          <span class="hkbox-ruler__mid"></span>
          <span class="hkbox-ruler__sell"></span>
          <span class="hkbox-ruler__marker ${markerClass}"></span>
        </div>
        <div class="hkbox-ruler__labels">
          <span>${levels.bottom.toFixed(2)}</span>
          <span>${levels.boxLow.toFixed(2)}</span>
          <span>${hk01810FormatPrice(price)}</span>
          <span>${levels.boxHigh.toFixed(2)}</span>
        </div>
      </div>
    </section>

    <div class="hkbox-grid">
      <section class="panel">
        <div class="panel__head"><h2>买入区</h2><p>分 3 份 · 收盘确认</p></div>
        <div class="table-wrap">
          <table class="data-table">
            <thead><tr><th>档位</th><th>价格</th><th>仓位</th></tr></thead>
            <tbody>${buyRows}</tbody>
          </table>
        </div>
      </section>
      <section class="panel">
        <div class="panel__head"><h2>卖出区</h2><p>只卖已买到的股份</p></div>
        <div class="table-wrap">
          <table class="data-table">
            <thead><tr><th>档位</th><th>价格</th><th>仓位</th></tr></thead>
            <tbody>${sellRows}</tbody>
          </table>
        </div>
      </section>
    </div>

    <div class="hkbox-grid">
      <section class="panel">
        <div class="panel__head"><h2>规则摘要</h2></div>
        <ul class="hkbox-rules">
          <li>箱子内：靠近下沿买、靠近上沿卖；中部不操作。</li>
          <li>收盘站上 ${levels.boxHigh.toFixed(2)}：空仓不追；测量目标约 ${Number(breakoutTarget).toFixed(2)}。</li>
          <li>收盘跌破 ${levels.bottom.toFixed(2)}：底部判断失效，清仓。</li>
          <li>假突破：盘中刺破、收盘回到箱子内，仍按原箱子做。</li>
          <li>${data.disclaimer || "仅供参考，不构成投资建议。"}</li>
        </ul>
      </section>
      <section class="panel">
        <div class="panel__head"><h2>近 8 日</h2><p>收盘 / 最高 / 最低</p></div>
        <div class="table-wrap">
          <table class="data-table">
            <thead><tr><th>日期</th><th>收盘</th><th>高</th><th>低</th></tr></thead>
            <tbody>${recentRows}</tbody>
          </table>
        </div>
      </section>
    </div>
  `;
}

async function refreshHk01810Box(marketData) {
  let box = hk01810BoxData;
  try {
    if (typeof fetchJson === "function") {
      box = (await fetchJson(HK01810_BOX_URL)) || box;
    } else {
      const res = await fetch(`${HK01810_BOX_URL}?t=${Date.now()}`, { cache: "no-store" });
      if (res.ok) box = await res.json();
    }
  } catch (err) {
    console.error("hk01810 box load failed", err);
  }
  const md = marketData || (typeof window !== "undefined" ? window.marketData : null) || null;
  renderHk01810Box(box, md);
  renderCockpitHk01810(box, md);
}

function renderCockpitHk01810(boxData, marketData) {
  const el = document.getElementById("cockpit-hk01810");
  if (!el) return;
  const data = hk01810Enrich(boxData, marketData);
  const advice = data.advice || {};
  const price = data.livePrice;
  el.innerHTML = `
    <p class="hkbox-cockpit__price">${hk01810FormatPrice(price)} 港元</p>
    <p class="hkbox-cockpit__action">${advice.actionLabel || "观望"}</p>
    <p class="hkbox-cockpit__hint">${advice.emptyAdvice || advice.detail || "箱体高抛低吸"}</p>
  `;
}

window.hk01810Decide = hk01810Decide;
window.renderHk01810Box = renderHk01810Box;
window.refreshHk01810Box = refreshHk01810Box;
window.renderCockpitHk01810 = renderCockpitHk01810;
