# 投资决策日报 · 收盘前瞻

**2026年09月04日 20:39（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-09-04 17:06 · 宏观：2026-09-04 17:07 · 问财：2026-09-04 17:34

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+1.06%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓 XRPS 模拟收益率 +10.90%，按网格与月线纪律执行。

战术实验有 **1** 笔 open 持仓，本日重点跟踪止损距离与突破延续性。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **5** 只、
下跌 **1** 只，平均涨跌 **+1.06%**。

**美股** +1.21%（偏强）；**港股** +1.74%（偏强）；**A股** -0.30%（震荡）。相对强势区域：美股、港股。

**波动居前指数：**

- **恒生指数** 25,650.87，日涨跌 +1.74%（周 +0.26% / 月 +0.47%）
- **纳斯达克** 26,584.06，日涨跌 +1.40%（周 +0.16% / 月 +0.84%）
- **日经 225** 65,020.94，日涨跌 +1.26%（周 -2.09% / 月 -1.93%）
- **道琼斯** 53,686.11，日涨跌 +1.18%（周 +0.22% / 月 -1.22%）

### 1.2 A股短线情绪

问财统计涨停 **70** 家、跌停 **4** 家，情绪定性 **偏多**，涨跌停比约 **17.5 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 14.2（normal）
- **美10Y收益率** 4.76%
- **10Y-2Y 利差（FRED）** 0.43%（偏窄）
- **USDCNH** 6.7100（日 —）
- **美股行业**：金融 领涨，能源 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.79（变动 0.00%，2026-09-02）
- 10Y-2Y 利差：0.43（变动 +7.50%，2026-09-03）
- 联邦基金利率：3.63（变动 0.00%，2026-08-01）
- 美国失业率：4.1（变动 -2.38%，2026-07-01）
- 美元/人民币(官方)：6.726（变动 +0.09%，2026-08-28）
- 美国CPI指数：332.8（变动 +1.63%，2026-07-01）

