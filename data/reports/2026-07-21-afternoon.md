# 投资决策日报 · 收盘前瞻

**2026年07月21日 18:31（北京时间）** · 午后至收盘策略 · 隔夜风险预案

> 数据来源：Yahoo Finance · Frankfurter(ECB) · FRED · Finnhub · 同花顺问财 · 量化策略引擎  
> 行情更新：2026-07-21 17:37 · 宏观：2026-07-21 17:38 · 问财：2026-07-21 17:37

---

## 核心观点

本报告为**收盘前瞻**，尾盘仓位管理、止损/止盈距离、次日开盘前需跟踪的变量。

全球跟踪指数平均涨跌 **+0.70%**，综合情绪 **偏多**。风险偏好有所修复，战术端可适度提高对突破信号的响应灵敏度，但仍需严守单笔止损。

A股问财短线情绪 **偏多**，与全球指数判断对照使用。

战役仓小米 XRPS 处于 **9 连阴月**积累阶段，模拟收益率 +8.97%；策略要求在此阶段坚持股数目标，不宜因净值回撤动摇持仓框架。

战术端暂无 buy 突破信号，建议以观察为主。

---

## 一、宏观与市场情绪

### 1.1 全球指数

跟踪 6 只主要指数：上涨 **2** 只、
下跌 **4** 只，平均涨跌 **+0.70%**。

**美股** -0.28%（震荡）；**港股** -0.04%（震荡）；**A股** +1.79%（偏强）。相对强势区域：A股。

**波动居前指数：**

- **日经 225** 66,232.19，日涨跌 +3.26%（周 -1.50% / 月 -7.04%）
- **上证指数** 3,864.37，日涨跌 +1.79%（周 -2.59% / 月 -7.18%）
- **道琼斯** 51,839.26，日涨跌 -0.59%（周 -1.26% / 月 +0.67%）
- **标普 500** 7,443.28，日涨跌 -0.19%（周 -0.96% / 月 +0.31%）

### 1.2 A股短线情绪

问财统计涨停 **100** 家、跌停 **27** 家，情绪定性 **偏多**，涨跌停比约 **3.7 : 1**。赚钱效应尚可，题材轮动活跃，但需警惕高位分歧。

### 1.3 宏观与跨资产

- **VIX** 17.4（normal）
- **美10Y收益率** 4.60%
- **10Y-2Y 利差（FRED）** 0.39%（偏窄）
- **美股行业**：能源 领涨，健康 靠后

**FRED 官方序列**
- 美10年期国债收益率：4.55（变动 -0.44%，2026-07-17）
- 10Y-2Y 利差：0.39（变动 +5.41%，2026-07-20）
- 联邦基金利率：3.63（变动 0.00%，2026-06-01）
- 美国失业率：4.2（变动 -2.33%，2026-06-01）
- 美元/人民币(官方)：6.776（变动 +0.05%，2026-07-17）
- 美国CPI指数：332.6（变动 +1.83%，2026-06-01）

