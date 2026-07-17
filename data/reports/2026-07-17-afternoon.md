# 投资决策日报 · 收盘前瞻

**2026年07月17日 14:08（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-17 12:26 · 宏观：2026-07-17 12:26 · 问财：2026-07-17 11:33

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **-1.78%**，综合情绪 **偏空**。风险厌恶情绪抬升，战术新开仓宜降频或观望；战役仓按网格纪律执行，避免情绪化减仓。

A股问财短线情绪 **震荡**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +7.69%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **0** 只、
下跌 **6** 只，平均涨跌 **-1.78%**。

**美股** -0.73%（偏弱）；**港股** -1.98%（偏弱）；**A股** -1.64%（偏弱）。相对弱势区域：美股、港股、A股，战术配置宜降权。

**波动居前指数：**

- **日经 225** 63,565.09，日涨跌 -4.89%（周 -7.28% / 月 -10.54%）
- **恒生指数** 24,514.29，日涨跌 -1.98%（周 +1.40% / 月 +0.08%）
- **上证指数** 3,818.59，日涨跌 -1.64%（周 -4.44% / 月 -7.05%）
- **纳斯达克** 25,881.95，日涨跌 -1.47%（周 -1.24% / 月 -3.01%）

### 1.2 A股短线情绪

问财统计涨停 **26** 家、跌停 **52** 家，情绪定性 **震荡**，涨跌停比约 **0.5 : 1**。跌多涨少，短线资金偏谨慎，追高需格外克制。

### 1.3 宏观与跨资产

