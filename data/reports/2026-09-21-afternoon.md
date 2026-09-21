# 投资决策日报 · 收盘前瞻

**2026年09月21日 17:22（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-09-21 14:16 · 宏观：2026-09-21 14:16 · 问财：2026-09-21 12:52

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.51%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +9.30%，按网格与月线纪律执行。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **5** 只、
下跌 **1** 只，平均涨跌 **+0.51%**。

**美股** +0.13%（震荡）；**港股** +0.66%（偏强）；**A股** +0.66%（偏强）。相对强势区域：港股、A股。

**波动居前指数：**

- **日经 225** 65,018.95，日涨跌 +1.38%（周 +1.57% / 月 -1.81%）
- **恒生指数** 24,913.23，日涨跌 +0.66%（周 -0.02% / 月 -4.21%）
- **上证指数** 3,937.70，日涨跌 +0.66%（周 +1.35% / 月 +0.83%）
- **纳斯达克** 26,522.54，日涨跌 +0.39%（周 +0.72% / 月 +0.73%）

### 1.2 A股短线情绪

问财统计涨停 **70** 家、跌停 **4** 家，情绪定性 **偏多**，涨跌停比约 **17.5 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 14.8（normal）
- **美10Y收益率** 5.00%
- **10Y-2Y 利差（FRED）** 0.25%（偏窄）
- **USDCNH** 6.6900（日 —）
- **美股行业**：科技 领涨，材料 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.94（变动 -1.40%，2026-09-17）
- 10Y-2Y 利差：0.25（变动 -7.41%，2026-09-18）
- 联邦基金利率：3.63（变动 0.00%，2026-08-01）
- 美国失业率：4.1（变动 0.00%，2026-08-01）
- 美元/人民币(官方)：6.708（变动 +0.03%，2026-09-11）
- 美国CPI指数：334.1（变动 +1.16%，2026-08-01）

