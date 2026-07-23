# 投资决策日报 · 收盘前瞻

**2026年07月23日 18:31（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-23 17:42 · 宏观：2026-07-23 17:42 · 问财：2026-07-23 17:32

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.21%**，综合情绪 **震荡**。指数方向不明，结构分化概率加大，宜精选个股、控制仓位，等待方向选择。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +8.25%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **3** 只、
下跌 **3** 只，平均涨跌 **+0.21%**。

**美股** -0.24%（震荡）；**港股** +1.28%（偏强）；**A股** +0.25%（震荡）。相对强势区域：港股。

**波动居前指数：**

- **恒生指数** 25,210.81，日涨跌 +1.28%（周 +0.81% / 月 +8.03%）
- **纳斯达克** 25,690.90，日涨跌 -0.57%（周 -2.20% / 月 -1.82%）
- **日经 225** 66,422.60，日涨跌 +0.46%（周 -3.39% / 月 -4.82%）
- **上证指数** 3,876.78，日涨跌 +0.25%（周 -0.15% / 月 -5.69%）

### 1.2 A股短线情绪

问财统计涨停 **100** 家、跌停 **1** 家，情绪定性 **偏多**，涨跌停比约 **100.0 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。（部分榜单沿用缓存，盘中宜以实时行情为准）

### 1.3 宏观与跨资产

