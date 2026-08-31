# 投资决策日报 · 收盘前瞻

**2026年08月31日 14:54（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-08-31 09:40 · 宏观：2026-08-31 09:40 · 问财：2026-08-31 13:26

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **-0.45%**，综合情绪 **偏空**。风险厌恶情绪抬升，战术新开仓宜降频或观望；战役仓按网格纪律执行，避免情绪化减仓。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +10.00%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **1** 只、
下跌 **5** 只，平均涨跌 **-0.45%**。

**美股** -0.26%（震荡）；**港股** +0.07%（震荡）；**A股** -0.11%（震荡）。

**波动居前指数：**

- **日经 225** 65,158.11，日涨跌 -1.88%（周 -0.56% / 月 +5.32%）
- **纳斯达克** 26,402.42，日涨跌 -0.52%（周 +0.85% / 月 +5.10%）
- **标普 500** 7,711.76，日涨跌 -0.25%（周 +0.49% / 月 +3.69%）
- **上证指数** 3,952.18，日涨跌 -0.11%（周 +1.20% / 月 +3.88%）

### 1.2 A股短线情绪

问财统计涨停 **70** 家、跌停 **4** 家，情绪定性 **偏多**，涨跌停比约 **17.5 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 14.4（normal）
- **美10Y收益率** 4.72%
- **10Y-2Y 利差（FRED）** 0.39%（偏窄）
- **USDCNH** 6.7300（日 —）
- **美股行业**：通信 领涨，科技 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.67（变动 +0.21%，2026-08-27）
- 10Y-2Y 利差：0.39（变动 -17.02%，2026-08-28）
- 联邦基金利率：3.63（变动 0.00%，2026-07-01）
- 美国失业率：4.1（变动 -2.38%，2026-07-01）
- 美元/人民币(官方)：6.721（变动 -0.02%，2026-08-21）
- 美国CPI指数：332.8（变动 +1.63%，2026-07-01）

