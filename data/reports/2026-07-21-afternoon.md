# 投资决策日报 · 收盘前瞻

**2026年07月21日 14:21（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-21 12:25 · 宏观：2026-07-21 12:25 · 问财：2026-07-21 11:39

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.43%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏空**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +10.09%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **3** 只、
下跌 **3** 只，平均涨跌 **+0.43%**。

**美股** -0.28%（震荡）；**港股** +0.03%（震荡）；**A股** +0.62%（偏强）。相对强势区域：A股。

**波动居前指数：**

- **日经 225** 65,905.01，日涨跌 +2.75%（周 -1.99% / 月 -7.50%）
- **上证指数** 3,819.66，日涨跌 +0.62%（周 -3.72% / 月 -8.25%）
- **道琼斯** 51,839.26，日涨跌 -0.59%（周 -1.26% / 月 +0.67%）
- **标普 500** 7,443.28，日涨跌 -0.19%（周 -0.96% / 月 +0.31%）

### 1.2 A股短线情绪

问财统计涨停 **46** 家、跌停 **100** 家，情绪定性 **偏空**，涨跌停比约 **0.5 : 1**。跌多涨少，短线资金偏谨慎，追高需格外克制。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 18.6（elevated）
- **美10Y收益率** 4.60%
- **10Y-2Y 利差（FRED）** 0.39%（偏窄）
- **USDCNH** 6.7700（日 —）
- **美股行业**：能源 领涨，健康 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.55（变动 -0.44%，2026-07-17）
- 10Y-2Y 利差：0.39（变动 +5.41%，2026-07-20）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.776（变动 +0.05%，2026-07-17）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [What is China's next surprise for oil markets? Lower imports, higher fuel exports? - Reuters](https://news.google.com/rss/articles/CBMi2wFBVV95cUxNNkVNby0tbVgtVUxCWFJyNVVXM2V4VUVOb0tDdlFLOUc4djJnRi1jTTBTNnY4T2doUVlYaWVyZkhHbU9CLTV2cDcwQzJTTGttdWIzZHpidkFiQ2RlSV9fbEFmcE9nVHlfQXRoUTFvOUFvUFJQQURsUkxFMUFWaXV6QnBYdmtrRTY2YlhYWk41clc4WlNTdUswYlZLNFBXeGlBQ0VvS0xWZ181cEdvdVF3djNLeUtwQ3VVMllwemJZNkRJTHc4cU9mXzAycGFWdUxkSy13MU1zTmZRdWc?oc=5)（Reuters）
- [Asian stocks rise as Mideast mediation takes oil lower - Reuters](https://news.google.com/rss/articles/CBMihAFBVV95cUxQNlZ6UW5NX1ZjZ3BJZXota1l4Qnc0SjdPWnZGTmsybzNSTXM4cWl1YzlhQ3BnbGREVWVvdjdGNU1nY2c4aFIyMFBkR1J2VkFreGt4d2RQLUgySFd4VjlGLWhKT1hSNzRoa3dmdks2RHJYOGRxamQzTTk0U3g2NWtzZGhobXA?oc=5)（Reuters）
- [Oil prices dip as mediation efforts offset US-Iran strikes - Reuters](https://news.google.com/rss/articles/CBMiqwFBVV95cUxPNE0xMnZLYmlVcE1nLTJzaGpmMW5pWkZyRWY3c3I5YnJtMlZ2OFo4TTlZTnJTTnRlUmpRRnFmcnB3S1U0bmx6N0k0LVp5YUFqX2tJeUZxX3Y1YjJIOTN2YWFSbi14ZzJ4THhoTG9XMi1WenpMd1dwTVhGYnFrWlRZTF9MSG15d2dpUE9uQUlDbmNtY0E4YVNmOU1jdnVudnU4aWhIWjlPRnNMdUU?oc=5)（Reuters）
- [Wall Street indexes fall, with Iran and earnings season in focus - Reuters](https://news.google.com/rss/articles/CBMixgFBVV95cUxOakxUc2hmUzNWRUJsczdpQTNsVHY4ZURqeFpTOEZkSFlGMk8zRFZxZHE5aHNIRUtTYzAwejgweG55eXNZQTc5S083Vm9HbGQ4T1E1S1RBbjcxQVJGdGFwcnNJM0pIbzRZZGtSV3hBQUZLSVp4V0pXUFRKMGZyZ0xqY0VIaHBtUjItQUY5dXgzREZYT0xUNWJJTkxlSUhrUS1FczhIYkV6VDJHQndKOFJJUm5zYy1OdVV3dVlUWGFrQjB2OGN0TUE?oc=5)（Reuters）
- [Houthi Red Sea blockade would lift oil prices, but workarounds could limit impact - Reuters](https://news.google.com/rss/articles/CBMixwFBVV95cUxNV09nNHJnRVFremV5MkNFSW9ER3Q2bDllSURrWk5tOGpvN0Q5X0xaX2VMTlFZY04tenI5WEltOEZvV25qSjQ1blhnRG1VUGxQZEljSFhfakNrMjZfUkk0SWZPN1BtTDVzb29BOGVPQ2VzWV9pT2U0dThaZDU5Ump6VnZYek5XZlpJR0NWanhrNTAxRnMyT0hqemZieUtjN2x2Y3dUX0tkdUY0SHRTaEk2dmxVZGVYUHpEX3FlRE43VDVwMVpyb3BV?oc=5)（Reuters）

**财报日历（关注标的）**
- **AAT** 2026-07-28  · EPS预期 0.12
- **AB** 2026-07-28  · EPS预期 0.85
- **ABG** 2026-07-28  · EPS预期 6.37
- **ACGL** 2026-07-28 amc · EPS预期 2.48
- **ACHC** 2026-07-28 amc · EPS预期 0.35
- **ACR** 2026-07-28  · EPS预期 0.18
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：能源 领涨（+0.45%），健康 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +10.09%，仓位 64.4%，持股 25,467 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.86 HKD。

- 下一档**滚动卖出**（涨 25%）：触发价 **29.35**，距现价 +5.30%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +54.63%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 中芯国际(65.6分) · 港股最高 美团(56.3分) · 美股最高 苹果(80.9分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 趋势达标待突破 | 评分 80.9 | 待突破 | 趋势过滤通过 | 止损缓冲 6.4% / 目标空间 23.1% | 决策 60.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **中芯国际**（A股）| 弱信号观察 | 评分 65.6 | 待突破 | 趋势过滤未过 | 止损缓冲 21.7% / 目标空间 78.3% | 决策 58.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **美团**（港股）| 弱信号观察 | 评分 56.3 | 待突破 | 趋势过滤未过 | 止损缓冲 12.7% / 目标空间 45.7% | 决策 57.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 苹果 80.9分 趋势达标待突破 RSI 63.9 RS +11.26%

- Meta 70.0分 建议观察 RSI 56.8 RS +14.70%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.194）。

*在线学习：市场环境 risk_off · 修订 r194 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.1 · PEG 0.75 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 17.1 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.5 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 15.48 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 6.7 · PEG 9.53 · ROE 11.9%

  - PE 6.67 — 深度价值区间，安全边际充足；PB 0.85 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.2 · ROE 11.3%

  - PE 7.25 — 深度价值区间，安全边际充足；PB 0.93 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.9 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.1 · PEG 0.75 · ROE 20.5%

  - PEG 0.75 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.1 · PEG 0.75 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 81.8 · PEG 31.57 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 22.9 · PEG 0.28 · ROE 9.2%

  - 近三月 -25.7% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **腾讯控股**（港股）| 匹配 85.4 | 符合风格 · 建议关注 | PE 17.1 · PEG 0.75 · ROE 20.5%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 17.1 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 69.2 | 部分符合 · 观察等待 | PE 40.5 · PEG 1.86 · ROE 141.5%

  - 近一月 +10.35% — 趋势强劲，反身性正反馈；相对强度 +10.04% — 跑赢大盘，宏观共振

- **Meta**（美股）| 匹配 69.2 | 部分符合 · 观察等待 | PE 23.5 · PEG 0.38 · ROE 32.9%

  - 近一月 +13.79% — 趋势强劲，反身性正反馈；相对强度 +13.48% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 79.9 | 符合风格 · 建议关注 | PE 426.3 · PEG 7.50 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 63.8 | 部分符合 · 观察等待 | PE 164.0 · PEG 1.80 · ROE 8.1%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：影子 T+5 55.6%/-1.1% vs 生产 57.7%/1.07% · 27 笔成熟

- 战术自适应：门槛 -1 · 中决策分 T+5 胜率 64.1% 良好，门槛 -1; A股 T+5 胜率 67.1% 良好，门槛 -1（市场门槛→-2）

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **AI infrastructure stock surges after landing massive $2.8B win**（NVDA）
  Some contract announcements move stocks. And then there are the ones that reframe an entire investment thesis. We saw th…
- [Yahoo] **Dow Jones Futures: Trump Comments Spark Stock Market Losses; Elon Musk-Led SpaceX, Tesla Tumble**（NVDA）
  Dow Jones Futures: Trump sparked losses Monday after he said Iran "will pay" for killing American soldiers. SpaceX and T…
- [Yahoo] **NBIS Stock Jumps Overnight As Nvidia Reveals Over 9% Stake, Analyst Sees More Upside**（NVDA）
  The stake is higher than estimated in March, when Nvidia announced a $2 billion investment in the neocloud operator.…
- [Yahoo] **Jamie Dimon Won’t Buy S&P 500 or Bonds. Here Are the Warnings Investors Are Missing**（^GSPC）
  Jamie Dimon says he would not buy stocks or long bonds at current prices. Here are the four warnings behind that call.…
- [Yahoo] **A Ransomware Attack Just Halted Coca-Cola's Fairlife Production and Knocked the Stock Down 4%. Should Dividend Investors Care?**（NVDA）
  A cyberattack shut down one of the company's fastest-growing brands. Here's how much it actually matters.…
- [Yahoo] **Nasdaq, S&P 500 Futures Rise As Chip Rally Counters Iran Jitters Ahead Of Big Tech Earnings: Why IREN, ACHR, TSLA, BA Stocks Are Drawing Focus**（^GSPC）
  Chip stocks staged a comeback on Monday, gaining at the close after a sharp selloff last week.…

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
2. 待突破观察：苹果 突破位 334.99
3. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-07-21-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
