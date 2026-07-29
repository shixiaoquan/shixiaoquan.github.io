# 投资决策日报 · 收盘前瞻

**2026年07月29日 18:46（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-29 18:01 · 宏观：2026-07-29 18:01 · 问财：2026-07-29 17:47

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **-0.59%**，综合情绪 **偏空**。风险厌恶情绪抬升，战术新开仓宜降频或观望；战役仓按网格纪律执行，避免情绪化减仓。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +20.33%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **3** 只、
下跌 **3** 只，平均涨跌 **-0.59%**。

**美股** +0.07%（震荡）；**港股** +2.38%（偏强）；**A股** -0.77%（偏弱）。相对强势区域：港股。相对弱势区域：A股，战术配置宜降权。

**波动居前指数：**

- **日经 225** 61,434.19，日涨跌 -5.39%（周 -4.22% / 月 -15.11%）
- **恒生指数** 25,807.92，日涨跌 +2.38%（周 +2.64% / 月 +11.83%）
- **道琼斯** 52,210.08，日涨跌 +0.96%（周 +0.12% / 月 +0.70%）
- **纳斯达克** 24,932.08，日涨跌 -0.82%（周 -2.30% / 月 -2.14%）

### 1.2 A股短线情绪

问财统计涨停 **86** 家、跌停 **9** 家，情绪定性 **偏多**，涨跌停比约 **9.6 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。

### 1.3 宏观与跨资产