**Finnhub 宏观要闻**
- [European banks set for profit boost from lending, trading windfall - Reuters](https://news.google.com/rss/articles/CBMirgFBVV95cUxQSzU2UlBIRHMtclU1eVE2a0ZsSDIwTUo4dU5rUjFqQTRrQ0xPTHczZDQ1bk5LdUozenloYTVSVWpRUmFGX3JoWWtVc3NuZUhaR1Y3SC1BLTNPZzlTU3cwUFF1bk9USTVOcktrZjlLRXljRkx1V1MtZXpKVlVYcUlDS2dPZGNOT3o2VnluSEZkd1JHelA1MmR4OXdfakxhZjk0Ymw4aDg1c1NXNjRMWkE?oc=5)（Reuters）
- [Gold rises 1% as hopes for US-Iran diplomacy pause oil rally - Reuters](https://news.google.com/rss/articles/CBMinwFBVV95cUxNazZ5bjNfa1hrcmFFNGQzQUhudG0yVEM3ZC1qMkpGbDlpX2dTOUlScEs3bFozWVFpT01SZ0ZXcTEzazhXOGNaWVlDMk1IaWtDUlFvbE5FdTN5bzZTV3J2ajdma1kwNy10MGxGLWJhQ1JOUkZtRWNWZ1RSbkw1TjhFRThLa21BVFgyM0dGUGdURl9aVzVUMXlqdm5GSVNWYzQ?oc=5)（Reuters）
- [Tanker crew abandons vessel after reported projectile strike in Strait of Hormuz, UKMTO says - Reuters](https://news.google.com/rss/articles/CBMizwFBVV95cUxQZFNJNnRSVFd3TWVJMmtSMU9tcjNzLTZybXpmMkFxTm5Wb0VkMHVabm5qWVlyWWNabW85OXZsRVJ5YXhpa2xFOC1ZUlBrSTNwTE9tM2JTU2thdkJGOE9FY1gxb3A2dmhzQ241dE1VVjU3LWtpWnNweFJmNHB5d0pORlFtSWZrd1JsUFpDWXBPZl9YSzdVdUhzSzUyNFpSRXNOYkhvV0NaZko2NC1rUVM0X2xJOGN3MHB5bDdvQTFJcG0wR3dIWjZJSG5JN2xfMDQ?oc=5)（Reuters）
- [US military completes its latest strikes on Iran, marking the 10th successive night of attacks - Reuters](https://news.google.com/rss/articles/CBMiyAFBVV95cUxPWjlJZGJYNm5OYjczNWZJZkMxZGFGRFRJSHVGZjFaMS1KTkNfUTgzV2Y3Qk5VU0RDR0ZXOXBBUldobElBb0hRV2Y5MmlkR0pVNkNlN3RESGlzUlY2bnFBUFNJN3JaVmpyR3RzVkt0QTRVcklEQm05cmNIaUIyQkVJeWtzbi1sSk9XeFZpaURvUU1rM2hJLTMxcGJZa0RzdDFUcV8zdkNuQndVay0yYUc1Q3piMThnS2M2Wm1GMGNVREcxejFLNWxEcw?oc=5)（Reuters）
- [Hormuz vessel crossings extend slide on fresh US-Iran attacks - Reuters](https://news.google.com/rss/articles/CBMisgFBVV95cUxPVEtLXy1sb3RPLTgzWnBsRWhIU2JKV0tEQ3cyMmoxakRWRlpZNk9xUnVsWWxfMklsYzZrelRyd29WTVd5M041dUsyTElCWDd2cmtQWkdVbHhLRk5BcjZEWWRXcWx5bG85LVlBaE90bEVBZldzSERpX0QwdEs3eGlJNFVrTkxWVXZiSWRKNVdxTi1weVJnMUdRUG1tSkk1Y0NYVjVLVnVpd2QtVmRweGlBdmRR?oc=5)（Reuters）

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

**模拟净值**：收益率 +8.97%，仓位 64.1%，持股 25,467 股，均价 22.74。

**月线状态**：连续 **9** 个月收跌，上月 -24.65%，近两月累计 -30.15%，近三月累计 -32.42%。我们判断当前仍处于 XRPS「股数积累」逻辑占优的阶段，浮亏不应成为削减核心仓的理由。

**阶段判断**：滚动做 T 期——上涨分批卖、回撤分批买，利润来自波动而非单边预测。

**现价参考**：27.42 HKD。

- 下一档**滚动卖出**（涨 25%）：触发价 **29.35**，距现价 +7.00%。

- 已 9 连阴月（上月 -24.65%），核心仓按规则加仓，勿因短期浮亏动摇长期股数目标。

**长期参照**：上市以来 XRPS 回测收益率 +54.63%，短期净值波动属于策略设计内的正常路径，勿与战术实验混淆。

---

## 三、战术实验（荐股 v1.3）

**全市场扫描**：A股最高 中芯国际(67.0分) · 港股最高 美团(63.0分) · 美股最高 苹果(80.9分)

**今日各市场代表标的**（v1.3 强趋势+突破过滤）：

- **苹果**（美股）| 趋势达标待突破 | 评分 80.9 | 待突破 | 趋势过滤通过 | 止损缓冲 6.4% / 目标空间 23.1% | 决策 60.6

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **中芯国际**（A股）| 弱信号观察 | 评分 67.0 | 待突破 | 趋势过滤未过 | 止损缓冲 21.7% / 目标空间 78.2% | 决策 58.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线；均线多头排列

- **美团**（港股）| 弱信号观察 | 评分 63.0 | 待突破 | 趋势过滤未过 | 止损缓冲 12.8% / 目标空间 46.1% | 决策 57.0

  - 逻辑：价格站上 20 日均线；价格站上 60 日均线

> **研究员提示**：虽有高分标的入选观察池，但 v1.3 仅对「突破确认」发出 buy 信号；趋势良好但未突破时维持 watch，避免追涨噪音。


暂无 open 战术信号持仓。


**候选池前列**（按评分）：

- 苹果 80.9分 趋势达标待突破 RSI 63.9 RS +11.26%

- Meta 70.0分 建议观察 RSI 56.8 RS +14.70%


> 战术回测（v1.3.0）当前区间 **0 笔成交**，反映强趋势+突破过滤下信号稀缺，与「少做噪音交易」的设计一致。

---

## 四、投资大师风格荐股

基于候选池基本面与价格特征，模拟 **7** 位投资大师选股框架（v1.2.196）。

*在线学习：市场环境 risk_off · 修订 r196 · 市场环境(risk_off)：graham×1.06、templeton×1.08、buffett×1.04、soros×0.94*


### 沃伦·巴菲特 · 价值投资

*以合理价格买入具有宽阔护城河、稳定盈利能力的优质企业，长期持有。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - ROE 20.52% — 资本回报优秀，符合巴菲特护城河标准；PE 17.01 — 估值在能力圈合理区间

- **小米集团**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 15.2 · ROE 14.0%

  - ROE 14.0% — 盈利能力稳健；PE 15.23 — 估值在能力圈合理区间


### 本杰明·格雷厄姆 · 深度价值

*安全边际是投资核心：在价格显著低于内在价值时分批买入，分散持有。*

- **招商银行**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 6.7 · PEG 9.50 · ROE 11.9%

  - PE 6.65 — 深度价值区间，安全边际充足；PB 0.85 — 资产折价，经典格雷厄姆信号

- **中国平安**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 7.3 · ROE 11.3%

  - PE 7.3 — 深度价值区间，安全边际充足；PB 0.94 — 资产折价，经典格雷厄姆信号


### 彼得·林奇 · 成长合理价 GARP

*投资你了解的公司；以 PEG 衡量成长是否被合理定价，偏好业绩可验证的成长股。*

- **五粮液**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 22.9 · PEG 0.28 · ROE 9.2%

  - PEG 0.28 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 82.6% — 成长故事可验证

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - PEG 0.74 — 成长相对估值便宜，林奇「十倍股」潜力；盈利增速 22.9% — 成长故事可验证


### 查理·芒格 · 优质复利

*以合理价格买入伟大的公司，胜过于以便宜价格买入平庸的公司。*

- **腾讯控股**（港股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - 净利率 30.61% — 轻资产高毛利特征；低杠杆 — 符合芒格「避免愚蠢」原则

- **中际旭创**（A股）| 匹配 100.0 | 符合风格 · 建议关注 | PE 84.5 · PEG 32.63 · ROE 53.9%

  - ROE 53.93% — 优质复利机器，芒格会长期持有；净利率 29.28% — 轻资产高毛利特征


### 约翰·邓普顿 · 逆向投资

*在最大悲观时买入，在最大乐观时卖出；关注被错杀的优质资产。*

- **五粮液**（A股）| 匹配 91.6 | 符合风格 · 建议关注 | PE 22.9 · PEG 0.28 · ROE 9.2%

  - 近三月 -25.66% — 深度回调，关注基本面是否错杀；价格接近 52 周底部 — 「极度悲观时买入」

- **腾讯控股**（港股）| 匹配 85.4 | 符合风格 · 建议关注 | PE 17.0 · PEG 0.74 · ROE 20.5%

  - 价格接近 52 周底部 — 「极度悲观时买入」；PE 17.01 — 悲观中仍有估值支撑


### 乔治·索罗斯 · 宏观趋势

*反身性理论：趋势与认知相互强化；在宏观拐点与趋势确认时果断行动。*

- **苹果**（美股）| 匹配 69.2 | 部分符合 · 观察等待 | PE 40.5 · PEG 1.86 · ROE 141.5%

  - 近一月 +10.35% — 趋势强劲，反身性正反馈；相对强度 +10.04% — 跑赢大盘，宏观共振

- **Meta**（美股）| 匹配 69.2 | 部分符合 · 观察等待 | PE 23.5 · PEG 0.38 · ROE 32.9%

  - 近一月 +13.79% — 趋势强劲，反身性正反馈；相对强度 +13.48% — 跑赢大盘，宏观共振


### 白毛股神 Serenity · 卡脖子 · 瓶颈猎手

*Own the bottleneck, not the brand — 不买 AI/机器人终端龙头，寻找供应链中绕不过、短期内无法替代的上游稀缺环节（紫苏叶理论）。*

- **绿的谐波**（A股）| 匹配 76.8 | 符合风格 · 建议关注 | PE 435.6 · PEG 7.67 · ROE 3.9%

  - 精密减速器 — AI/机器人供应链瓶颈相关环节；紫苏叶环节 · 精密减速器 — 人形机器人卡脖子环节

- **AMD**（美股）| 匹配 69.7 | 部分符合 · 观察等待 | PE 164.0 · PEG 1.80 · ROE 8.1%

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

- [问财] **华邦健康：关于全资子公司收到《税务处理决定书》的公告**（华邦健康 (002004.SZ)）
  公告…
- [问财] **久立特材：第七届董事会第二十一次会议决议公告**（久立特材 (002318.SZ)）
  公告…
- [问财] **久立特材：关于回购公司股份方案的公告**（久立特材 (002318.SZ)）
  公告…
- [问财] **天和磁材：关于使用部分闲置募集资金进行现金管理到期赎回的公告**（天和磁材 (603072.SH)）
  公告…
- [问财] **申万宏源：关于申万宏源证券有限公司2026年面向专业投资者公开发行次级债券（第一期）发行结果的公告**（申万宏源 (000166.SZ)）
  公告…
- [问财] **日照港：日照港股份有限公司关于董事会完成换届选举暨聘任公司高级管理人员、证券事务代表的公告**（日照港 (600017.SH)）
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

*报告 ID：`2026-07-21-afternoon` · 自动生成于 shixiaoquan.win 投资决策工作台*
