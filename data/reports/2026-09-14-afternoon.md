# 投资决策日报 · 收盘前瞻

**2026年09月14日 22:56（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-09-14 20:37 · 宏观：2026-09-14 20:37 · 问财：2026-09-14 20:40

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.40%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +9.04%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **4** 只、
下跌 **2** 只，平均涨跌 **+0.40%**。

**美股** +0.93%（偏强）；**港股** +0.45%（偏强）；**A股** -0.07%（震荡）。相对强势区域：美股、港股。

**波动居前指数：**

- **道琼斯** 52,573.29，日涨跌 +0.98%（周 -2.07% / 月 -2.23%）
- **纳斯达克** 26,333.04，日涨跌 +0.96%（周 -0.94% / 月 -0.96%）
- **标普 500** 7,656.98，日涨跌 +0.86%（周 -1.17% / 月 -1.18%）
- **日经 225** 63,492.99，日涨跌 -0.81%（周 -4.38% / 月 -7.60%）

### 1.2 A股短线情绪

问财统计涨停 **70** 家、跌停 **4** 家，情绪定性 **偏多**，涨跌停比约 **17.5 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 17.6（normal）
- **美10Y收益率** 4.98%
- **10Y-2Y 利差（FRED）** 0.33%（偏窄）
- **USDCNH** 6.7100（日 —）
- **美股行业**：科技 领涨，公用事业 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.95（变动 +2.48%，2026-09-10）
- 10Y-2Y 利差：0.33（变动 -15.38%，2026-09-11）
- 联邦基金利率：3.63（变动 0.00%，2026-08-01）
- 美国失业率：4.1（变动 0.00%，2026-08-01）
- 美元/人民币(官方)：6.7108（变动 -0.11%，2026-09-04）
- 美国CPI指数：334.1（变动 +1.16%，2026-08-01）

