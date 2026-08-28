# 投资决策日报 · 收盘前瞻

**2026年08月28日 23:45（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-08-28 14:22 · 宏观：2026-08-28 14:22 · 问财：2026-08-28 13:21

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.53%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +10.17%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **6** 只、
下跌 **0** 只，平均涨跌 **+0.53%**。

**美股** +0.83%（偏强）；**港股** +0.20%（震荡）；**A股** +0.09%（震荡）。相对强势区域：美股。

**波动居前指数：**

- **纳斯达克** 26,541.35，日涨跌 +1.57%（周 +1.82% / 月 +8.58%）
- **标普 500** 7,730.99，日涨跌 +0.72%（周 +1.18% / 月 +5.67%）
- **日经 225** 66,380.90，日涨跌 +0.38%（周 +0.55% / 月 +8.05%）
- **道琼斯** 53,569.44，日涨跌 +0.20%（周 +1.54% / 月 +3.83%）

### 1.2 A股短线情绪

问财统计涨停 **70** 家、跌停 **4** 家，情绪定性 **偏多**，涨跌停比约 **17.5 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 14.5（normal）
- **美10Y收益率** 4.67%
- **10Y-2Y 利差（FRED）** 0.47%（偏窄）
- **USDCNH** 6.7200（日 —）
- **美股行业**：科技 领涨，必需消费 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.66（变动 +0.43%，2026-08-26）
- 10Y-2Y 利差：0.47（变动 0.00%，2026-08-27）
- 联邦基金利率：3.63（变动 0.00%，2026-07-01）
- 美国失业率：4.1（变动 -2.38%，2026-07-01）
- 美元/人民币(官方)：6.721（变动 -0.02%，2026-08-21）
- 美国CPI指数：332.8（变动 +1.63%，2026-07-01）

