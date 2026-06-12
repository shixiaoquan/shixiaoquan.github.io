(function () {
  'use strict';

  const globalIndices = [
    { name: '上证指数', code: '000001.SS', market: '上海', price: 3368.07, change: 28.56, pct: 0.86 },
    { name: '深证成指', code: '399001.SZ', market: '深圳', price: 10254.32, change: -45.18, pct: -0.44 },
    { name: '恒生指数', code: 'HSI', market: '香港', price: 20112.54, change: 156.73, pct: 0.79 },
    { name: '道琼斯工业', code: 'DJIA', market: '美国', price: 42456.80, change: -112.35, pct: -0.26 },
    { name: '纳斯达克综合', code: 'IXIC', market: '美国', price: 19234.56, change: 89.23, pct: 0.47 },
    { name: '标普500', code: 'SPX', market: '美国', price: 5892.45, change: 12.67, pct: 0.22 },
    { name: '日经225', code: 'N225', market: '日本', price: 38460.12, change: -234.56, pct: -0.61 },
    { name: '富时100', code: 'FTSE', market: '英国', price: 8234.78, change: 45.32, pct: 0.55 },
  ];

  const stocks = [
    {
      name: '小米集团', code: '1810.HK', exchange: '港交所', currency: 'HKD',
      price: 58.35, change: 1.85, pct: 3.27,
      high: 59.20, low: 56.80, volume: '3.2亿',
      ma5: 56.80, ma20: 54.20, rsi: 62.5,
      intraday: [56.80, 57.20, 57.50, 57.10, 57.80, 58.00, 57.60, 58.30, 58.50, 58.10, 57.90, 58.35]
    },
    {
      name: '泡泡玛特', code: '9992.HK', exchange: '港交所', currency: 'HKD',
      price: 112.60, change: -3.40, pct: -2.93,
      high: 116.50, low: 111.80, volume: '1.8亿',
      ma5: 114.20, ma20: 108.50, rsi: 48.3,
      intraday: [115.80, 115.20, 114.60, 115.00, 113.80, 114.20, 113.50, 113.00, 112.40, 112.80, 112.20, 112.60]
    },
    {
      name: 'SK海力士', code: '000660.KS', exchange: '韩交所', currency: 'KRW',
      price: 198500, change: 4500, pct: 2.32,
      high: 201000, low: 194000, volume: '850万',
      ma5: 195200, ma20: 189800, rsi: 68.1,
      intraday: [194000, 195500, 196200, 195800, 197000, 197500, 196800, 198000, 198500, 197800, 198200, 198500]
    }
  ];

  const news = [
    { source: '财联社', time: '14:32', title: '美联储会议纪要释放鸽派信号，市场预期年内降息两次', summary: '最新公布的美联储FOMC会议纪要显示，多数委员认为当前通胀数据支持逐步降息的路径，市场对此反应积极。', tag: '宏观政策' },
    { source: '华尔街见闻', time: '13:15', title: '小米SU7交付量持续攀升，机构上调目标价至68港元', summary: '小米汽车4月交付量突破2万辆，多家投行上调小米集团目标价，看好智能汽车业务长期增长潜力。', tag: '个股动态' },
    { source: '证券时报', time: '11:48', title: '泡泡玛特海外业务营收同比增长超200%', summary: '泡泡玛特公布季度运营数据，海外市场表现亮眼，东南亚及欧美地区门店扩张顺利，潮玩出海战略成效显著。', tag: '公司财报' },
    { source: '路透社', time: '10:20', title: 'SK海力士HBM芯片订单排至明年，半导体周期持续上行', summary: '受AI算力需求推动，SK海力士HBM3E芯片订单已排至2026年，公司计划扩大产能以满足英伟达等客户需求。', tag: '行业动态' },
    { source: '新华社', time: '09:05', title: 'A股三大指数集体高开，北向资金净流入超50亿', summary: '受外围市场提振，A股今日高开高走，新能源、半导体板块领涨，市场情绪显著回暖。', tag: '市场综述' },
    { source: '第一财经', time: '08:30', title: '日本央行维持利率不变，日元汇率波动加剧', summary: '日本央行今日维持基准利率在0.25%不变，但暗示年内可能进一步收紧货币政策，日元兑美元汇率出现较大波动。', tag: '央行动态' },
  ];

  function fmt(n, decimals) {
    if (n === undefined || n === null) return '--';
    return n.toLocaleString('zh-CN', { minimumFractionDigits: decimals || 2, maximumFractionDigits: decimals || 2 });
  }

  function cls(v) {
    if (v > 0) return 'up';
    if (v < 0) return 'down';
    return 'flat';
  }

  function arrow(v) {
    if (v > 0) return '▲';
    if (v < 0) return '▼';
    return '—';
  }

  function renderIndices() {
    var html = '';
    globalIndices.forEach(function (idx) {
      var c = cls(idx.change);
      var barW = Math.min(Math.abs(idx.pct) * 20, 100);
      html += '<div class="index-card">' +
        '<div class="index-header">' +
          '<span class="index-name">' + idx.name + '</span>' +
          '<span class="index-market">' + idx.market + '</span>' +
        '</div>' +
        '<div class="index-price">' + fmt(idx.price) + '</div>' +
        '<div class="index-change ' + c + '">' +
          '<span class="arrow">' + arrow(idx.change) + '</span>' +
          '<span>' + (idx.change > 0 ? '+' : '') + fmt(idx.change) + '</span>' +
          '<span>' + (idx.pct > 0 ? '+' : '') + idx.pct.toFixed(2) + '%</span>' +
        '</div>' +
        '<div class="index-bar"><div class="index-bar-fill ' + c + '" style="width:' + barW + '%"></div></div>' +
      '</div>';
    });
    document.getElementById('globalIndices').innerHTML = html;
  }

  function renderStocks() {
    var html = '';
    stocks.forEach(function (s, i) {
      var c = cls(s.change);
      html += '<div class="stock-card">' +
        '<div class="stock-header">' +
          '<div><div class="stock-name">' + s.name + '</div><div class="stock-code">' + s.code + '</div></div>' +
          '<span class="stock-exchange">' + s.exchange + '</span>' +
        '</div>' +
        '<div class="stock-price-row">' +
          '<span class="stock-price">' + (s.currency === 'KRW' ? fmt(s.price, 0) : fmt(s.price)) + ' ' + s.currency + '</span>' +
          '<span class="stock-change-badge ' + c + '">' + (s.change > 0 ? '+' : '') + s.pct.toFixed(2) + '%</span>' +
        '</div>' +
        '<div class="stock-meta">' +
          '<div class="meta-item"><div class="meta-label">最高</div><div class="meta-value">' + fmt(s.high) + '</div></div>' +
          '<div class="meta-item"><div class="meta-label">最低</div><div class="meta-value">' + fmt(s.low) + '</div></div>' +
          '<div class="meta-item"><div class="meta-label">成交量</div><div class="meta-value">' + s.volume + '</div></div>' +
        '</div>' +
        '<div class="stock-meta">' +
          '<div class="meta-item"><div class="meta-label">MA5</div><div class="meta-value">' + fmt(s.ma5) + '</div></div>' +
          '<div class="meta-item"><div class="meta-label">MA20</div><div class="meta-value">' + fmt(s.ma20) + '</div></div>' +
          '<div class="meta-item"><div class="meta-label">RSI</div><div class="meta-value">' + s.rsi.toFixed(1) + '</div></div>' +
        '</div>' +
        '<div class="stock-chart-wrap"><canvas id="stockChart' + i + '"></canvas></div>' +
      '</div>';
    });
    document.getElementById('stockCards').innerHTML = html;

    stocks.forEach(function (s, i) {
      var canvas = document.getElementById('stockChart' + i);
      if (!canvas) return;
      var c = cls(s.change);
      var color = c === 'up' ? '#ef4444' : c === 'down' ? '#22c55e' : '#6b7280';
      new Chart(canvas, {
        type: 'line',
        data: {
          labels: s.intraday.map(function (_, j) { return j + ''; }),
          datasets: [{
            data: s.intraday,
            borderColor: color,
            backgroundColor: color + '15',
            fill: true,
            tension: 0.4,
            pointRadius: 0,
            borderWidth: 2,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { display: false },
            y: { display: false }
          }
        }
      });
    });
  }

  function renderNews() {
    var html = '';
    news.forEach(function (n) {
      html += '<div class="news-item">' +
        '<div class="news-meta">' +
          '<span class="news-source">' + n.source + '</span>' +
          '<span class="news-time">今天 ' + n.time + '</span>' +
        '</div>' +
        '<div class="news-title">' + n.title + '</div>' +
        '<div class="news-summary">' + n.summary + '</div>' +
        '<span class="news-tag">' + n.tag + '</span>' +
      '</div>';
    });
    document.getElementById('newsList').innerHTML = html;
  }

  function updateTime() {
    var now = new Date();
    var str = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0') + ' ' +
      String(now.getHours()).padStart(2, '0') + ':' +
      String(now.getMinutes()).padStart(2, '0') + ':' +
      String(now.getSeconds()).padStart(2, '0');
    document.getElementById('updateTime').textContent = '最后更新: ' + str;
  }

  renderIndices();
  renderStocks();
  renderNews();
  updateTime();
  setInterval(updateTime, 1000);
})();