- **VIX** 18.2（elevated）
- **美10Y收益率** 4.64%
- **10Y-2Y 利差（FRED）** 0.35%（偏窄）
- **USDCNH** 6.7700（日 —）
- **美股行业**：必需消费 领涨，能源 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.65（变动 -0.85%，2026-07-27）
- 10Y-2Y 利差：0.35（变动 +2.94%，2026-07-28）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.7719（变动 +0.03%，2026-07-24）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [Oil rises as US-Iran tension escalates after Iraq strikes, missile attack - Reuters](https://news.google.com/rss/articles/CBMiygFBVV95cUxPd0ctWlZRN0hINkdrNUJmWWxpV0ZGNGw2Y2taRk1DbFBpdzd5bFdXQmJEcW9VRExnRFBtTWlTTHBRTU5tcDN2azF6VmtxdDN6WlVncmJxSVJhYjM4Wlctb3NEcnEzSWt4djdPSWJJX3ItYmpaN0UyZ09pbV85YjlRMkQ4RTV2RDE2c2NhYlRTdEVEUUFoWEVLMVBqUzhhX2xtVlJLUFp0RWFZTFpCSGJwMTRydUQ3NUx6ejJyYWFCdzBMVWpOYWZqbzF3?oc=5)（Reuters）
- [Zendaya, Tom Holland and more at Spider Man: Brand New Day premiere - Reuters](https://news.google.com/rss/articles/CBMivAFBVV95cUxPSGdyZGU4NERmYzlkMjdIYmptUk5GYXRvVUVuT1pPN3NlcjFEYzBaeVA0bmxrY0lNajJDTGoxb0FSWVd1bnJtZGFtRUtCMC1Cby1IV21XMUU1NGxJVThrc1lkR0RFdEozODVvNURqUXJySHpqcUNHR0lxeGFpQkpxYTNNWmNGd0ZkeXRPU0hsYkN6OGcyZGdZNFNNOGdJTnFocG54cVMtdGVxZ0kwTWJ6XzN5ZEUzTG1JX0wwZg?oc=5)（Reuters）
- [Iran rules out regional management of Hormuz Strait, hitting hopes for breakthrough - Reuters](https://news.google.com/rss/articles/CBMiyAFBVV95cUxQcm9JU2paOWtPTENMY1JfVDZWWTA5MDVrNUQ5b1FndWhaSVk5Q2psS3dhc0lPeFg5cEE0ZktEVXBzb2JZRmFiUWdXZHNBSU1ON1BLZEM2X21FYmd1T3BFd2tjbU4xSGlibVluMm1xY2xMV0plaTlhUExiMWZtYml6aWNhd1d3ZkcxWC1tN2Q4UzdFdE5QOEc1eWxVNEZIaHdmWTNPczRwbXFGNHZjQ3E1dVdyd3ZLYkRISndfOXFrbFhYdVdFWFdIQw?oc=5)（Reuters）
- [Major Gulf fighting restarts as US and Saudi strike Iran's allies in Iraq - Reuters](https://news.google.com/rss/articles/CBMixAFBVV95cUxNcFJoOXIwZmxCNHBjd05nc3dlYjNXXzd1NzdyQldTOVQ4S3NjZnNDRWdqdG1WUFRUS2tRSkJJTEhQYjJWa1FraklySUtoamVybzBfbUR4aUItanFrRG1hMDZJTzlSQ3lrS25SLUo4QzR0RVQxdmFSVUFaUFpHYWV0cmdnVURNVHJ1QzBzM0pIRTMwUmVFZmxwVVpyTklTallXU2ZLOGl3TDJ1U3VnRzd3bmZnQjVfcUw2a1pWSGdFOTNlUXFa?oc=5)（Reuters）
- [EXCLUSIVE: Iran to get Chinese shoulder-launched missile systems in weeks, sources say - Reuters](https://news.google.com/rss/articles/CBMitwFBVV95cUxPR19sNWVrRDdhcXlNdTlxcUdNR0dNWDRBcjZPd21xOEM2bEYtdDJiWTEtYzlweWs5ZmtILVlhQkVUNzdaaENHbnhqTl9SSFNCZjk3eXNMS1o4SXFzT2VBS3VZZ0p6MVlrQldWNjRMUGlTN2tDR2xUOVBUdkdkTndueExrQm9vRGtTLTdBWjNGMDhZRC1qNDZXYVk3TXB0bWZ4ZFhpYUtfZ2JaalVZdjU3emN6LUptbjA?oc=5)（Reuters）

**财报日历（关注标的）**
- **AATC** 2026-08-05  · EPS预期 —
- **ABCL** 2026-08-05  · EPS预期 -0.15
- **ACA** 2026-08-05  · EPS预期 1.20
- **ACFN** 2026-08-05  · EPS预期 —
- **ACLX** 2026-08-05 amc · EPS预期 -1.15
- **ACT** 2026-08-05 amc · EPS预期 1.20
- 美债收益率回落，利于风险资产估值修复。
- 美股行业轮动：必需消费 领涨（+2.58%），能源 靠后。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、ExchangeRate-API、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +20.33%，仓位 67.5%，持股 25,467 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：31.88 HKD。

- 下一档**滚动卖出**（涨 25%）：触发价 **29.35**，距现价 -7.90%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +53.81%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(61.2分) · 港股最高 美团(79.0分) · 美股最高 苹果(70.0分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **美团**（港股）| 趋势达标待突破 | 评分 79.0 | 待突破 | 趋势过滤通过 | 止损缓冲 11.4% / 目标空间 41.2% | 决策 47.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **苹果**（美股）| 弱信号观察 | 评分 70.0 | 待突破 | 趋势过滤未过 | 止损缓冲 5.9% / 目标空间 21.2% | 决策 48.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **招商银行**（A股）| 弱信号观察 | 评分 61.2 | 待突破 | 趋势过滤未过 | 止损缓冲 4.6% / 目标空间 16.7% | 决策 48.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 美团 79.0分 趋势达标待突破 RSI 68.7 RS +26.21%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.276）。

*在线学习：市场环境 risk_off · 修订 r276 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 16.69 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.6 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 17.61 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.0 · PEG 9.92 · ROE 11.9%

  - PE 6.95 — 深度价值区间，安全边际充足；PB 0.88 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.5 · ROE 11.3%

  - PE 7.49 — 深度价值区间，安全边际充足；PB 0.97 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 23.1 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - PEG 0.73 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 70.8 · PEG 27.32 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 23.1 · PEG 0.28 · ROE 9.2%

  - 近三月 -23.11% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **腾讯控股**（港股）| 匹配 85.4 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 16.69 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **美团**（港股）| 匹配 70.3 | 部分符合 · 观察等待 | PE 19.6 · ROE -24.1%

  - 近一月 +36.44% — 趋势强劲，反身性正反馈；相对强度 +24.61% — 跑赢大盘，宏观共振

- **苹果**（美股）| 匹配 69.2 | 部分符合 · 观察等待 | PE 40.8 · PEG 1.87 · ROE 141.5%

  - 近一月 +22.45% — 趋势强劲，反身性正反馈；相对强度 +21.7% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 83.9 | 符合风格 · 建议关注 | PE 373.2 · PEG 6.57 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 63.6 | 部分符合 · 观察等待 | PE 164.1 · PEG 1.80 · ROE 8.1%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 25 对 · 影子胜率 40.0% · 均边际 0.1%

- 配对归因：25 对 · 影子胜率 40.0% · 均边际 0.10%

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 64.0% 良好，门槛 -1; 偏多环境 T+5 胜率 61.5% 良好，门槛 -1

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **Micron Stock Has Gained Roughly 190% in 2026. History Says Its Next 30%+ Drawdown Could Come at Any Time.**（NVDA）
  The memory chipmaker will remain a wildly volatile stock.…
- [Yahoo] **With Inflation at 3.5%, Is Now a Good Time to Buy the SPDR Gold ETF? Here's What History Says.**（NVDA）
  Gold is currently pulling back after a blistering return in 2025.…
- [Yahoo] **Prediction: 3 Unstoppable Artificial Intelligence (AI) Stocks That Will Join the $2 Trillion Club by 2027 (Hint: Not SpaceX)**（NVDA）
  The $2 trillion club is going to get more crowded during the next year.…
- [Yahoo] **"Hope Is Not an Investment Strategy," Says the Lone Wall Street Analyst Who Hasn't Been Wrong About SpaceX**（NVDA）
  Thirty-seven analysts have placed a buy- or hold-equivalent rating on SpaceX stock over the last seven weeks -- and they…
- [Yahoo] **Anthropic's lonely island**（NVDA）
  Anthropic spent this winter and spring as the darling of America's AI boom, conquering the frontier while casting itself…
- [Yahoo] **Stock Market Investors Just Got Bad News About President Trump's Economy. It Hints at a Big Move in the S&P 500 and Nasdaq.**（^GSPC）
  The Federal Reserve is expected to raise interest rates twice by year-end -- history suggests that tighter monetary poli…

---

## 七、风险提示

1. 本报告基于公开行情与规则化模型，**不构成投资建议**；战术实验与战役 XRPS 为相互独立的两套体系，请勿混仓决策。  
2. 港股 / 美股存在汇率、流动性及隔夜缺口风险；A股须关注涨跌停制度下的执行偏差。  
3. 问财等非官方数据源可能延迟或缓存；涨停榜等情绪指标需与实时盘口交叉验证。  
4. 模拟盘收益不代表未来表现；连阴月加仓逻辑基于历史回测，极端宏观冲击下可能失效。
5. 大师风格荐股为规则化模拟，非真实人物操作建议；基本面数据可能有延迟或缺失。

---

## 八、本时段关注清单

1. 小米滚动卖出触发：涨 25% @ 29.35
2. 待突破观察：美团 突破位 92.20
3. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-07-29-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