**Finnhub 宏观要闻**
- [Bessent expects new US secondary sanctions weekly, aiming to increase pressure on Iran - Reuters](https://news.google.com/rss/articles/CBMizAFBVV95cUxNdWJLRHJBSlpLeHYxNEtndmNRX19YTG9GWENmSEdTZXRTbnZnUFJITUtYcV83YnlPWmlpbC00WnZic3FMYVowRlA4Zzk5V2NKc2ZSSkxtUXl6N1A2MmdQbTI3cWhqbWxfMXVNekZQWFYwY2hPcENiOXR1N1JjRU4ydTRGTWZoV0U2Ul9KdmVZZ1pBQzVFTnR1MUl5YXRpTV9DWXE1bEtOc0FkVTRpNkFHOV9XZ2JOUGJ2eUQ0WFFqRDdLdlZlWWdQdlpjSHY?oc=5)（Reuters）
- [Iran's IRGC says it launched attack on two US bases in Jordan - Reuters](https://news.google.com/rss/articles/CBMirAFBVV95cUxOclJRRzlZV2lpOFlsSGdGcE1fUXVlel9CRndnX1NoM3lHcXkya2JMMWdrTEhUcnJyTHY0WDBqeFVoRzJmdEw5TlFXSGY1SVd1NXJERFdHS0IzQkhtRTdNTlJOMlp3RjgwYVVFYjY3NnV6d1c5cEt0UlVmaDJOdFBlT1ZRc0RpTVRVSkliRkU0SWZGYXZFa1JJdzNaOGxqVEFkX0FuV0l5WUNoaEFO?oc=5)（Reuters）
- [US Treasury's Bessent faces G20 diplomacy test amid tariffs, Iran war, bond turmoil - Reuters](https://news.google.com/rss/articles/CBMixwFBVV95cUxORVlaS1VmZVF5Rjh3RFkwVk40ZGpBSU1LLXM3XzQ1REFxbnl0aHREWXhieU9vUnU0aUdkTWgtNmJrYk9BRDE3aEllamozWFJVMHZ5QTJUS0pkckpwbjFVQ2dxaEhBaWZWZXg3a05ISG1Fb3k4aWV0QmRSbGFiOHdsQ0x6QWZjUUN6b3lsc2c5MEZOc2RCWXZXcERhdkN4NFJGVHBGejVxbTBZWDdvczdJamxDQ3Jib29xS1lzcURfX05MQ1BET25r?oc=5)（Reuters）
- [Iran is attacking US forces in Jordan, Fox News reports, citing a US source - Reuters](https://news.google.com/rss/articles/CBMivwFBVV95cUxQT3Q5VzJ4c1pXc3pPc1VrUmdQOC1PQmxJaXhsTV9KS1hvVnJGTmt3NUZNUlp3UHRJeEg2QlA3aFRIdHE3VjRCODNSV0NvV2xQbFNyZ1hBYXdYSnNDcDc4TE1fYnYtQ3RxdnNrQXlJVWJCZHdDbm0yWlM4emozcDY0SDFjZGMyeVBGNlFibzhZNUpKQWg2M0ZwTTNCb2I1Um9WbmRhQUo1ajBhWm9tVTcyaDFYYUhMeDdoWVZLSnQtMA?oc=5)（Reuters）
- [Oil jumps more than 1% after US attack on Iran's Larak island - Reuters](https://news.google.com/rss/articles/CBMirAFBVV95cUxQSGRJUGVDenVxZzdzdXZ4aTJudWV6LS1adkVVMmVUNnc1QnMyNVNsLThHcG44U2p6SWoxYm9LbjJnUGdkZDAzTENhSDR2OW90cWV2aDJNZWpKRllRNUhselE2djRhQlI3ejVmUUl6cFNnVDN1UmU4QXVadDNmQloya3daeWVHSmtGNDh4QWktSk1fenV3czlkbnhwNjJ3VzNXWEhZelFCRTIzaWpR?oc=5)（Reuters）

**财报日历（关注标的）**
- **ALMU** 2026-09-07  · EPS预期 -0.08
- **ALOT** 2026-09-07  · EPS预期 —
- **BNR** 2026-09-07  · EPS预期 —
- **BWTL** 2026-09-07  · EPS预期 —
- **CGNT** 2026-09-07  · EPS预期 0.09
- **DBI** 2026-09-07  · EPS预期 0.26
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：通信 领涨（+1.42%），科技 靠后。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +10.00%，仓位 36.6%，持股 14,481 股，均价 23.75。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.82 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +27.00%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +8.30%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +57.35%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 中国平安(38.8分) · 港股最高 小米集团(37.0分) · 美股最高 英伟达(67.0分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **英伟达**（美股）| 建议观察 | 评分 67.0 | 待突破 | 趋势过滤通过 | 止损缓冲 7.9% / 目标空间 28.4% | 决策 45.5

  - 逻辑：价格站上 60 日均线

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 -1.90% | 距止损 6.8% | 距目标 +33.2% | 持有 28 天


**候选池前列**（按评分）：

- 英伟达 67.0分 建议观察 RSI 52.3 RS +6.13%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.758）。

*在线学习：市场环境 risk_off · 修订 r758 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.2 · PEG 8.44 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 15.2 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.6 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 19.63 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 80.6 | 符合风格 · 建议关注 | PE 6.9 · PEG 9.84 · ROE 11.9%

  - PE 6.89 — 深度价值区间，安全边际充足；PB 0.88 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 80.6 | 符合风格 · 建议关注 | PE 6.7 · PEG 0.13 · ROE 13.1%

  - PE 6.7 — 深度价值区间，安全边际充足；PB 0.98 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.0 · PEG 0.27 · ROE 9.2%

  - PEG 0.27 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.6 · PEG 0.62 · ROE 24.8%

  - PEG 0.62 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **谷歌**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 17.4 · PEG 5.92 · ROE 48.7%

  - ROE 48.68% — 优质复利机器，芒格会长期持有；净利率 54.77% — 轻资产高毛利特征

- **微软**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 28.6 · PEG 0.90 · ROE 34.0%

  - ROE 34.04% — 优质复利机器，芒格会长期持有；净利率 40.3% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.0 · PEG 0.27 · ROE 9.2%

  - 近一月 -8.97% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.6 · ROE 12.6%

  - 近一月 -10.37% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **亚马逊**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 21.4 · PEG 8.85 · ROE 30.6%

  - 近一月 +13.13% — 趋势强劲，反身性正反馈；相对强度 +9.44% — 跑赢大盘，宏观共振

- **微软**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 28.6 · PEG 0.90 · ROE 34.0%

  - 近一月 +14.05% — 趋势强劲，反身性正反馈；相对强度 +10.36% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 369.6 · PEG 6.51 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **中芯国际**（A股）| 匹配 91.9 | 符合风格 · 建议关注 | PE 144.7 · PEG 55.86 · ROE 4.2%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 晶圆制造 — AI 算力上游产能瓶颈


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 24 对：影子胜率 70.8%，均边际 +0.62% — 可申请升级 PR

- 配对归因：24 对 · 影子胜率 70.8% · 均边际 0.62%

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 62.4% 良好，门槛 -1; 偏多环境 T+5 胜率 67.2% 良好，门槛 -1

- 队列待办：**影子轨验证通过 · 可申请升级战术参数** — 影子轨已满 4 周且优于生产。请更新 strategy_config.py：BUY_SCORE=72, BREAKOUT_SCORE_MIN=62，追加 strategy_versions.json 记录并开 PR。

> **提示**：影子轨验证通过，可请 Cursor 按 EVOLUTION_PLAYBOOK 开策略升级 PR。

---

## 六、资讯与主题线索

- [Yahoo] **Dow Jones Futures Fall, Oil Prices Pop As U.S. Strikes Iran**（^GSPC）
  Dow Jones futures fell slightly while oil prices bounced as the U.S. struck Iran publicly for the first time in a month.…
- [Yahoo] **John Ternus to lead Apple into the age of AI**（AAPL）
  John Ternus takes over as Apple's chief executive on Tuesday, inheriting a company that towers over the smartphone marke…
- [Yahoo] **1 Top Warren Buffett Stock for Dividend Investors**（AAPL）
  This tech giant could become a dividend beast over the next decade and beyond.…
- [Yahoo] **According to BlackRock, Bitcoin Is Still a Great Portfolio Diversifier. So How Much Bitcoin Should You Be Holding in Your Portfolio?**（NVDA）
  Even if you're bullish on Bitcoin, it still shouldn't take up much of your portfolio.…
- [Yahoo] **IREN Stock Plunged Last Week. Now Could Be a Good Time to Buy.**（NVDA）
  Investors have a chance to buy the AI computing supplier at a sizable discount.…
- [Yahoo] **If You Invested $1,000 In Nvidia Stock at IPO, Here's How Much You'd Have Now**（NVDA）
  NVIDIA Corp CEO Jensen Huang may not check the price of the stock for the company he runs and co-founded, but millions o…

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
3. ⚠️ 亚马逊 距止损仅 6.8%
4. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-08-31-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
