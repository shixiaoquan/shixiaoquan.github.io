# 投资决策日报 · 收盘前瞻

**2026年09月22日 21:19（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-09-22 18:15 · 宏观：2026-09-22 18:16 · 问财：2026-09-22 17:53

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+1.01%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +9.10%，按网格与月线纪律执行。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **6** 只、
下跌 **0** 只，平均涨跌 **+1.01%**。

**美股** +1.49%（偏强）；**港股** +0.18%（震荡）；**A股** +0.06%（震荡）。相对强势区域：美股。

**波动居前指数：**

- **纳斯达克** 27,122.09，日涨跌 +2.26%（周 +3.57% / 月 +4.05%）
- **标普 500** 7,764.70，日涨跌 +1.49%（周 +1.90% / 月 +1.62%）
- **日经 225** 65,018.95，日涨跌 +1.38%（周 +1.57% / 月 -1.81%）
- **道琼斯** 52,048.83，日涨跌 +0.71%（周 -0.71% / 月 -1.35%）

### 1.2 A股短线情绪

问财统计涨停 **70** 家、跌停 **4** 家，情绪定性 **偏多**，涨跌停比约 **17.5 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 14.8（normal）
- **美10Y收益率** 4.96%
- **10Y-2Y 利差（FRED）** 0.20%（偏窄）
- **USDCNH** 6.7000（日 —）
- **美股行业**：通信 领涨，能源 靠后

**FRED 官方序列**
- 美10年期国债收益率：5.01（变动 +1.42%，2026-09-18）
- 10Y-2Y 利差：0.2（变动 -20.00%，2026-09-21）
- 联邦基金利率：3.63（变动 0.00%，2026-08-01）
- 美国失业率：4.1（变动 0.00%，2026-08-01）
- 美元/人民币(官方)：6.6975（变动 -0.15%，2026-09-18）
- 美国CPI指数：334.1（变动 +1.16%，2026-08-01）