**Finnhub 宏观要闻**
- [Iran war diplomacy turns toward reopening Strait of Hormuz - Reuters](https://news.google.com/rss/articles/CBMirgFBVV95cUxObFhWQ0dIN3p1bUEzcUdpNlN2VFhmaWRhUk5zbkhfWE45U2swM1ViQ0RvRHhxZjJfT2xaUEhnWU9jZ3MzRXl3bXdabG1mM0xpTmdoRzZEQ3dRNDJOVEpTUnJfX3lCV0s4b2RPSzhPbXlZSllrb1l6SjA0NVRVRzNRR0pBYWFwTWdPU0xtOTduNnUyd3hpZjFUUDZUb1NnMkRoanl1Z2V5SjIwYWpubGc?oc=5)（Reuters）
- [Oil on track for weekly loss even as Iran tensions simmer - Reuters](https://news.google.com/rss/articles/CBMioAFBVV95cUxNMDRjQUkzbzJPY3ZkSGVLX1NmU05FVWxRUXZod3V6MkU5TTUxTjl0cm5yMzB2R0UyMy1mUUZsZVZ5TkVGMkdXNWR1X0FqUk5OaFRsZjg4NVhreGM5bUFHQ1BiT1E0SFB1ZzJKNlVLdGFRZ2ZEd1BEV0s5ZFBEOVdtWHMtZzh3b0lBaHhHSkdSYTZWNWUzSjhNX1RLcEg0My1x?oc=5)（Reuters）
- [US-hosted G20 finance meeting to target growth, imbalances, Iran sanctions, Treasury official says - Reuters](https://news.google.com/rss/articles/CBMivAFBVV95cUxNNW43Vk95endNOWY5dnh3SUs0amx5SDJXVEFuWTRoX0F0Vnl6azdkM3NYWmRMZXZPZ0pIRkpZTmZrcExyVG9GWVYyaHlXeFR6aVR1dS15RWcyNmxWZVNDNTBmRXRQSU9ESG1BcHE2YWU0d0M5MW1fcDgtUFFQYnZRTDYxMEp6S2l1c1ZaS3hodWRnSnlPR3hBLVFSLWlCUXR4SlFrb0Z6dnpCVFZneS1CZzVPR2JoRUJ5am0zdw?oc=5)（Reuters）
- [After six months, the Iran war has reached its endgame — a costly stalemate - Reuters](https://news.google.com/rss/articles/CBMitAFBVV95cUxPanlhWGJGcHdKencyMnlRUHBUejVOZlByMTJjWm8wSVVOdWRZV3FBQUlFNFI1WXVqTUdQaEtFeEJkeHl4aTEwaXJmd0MwTFY4VmJOMS02cWJ6ZGZzVEczaGFNelFqdmJoeFNhMGlzNzVzQ3hQOVFtejNvRXZqcVBQek5zY2l2VERfVlk4aHd3WXQ4YTc0MVhIdXF6ZHA4bFVBRlNNWXlKS0ZnbU1JdFo3MWFzMDg?oc=5)（Reuters）
- [Jim Cramer says Nvidia and Salesforce earnings upended two bear narratives](https://www.cnbc.com/2026/08/27/cramer-nvidia-salesforce-earnings-upended-two-bear-narratives.html)（CNBC）

**财报日历（关注标的）**
- **ARDC** 2026-09-04  · EPS预期 —
- **BDJ** 2026-09-04  · EPS预期 —
- **BYSI** 2026-09-04  · EPS预期 —
- **HURC** 2026-09-04  · EPS预期 —
- **KNOP** 2026-09-04  · EPS预期 0.15
- **PAXS** 2026-09-04  · EPS预期 —
- 美股行业轮动：科技 领涨（+3.16%），必需消费 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +10.17%，仓位 37.0%，持股 14,574 股，均价 23.75。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.94 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +26.40%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +8.70%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +60.29%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 中国平安(38.9分) · 港股最高 小米集团(37.0分) · 美股最高 英伟达(83.2分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **英伟达**（美股）| 趋势达标待突破 | 评分 83.2 | 待突破 | 趋势过滤通过 | 止损缓冲 7.1% / 目标空间 25.7% | 决策 58.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 -5.64% | 距止损 3.1% | 距目标 +38.5% | 持有 25 天 ⚠️ 接近止损


**候选池前列**（按评分）：

- 英伟达 83.2分 趋势达标待突破 RSI 61.3 RS +15.91%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.754）。

*在线学习：市场环境 risk_on · 修订 r754 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.3 · PEG 8.52 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 15.33 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.7 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 19.68 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 78.6 | 符合风格 · 建议关注 | PE 6.9 · PEG 9.84 · ROE 11.9%

  - PE 6.89 — 深度价值区间，安全边际充足；PB 0.88 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 78.6 | 符合风格 · 建议关注 | PE 6.7 · PEG 0.13 · ROE 13.1%

  - PE 6.71 — 深度价值区间，安全边际充足；PB 0.98 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.0 · PEG 0.27 · ROE 9.2%

  - PEG 0.27 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.7 · PEG 0.62 · ROE 24.8%

  - PEG 0.62 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **谷歌**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 17.1 · PEG 5.83 · ROE 48.7%

  - ROE 48.68% — 优质复利机器，芒格会长期持有；净利率 54.77% — 轻资产高毛利特征

- **微软**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 28.1 · PEG 0.89 · ROE 34.0%

  - ROE 34.04% — 优质复利机器，芒格会长期持有；净利率 40.3% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.0 · PEG 0.27 · ROE 9.2%

  - 近一月 -9.23% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.7 · ROE 12.6%

  - 近一月 -9.99% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **亚马逊**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 20.9 · PEG 8.64 · ROE 30.6%

  - 近一月 +13.06% — 趋势强劲，反身性正反馈；相对强度 +7.39% — 跑赢大盘，宏观共振

- **微软**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 28.1 · PEG 0.89 · ROE 34.0%

  - 近一月 +29.57% — 趋势强劲，反身性正反馈；相对强度 +23.9% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 375.6 · PEG 6.61 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 121.9 · PEG 76.67 · ROE 10.2%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：影子 T+5 50.7%/-0.86% vs 生产 62.2%/0.51% · 140 笔成熟

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 64.4% 良好，门槛 -1; 偏多环境 T+5 胜率 72.3% 良好，门槛 -1

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **Nvidia’s Monster Quarter Wins Praise From Elon Musk, ‘Big Short’ Investor And Ex-Trump Adviser As AI Bears Get ‘Shredded’**（NVDA）
  Steve Eisman said “the AI story goes on,” but identified OpenAI and Anthropic as its potential weak points.…
- [Yahoo] **Is $100,000 the Magic Number to Bring Back Bitcoin Investors? Anthony Scaramucci Makes a Bold Case to Buy BTC Now.**（^GSPC）
  Anthony Scaramucci's assessment of Bitcoin highlights the risks investors face with the cryptocurrency.…
- [Yahoo] **Shares turn cautious ahead of Warsh's Jackson Hole debut; FX, bonds hold breath**（NVDA）
  By Stella Qiu SYDNEY, Aug 28 (Reuters) - Shares in Asia turned cautious on Friday after a Nvidia-fuelled technology rall…
- [Yahoo] **Dow Jones Futures Rise With Fed Chief Warsh Due; Nvidia, These 7 Stocks Are In Buy Zones**（^GSPC）
  Nvidia broke out on earnings but didn't have coattails. Meanwhile several software stocks flashed buy signals on a trio …
- [Yahoo] **Nasdaq Futures Sink While S&P 500, Dow Futures Gain Ahead Of Fed Chief Warsh’s Jackson Hole Speech: PYPL, MRVL, IREN, AFRM Stocks In Focus**（^IXIC）
  Kevin Warsh is scheduled to speak on Friday at the Fed’s annual symposium in Jackson Hole, Wyoming.…
- [Yahoo] **Asian shares mostly gain after upbeat results for Nvidia and others lift US stocks**（000001.SS）
  Shares were mostly higher Friday in Asia after Nvidia and other technology stocks led an advance on Wall Street. U.S. fu…

---

## 七、风险提示

1. 本报告基于公开行情与规则化模型，**不构成投资建议**；战术实验与战役 XRPS 为相互独立的两套体系，请勿混仓决策。  
2. 港股 / 美股存在汇率、流动性及隔夜缺口风险；A股须关注涨跌停制度下的执行偏差。  
3. 问财等非官方数据源可能延迟或缓存；涨停榜等情绪指标需与实时盘口交叉验证。  
4. 模拟盘收益不代表未来表现；连阴月加仓逻辑基于历史回测，极端宏观冲击下可能失效。
5. 大师风格荐股为规则化模拟，非真实人物操作建议；基本面数据可能有延迟或缺失。

---

## 八、本时段关注清单

1. 小米滚动卖出触发：涨 40% @ 35.32
2. 小米回撤买回触发：回撤 20% @ 25.50
3. ⚠️ 亚马逊 距止损仅 3.1%
4. 待突破观察：英伟达 突破位 227.92
5. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-08-28-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
