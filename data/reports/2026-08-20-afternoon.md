# 投资决策日报 · 收盘前瞻

**2026年08月20日 16:48（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-08-20 16:00 · 宏观：2026-08-20 16:00 · 问财：2026-08-20 15:53

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.53%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +10.03%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **6** 只、
下跌 **0** 只，平均涨跌 **+0.53%**。

**美股** +0.20%（震荡）；**港股** +0.98%（偏强）；**A股** +0.24%（震荡）。相对强势区域：港股。

**波动居前指数：**

- **日经 225** 66,216.79，日涨跌 +1.36%（周 -3.06% / 月 -0.02%）
- **恒生指数** 25,746.04，日涨跌 +0.98%（周 +1.38% / 月 +3.43%）
- **上证指数** 3,903.72，日涨跌 +0.24%（周 -0.59% / 月 +0.95%）
- **道琼斯** 53,463.05，日涨跌 +0.22%（周 -0.57% / 月 +2.37%）

### 1.2 A股短线情绪

问财统计涨停 **83** 家、跌停 **13** 家，情绪定性 **偏多**，涨跌停比约 **6.4 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 15.0（normal）
- **美10Y收益率** 4.65%
- **10Y-2Y 利差（FRED）** 0.46%（偏窄）
- **美股行业**：健康 领涨，科技 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.71（变动 -0.21%，2026-08-18）
- 10Y-2Y 利差：0.46（变动 -11.54%，2026-08-19）
- 联邦基金利率：3.63（变动 0.00%，2026-07-01）
- 美国失业率：4.1（变动 -2.38%，2026-07-01）
- 美元/人民币(官方)：6.7412（变动 -0.02%，2026-08-14）
- 美国CPI指数：332.8（变动 +1.63%，2026-07-01）