**Finnhub 宏观要闻**
- [Trump set for whirlwind UN meetings with wars in Iran, Ukraine on agenda - Reuters](https://news.google.com/rss/articles/CBMisgFBVV95cUxOOFdkQk9aWHdzT0hrcFhDNDZPSmlwQVBUUm12TGd4SUVPUURUMVo4Y3I0WHZBSTIxdjdKTWZ4WkF3cVUzUnlrWmNrbTA5T21UN3R0Z0JnekdrZm5ReC1ZS2JmUWVQRXRVNzhaYmNucDI5YVh6d2JxeHp5Yi00Y3p2d0loRTY5YXNiWGRHTlJZb1ZiX1paMVh3UU1XVThfUXR2NHF3T0pod3BBS3VpU3AyTDB3?oc=5)（Reuters）
- [Oil rises amid worries of growing Iran-U.S. tensions after Bessent issues Iranian airline shutdown warning](https://www.cnbc.com/2026/09/22/oil-iran-us-bessent-un-crude.html)（CNBC）
- [Alibaba deepens AI push with new chip, bigger model; shares jump 5% - Reuters](https://news.google.com/rss/articles/CBMi1gFBVV95cUxPUlcybzdOMWxNcmJHT1ZvUHFRTkczZzRNbHpkeUM1QjVxak5WMVdfTldrMWRtaTdHd1FvZkUwbGN4NmhwdUFSdmJxdVBVTGZxNFBWMUNqQXU3dlJzM1VXOHZsYmliZmxBRl90eFF6dEFZWl9BQTJTdkdxaDBSMGVrSXBJUkFVQkx1RTFOcktHZDQ4blo4VFh0amtSRmYxU2YxeGdQdUhFa25DeDBjSllsaVBsUVQ3X3VYdnRKMTAxN1BzZFQzUUpGSVI3TXZBZmRuTlhjejFB?oc=5)（Reuters）
- [G7 foreign ministers call on Iran to stop arming Houthis - Reuters](https://news.google.com/rss/articles/CBMiowFBVV95cUxQS01wSTFweHdPbVI1QkNWSXlpQzMxd1FsX0lCcnBpNlQ4dFFVeDdTLWkxNmJNWEdBUi1iZ3VYQ0JjbGdIeGY4Q0ZZXzB6NW9fdVpkSXpLSzdvSzBKNHVBZDNVVGJJV1ZDZXNYMGpwVW9fMklhN0hjMVRia3FNcGFITkVrd1QyTVc4SWI3VXpyelRzbG5uTVZjZkNEZ1lETnpObGs4?oc=5)（Reuters）
- [Indian shares edge higher on easing oil prices, bond yields; IT caps gains - Reuters](https://news.google.com/rss/articles/CBMiuAFBVV95cUxOQXlPVWFzejJKbzBBSVA5ZFhMbUdTZ0VVS1RZVXBpMlJRZC1Lak9aNmdldDEwdVZ1RGlPMjlUUFdFSGdocFlTbVpjLTFLcXJsN2VqTFhVZ1d0YmYwLTBUNG9tUHVmWEs2Q1E3em4za29OcHo3MFk2Q0twV3M5WFB4Q2ppeW9LVnd3SzJ2SHhLN1N6MTI4YVU0dDBuS0htU3R5SW9maHVnR2NDUFlManVqYTRidGZiYzVv?oc=5)（Reuters）

**财报日历（关注标的）**
- **BTM** 2026-09-29  · EPS预期 -0.45
- **CAG** 2026-09-29  · EPS预期 0.28
- **CNXC** 2026-09-29 amc · EPS预期 2.76
- **CTRM** 2026-09-29  · EPS预期 —
- **GFUZ** 2026-09-29  · EPS预期 —
- **KMX** 2026-09-29  · EPS预期 0.72
- 美债收益率回落，利于风险资产估值修复。
- 美股行业轮动：通信 领涨（+3.90%），能源 靠后。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +9.10%，仓位 36.1%，持股 14,481 股，均价 23.75。

**月线状态**：连续 **1** 个月收跌，上月 -1.22%，近两月累计 +22.21%，近三月累计 -3.83%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.20 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +29.90%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +6.20%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +54.15%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 招商银行(52.4分) · 港股最高 阿里巴巴(57.8分) · 美股最高 苹果(85.1分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **Meta**（美股）| 建议观察 | 评分 69.0 | 待突破 | 趋势过滤通过 | 止损缓冲 9.2% / 目标空间 33.2% | 决策 59.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **阿里巴巴**（港股）| 弱信号观察 | 评分 57.8 | 待突破 | 趋势过滤未过 | 止损缓冲 7.4% / 目标空间 26.7% | 决策 57.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

- **招商银行**（A股）| 弱信号观察 | 评分 52.4 | 待突破 | 趋势过滤未过 | 止损缓冲 4.2% / 目标空间 15.1% | 决策 60.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 苹果 85.1分 趋势达标待突破 RSI 66.4 RS +8.15%

- AMD 75.4分 建议观察 RSI 73.0 RS +30.37%

- 微软 71.1分 建议观察 RSI 57.3 RS +3.51%

- Meta 69.0分 建议观察 RSI 77.9 RS +35.17%

- 谷歌 67.2分 建议观察 RSI 58.9 RS +3.52%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.865）。

*在线学习：市场环境 risk_on · 修订 r865 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.2 · PEG 8.42 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 15.15 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 19.0 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 19.02 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 76.3 | 符合风格 · 建议关注 | PE 6.5 · PEG 0.12 · ROE 13.1%

  - PE 6.54 — 深度价值区间，安全边际充足；PB 0.96 — 资产折价，经典格雷厄姆信号

- **招商银行**（A股）| 匹配 69.8 | 部分符合 · 观察等待 | PE 7.0 · PEG 1.24 · ROE 11.5%

  - PE 7.05 — 深度价值区间，安全边际充足；PB 0.9 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **宁德时代**（A股）| 匹配 92.8 | 符合风格 · 建议关注 | PE 16.3 · PEG 0.51 · ROE 24.8%

  - PEG 0.51 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证

- **微软**（美股）| 匹配 92.8 | 符合风格 · 建议关注 | PE 27.9 · PEG 0.88 · ROE 34.0%

  - PEG 0.88 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.7% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **谷歌**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 17.8 · PEG 6.06 · ROE 48.7%

  - ROE 48.68% — 优质复利机器，芒格会长期持有；净利率 54.77% — 轻资产高毛利特征

- **Meta**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 27.9 · ROE 29.9%

  - ROE 29.85% — 优质复利机器，芒格会长期持有；净利率 29.83% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.3 · PEG 0.51 · ROE 24.8%

  - 近一月 -21.46% — 市场悲观，邓普顿式逆向机会；近三月 -22.11% — 深度回调，关注基本面是否错杀

- **美团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.2 · ROE -21.8%

  - 近一月 -11.49% — 市场悲观，邓普顿式逆向机会；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 38.9 · PEG 1.36 · ROE 148.8%

  - 近一月 +8.89% — 趋势强劲，反身性正反馈；相对强度 +7.27% — 跑赢大盘，宏观共振

- **AMD**（美股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 157.0 · PEG 98.75 · ROE 10.2%

  - 近一月 +31.11% — 趋势强劲，反身性正反馈；相对强度 +29.49% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 370.4 · PEG 23.30 · ROE 4.0%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **中际旭创**（A股）| 匹配 95.4 | 符合风格 · 建议关注 | PE 50.8 · PEG 22.38 · ROE 64.6%

  - 光模块 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 光模块 — CPO/光互连供应链瓶颈


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：配对归因 17 对 · 影子胜率 23.5% · 均边际 0.1%

- 配对归因：17 对 · 影子胜率 23.5% · 均边际 0.10%

- 战术自适应：门槛 +0 · 港股 T+5 胜率 42.4% 偏低，门槛 +1（市场门槛→+1）; 美股 T+5 胜率 69.2% 良好，门槛 -1（市场门槛→-1）

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **3 No-Brainer Cybersecurity Stocks to Buy With $1,000 Right Now**（NVDA）
  Security spending keeps climbing as data breach costs hit record highs.…
- [Yahoo] **Bull of the Day: NVIDIA Corp. (NVDA)**（NVDA）
  Are you a believer again?…
- [Yahoo] **Nike vs. PepsiCo: Which Consumer Goods Dividend Stock Is the Better Buy for a Lifetime of Passive Income?**（NVDA）
  Which of these high-yield dividend stocks is the better play for ultra-long-term passive income right now?…
- [Yahoo] **2 Cannabis Stocks That Are Quietly Trouncing the Market in 2026**（^GSPC）
  Trulieve and Cronos are turning stronger results into market-beating gains.…
- [Yahoo] **Why Muse really just added billions to Meta's market cap and to Mark Zuckerberg's net worth**（AAPL）
  Why Muse is the new darling of Meta investors.…
- [Yahoo] **Should You Invest $1,000 in SCHD Right Now?**（^GSPC）
  The Schwab U.S. Dividend Equity ETF (SCHD) is up 23% year to date. The gains might not be done.…

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

*报告 ID：`2026-09-22-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