**Finnhub 宏观要闻**
- [College students feel more pressure to be perfect. Experts explain why](https://www.cnbc.com/2026/09/14/college-students-more-perfectionistic.html)（CNBC）
- [Trump downplays report China entities helped Iran before attack that killed US troops - Reuters](https://news.google.com/rss/articles/CBMixAFBVV95cUxPZF9XUXZXZ0J5UzkzN2pGQlpxQkI3dklSRmIyMDUzYWZqdzhZQXdYMlF5djdTNjAzcGUxRUVDdHdOU3hXWGlGb0J5bVAzTWRlWjNYaWV3eUczcHB2R3dudTBYZmRtZ3lOVy00ZUJycDJtZUlJMTZNaHRRVEFVRHdPUEpjSVhyTUpOd2Q4R2Z5ZGlscTdSNzd6VHRLSXJWMTc4NUlaZzAydWhRekFJdDF4R19nMmJhSVNsLWRLMUJTc2xOT0pU?oc=5)（Reuters）
- [AirBaltic files for Chapter 11 bankruptcy as Iran war costs bite - Reuters](https://news.google.com/rss/articles/CBMikgFBVV95cUxOSTBsQlVVMThMRmZ6a3gxOE5lRG1fbENPRnEwUmlWN3pXNUdGT1ZhMDZOQnFMbGZWZUk5ZTQzYUd0VVByOXdZVy01ZE85UTJ2dVBIZW1EX0ZzZjVaRjRyc09PTkpGQlJQc0JGQmh3b1J0NkllWFItWHhaNTVIRUxrbEJVaWQyVkpfcm0zcks0X1ZZdw?oc=5)（Reuters）
- [Morning Bid: Shipping oil gets ever harder, costlier - Reuters](https://news.google.com/rss/articles/CBMigwFBVV95cUxOYmJCUUMxaW05Wm0yazVud3pVRFlHLTJKai13QUcxaUhtX2dlTEJPcV9XOWZGSnRzdFRXejctZE1sUGZrcEd3Sy1JOUZxVktnQW9hVl9vbTVSdEhldXBEaUxQTlJRanQyWDFpQXNaTlE1UWUwaVgzMU8yTmF2dzFGYUNuUQ?oc=5)（Reuters）
- [COMMENTARY: Oil markets survived the Iran war sprint. Now comes the marathon - Reuters](https://news.google.com/rss/articles/CBMiwgFBVV95cUxPYkNyZjhwWkFHcjR0aVV2b3lPNFROSy0tNDZBQVJpWE9JelJyVWhtNFJjWlY3OW56NmdXY2s3Q0luV1h1cGZnRXJiM0VzMWxqVDFROENnOEFFMHpPN2VfWXJYTjZ3TW1EWlZLdU16clZBN28wVlI4SXJYeWR1U3kzZlAyempIWXVhaC1LdWNKbVo3QS1YMjZucjZnd3FTdnNaWmpNd2phODkxTlFwcng2aWo3WjZhdUdCOXZBejRyaW5kdw?oc=5)（Reuters）

**财报日历（关注标的）**
- **AIR** 2026-09-21  · EPS预期 1.34
- **BNC** 2026-09-21  · EPS预期 —
- **BNTC** 2026-09-21 amc · EPS预期 -0.28
- **CBIH** 2026-09-21  · EPS预期 —
- **COOT** 2026-09-21  · EPS预期 —
- **EBF** 2026-09-21  · EPS预期 0.39
- 美股行业轮动：科技 领涨（+1.32%），公用事业 靠后。
- 原油强、黄金弱 — 偏再通胀/增长预期。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +9.04%，仓位 36.1%，持股 14,481 股，均价 23.75。

**月线状态**：连续 **1** 个月收跌，上月 -1.22%，近两月累计 +22.21%，近三月累计 -3.83%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.16 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +30.00%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +6.10%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +54.06%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(65.0分) · 港股最高 小米集团(43.6分) · 美股最高 苹果(84.7分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 趋势达标待突破 | 评分 84.7 | 待突破 | 趋势过滤通过 | 止损缓冲 5.9% / 目标空间 21.2% | 决策 60.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **招商银行**（A股）| 弱信号观察 | 评分 65.0 | 待突破 | 趋势过滤未过 | 止损缓冲 4.1% / 目标空间 14.7% | 决策 65.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 -5.45% | 距止损 3.2% | 距目标 +38.2% | 持有 42 天 ⚠️ 接近止损


**候选池前列**（按评分）：

- 苹果 84.7分 趋势达标待突破 RSI 62.8 RS +10.85%

- Meta 74.8分 建议观察 RSI 67.2 RS +12.87%

- AMD 74.6分 建议观察 RSI 58.0 RS +7.79%

- 微软 66.0分 建议观察 RSI 56.9 RS +1.76%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.828）。

*在线学习：市场环境 risk_on · 修订 r828 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 14.5 · PEG 8.05 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 14.48 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.0 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 18.99 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.2 · PEG 1.27 · ROE 11.5%

  - PE 7.22 — 深度价值区间，安全边际充足；PB 0.92 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 6.6 · PEG 0.12 · ROE 13.1%

  - PE 6.57 — 深度价值区间，安全边际充足；PB 0.96 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **宁德时代**（A股）| 匹配 91.1 | 符合风格 · 建议关注 | PE 18.0 · PEG 0.57 · ROE 24.8%

  - PEG 0.57 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证

- **微软**（美股）| 匹配 91.1 | 符合风格 · 建议关注 | PE 27.6 · PEG 0.87 · ROE 34.0%

  - PEG 0.87 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.7% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **谷歌**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 17.0 · PEG 5.77 · ROE 48.7%

  - ROE 48.68% — 优质复利机器，芒格会长期持有；净利率 54.77% — 轻资产高毛利特征

- **Meta**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 24.4 · ROE 29.9%

  - ROE 29.85% — 优质复利机器，芒格会长期持有；净利率 29.83% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 18.0 · PEG 0.57 · ROE 24.8%

  - 近一月 -14.42% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」

- **阿里巴巴**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 24.5 · ROE 6.4%

  - 近一月 -11.68% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **Meta**（美股）| 匹配 73.2 | 符合风格 · 建议关注 | PE 24.4 · ROE 29.9%

  - 近一月 +11.95% — 趋势强劲，反身性正反馈；相对强度 +13.13% — 跑赢大盘，宏观共振

- **招商银行**（A股）| 匹配 70.7 | 部分符合 · 观察等待 | PE 7.2 · PEG 1.27 · ROE 11.5%

  - 近一月 +8.76% — 趋势强劲，反身性正反馈；相对强度 +9.83% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 353.6 · PEG 22.24 · ROE 4.0%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 131.7 · PEG 82.81 · ROE 10.2%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 16 对 · 影子胜率 31.2% · 均边际 -0.44%

- 配对归因：16 对 · 影子胜率 31.2% · 均边际 -0.44%

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 61.7% 良好，门槛 -1; 偏多环境 T+5 胜率 61.1% 良好，门槛 -1

- 队列待办：**流水线过期 · Truth Social 镜像** — 检查工作流 update-truth-social.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **Stocks Fall Pre-Bell Amid AI Safety Warnings; Investors Await Fed Rate Decision**（^GSPC）
  The benchmark US stock measures were tracking in the red before the opening bell Monday as traders a…
- [Yahoo] **$10,000 Invested in SCHD a Decade Ago Would Be Worth This Much Today**（NVDA）
  The Schwab U.S. Dividend Equity ETF has been an elite performer in this category for a long time.…
- [Yahoo] **3 Situations Where Planning to Claim Social Security at 70 Can Backfire**（NVDA）
  Holding out for larger checks doesn't always work out for the best.…
- [Yahoo] **2 Numbers Matter More to Alphabet Stock's Performance Than Anything Else Right Now**（NVDA）
  Despite its massive size, this internet titan's share price is up 150% in the past three years.…
- [Yahoo] **This Could Be the Most Underrated Artificial Intelligence Stock to Buy Right Now**（NVDA）
  Qualcomm stock has underperformed the market over the past year, but a deal with Amazon could give it a much-needed boos…
- [Yahoo] **Apple Foldable iPhone Could Change Smartphones Forever**（AAPL）
  Apple Just Entered the Foldable War. Gurman Says Its New iPhone Could Transform the Market…

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
3. ⚠️ 亚马逊 距止损仅 3.2%
4. 待突破观察：苹果 突破位 344.27
5. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-09-14-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
