# 投资决策日报 · 收盘前瞻

**2026年08月06日 14:21（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-08-06 12:24 · 宏观：2026-08-06 12:24 · 问财：2026-08-06 11:31

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **-0.56%**，综合情绪 **偏空**。风险厌恶情绪抬升，战术新开仓宜降频或观望；战役仓按网格纪律执行，避免情绪化减仓。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +8.86%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **2** 只、
下跌 **4** 只，平均涨跌 **-0.56%**。

**美股** -0.17%（震荡）；**港股** -1.75%（偏弱）；**A股** +0.01%（震荡）。相对弱势区域：港股，战术配置宜降权。

**波动居前指数：**

- **恒生指数** 25,463.51，日涨跌 -1.75%（周 -1.53% / 月 +5.22%）
- **日经 225** 65,543.20，日涨跌 -1.14%（周 +5.94% / 月 -3.98%）
- **纳斯达克** 26,363.44，日涨跌 -0.83%（周 +7.86% / 月 +2.11%）
- **道琼斯** 54,349.12，日涨跌 +0.49%（周 +5.34% / 月 +2.69%）

### 1.2 A股短线情绪

问财统计涨停 **58** 家、跌停 **1** 家，情绪定性 **偏多**，涨跌停比约 **58.0 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。

### 1.3 宏观与跨资产