**Finnhub 宏观要闻**
- [Oil prices set for weekly gain as US-Iran hostilities intensify - Reuters](https://news.google.com/rss/articles/CBMiygFBVV95cUxOQVZJdUE0TzFvS2xtSUJLOVUxZUVRZVRpMi1aUlNuSFZzX3h5TW4zSGJya0w3SjFlSno4QUlvdU90cHBBOS1xRllCZjR2aVRnUW16ZmQyN3M1SlRVSl9BYlk2Z2dvWGIzdEo3cXdTZjdWZkIzYXRNRzk3ZkM2cWMwN2ZWMVh1T09pNnRKVVAwRDhNSnJnSTFwVi1MZXdMNUNwOFJTU215REpkR1V0X1pVa09vNkVHeG9oX2lpVjdoTVl1ajI5MzU0dUN3?oc=5)（Reuters）
- [US probes Iran wedding strike that analysis shows was likely direct hit by US munition - Reuters](https://news.google.com/rss/articles/CBMiywFBVV95cUxPdWJyTEVVNzlNV2lCVktTZkk3dHZpYUFndlRkdTVXMzlnR0hEMXZYVnN5U3V5dC1JMEpWVDMwZng4YjhUc3pfOVpiNWNwdDRwbHY1TFhMLWZFZFh3YlF2SVEwYnJjNGkzTlpGR0hsRkwyMkQ4QVRSdmV4Ykxtd0xZamtOYkNNUV90TzhWdnF5ejhGRGhxSHgtcmp0SGdFVkhUa2owblM0QnN0aDRpeXlnRlBHUDdqZnE5TmRjd2FuR1dyVE5qY3VsNFJHWQ?oc=5)（Reuters）
- [Deadly strike on Iranian wedding was likely a direct hit by a US munition, analysis shows - Reuters](https://news.google.com/rss/articles/CBMixAFBVV95cUxQUEFXVU5xRXZGVUVkV3B2TUVQcTBseVZsSGd0blBwQktIaGlIc3R5TzMtNXFISkFTb1VOdlhWOXBmQ052RWFuT1pQaXJqQndNaXB3TmhLQTZPQXNQSFFXQ3JGY0NBdE1RY09razBPZFh2VnJiYmlBSld3akdLeHZxbVA5bWNqVWFycjFlUHFNd3VPdE4tYTFVaWxmdDBoOUlxUk80X0dkbkFqOV9SU3lxNkFsd0JGZnB5Qk9SV3JGWkxRWlhn?oc=5)（Reuters）
- [Vance says Iran conflict is not a war, declines to offer timeline for end - Reuters](https://news.google.com/rss/articles/CBMitwFBVV95cUxOVWVqMkRjNklKdUhYTF9BTE5GN1ctUG5zaGI0cVdEcW9ReEhYMmxJREpHX1o5RE5mS1VZMHAwTlBTTmZhWURSV3dMUkY1YjhBMjZEN2hvZWhYc1hiaTk1MFRacnpEVDVYWnRuTEVrVW8yZnRnTVUxcTV0UEd5NXRRVDlzTmM0NFA5b3o3Q3JPMFhHMGFJb3JVN05DTVZSbUZlNHlNVFdMTmhmajRfR25zZ05LblhOZjg?oc=5)（Reuters）
- [South Korea reviewing military options for Hormuz, no decision made, official says - Reuters](https://news.google.com/rss/articles/CBMivAFBVV95cUxPdWViay1UelBGa2N2MVRMeTBDRUFURDhZblFPbFcwLXc1VG92Y3ZTeE1ZZHU3b1JicEYxOHBEdWQzSEQ1aXZiNmNCZjBVcUl0Y19yOGRQZE5wZjRkdHFYbzJxZTE3QTZDdlRVUGtFSTRyR0JSNkxRU0dBZGRTT1BWalZjdGpKV1BCRjFQV0dXTzZwZEw4aElNSXhJVy1ldVRZV2VqTlYzejVUdzZ3bUhoMlRpbFFsV2FWUjNYUg?oc=5)（Reuters）

**财报日历（关注标的）**
- **ANAB** 2026-09-11 amc · EPS预期 -0.07
- **BUKS** 2026-09-11  · EPS预期 —
- **CRMT** 2026-09-11  · EPS预期 -0.79
- **HOFT** 2026-09-11  · EPS预期 -0.02
- **MNY** 2026-09-11  · EPS预期 -0.02
- **RENT** 2026-09-11  · EPS预期 -4.42
- 美债收益率回落，利于风险资产估值修复。
- 美股行业轮动：金融 领涨（+1.56%），能源 靠后。
- 黄金强、原油弱 — 偏避险/衰退交易特征。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +10.90%，仓位 37.1%，持股 14,481 股，均价 23.75。

**月线状态**：连续 **1** 个月收跌，上月 -1.22%，近两月累计 +22.21%，近三月累计 -3.83%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：28.44 HKD。

- 下一档**滚动卖出**（涨 40%）：触发价 **35.32**，距现价 +24.20%。

- 下一档**回撤买回**（回撤 20%）：触发价 **25.50**，距现价 +10.30%。

- XRPS-X 运行正常：股数优先、成本优先、核心仓保留。

**长期参照**：上市以来 XRPS 回测收益率 +57.35%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 中国平安(65.6分) · 港股最高 小米集团(65.6分) · 美股最高 英伟达(75.6分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 建议观察 | 评分 72.5 | 待突破 | 趋势过滤通过 | 止损缓冲 5.3% / 目标空间 19.1% | 决策 60.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **中国平安**（A股）| 弱信号观察 | 评分 65.6 | 待突破 | 趋势过滤未过 | 止损缓冲 4.9% / 目标空间 17.6% | 决策 66.7

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **小米集团**（港股）| 弱信号观察 | 评分 65.6 | 待突破 | 趋势过滤未过 | 止损缓冲 10.6% / 目标空间 38.1% | 决策 62.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


**战术持仓跟踪**（实验策略，非战役仓）：

- **亚马逊**（美股）| 浮盈 -4.67% | 距止损 4.0% | 距目标 +37.1% | 持有 32 天 ⚠️ 接近止损


**候选池前列**（按评分）：

- 英伟达 75.6分 趋势达标待突破 RSI 59.2 RS +4.07%

- 苹果 72.5分 建议观察 RSI 63.5 RS +5.48%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.785）。

*在线学习：市场环境 risk_on · 修订 r785 · 市场环境(risk_on)：soros×1.08、lynch×1.06、serenity×1.08、graham×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 14.9 · PEG 8.29 · ROE 19.9%

  - ROE 19.91% — 盈利能力稳健；PE 14.93 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 20.0 · ROE 12.6%

  - ROE 12.63% — 盈利能力稳健；PE 20.03 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.2 · PEG 1.26 · ROE 11.5%

  - PE 7.2 — 深度价值区间，安全边际充足；PB 0.92 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.0 · PEG 0.13 · ROE 13.1%

  - PE 6.99 — 深度价值区间，安全边际充足；PB 1.03 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 18.7 · PEG 0.59 · ROE 24.8%

  - PEG 0.59 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 31.8% — 成长故事可验证

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.0 · PEG 0.13 · ROE 13.1%

  - PEG 0.13 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 52.6% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **谷歌**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 16.9 · PEG 5.76 · ROE 48.7%

  - ROE 48.68% — 优质复利机器，芒格会长期持有；净利率 54.77% — 轻资产高毛利特征

- **微软**（美股）| 匹配 81.4 | 符合风格 · 建议关注 | PE 28.4 · PEG 0.90 · ROE 34.0%

  - ROE 34.04% — 优质复利机器，芒格会长期持有；净利率 40.3% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **宁德时代**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 18.7 · PEG 0.59 · ROE 24.8%

  - 近一月 -9.21% — 市场悲观，邓普顿式逆向机会；PE 18.74 — 悲观中仍有估值支撑

- **腾讯控股**（港股）| 匹配 97.8 | 符合风格 · 建议关注 | PE 14.9 · PEG 8.29 · ROE 19.9%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 14.93 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **中国平安**（A股）| 匹配 87.8 | 符合风格 · 建议关注 | PE 7.0 · PEG 0.13 · ROE 13.1%

  - 近一月 +8.86% — 趋势强劲，反身性正反馈；相对强度 +8.1% — 跑赢大盘，宏观共振

- **招商银行**（A股）| 匹配 81.3 | 符合风格 · 建议关注 | PE 7.2 · PEG 1.26 · ROE 11.5%

  - 相对强度 +6.22% — 跑赢大盘，宏观共振；均线多头排列 — 趋势交易确认


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 44.5 · PEG 19.61 · ROE 64.6%

  - 光模块 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 光模块 — CPO/光互连供应链瓶颈

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 358.7 · PEG 6.32 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节


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

- [Yahoo] **BlackRock Wants 5% to 20% of Your Target-Date Fund in Private Assets**（NVDA）
  This initial offering may not go as far as some investors hoped, but it's a start for the accounts where private venture…
- [Yahoo] **Nasdaq Futures Edge Higher As Jobs Report Takes Center Stage: TSLA, LULU, ORCL, PL, NVDA, PLTR, RKLB In Focus**（^GSPC）
  Retail sentiment on Stocktwits remained ‘bearish’ on SPY and flipped to ‘bullish’ on QQQ.…
- [Yahoo] **Dow Jones Futures: Jobs Report Due After Bullish Market Move; Tesla Falls After Cybercab News**（^GSPC）
  The stock market jumped above key levels Thursday, buoyed by Snowflake and dovish Fed comments. Tesla Cybercabs are now …
- [Yahoo] **Everyone's Missing These 2 Game-Changing Numbers Buried in SpaceX's Latest Report**（NVDA）
  Have we been getting SpaceX's profit potential wrong?…
- [Yahoo] **AAPL Heads For Third Weekly Gain — But Foldable iPhone Is Reportedly Stuck At ‘A Few Hundred’ Units A Day**（AAPL）
  Apple is racing to scale foldable iPhone production ahead of its Sept. 9 debut as tight quality controls and memory shor…
- [Yahoo] **The Federal Reserve's Initial September Inflation Forecast Has Arrived, and It Contains a Glaring Red Flag for Wall Street**（^GSPC）
  Although headline inflation is projected to decline, a far more important price-change measure is predicted to reacceler…

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
3. ⚠️ 亚马逊 距止损仅 4.0%
4. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-09-04-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
