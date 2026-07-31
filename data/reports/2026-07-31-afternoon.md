# 投资决策日报 · 收盘前瞻

**2026年07月31日 18:47（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-31 18:16 · 宏观：2026-07-31 18:16 · 问财：2026-07-31 17:51

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+1.75%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **震荡**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +12.78%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **6** 只、
下跌 **0** 只，平均涨跌 **+1.75%**。

**美股** +1.88%（偏强）；**港股** +0.10%（震荡）；**A股** +0.72%（偏强）。相对强势区域：美股、A股。

**波动居前指数：**

- **日经 225** 64,362.02，日涨跌 +4.03%（周 -0.39% / 月 -8.67%）
- **纳斯达克** 25,122.18，日涨跌 +2.78%（周 -0.06% / 月 -4.16%）
- **标普 500** 7,437.63，日涨跌 +1.66%（周 +0.40% / 月 -0.82%）
- **道琼斯** 52,208.06，日涨跌 +1.19%（周 +0.96% / 月 -0.21%）

### 1.2 A股短线情绪

问财统计涨停 **99** 家、跌停 **76** 家，情绪定性 **震荡**，涨跌停比约 **1.3 : 1**。涨跌家数相对均衡，结构性机会为主。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 16.8（normal）
- **美10Y收益率** 4.66%
- **10Y-2Y 利差（FRED）** 0.45%（偏窄）
- **USDCNH** 6.7500（日 —）
- **美股行业**：科技 领涨，通信 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.67（变动 +1.30%，2026-07-29）
- 10Y-2Y 利差：0.45（变动 0.00%，2026-07-30）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.7719（变动 +0.03%，2026-07-24）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [Oil falls on slightly improved flows through Gulf; set for monthly gain - Reuters](https://news.google.com/rss/articles/CBMiqwFBVV95cUxNTWtnbUQ2S2JIalNxeXVETFdYcU95VDBtOHpPdlAxWDkzd1B0VVBPNnNpMW8xTGVRbkJ1NTFqbmJ0Ui1ucUUtSVhZeXZwRTQ4eE5FTWRkdzBlZEVJUzZHR0tKdnZTeXFoQlFPSHpGX0pqaEVVU3RhWFJqR2xNZnVJeDdOaG9ONUEtaThtRXhXakladzRkT2JvR1hxSEREVmxkRGRjQWw5ZTNoeTQ?oc=5)（Reuters）
- [IBM CEO says quantum computing will have a 'measurable impact' on earnings by 2028 or 2029](https://www.cnbc.com/2026/07/30/ibm-ceo-quantum-computing-measurable-impact-earnings-2028-2029.html)（CNBC）
- [US cyber defense agency warns hackers are increasingly targeting water systems - Reuters](https://news.google.com/rss/articles/CBMitAFBVV95cUxNdWNJNFA5THZLRlg3TTVYX2tkQmJzOUdQamtWQXZDOU81R1RTdjBtX3E2S3k3RlVfR2p6WE9uZGpfbzNCUHpGN0hhZ3ROY3pmN1FiS1JZa0FjQ2FDMDZuOUFRSjJad0wyX3lZWUFfQ1FjdGs4RGZvRVpnYzBwT1o0UlkyaGVRTkpvdVo0SmpCUkdhWFN3TEVaVHpfTnB1YWUwbzNuMUpoa2VsdHdtM2hNZ2JaRUE?oc=5)（Reuters）
- [Drone strike in Egypt sparks security concerns about Suez oil exports - Reuters](https://news.google.com/rss/articles/CBMiugFBVV95cUxNY19zWlhiQmx4WmRhRHRLMUdTbjhwdEdVcHpaUmMtWndRMlB1MFNiZ2pJMzJZcFJQWEJSTzdfSGl6R0FXV016c2JUODlSV0Y3ZzBEbWRFeUVkRDQxQ2p5S0VPRWoyc0lZS3pobjVGR0l5YTV1V1FEbmE2N1BscGlFZWlLTjl6Qmp4TDJmalFTX1ZYVUJEYkV2NjBCWVhuNmRsdC1UZzBCVm1GQ2djejdiWUo1UnBfT1UzNmc?oc=5)（Reuters）
- ['The Odyssey' extends stay in 70mm IMAX theaters as shows sell out weeks in advance](https://www.cnbc.com/2026/07/30/the-odyssey-70mm-imax-run-extended-until-september.html)（CNBC）

**财报日历（关注标的）**
- **ACMR** 2026-08-07  · EPS预期 0.34
- **AIRS** 2026-08-07 bmo · EPS预期 0.01
- **AIRT** 2026-08-07  · EPS预期 —
- **AMR** 2026-08-07 bmo · EPS预期 -0.27
- **ANIP** 2026-08-07  · EPS预期 2.09
- **ASIX** 2026-08-07  · EPS预期 0.57
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：科技 领涨（+5.50%），通信 靠后。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +12.78%，仓位 62.1%，持股 24,344 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：28.78 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **32.87**，距现价 +14.20%。

- 下一档**回撤买回**（回撤 10%）：触发价 **28.69**，距现价 +0.30%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +53.81%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(68.5分) · 港股最高 京东集团(82.7分) · 美股最高 苹果(82.2分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 弱信号观察 | 评分 82.2 | 待突破 | 趋势过滤未过 | 止损缓冲 6.1% / 目标空间 21.8% | 决策 60.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **美团**（港股）| 趋势达标待突破 | 评分 77.4 | 待突破 | 趋势过滤通过 | 止损缓冲 11.7% / 目标空间 42.3% | 决策 57.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **招商银行**（A股）| 弱信号观察 | 评分 68.5 | 待突破 | 趋势过滤未过 | 止损缓冲 5.2% / 目标空间 18.8% | 决策 60.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 京东集团 82.7分 趋势达标待突破 RSI 69.3 RS +10.51%

- 美团 77.4分 趋势达标待突破 RSI 68.7 RS +17.43%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.297）。

*在线学习：市场环境 risk_on · 修订 r297 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 16.98 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 15.9 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.6 · ROE 11.3%

  - PE 7.57 — 深度价值区间，安全边际充足；PB 0.98 — 资产折价，经典格雷厄姆信号

- **招商银行**（A股）| 匹配 98.9 | 符合风格 · 建议关注 | PE 6.9 · PEG 9.91 · ROE 11.9%

  - PE 6.94 — 深度价值区间，安全边际充足；PB 0.88 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 24.1 · PEG 0.29 · ROE 9.2%

  - PEG 0.29 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - PEG 0.74 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 67.4 · PEG 26.01 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **Meta**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.1 · PEG 0.35 · ROE 32.9%

  - 近三月 -20.5% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 24.1 · PEG 0.29 · ROE 9.2%

  - 近三月 -19.44% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 86.1 | 符合风格 · 建议关注 | PE 41.0 · PEG 1.88 · ROE 141.5%

  - 近一月 +15.23% — 趋势强劲，反身性正反馈；相对强度 +16.05% — 跑赢大盘，宏观共振

- **微软**（美股）| 匹配 86.1 | 符合风格 · 建议关注 | PE 21.7 · PEG 0.93 · ROE 34.0%

  - 近一月 +20.93% — 趋势强劲，反身性正反馈；相对强度 +21.75% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 91.1 | 符合风格 · 建议关注 | PE 399.5 · PEG 7.03 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 70.6 | 部分符合 · 观察等待 | PE 142.8 · PEG 1.57 · ROE 8.1%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 25 对 · 影子胜率 40.0% · 均边际 0.1%

- 配对归因：25 对 · 影子胜率 40.0% · 均边际 0.10%

- 战术自适应：门槛 -2 · 中决策分 T+5 胜率 64.0% 良好，门槛 -1; 偏多环境 T+5 胜率 61.5% 良好，门槛 -1

- 队列待办：**影子轨积累中** — 无需操作，继续观察 shadow_reco.json comparison。

---

## 六、资讯与主题线索

- [Yahoo] **Meet the Micron and SK Hynix Competitor That Just Rocketed 466% Higher in 1 Day**（NVDA）
  How big a threat is the competition after receiving billions in fresh capital?…
- [Yahoo] **Teetering US stock market faces jobs report, big earnings week**（^GSPC）
  By Lewis Krauskopf NEW YORK, July 31 (Reuters) - U.S. employment data and a batch of corporate results this coming week …
- [Yahoo] **Dow Jones Futures: Apple, Amazon Diverge Late; What To Do After AI Stocks Surge**（^GSPC）
  The stock market jumped Thursday as Microsoft powered a big AI rebound. Apple and Amazon led earnings late.…
- [Yahoo] **A Can Of Coke Cost 35 Cents When Warren Buffett First Bought Shares in 1988. Here’s How Much You’d Have If You’d Invested $10,000 In Coca-Cola Stock Then.**（NVDA）
  Warren Buffett quietly poured over a billion dollars into Coca-Cola stock back when a can cost pocket change, then never…
- [Yahoo] **If a Bear Market Is Coming in 2026, History Says This 1 Investment Is the Safest Place to Park Your Money**（^GSPC）
  It might not be a good choice over the long term.…
- [Yahoo] **Realty Income Reports Earnings Aug. 5. Here's How Much $15,000 Invested Pays Annually.**（NVDA）
  More of the same is exactly what investors want from the surprisingly rewarding dividend payer.…

---

## 七、风险提示

1. 本报告基于公开行情与规则化模型，**不构成投资建议**；战术实验与战役 XRPS 为相互独立的两套体系，请勿混仓决策。  
2. 港股 / 美股存在汇率、流动性及隔夜缺口风险；A股须关注涨跌停制度下的执行偏差。  
3. 问财等非官方数据源可能延迟或缓存；涨停榜等情绪指标需与实时盘口交叉验证。  
4. 模拟盘收益不代表未来表现；连阴月加仓逻辑基于历史回测，极端宏观冲击下可能失效。
5. 大师风格荐股为规则化模拟，非真实人物操作建议；基本面数据可能有延迟或缺失。

---

## 八、本时段关注清单

1. 小米滚动卖出触发：涨 40% @ 32.87
2. 小米回撤买回触发：回撤 10% @ 28.69
3. 待突破观察：苹果 突破位 344.57
4. 待突破观察：美团 突破位 94.50
5. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-07-31-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