**Finnhub 宏观要闻**
- [China boosts imports of Russian crude, stymieing India's refiners - Reuters](https://news.google.com/rss/articles/CBMiyAFBVV95cUxPZU9oV2RaZ2RZNW5hZlFqbXFNNmd5RnJkM21hWmo0WVhJX1paTlBWaE50SHhMazFzdHJuVVF2QlpzT1lRZG1VUEdERkdsSXcxTjFmQjd5RXlJeDM1eVR1NHZnd0xlRWJFXzlsbS0tdmpJMlVzeFNrLUk1R25abzR3cUxDYXRCUW1lekg0LU9lWmNzdWFyekI1SFJOdmxJSWVaRS0zT3Z5QzRVNkt3VndialQySlRtbTVKTTdJb3g1T0h2ZXFabXNLMQ?oc=5)（Reuters）
- [Hormuz shipping unchanged amid US-Iran stalemate, data shows - Reuters](https://news.google.com/rss/articles/CBMiswFBVV95cUxPR2wyclNjWVpvOTM3X0dCUjJNdEhZYkYwOC0taHk5bnNRXzZ2d3R2V092Z0pNTlBiVDdzejJXS0ozSnc1aGRjenhxbXRUY3RsMjgzUV9wSkFlTEJxbk1VbUFvbDZMTjhwTXpzR2lJVndmanZhUDhudjFlMUNVdVptcjlQYXZ1UTczRnVNM3pIUTQzQ3ctcUxwd2VYalFHYXRXdzJHemNSOUE5Vmwzdzd0NFNEcw?oc=5)（Reuters）
- [Trump warns of economic consequences for any country that supports Iran - Reuters](https://news.google.com/rss/articles/CBMiugFBVV95cUxQc0t6ejR6ZDNSMllnR0lXWC1vV3ZyTXoxUDEyeHRXczFpRWtRbzEyWmdkRVRqWi1oZzJEaEF6UnAxcHItbXZ6Z1hKTzBQV2hPOUVFQml3Wk80T1F2UmFRSzIwakhFR2hKbmp3MFJ6LUFDX1BHV3BKeDZxYXdaT2wwWi1kaU5LbkFaX19IekRKSGNUT0VBc1FQeWVRdUxLd0U3V1I5WjZoMmtIcXZUQnRBczZKcTFZa19zUVE?oc=5)（Reuters）
- [Oil gains on Middle East supply concerns amid impasse in US-Iran war - Reuters](https://news.google.com/rss/articles/CBMiqgFBVV95cUxOM1ZTcG5JRHQxeFFrOEd6Q0s4eWdFZGZwRmUyaFlPQkEwWEFLZ2xtLUJxMDFGRzZEZ1VEMjA5MjlMazgtZkJRM01FRXJ3Yk5wZUJSRW8yUEc5THM4VEZBd3V0LVhiRHBBWExnTElPMTRCX3d1ODhKR2lDdHVDVktTZS1BTUtuLXN2ZGRwUmpnNzhEdDJBZnp3cHExVndUYWlrenVEOXI0dVppdw?oc=5)（Reuters）
- [US provides $206 million for Gaza force despite deadlocked peace plan - Reuters](https://news.google.com/rss/articles/CBMiswFBVV95cUxNSDlEb1ZYVnh6OFBkdGh1aW9EQi1CUnQyMTl3dFpBenBWRXJlR0NLLVdQeU9jOHQ4amlnQVpmNk5GVDBLVXhaZXFHUXVrNVhldlEwSWZPNGlDS0JEeHZULXpkbFJNVFBZX284a3hPNHJQT3Zzdnd1WnNGX3lFRVRYYy1jYk5TMzlWcWM0M3pzbTNqTUdORUNlTWJTTjdnZDVfLWxmaUlxVzh0cjZPQ1V4eGQzMA?oc=5)（Reuters）

**财报日历（关注标的）**
- **ADNH** 2026-08-27  · EPS预期 —
- **ADSK** 2026-08-27  · EPS预期 3.18
- **AFRM** 2026-08-27 amc · EPS预期 0.35
- **AWF** 2026-08-27  · EPS预期 —
- **BBY** 2026-08-27  · EPS预期 1.35
- **BILI** 2026-08-27  · EPS预期 1.54
- 美债收益率回落，利于风险资产估值修复。
- 美股行业轮动：健康 领涨（+3.51%），科技 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +10.03%，仓位 38.7%，持股 15,285 股，均价 23.75。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.86 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +26.80%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +8.50%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +51.37%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(26.7分) · 港股最高 阿里巴巴(57.4分) · 美股最高 英伟达(70.9分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **微软**（美股）| 建议观察 | 评分 69.1 | 待突破 | 趋势过滤通过 | 止损缓冲 6.6% / 目标空间 23.8% | 决策 61.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **阿里巴巴**（港股）| 弱信号观察 | 评分 57.4 | 待突破 | 趋势过滤未过 | 止损缓冲 9.0% / 目标空间 32.5% | 决策 59.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 -2.11% | 距止损 6.5% | 距目标 +33.5% | 持有 17 天


**候选池前列**（按评分）：

- 英伟达 70.9分 建议观察 RSI 54.2 RS +1.39%

- 微软 69.1分 建议观察 RSI 63.5 RS +18.20%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.595）。

*在线学习：市场环境 risk_on · 修订 r595 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.3 · PEG 8.50 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 15.3 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.6 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 19.61 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 95.7 | 符合风格 · 建议关注 | PE 7.2 · ROE 11.3%

  - PE 7.19 — 深度价值区间，安全边际充足；PB 0.93 — 资产折价，经典格雷厄姆信号

- **招商银行**（A股）| 匹配 90.3 | 符合风格 · 建议关注 | PE 6.8 · PEG 9.72 · ROE 11.9%

  - PE 6.81 — 深度价值区间，安全边际充足；PB 0.87 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.2 · PEG 0.27 · ROE 9.2%

  - PEG 0.27 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 20.6 · PEG 0.65 · ROE 24.8%

  - PEG 0.65 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **贵州茅台**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.9 · ROE 33.0%

  - ROE 33.0% — 优质复利机器，芒格会长期持有；净利率 47.86% — 轻资产高毛利特征

- **泡泡玛特**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 13.8 · PEG 5.10 · ROE 77.6%

  - ROE 77.6% — 优质复利机器，芒格会长期持有；净利率 34.42% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **Meta**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 20.5 · ROE 29.9%

  - 近一月 -15.19% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」

- **泡泡玛特**（港股）| 匹配 97.8 | 符合风格 · 建议关注 | PE 13.8 · PEG 5.10 · ROE 77.6%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 13.82 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **微软**（美股）| 匹配 94.0 | 符合风格 · 建议关注 | PE 26.8 · PEG 0.85 · ROE 34.0%

  - 近一月 +21.76% — 趋势强劲，反身性正反馈；相对强度 +19.11% — 跑赢大盘，宏观共振

- **亚马逊**（美股）| 匹配 80.7 | 符合风格 · 建议关注 | PE 20.9 · PEG 8.63 · ROE 30.6%

  - 均线多头排列 — 趋势交易确认；高 Beta 放大趋势 — 索罗斯式进攻配置


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 413.3 · PEG 7.28 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 87.6 | 符合风格 · 建议关注 | PE 123.4 · PEG 77.60 · ROE 10.2%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 9 对 · 影子胜率 22.2% · 均边际 -0.05%

- 配对归因：9 对 · 影子胜率 22.2% · 均边际 -0.05%

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 64.4% 良好，门槛 -1; 偏多环境 T+5 胜率 72.3% 良好，门槛 -1

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [问财] **新天然气：新天然气-2026年第一次临时股东会会议资料**（新天然气 (603393.SH)）
  公告…
- [问财] **洁特生物：关于“洁特转债”可选择回售的第九次提示性公告**（洁特生物 (688026.SH)）
  公告…
- [问财] **成都银行：成都银行股份有限公司关于召开2026年半年度业绩说明会的公告**（成都银行 (601838.SH)）
  公告…
- [问财] **通化金马：2026年半年度报告摘要**（通化金马 (000766.SZ)）
  公告…
- [问财] **通化金马：第十二届董事会第二次会议决议公告**（通化金马 (000766.SZ)）
  公告…
- [问财] **通化金马：2026年半年度报告**（通化金马 (000766.SZ)）
  公告…

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
3. ⚠️ 亚马逊 距止损仅 6.5%
4. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-08-20-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
