# 投资决策日报 · 收盘前瞻

**2026年07月27日 14:53（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-27 12:57 · 宏观：2026-07-27 12:58 · 问财：2026-07-27 11:58

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **-1.36%**，综合情绪 **偏空**。风险厌恶情绪抬升，战术新开仓宜降频或观望；战役仓按网格纪律执行，避免情绪化减仓。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +12.38%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **0** 只、
下跌 **6** 只，平均涨跌 **-1.36%**。

**美股** -1.44%（偏弱）；**港股** -0.18%（震荡）；**A股** -1.22%（偏弱）。相对弱势区域：美股、A股，战术配置宜降权。

**波动居前指数：**

- **日经 225** 64,813.63，日涨跌 -2.42%（周 -3.03% / 月 -6.30%）
- **纳斯达克** 25,137.69，日涨跌 -2.15%（周 -2.88% / 月 -1.76%）
- **上证指数** 3,829.39，日涨跌 -1.22%（周 +1.73% / 月 -7.06%）
- **标普 500** 7,408.30，日涨跌 -1.21%（周 -1.67% / 月 +0.58%）

### 1.2 A股短线情绪

问财统计涨停 **74** 家、跌停 **3** 家，情绪定性 **偏多**，涨跌停比约 **24.7 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 18.7（elevated）
- **美10Y收益率** 4.70%
- **10Y-2Y 利差（FRED）** 0.36%（偏窄）
- **USDCNH** 6.7700（日 —）
- **美股行业**：工业 领涨，可选消费 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.71（变动 +0.86%，2026-07-23）
- 10Y-2Y 利差：0.36（变动 +5.88%，2026-07-24）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.776（变动 +0.05%，2026-07-17）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [Gold gains on pause in US-Iran fighting; Fed decision looms - Reuters](https://news.google.com/rss/articles/CBMiogFBVV95cUxOVHhXdm1LMW9wUmp6UHctWldmTGpCQWlBOWVTdk5GeEtuMzNYQU42TGlWWXQtSDAxeE1aa3JvNFRDRUx6WVB5eGliS21TMEluRkJEUndXeHE1MUYzUVZlZG9CQ1V4VXFITFIyMEhJNUNlczhueTJpX2FjbFBoSmVkSnZJX0pQOS05RExueWpHMGpRMElqUTBVV0lqajBCRG9Kc1E?oc=5)（Reuters）
- [Shares, bonds make guarded gains as oil slips - Reuters](https://news.google.com/rss/articles/CBMie0FVX3lxTFA2VEF4Z09wNW9GaGZxaENhMVk5X3ZPSVhjSDNwb1ZKeld2S0xDZFNkZ1l6RDRNdHZ6bktSMnhrOFpNNTJQaU83eEtHa3FVQ0swVjVjSGF0SDlqbjZoWVpQbW1icmJoM1Y2TldZUERiTHdGNUpRbnpWR080TQ?oc=5)（Reuters）
- [Dollar pulls back as US-Iran attacks pause, oil drops - Reuters](https://news.google.com/rss/articles/CBMipwFBVV95cUxQdWQ5R1NLZkN4LVQtZkhaQVlCVE9jV0pFNE5JamoxMFdleEdnS0I5YjhzVWtOVW5RVHk0d1BhSVRSc2I0THJIbzlrWXVhX00wemJRX2c2eTRKQ1BOb3FIZnBONjhvUktZVzlWRFl2RG1EYUQ1NTctRWFGa0htZzNBQ2dQdTVZSnBHZ2FXYkpNUVJJVVZQVGkzZ0IzbEZPQUF0dkVMOTBhMA?oc=5)（Reuters）
- [Red Sea shipping slows after Houthi attack on Saudi Arabia, data shows - Reuters](https://news.google.com/rss/articles/CBMivAFBVV95cUxQNWxxNDU1SHBqVXozbmd1VHRWYVpQWGVqVUVTUHVlakJjS2lKMHBCbDJCS1hucGROTV90dUhuNS1mUEdKVEtBZjR2b1FwSFZJejdVLWR3WFMxWGV6NVk5YWFOa2o3ZHdnX1R2enpyRm53YnBmRmZyS2trSjFiQ2VSbjZQZ2JhbTdRbnh0RVlleDhYTmtUUjJWN0JpTV9lNXU1X3cwazNYcHhzZkNic1hQdTdxMXZEaEM5MDhQZA?oc=5)（Reuters）
- [Oil slips 4% after US, Iran pause fighting over weekend - Reuters](https://news.google.com/rss/articles/CBMipAFBVV95cUxNZXVDd2dEeUdKdzZkTFduSnE1cGp0S2YtaGwyNTRxekczRW5TdGdtM3JGTFFtYlNiSzNsTVFmTzlYZ0ttZmtJdGtjU3g4U0FPUnFPenFkaWp3ZENtbzFGVFdtUk11TzRSbzg3dmZvWVFqRHZDR3FBZEpxR2dSZEUwU0w3d0pRUkVHd3dWZXg3Yk95SjdMbUZxdDEyTDlaRHdFN3JXLQ?oc=5)（Reuters）

**财报日历（关注标的）**
- **AACB** 2026-08-03  · EPS预期 —
- **ABTC** 2026-08-03  · EPS预期 0.00
- **ADEA** 2026-08-03  · EPS预期 0.31
- **ADTN** 2026-08-03  · EPS预期 0.13
- **ADUS** 2026-08-03  · EPS预期 1.73
- **AEIS** 2026-08-03 amc · EPS预期 2.24
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：工业 领涨（+1.73%），可选消费 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +12.38%，仓位 65.2%，持股 25,467 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：28.76 HKD。

- 下一档**滚动卖出**（涨 25%）：触发价 **29.35**，距现价 +2.10%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +53.81%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(60.6分) · 港股最高 美团(63.9分) · 美股最高 苹果(74.1分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 弱信号观察 | 评分 74.1 | 待突破 | 趋势过滤未过 | 止损缓冲 5.8% / 目标空间 20.9% | 决策 48.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **美团**（港股）| 弱信号观察 | 评分 63.9 | 待突破 | 趋势过滤未过 | 止损缓冲 11.7% / 目标空间 42.2% | 决策 47.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **招商银行**（A股）| 弱信号观察 | 评分 60.6 | 待突破 | 趋势过滤未过 | 止损缓冲 4.8% / 目标空间 17.2% | 决策 48.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.250）。

*在线学习：市场环境 risk_off · 修订 r250 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 15.87 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 15.89 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 6.8 · PEG 9.74 · ROE 11.9%

  - PE 6.82 — 深度价值区间，安全边际充足；PB 0.87 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.3 · ROE 11.3%

  - PE 7.35 — 深度价值区间，安全边际充足；PB 0.95 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.8 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - PEG 0.69 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 78.1 · PEG 30.15 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 22.8 · PEG 0.28 · ROE 9.2%

  - 近三月 -24.42% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **谷歌**（美股）| 匹配 88.5 | 符合风格 · 建议关注 | PE 16.1 · PEG 5.46 · ROE 48.7%

  - 近一月 -8.22% — 市场悲观，邓普顿式逆向机会；PE 16.05 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 69.4 | 部分符合 · 观察等待 | PE 40.3 · PEG 1.85 · ROE 141.5%

  - 近一月 +9.3% — 趋势强劲，反身性正反馈；相对强度 +8.72% — 跑赢大盘，宏观共振

- **美团**（港股）| 匹配 67.2 | 部分符合 · 观察等待 | PE 19.2 · ROE -24.1%

  - 近一月 +36.91% — 趋势强劲，反身性正反馈；相对强度 +29.42% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 395.0 · PEG 6.95 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 91.9 | 符合风格 · 建议关注 | PE 175.2 · PEG 1.92 · ROE 8.1%

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

- [Yahoo] **Dow Jones Futures Rise, Oil Prices Dive On Iran Hopes; Apple Leads Earnings Wave, Fed Meeting Ahead**（^GSPC）
  U.S.-Iran attacks have paused amid deal hopes. Apple, Amazon, Meta lead an earnings wave. A Fed rate hike is on the tabl…
- [Yahoo] **Prediction: CEO Andy Jassy Will Raise Amazon's Full-Year 2026 Capex Guide on July 30**（NVDA）
  Amazon has already guided for $200 billion of artificial intelligence (AI)-related capital expenditures in 2026.…
- [Yahoo] **Alphabet, Amazon, and Meta Will Spend Over $500 Billion on AI in 2026. Nvidia Collects a Huge Share.**（NVDA）
  Three of the biggest AI budgets on Earth seem to just keep growing. The company selling the hardware fell anyway.…
- [Yahoo] **This Quantum Stock Is a Key Nvidia Partner and Looks Like a Buy Near a 52-Week Low**（NVDA）
  Infleqtion is securing the right partnerships and customers that can set it up for a multiyear run when quantum computin…
- [Yahoo] **Nvidia Deepens South Korea AI Push With $1 Billion NAVER Investment**（NVDA）
  NVIDIA Corp (NASDAQ:NVDA) plans to invest about $1 billion in NAVER Corp as part of a broader effort to expand artificia…
- [Yahoo] **SK Hynix, Samsung Ink $950 Billion AI Chip Deals, But Stocks Still Slide**（NVDA）
  SK Hynix and Samsung signed $950 billion in AI chip deals with Nvidia and Broadcom, yet both stocks fell Monday as inves…

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
2. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-07-27-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