**Finnhub 宏观要闻**
- [Xi rolls into Trump summit with China's trade engine roaring - Reuters](https://news.google.com/rss/articles/CBMiqwFBVV95cUxQTjdmUF9fTEcySTFqT2t2NUZsd1prTmZjTjJVbmZwOVVVQzVCYV9mem5YNGRVUUdYT05uRTlXTWFheEh5azN5blpURFI1YXItOEJBZWZRRDlLQkx3aGJsdkZia0M2WEpaNHRhTTVmOEpUeU5FdWRPYVN1dUV1bVZrbHpzVEhZZzBrRXNXMTYzOTZzQTVETVkxM1pJT3JIZlpucUJoQTVFaE5LX28?oc=5)（Reuters）
- [Vessels trickle through Strait of Hormuz as Middle East conflict persists - Reuters](https://news.google.com/rss/articles/CBMitwFBVV95cUxPNHdMbF8wY2pMdE0tcHdWa3l5dkc5MGpKWVJEZW9VUnV2UTFlaTlVbVpOZ1pQN245SWZOLU4zWDd3ODlBTUhhZmlmaE1jUGltMzRKUF9xRl9CT2ZpMnNxcXkxOXdQeHJHajFzMkpoNWVnS3N6X3ExamF1ejcyQ3I1LW5DVHRXTXQ5MVVtTEE1cmtxLWhGMURaZ19pajA1blpROVVxRXQ3MHE4Zy1BLUVybldpUm01NU0?oc=5)（Reuters）
- [Indian shares open muted as high oil prices, IPO rush weigh - Reuters](https://news.google.com/rss/articles/CBMinwFBVV95cUxOQ3NYaXdLM1g3c3NKZkFDM2I0b0xENENVUGJFaFJIY01mVjQtV2swdVJVelBWV0hMNjBNeGFyTTItOGtRM0tYOTkxcTR1ZXJyS01WclBmMXRCTkdMOUdpbnpTdHhSamd2elBWMWlKVWpVNUoxX1c1emdyU2FlOE1aOHNvZXc1MDRtVlFtYzN4Ui0wMDZSUWNHZFRwSHE4Wm8?oc=5)（Reuters）
- [Oil hits over 1-week low on hopes of boost to diplomacy in Iran war - Reuters](https://news.google.com/rss/articles/CBMimwFBVV95cUxOdEljbFotbFNVU2Nyb1oyaElIUXJJc1ltUmF5a1FrMl9xbEwyNG9LOWwyZ3F2dUZIUl9QYnd6OXU1cU10UGx0QzkxaVp6QkoxY3ZYSm1qc3FvbFprT29VcldJZ3V1Y1YtZ1A3MjEtTUo2dk9laHFBaWZBMFNOMmZDVC16aDBhYUdmdmZFdUJ4d0hoMW5hZTgxRk1ETQ?oc=5)（Reuters）
- [France vows response after Iran closes language centre in Tehran - Reuters](https://news.google.com/rss/articles/CBMitgFBVV95cUxQeGRiOTFBU2NRT2UtR2l0OEZGUmhIWHRpdmgta1ZzazcyT2JsWlMxV25qWVdVbnJFd2gxOTVZM2F5Z2Y1enJfODBQaXZLOENKQzlDWXhoZktaU0NzbThxYk9PSkZUd2lQUkNhM09FaHVVOG8ydVZVQjc5cHVkRXBNaGdVc1VEVXg0UmlicmxmVGNPbngzTG5oTG41YnRQc3JSci1RUXJwMWJpdXdtd19tOHZCOHBJUQ?oc=5)（Reuters）

**财报日历（关注标的）**
- **ABLV** 2026-09-28  · EPS预期 —
- **AIFU** 2026-09-28  · EPS预期 —
- **AIIO** 2026-09-28  · EPS预期 —
- **ALP** 2026-09-28  · EPS预期 —
- **AMST** 2026-09-28  · EPS预期 —
- **ANEB** 2026-09-28 amc · EPS预期 -0.10
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：科技 领涨（+0.82%），材料 靠后。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +9.30%，仓位 36.2%，持股 14,481 股，均价 23.75。

**月线状态**：连续 **1** 个月收跌，上月 -1.22%，近两月累计 +22.21%，近三月累计 -3.83%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.34 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +29.20%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +6.70%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +54.15%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(55.3分) · 港股最高 泡泡玛特(45.5分) · 美股最高 Meta(86.2分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **Meta**（美股）| 趋势达标待突破 | 评分 86.2 | 待突破 | 趋势过滤通过 | 止损缓冲 8.2% / 目标空间 29.5% | 决策 59.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **招商银行**（A股）| 弱信号观察 | 评分 55.3 | 待突破 | 趋势过滤未过 | 止损缓冲 4.1% / 目标空间 14.9% | 决策 58.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **泡泡玛特**（港股）| 弱信号观察 | 评分 45.5 | 待突破 | 趋势过滤未过 | 止损缓冲 5.1% / 目标空间 18.5% | 决策 57.0

  - 逻辑：价格站上 20 日均线

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- Meta 86.2分 趋势达标待突破 RSI 65.8 RS +22.47%

- 苹果 81.6分 趋势达标待突破 RSI 64.3 RS +6.63%

- AMD 73.6分 建议观察 RSI 65.4 RS +20.56%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.859）。

*在线学习：市场环境 risk_on · 修订 r859 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 14.4 · PEG 7.99 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 14.37 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.1 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 19.13 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 84.6 | 符合风格 · 建议关注 | PE 6.5 · PEG 0.12 · ROE 13.1%

  - PE 6.46 — 深度价值区间，安全边际充足；PB 0.95 — 资产折价，经典格雷厄姆信号

- **京东集团**（港股）| 匹配 77.7 | 符合风格 · 建议关注 | PE 17.8 · PEG 0.84 · ROE 6.8%

  - PE 17.83 — 低于市场平均，具备安全边际；PB 1.09 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **宁德时代**（A股）| 匹配 84.9 | 符合风格 · 建议关注 | PE 15.8 · PEG 0.50 · ROE 24.8%

  - PEG 0.5 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证

- **微软**（美股）| 匹配 84.9 | 符合风格 · 建议关注 | PE 27.5 · PEG 0.87 · ROE 34.0%

  - PEG 0.87 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.7% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **谷歌**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 17.6 · PEG 5.97 · ROE 48.7%

  - ROE 48.68% — 优质复利机器，芒格会长期持有；净利率 54.77% — 轻资产高毛利特征

- **Meta**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 25.1 · ROE 29.9%

  - ROE 29.85% — 优质复利机器，芒格会长期持有；净利率 29.83% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.8 · PEG 0.50 · ROE 24.8%

  - 近一月 -24.31% — 市场悲观，邓普顿式逆向机会；近三月 -27.35% — 深度回调，关注基本面是否错杀

- **美团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.2 · ROE -21.8%

  - 近一月 -13.59% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 38.6 · PEG 1.34 · ROE 148.8%

  - 相对强度 +6.84% — 跑赢大盘，宏观共振；均线多头排列 — 趋势交易确认

- **AMD**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 142.8 · PEG 89.82 · ROE 10.2%

  - 近一月 +20.02% — 趋势强劲，反身性正反馈；相对强度 +20.77% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 365.1 · PEG 22.96 · ROE 4.0%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **中芯国际**（A股）| 匹配 84.5 | 符合风格 · 建议关注 | PE 139.7 · PEG 53.95 · ROE 4.2%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 晶圆制造 — AI 算力上游产能瓶颈


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 17 对 · 影子胜率 23.5% · 均边际 0.1%

- 配对归因：17 对 · 影子胜率 23.5% · 均边际 0.10%

- 战术自适应：门槛 +0 · 港股 T+5 胜率 42.4% 偏低，门槛 +1（市场门槛→+1）; 美股 T+5 胜率 69.2% 良好，门槛 -1（市场门槛→-1）

- 队列待办：**流水线过期 · Truth Social 镜像** — 检查工作流 update-truth-social.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **‘RAMageddon’: tech crunch hikes the price of your next iPhone by £100**（AAPL）
  Shortage of memory chips and other critical components reverses trend of electronics becoming cheaper…
- [Yahoo] **Stock Market: Will S&P 500 Open Up or Down Today?**（^GSPC）
  U.S. stock futures are trending higher early Monday as investors digest a stark warning from President Donald Trump to I…
- [Yahoo] **Investing $150 per Month in This S&P 500 ETF Could Grow Into $300,000 Over 30 Years. Here's the Math.**（NVDA）
  Stay consistent and let time do the heavy lifting for you.…
- [Yahoo] **Amazon.com vs. Uber Technologies: Analyzing Recent Quarterly Revenue Trends Between Two Consumer Companies**（NVDA）
  Amazon's revenue towers over Uber's across eight quarters, yet both companies posted double-digit operating margins in Q…
- [Yahoo] **Tech lifts share markets in Asia as oil slips**（^GSPC）
  By Wayne Cole SYDNEY, Sept 21 (Reuters) - Share markets rose in Asia on Monday as AI's insatiable demand for data buoyed…
- [Yahoo] **Tesla's Free Cash Flow Went Negative. It Still Has a $43.5 Billion Cash Cushion.**（NVDA）
  The company's ability to fund an aggressive capital spending program might surprise some investors.…

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
3. 待突破观察：Meta 突破位 685.31
4. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-09-21-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