- **VIX** 17.6（normal）
- **美10Y收益率** 4.66%
- **10Y-2Y 利差（FRED）** 0.36%（偏窄）
- **USDCNH** 6.7700（日 —）
- **美股行业**：公用事业 领涨，通信 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.63（变动 +0.65%，2026-07-21）
- 10Y-2Y 利差：0.36（变动 -2.70%，2026-07-22）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.776（变动 +0.05%，2026-07-17）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [EXCLUSIVE: Buyers to press Qatar, UAE for cheaper, more flexible LNG deals after Hormuz shock - Reuters](https://news.google.com/rss/articles/CBMiwwFBVV95cUxNTk54Z0F2YlpXOS0tWUs2V1hwZ0cyRTN3MHo1VGQ4b2FIb0Q1bng3bXRpY2M4X1M3OVgxWHpsanpRRVk0QTdhYU9qWkJKd3ZJejU0TnpWREJZcFBVWC04YTYxWll4TXVXdTdRdlBoQTI2ZDU2SzYyWHY1NURjckpYQXdmZFpvWmtsVURZZ1pPaWt4MzlWUDBIUHNpenMzMkRhVGI3eUJEM1h1dU0wRThBY3E4NzJpUmF6elI3dk1Xekl2TG8?oc=5)（Reuters）
- [TotalEnergies posts strongest profit in nearly three years as Iran conflict lifts oil prices - Reuters](https://news.google.com/rss/articles/CBMivwFBVV95cUxOUER3VHByUm5HZ2kwZ2szVWZ3cURpT0w4MkQ0VkRlUGpCLWI2b2ZLdThEV3ZmdXFRd2lhM3hBcnl5ZHAwOERRb0d0SXBZaHpsM3duMjlncFZHcktoc2U3S3dtUGtNLTV5VE1FaTFmWXp2VVc3QmZGRmMtaVh5MENmMU1kc2IzMlc1dVlXV1dyQWFWNW5aYmszalVURjdDOTI1UV8yamdPRFYyNHhQSTJWbkJkVXlLdXhoTElpZW1nWQ?oc=5)（Reuters）
- [Houthis say they attacked Saudi tankers in the Red Sea, threatening new chokepoint in Iran war - Reuters](https://news.google.com/rss/articles/CBMizgFBVV95cUxOck9rMklSSHp1Z0E2UmlqZUJHSWNxRXNSZGtZd1JTOFdSbUE2amI3RHFmaUNuSS1nU1NzaThJdVIwVzZFcXVIaXNjU3lrSVYtaDF5THNwWkpqUHVwTEFsWklsbnp4ZllTMndIYWhRM0RZa09qaTNiVXVCNmh5a2p6MnBidG1kWkJSUVJnb1RuOXdUcU5MRDVxbzJmcDE2UWZsaVZYRDdCdHlYcG1kUTdKT093ZXI4b3VkWjZNRzdDUDIwWEFWMHRia2FIY3dIdw?oc=5)（Reuters）
- [US military completes 12th straight night of strikes on Iran - Reuters](https://news.google.com/rss/articles/CBMirAFBVV95cUxQSTE4NEl0QlphNDg2Z3VzWFlvd3cxQjBmVzYtOC1HS18tRTNNUWJodlRhUzI4M05DN1lhLWZJWkJCU2wzaXVfVEdqWTBJSmtjeTI1M1BmRkdOclRtOGtCQ3B4bWpxbFVSeXMxRWtwdUtpdFRCOFNLVGFHaFFYRGUtOHZZbFdpRlNScTI5TVZBbi1uMVRvWDlHSWx2RlYxWkFrVGItb1RsdkRpQThH?oc=5)（Reuters）
- [Two Chinese supertankers with Saudi oil head to Bab el-Mandeb for Red Sea exit - Reuters](https://news.google.com/rss/articles/CBMiwAFBVV95cUxPMzBfZ2dVYUNDa2lMZlVQYXFfSWU3bWlaZjRVTV9DM0V3NjRDN2pvWnRhMVE4T2RwYXhGdTd1ZEMybWE4ekJGcC1Oa3lsWnFwQ1ZISE5XcUZOazlVaEZQaU9jLTQ2UmstZkZ3UWw5amhGQU1TTVY4VGRXX2R6d0xOMENmTmlYTHBKOGJnRTNDdzVZQ1p3NXA0alZSOVJxV0dwS3AxQkliUkpES0hneVdYMmtjNFpERW1TRkNUVDN5Z2E?oc=5)（Reuters）

**财报日历（关注标的）**
- **AAPL** 2026-07-30 amc · EPS预期 1.93
- 美债收益率上行，对高估值成长股形成压力。
- 美股行业轮动：公用事业 领涨（+2.25%），通信 靠后。
- 原油强、黄金弱 — 偏再通胀/增长预期。
- FRED：10Y-2Y 利差偏窄，宏观流动性预期趋紧。

*数据源：Yahoo Finance、Frankfurter (ECB)、FRED (St. Louis Fed)、Finnhub*

### 1.4 本时段研判侧重

尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

---

## 二、战役持仓（XRPS-X 小米滚动仓）

**标的**：小米集团（1810.HK）

**模拟净值**：收益率 +8.25%，仓位 63.8%，持股 25,467 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.14 HKD。

- 下一档**滚动卖出**（涨 25%）：触发价 **29.35**，距现价 +8.10%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +54.63%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 贵州茅台(67.0分) · 港股最高 美团(51.4分) · 美股最高 苹果(80.8分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 趋势达标待突破 | 评分 80.8 | 待突破 | 趋势过滤通过 | 止损缓冲 6.2% / 目标空间 22.4% | 决策 50.5

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **贵州茅台**（A股）| 弱信号观察 | 评分 67.0 | 待突破 | 趋势过滤未过 | 止损缓冲 6.4% / 目标空间 22.9% | 决策 49.5

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

- **美团**（港股）| 弱信号观察 | 评分 51.4 | 待突破 | 趋势过滤未过 | 止损缓冲 12.9% / 目标空间 46.5% | 决策 49.5

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 苹果 80.8分 趋势达标待突破 RSI 62.5 RS +9.74%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.223）。

*在线学习：市场环境 neutral · 修订 r223*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 15.91 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.0 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 14.99 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **中国平安**（A股）| 匹配 81.8 | 符合风格 · 建议关注 | PE 7.5 · ROE 11.3%

  - PE 7.49 — 深度价值区间，安全边际充足；PB 0.97 — 资产折价，经典格雷厄姆信号

- **招商银行**（A股）| 匹配 77.9 | 符合风格 · 建议关注 | PE 6.8 · PEG 9.73 · ROE 11.9%

  - PE 6.81 — 深度价值区间，安全边际充足；PB 0.87 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 23.1 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - PEG 0.69 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 79.6 · PEG 30.74 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 23.1 · PEG 0.28 · ROE 9.2%

  - 近三月 -23.96% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **腾讯控股**（港股）| 匹配 85.4 | 符合风格 · 建议关注 | PE 15.9 · PEG 0.69 · ROE 20.5%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 15.91 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 6.8 · PEG 9.73 · ROE 11.9%

  - 近一月 +8.75% — 趋势强劲，反身性正反馈；相对强度 +14.44% — 跑赢大盘，宏观共振

- **京东集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.3 · ROE 6.0%

  - 近一月 +16.34% — 趋势强劲，反身性正反馈；相对强度 +8.31% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 405.6 · PEG 7.14 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 99.1 | 符合风格 · 建议关注 | PE 181.7 · PEG 1.99 · ROE 8.1%

  - 半导体 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · GPU/CPU — 算力供应链关键环节


*大师风格荐股为规则化模拟，非真实人物操作建议；权重学习基于历史快照与公开行情，样本不足时变化极小；Serenity 相关内容为对其公开框架的量化近似，勿当作 X 账号买卖信号；仅供研究，不构成投资建议。*

---

## 五、持续进化状态

**系统进化看板**（GitHub Actions 自动维护）

- 影子轨：影子 T+5 55.6%/-1.1% vs 生产 57.7%/1.07% · 27 笔成熟

- 战术自适应：门槛 -1 · 中决策分 T+5 胜率 64.1% 良好，门槛 -1; A股 T+5 胜率 67.1% 良好，门槛 -1（市场门槛→-2）

- 队列待办：**影子轨积累中** — 无需操作，继续观察 shadow_reco.json comparison。

---

## 六、资讯与主题线索

- [问财] **山鹰国际：关于控股股东部分股份解除质押及再质押的公告**（山鹰国际 (600567.SH)）
  公告…
- [问财] **华电新能：华电新能源集团股份有限公司关于控股股东国有股份无偿划转的提示性公告**（华电新能 (600930.SH)）
  公告…
- [问财] **瑞立科密：财通证券股份有限公司关于广州瑞立科密汽车电子股份有限公司发行股份购买资产暨关联交易之标的资产过户情况的独立财务顾问核查意见**（瑞立科密 (001285.SZ)）
  公告…
- [问财] **瑞立科密：关于发行股份购买资产暨关联交易之标的资产过户完成的公告**（瑞立科密 (001285.SZ)）
  公告…
- [问财] **瑞立科密：上海市锦天城律师事务所关于广州瑞立科密汽车电子股份有限公司发行股份购买资产暨关联交易之标的资产过户情况的法律意见书**（瑞立科密 (001285.SZ)）
  公告…
- [问财] **高能环境：高能环境关于回购事项前十大股东及前十大无限售条件股东持股情况的公告**（高能环境 (603588.SH)）
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

1. 小米滚动卖出触发：涨 25% @ 29.35
2. 待突破观察：苹果 突破位 334.99
3. 收盘前：核对战役/战术止损位是否需手动校准（模拟盘仅作纪律参照）

---

*报告 ID：`2026-07-23-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