- **VIX** 16.7（normal）
- **美10Y收益率** 4.57%
- **10Y-2Y 利差（FRED）** 0.41%（偏窄）
- **USDCNH** 6.7800（日 —）
- **美股行业**：必需消费 领涨，科技 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.55（变动 -0.66%，2026-07-15）
- 10Y-2Y 利差：0.41（变动 -2.38%，2026-07-16）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.7766（变动 -0.23%，2026-07-10）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [Oil rises on intensifying US-Iran hostilities and threat of Red Sea closure - Reuters](https://news.google.com/rss/articles/CBMiuAFBVV95cUxQYnAzc0RfelUyaHNBcU5ERWVndUwxNkhxOC1sREo3M2xoeGp0Vko0MTREMXludzBTcG52UVpvSmpRdlpLV2FFU0VNT2cybFU2b3NjTkhUMkZKWlNZMmo0RWFDV0pfSEU1RDFtVURxQjAtRVBXeTB6VWZCNUpFUVRJRFRSRDA0NzJlN1d2bjl5T3VLZ2lxQndYZ29SUFB0Y05YUkxzd1pOSktyME9XMTFMVWRsVnhRV2RG?oc=5)（Reuters）
- [Microsoft's Nadella rips Anthropic's Fable restrictions in staff meeting: 'Doesn't make sense'](https://www.cnbc.com/2026/07/16/microsoft-ceo-says-anthropic-fable-request-policy-doesnt-make-sense.html)（CNBC）
- [US House Republicans push forward on Trump funding plan for Iran war, election overhaul - Reuters](https://news.google.com/rss/articles/CBMizAFBVV95cUxPYW1SRVdSN09Ld296TUtRNjA3UGVjVGRFenVuOEQweFRZNjM0NUNkSktZY21KNEhhQllpMFd1cUtDeUVKclh1WmhtaV9IQWRUcThMZnRFRFVrNzJRSk5oR2VUXzlUWktfXzU0anQ3V0QwVEVTNlZibmlULVRiZFItcGFzNXVTLWx2SWw1ZERJa2V3cXZkbzFkRXo0LXJ4Zm1aY29RY200d2M3b0tOaU9NSFVabFdCRndISjZlbFB5UG9HcDdnRGN4bUlWQUI?oc=5)（Reuters）
- [Iran and US step up attacks, release of American in dispute - Reuters](https://news.google.com/rss/articles/CBMiogFBVV95cUxQbGxQSEpXZmFYRldBSGhRcTZWZlBvbUFOZFJDeVoxdXVZczVtY2w1TlhqSnhFaGxsSWlINnBKbDZhNi1mT0Q1anJRTjM0Z0toaVg3QXhMcmkyZlBQRTZ1cVZvbmhZSmU4WDU4NGdnN3FJZGRzbnYzdm0zQUVxWjNUZ1dTZHlwMTA0VTNhbUg0UHVxZmFLUlVtSmVfeHZCb0tfWEE?oc=5)（Reuters）
- [Dubai media office says no sounds of 'explosions' in downtown Dubai - Reuters](https://news.google.com/rss/articles/CBMioAFBVV95cUxQSF95OG9ET3BDTFJ1NGZZTlROWmJoNk90YVlsc2pPdzVTMG1PQm1DZzFNZWdZQUQ0aDlEUTFiaElRcGdpQWJkRGFXb0lPQ3ZiYkJwM3RxYmFoeElPblRfc2VqeFE5TFZaVVhtWUIxMF9LdUpoWFkzbk5nci0wcXFwV09DTWwzZnp5TEpIczdNMG1CMVpRX3JZT0ExdjUzaTZZ?oc=5)（Reuters）

**财报日历（关注标的）**
- **ABR** 2026-07-24  · EPS预期 0.05
- **ACRE** 2026-07-24 bmo · EPS预期 0.06
- **AXP** 2026-07-24 bmo · EPS预期 4.45
- **BAH** 2026-07-24  · EPS预期 1.51
- **CHTR** 2026-07-24  · EPS预期 10.37
- **CNH** 2026-07-24 bmo · EPS预期 0.11
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：必需消费 领涨（+2.80%），科技 靠后。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +7.69%，仓位 63.7%，持股 25,467 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：26.92 HKD。

- 下一档**滚动卖出**（涨 25%）：触发价 **29.35**，距现价 +9.00%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +49.32%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 中芯国际(59.0分) · 港股最高 美团(57.0分) · 美股最高 苹果(78.0分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 趋势达标待突破 | 评分 78.0 | 待突破 | 趋势过滤通过 | 止损缓冲 6.5% / 目标空间 23.4% | 决策 45.1

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **中芯国际**（A股）| 弱信号观察 | 评分 59.0 | 待突破 | 趋势过滤未过 | 止损缓冲 22.1% / 目标空间 79.4% | 决策 42.5

  - 逻辑：价格站上 60 日均线；均线多头排列

- **美团**（港股）| 弱信号观察 | 评分 57.0 | 待突破 | 趋势过滤未过 | 止损缓冲 13.5% / 目标空间 48.7% | 决策 41.5

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 苹果 78.0分 趋势达标待突破 RSI 71.4 RS +11.05%

- Meta 76.0分 建议观察 RSI 61.9 RS +10.59%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.167）。

*在线学习：市场环境 risk_off · 修订 r167 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 16.69 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.0 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 14.96 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 93.9 | 符合风格 · 建议关注 | PE 6.7 · PEG 9.52 · ROE 11.9%

  - PE 6.66 — 深度价值区间，安全边际充足；PB 0.85 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 93.9 | 符合风格 · 建议关注 | PE 7.0 · ROE 11.3%

  - PE 7.03 — 深度价值区间，安全边际充足；PB 0.91 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.5 · PEG 0.27 · ROE 9.2%

  - PEG 0.27 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - PEG 0.73 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 16.7 · PEG 0.73 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 74.3 · PEG 28.69 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **泡泡玛特**（港股）| 匹配 97.8 | 符合风格 · 建议关注 | PE 14.8 · PEG 5.47 · ROE 77.6%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 14.84 — 悲观中仍有估值支撑

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 22.5 · PEG 0.27 · ROE 9.2%

  - 近三月 -26.41% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 86.0 | 符合风格 · 建议关注 | PE 39.7 · PEG 1.82 · ROE 141.5%

  - 近一月 +12.43% — 趋势强劲，反身性正反馈；相对强度 +12.7% — 跑赢大盘，宏观共振

- **Meta**（美股）| 匹配 86.0 | 符合风格 · 建议关注 | PE 24.8 · PEG 0.40 · ROE 32.9%

  - 近一月 +11.97% — 趋势强劲，反身性正反馈；相对强度 +12.24% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 447.4 · PEG 7.88 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 94.0 | 符合风格 · 建议关注 | PE 175.2 · PEG 1.92 · ROE 8.1%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：影子 T+5 54.2%/-1.4% vs 生产 57.7%/1.26% · 24 笔成熟

- 战术自适应：门槛 -1 · 中决策分 T+5 胜率 64.1% 良好，门槛 -1; A股 T+5 胜率 66.7% 良好，门槛 -1（市场门槛→-2）

- 队列待办：**流水线过期 · 行情·荐股·模拟盘** — 检查工作流 update-market-data.yml 日志与 Secrets。

---

## 六、资讯与主题线索

- [Yahoo] **Netflix Reported Record Quarterly Revenue of $12.6 Billion, but Guidance Came in Below Expectations. Here’s What It Means for Investors.**（NVDA）
  That guidance miss didn't help improve sentiment on the beaten-down streaming giant.…
- [Yahoo] **2 Stocks Down 44% and 30% to Buy Right Now and Hold for the Next Decade**（NVDA）
  These two beaten-down consumer giants could reward investors willing to look past today's challenges and think 10 years …
- [Yahoo] **Dow Jones Futures Fall, Netflix Dives, SpaceX Scrubs Launch After Latest AI Sell-Off**（^GSPC）
  The Nasdaq tumbled on Sandisk, Micron, other AI stocks, but regional banks and transports rose. SpaceX fell late as a St…
- [Yahoo] **Why Did AAPL, ATAI, UNH Stocks Jump To 52-Week Highs Today?**（AAPL）
  Apple, AtaiBeckley and UnitedHealth Group jumped to yearly highs as positive company catalysts, Wall Street upgrades, an…
- [Yahoo] **Why Abbott Stock Jumped Today**（NVDA）
  A recent acquisition is already bearing fruit.…
- [Yahoo] **Should You Buy Intuitive Surgical With the Stock Down 35%? Here's What History Says.**（NVDA）
  Intuitive Surgical is a leader in surgical robotics, and the stock has a history of deep drawdowns.…

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
2. 待突破观察：苹果 突破位 328.73
3. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-07-17-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
