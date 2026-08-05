# 投资决策日报 · 收盘前瞻

**2026年08月05日 14:17（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-08-05 12:19 · 宏观：2026-08-05 12:20 · 问财：2026-08-05 11:28

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+1.81%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +10.83%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **6** 只、
下跌 **0** 只，平均涨跌 **+1.81%**。

**美股** +2.03%（偏强）；**港股** +0.11%（震荡）；**A股** +1.34%（偏强）。相对强势区域：美股、A股。

**波动居前指数：**

- **日经 225** 66,075.04，日涨跌 +3.31%（周 +7.55% / 月 -5.25%）
- **纳斯达克** 26,584.99，日涨跌 +2.59%（周 +6.87% / 月 +1.78%）
- **标普 500** 7,736.52，日涨跌 +1.79%（周 +4.14% / 月 +2.64%）
- **道琼斯** 54,085.88，日涨跌 +1.71%（周 +2.54% / 月 +1.94%）

### 1.2 A股短线情绪

问财统计涨停 **88** 家、跌停 **2** 家，情绪定性 **偏多**，涨跌停比约 **44.0 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。

### 1.3 宏观与跨资产

- **VIX** 16.5（normal）
- **美10Y收益率** 4.63%
- **10Y-2Y 利差（FRED）** 0.43%（偏窄）
- **USDCNH** 6.7500（日 —）
- **美股行业**：科技 领涨，公用事业 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.7（变动 -1.05%，2026-08-03）
- 10Y-2Y 利差：0.43（变动 -4.44%，2026-08-04）
- 联邦基金利率：3.63（变动 0.00%，2026-07-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.7509（变动 -0.06%，2026-07-31）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [Oil steadies after two-day slump as investors eye Hormuz traffic - Reuters](https://news.google.com/rss/articles/CBMiswFBVV95cUxOZDd2cFJ5Z2dsbTliajVMY1o5eVQ3Q3djdGVaYXA2aVhJQUROSVk5NmVjSkUydkw0YUItOGI1VFl1Wl9uZVY2SWhZLVZZY2hFTTFyaEoxM0otRWQ0Vzk4bjdEV18yYkhQS05GUzQ5dHdsY0wwemg4cG53dnZkVmx0M1pMdzl2cDk2MDBlZlN3ZVY0RVMxU2JNcE5Ta2Nrd3l4OVpvTnlIY0hscHRpOUozRVpDUQ?oc=5)（Reuters）
- [Qatar says mediators make progress in efforts to end US-Iran war - Reuters](https://news.google.com/rss/articles/CBMipgFBVV95cUxOaUY3M2pidURfcVlodzZaVEctbGNSYS1rNlJrR21pQm8yVm50U05QSmRlWURQWWh5UklWZUVMVmlRdzhmbVJrN05IdVNXVW83T3l1TUo0ZjJTMzNURzlOdmNMM2YxY2JwVHQtby1aTFVfZmFnSjRFT0hSaHlzeW50XzNPcUZROG13MUxxNVMwdGd3UkR2cTgyeURHNERQWlUxeFJYR1ln?oc=5)（Reuters）
- [Stock indexes register records after upbeat company forecasts; oil drops - Reuters](https://news.google.com/rss/articles/CBMie0FVX3lxTE9FbUhCcDNQSE1IQ3dnM055RTJNZ0N1WHYtTUswbUtjZmRTS3FwbEtKZkd5Ti1WT0JndWtUSEJJTktud19OQzRELW93em1SMFdjcnphTVBMQ1BPMzBJLTdEYmxMbnJ2bFB4NVN4ZVlKYjIyZUlFZGx3RUljSQ?oc=5)（Reuters）
- [Dow, S&P 500 close at record on AI-linked earnings, Mideast deal hopes - Reuters](https://news.google.com/rss/articles/CBMitAFBVV95cUxOMHk5N1NJZXlfQ196NTA1SjFaUUtUaDd0UXNDY2FsLWM2aE1VTElKc1oxaXFMbmd1M2kwcXVmaFBKbEo3TmFmY2lfRVFraDFVcTZpTTNfbGU2VU9iZnQ0Q2xBR0ZCVHFmRUktbVk0VTR1RVVYNzVxNEVUa3dJbmFQXzQ0SldqNzVoSXAtRnF3SDJ0M0UwNEhRLVhsUTd3Yk9jdnhTQUJ0WGdOUEdRTHJfeUpKZUw?oc=5)（Reuters）
- [Jim Cramer says one hedge fund's collapse cleared the way for tech's rally](https://www.cnbc.com/2026/08/04/cramer-one-hedge-fund-collapse-cleared-way-for-tech-rally.html)（CNBC）

**财报日历（关注标的）**
- **AADX** 2026-08-12  · EPS预期 0.03
- **AAPI** 2026-08-12  · EPS预期 —
- **AASP** 2026-08-12  · EPS预期 —
- **ABEO** 2026-08-12  · EPS预期 -0.23
- **AC** 2026-08-12  · EPS预期 —
- **ACRS** 2026-08-12  · EPS预期 -0.16
- 美债收益率回落，利于风险资产估值修复。
- 美股行业轮动：科技 领涨（+4.98%），公用事业 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +10.83%，仓位 57.6%，持股 22,889 股，均价 23.75。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.88 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +26.70%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +8.50%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +64.32%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(72.9分) · 港股最高 美团(77.9分) · 美股最高 微软(83.0分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **亚马逊**（美股）| 建议观察 | 评分 73.6 | 待突破 | 趋势过滤通过 | 止损缓冲 9.0% / 目标空间 32.4% | 决策 57.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

- **招商银行**（A股）| 弱信号观察 | 评分 72.9 | 待突破 | 趋势过滤未过 | 止损缓冲 5.5% / 目标空间 19.7% | 决策 60.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **京东集团**（港股）| 建议观察 | 评分 72.6 | 待突破 | 趋势过滤通过 | 止损缓冲 6.5% / 目标空间 23.3% | 决策 57.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 +2.15% | 距止损 10.4% | 距目标 +27.9% | 持有 2 天


**候选池前列**（按评分）：

- 微软 83.0分 趋势达标待突破 RSI 79.0 RS +24.05%

- 美团 77.9分 趋势达标待突破 RSI 67.4 RS +8.60%

- 亚马逊 73.6分 建议观察 RSI 67.0 RS +10.24%

- 京东集团 72.6分 建议观察 RSI 71.8 RS +14.64%

- 英伟达 68.2分 建议观察 RSI 56.9 RS +5.00%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.326）。

*在线学习：市场环境 risk_on · 修订 r326 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.7 · PEG 0.77 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 17.71 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.4 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 15.4 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 76.3 | 符合风格 · 建议关注 | PE 7.7 · ROE 11.3%

  - PE 7.65 — 深度价值区间，安全边际充足；PB 0.96 — 资产折价，经典格雷厄姆信号

- **招商银行**（A股）| 匹配 73.0 | 符合风格 · 建议关注 | PE 7.0 · PEG 9.99 · ROE 11.9%

  - PE 7.0 — 深度价值区间，安全边际充足；PB 0.87 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 23.2 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.7 · PEG 0.77 · ROE 20.5%

  - PEG 0.77 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.7 · PEG 0.77 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 62.0 · PEG 23.93 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 23.2 · PEG 0.28 · ROE 9.2%

  - 近三月 -19.5% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **泡泡玛特**（港股）| 匹配 85.4 | 符合风格 · 建议关注 | PE 14.7 · PEG 5.44 · ROE 77.6%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 14.73 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 21.6 · PEG 0.68 · ROE 24.8%

  - 近一月 +8.57% — 趋势强劲，反身性正反馈；相对强度 +11.49% — 跑赢大盘，宏观共振

- **美团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.6 · ROE -24.1%

  - 近一月 +18.19% — 趋势强劲，反身性正反馈；相对强度 +8.04% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 437.2 · PEG 7.70 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 161.1 · PEG 1.77 · ROE 8.1%

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

- [Yahoo] **Is Micron Stock Going Higher? You Need To Hear What Elon Musk Just Said**（NVDA）
  SpaceX is ramping up spending, and that could mean big things for Micron.…
- [Yahoo] **Hyperscaler Rally: 4 Stocks to Buy Before It's Too Late**（NVDA）
  Now is the time to buy hyperscaler stocks as they start to break out.…
- [Yahoo] **Covered-Call Trap: Why JEPQ’s Income Distributions Are Taxed Like a Paycheck, Not Dividends**（^IXIC）
  JEPQ's monthly checks look generous until the IRS shows up and takes a cut that most yield-focused investors never see c…
- [Yahoo] **Tech back in fashion as Asian markets extend rebound**（^GSPC）
  Asian equities climbed again Wednesday, tracking another record on Wall Street, as tech firms continued to enjoy a reviv…
- [Yahoo] **Dow Jones Futures Rise; SpaceX, AMD, Arista Lead Earnings Movers After S&P 500 Jumps To High**（^GSPC）
  The Dow and S&P 500 hit new highs while the Nasdaq powered higher again. SpaceX, AMD and Arista led earnings movers late…
- [Yahoo] **Why Backblaze Stock Jumped Today**（NVDA）
  The data management specialist is partnering with an artificial intelligence (AI) leader.…

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

*报告 ID：`2026-08-05-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