- **VIX** 15.8（normal）
- **美10Y收益率** 4.62%
- **10Y-2Y 利差（FRED）** 0.45%（偏窄）
- **USDCNH** 6.7500（日 —）
- **美股行业**：健康 领涨，能源 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.63（变动 -1.49%，2026-08-04）
- 10Y-2Y 利差：0.45（变动 +4.65%，2026-08-05）
- 联邦基金利率：3.63（变动 0.00%，2026-07-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.7509（变动 -0.06%，2026-07-31）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [Yen and dollar drift on Iran deal concerns, payroll jitters - Reuters](https://news.google.com/rss/articles/CBMiqgFBVV95cUxQT2VsMnRGWG5QTmNmeVNLM21MZHV1dkdiRnBOWnNrZUdicjNhZTB3M3JjLTdJVGk0VTc4VjhEUkxtdUpGZ0J5bV9BMklYVWhSb1lMQkFlWk1JRm5SY3BmcU1tUkhUbWNaRGZDUHhNcW42RU1QZ0Y0ODdxWXZSa1l4OWxfSVlhMEx1ODdCZUI5UlJRUUpmMEJ4Z3lFOERXVWFXRGRjV3h1MjRlQQ?oc=5)（Reuters）
- [Asia shares ease on tech pullback, oil stable as Iran talks stay in focus - Reuters](https://news.google.com/rss/articles/CBMigwFBVV95cUxNcE5UZ1dJanFrQ1hFUUNWWmM2N2cxckRKUFYtOHNLUHhtVkdpLXpmNXZjeVMzd2dycVUxSmVlNU54aE1DLVFnMmY0VnVsZk1IT1puQVQydHlUS19RNkVhRXlfbU1fdlhIZ0tORnBOWHl4a2dUZFUyZFpoUzZuZDFkUFZucw?oc=5)（Reuters）
- [Gold touches seven-week high on Strait of Hormuz reopening hopes - Reuters](https://news.google.com/rss/articles/CBMiqgFBVV95cUxQVWd6ZjFIZXZHQ2JsNi1UdXBvS1JIUm0xYWtjaDQ1UXVOczhzTzZLNEY0ZTRtb1l5N2lrY09ERHFySlMyakJJNndhRUx5M0FabFZ5TllJZWZPU05na2VqMkRVckJ2VndLdUlFUGd1NklHQlN6V1VJUzRxS09jUmtVVWhMTGRuVlN3YzctZjhBWVI2UUZkQkJqZ0NvdF9uQ1I0RGtCNVNORThqQQ?oc=5)（Reuters）
- [Oil prices slip as Iran-Oman talks fuel hopes for US-Iran peace deal - Reuters](https://news.google.com/rss/articles/CBMiswFBVV95cUxQTmw0WV9PeEJVU0pBczd6UzhWSjdUMlQ2aDhwUGxDbWdvc3hMakw5d3h3Q2wxMXNRakctZjRlTW8wNi1PNnU2eDY0anYxakZYSkZBSVN6SUhJOEF4aW1HSTVnUWREc3k2dFBvUEl0azM4TXFoV1I1S1pJRVlVUm1SakpIeVFqM0wxS2gtMDFvc3ktZ05QYjc3VXRtSHdsNk9hLWUwb3VxTzBFcVhBeUx3Zm82Zw?oc=5)（Reuters）
- [Dow closes at record on Mideast optimism; SpaceX, AMD drag Nasdaq - Reuters](https://news.google.com/rss/articles/CBMivwFBVV95cUxPdklHVUNCN0JQTDlLR0piZnVyYXRkNkU1akFlU3dWWFRoQTUyVUFxTXVtbnU2V3pTY2QwZ3pXRUw3eTFZeG1IbDAzM0Q5eEJPd0VSRldTckFHb1dBYXUtQ2tocm44b2p1SE5EbGhCNUJyMG9SX0RhZTlRZjFFbURfWmhPbnN2YmNSTlF3NFFZbG5yNmFzWTNiZFBOTlFfOWp1cmZIMkxicE50d2tJWkVXOVZQRmFxc21qN01jaDR6RQ?oc=5)（Reuters）

**财报日历（关注标的）**
- **ACOG** 2026-08-13  · EPS预期 -0.40
- **AEBI** 2026-08-13  · EPS预期 0.14
- **AEYE** 2026-08-13  · EPS预期 0.22
- **AFCG** 2026-08-13  · EPS预期 0.13
- **AGIG** 2026-08-13  · EPS预期 —
- **AIRO** 2026-08-13  · EPS预期 -0.21
- 美股行业轮动：健康 领涨（+1.27%），能源 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +8.86%，仓位 53.5%，持股 21,591 股，均价 23.75。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：26.98 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +30.90%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +5.50%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +64.32%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 贵州茅台(67.0分) · 港股最高 阿里巴巴(66.0分) · 美股最高 英伟达(78.2分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **亚马逊**（美股）| 建议观察 | 评分 73.0 | 待突破 | 趋势过滤通过 | 止损缓冲 9.3% / 目标空间 33.4% | 决策 47.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

- **贵州茅台**（A股）| 弱信号观察 | 评分 67.0 | 待突破 | 趋势过滤未过 | 止损缓冲 6.2% / 目标空间 22.2% | 决策 44.5

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **阿里巴巴**（港股）| 弱信号观察 | 评分 66.0 | 待突破 | 趋势过滤未过 | 止损缓冲 10.1% / 目标空间 36.5% | 决策 44.5

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 +0.39% | 距止损 8.9% | 距目标 +30.2% | 持有 3 天


**候选池前列**（按评分）：

- 英伟达 78.2分 建议观察 RSI 61.6 RS +8.85%

- 亚马逊 73.0分 建议观察 RSI 63.5 RS +8.37%

- 微软 70.2分 建议观察 RSI 76.1 RS +22.89%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.334）。

*在线学习：市场环境 risk_off · 修订 r334 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.2 · PEG 0.75 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 17.22 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 14.9 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 14.91 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 79.7 | 符合风格 · 建议关注 | PE 7.4 · ROE 11.3%

  - PE 7.36 — 深度价值区间，安全边际充足；PB 0.95 — 资产折价，经典格雷厄姆信号

- **招商银行**（A股）| 匹配 75.7 | 符合风格 · 建议关注 | PE 6.8 · PEG 9.67 · ROE 11.9%

  - PE 6.77 — 深度价值区间，安全边际充足；PB 0.86 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.9 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.2 · PEG 0.75 · ROE 20.5%

  - PEG 0.75 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.2 · PEG 0.75 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 71.4 · PEG 27.57 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 22.9 · PEG 0.28 · ROE 9.2%

  - 近三月 -16.39% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **Meta**（美股）| 匹配 88.5 | 符合风格 · 建议关注 | PE 22.1 · ROE 29.9%

  - PE 22.13 — 悲观中仍有估值支撑；盈利能力仍在 — 逆向不是接飞刀


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **亚马逊**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.3 · PEG 9.23 · ROE 30.6%

  - 近一月 +10.84% — 趋势强劲，反身性正反馈；相对强度 +7.91% — 跑赢大盘，宏观共振

- **微软**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 27.5 · PEG 0.87 · ROE 34.0%

  - 近一月 +25.36% — 趋势强劲，反身性正反馈；相对强度 +22.43% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 446.4 · PEG 7.86 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 172.2 · PEG 1.89 · ROE 8.1%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 25 对 · 影子胜率 44.0% · 均边际 -0.02%

- 配对归因：25 对 · 影子胜率 44.0% · 均边际 -0.02%

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 65.6% 良好，门槛 -1; 偏多环境 T+5 胜率 71.9% 良好，门槛 -1

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **AI Electricity Demand: GE Vernova and Eaton Will Capture This Next Wave of Capex**（NVDA）
  GE Vernova and Eaton both reported blowout quarters fueled by AI power demand, but one company is collecting cash right …
- [Yahoo] **How Vertiv is Becoming a Pure Play Digital Version of Schneider Electric for an AI-First World**（NVDA）
  Vertiv and Eaton both rode the AI infrastructure wave in Q2 2026, but one is sharpening itself into a pure-play weapon w…
- [Yahoo] **Who Will Benefit Most From Amazon and Microsoft’s Hyperscaler Leading AI Capex This Quarter?**（NVDA）
  Amazon and Microsoft are burning through roughly $100 billion a quarter on AI infrastructure, and two companies sit dire…
- [Yahoo] **Divorced at 60 With Half the Savings You Planned On. These 3 ETFs Help Rebuild a Retirement**（AAPL）
  A grey divorce at 60 can cut your retirement savings in half and leave you with a compressed timeline that punishes the …
- [Yahoo] **Astera Labs and Amphenol: Quiet AI Capex Tax Collectors to Know Before Others Catch On**（NVDA）
  Two companies collecting a quiet tax on every AI rack ever built just reported blowout quarters, and they do it through …
- [Yahoo] **What Determines Applied Materials’ Resilience on Aug 13 Earnings**（NVDA）
  Applied Materials has doubled in a year, analysts see another 18% upside, and the crowd gives a 92.5% chance of a beat. …

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
3. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-08-06-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
