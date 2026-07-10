# 零增量成本进化手册 · GitHub + Cursor

本仓库的「进化」不依赖新服务器、新 API 或付费服务，只靠：

1. **GitHub Actions** — 定时写 `data/*.json` 并推 `master`
2. **GitHub Issues** — 流水线失败 / 数据过期告警
3. **GitHub PR + Dependabot** — 策略升级与依赖维护可审计
4. **Cursor Agent** — 审阅机器产出，改代码、开 PR、合并

## 机器负责什么

| 产物 | 脚本 | 频率 |
|------|------|------|
| 行情、荐股、大师权重 | `fetch_data.py` | 5 分钟 |
| 荐股 T+5 归因 | `reco_attribution.py` | 每周 |
| 战术参数候选 | `strategy_param_sweep.py` | 每周 |
| **影子荐股轨** | `shadow_reco.py` | 行情更新后 / 周回测后 |
| **影子轨 T+5 归因** | `shadow_attribution.py` | 周回测后 / followup |
| **决策质量分** | `decision_score.py` | 随 `fetch_data.py` |
| **进化指令队列** | `build_evolution_queue.py` | 每次数据更新后 |
| **数据契约校验** | `validate_data.py` | CI 提交前 |
| **交易日历** | `market_calendar.py` | 每次行情流水线 |
| 进化事件日志 | `evolution_log.py` | 每次触发时追加 |
| 流水线健康 | `pipeline_health.py` | 每小时 |
| 看板汇总 | `build_site_status.py` | 每次数据更新后 |

## 六项进阶机制

### 1. 影子荐股轨（Shadow Track）

探索参数优于当前时，**不再**直接 `recommendUpgrade=true` 升生产。候选写入 `data/shadow_reco.json`，与 `reco_history` 并行记账满 4 周后，由 `shadow_attribution.json` 与生产 `reco_attribution.json` 双轨 T+5 对比，`comparison.readyForUpgradePR` 为真才可开 PR。

### 2. 决策质量分（Decision Score）+ 分桶反哺

`decision_score.py` 对每只荐股计算宏观 / 问财 / 大师共识 / Truth 舆情四维加权分。`reco_attribution.py` 按高/中/低分桶汇总 T+5 胜率，`tactic_tune.py` 据此微调 `buyScoreAdjust`（高决策分表现好则降门槛，低决策分拖累则升门槛）。

### 3. 事件驱动 Actions + 交易日历

- `market_calendar.py` 输出 `high` / `low` / `closed`；休市时 `update-market-data.yml` 跳过重型 fetch，仅跑轻量 refresh。
- `evolution-followup.yml` 在行情/周回测工作流成功后跑影子轨对比与队列刷新。

### 4. Schema Gate

`validate_data.py` 校验 market、reports、shadow、evolution_queue 等契约；**ERROR 时 CI 失败**，WARN 仅提示。

### 5. 进化指令总线

`data/evolution_queue.json` 汇总影子轨、流水线过期、tactic_tune、paper_ab 等待办，驾驶舱 `#cockpit-evolution-queue` 与 Cursor 单入口消费。

### 6. 前端 SWR 缓存

`js/data-cache.js` 用 sessionStorage 做 stale-while-revalidate，首屏先渲染缓存再后台刷新。

## Cursor 负责什么

当 `data/evolution_queue.json` 出现 **`shadow-upgrade-pr`**（或 `shadow_reco.comparison.readyForUpgradePR`）时：

1. 读取 `candidateParams` 与 `comparison`
2. 创建分支 `cursor/strategy-vX-Y-93a1`
3. 更新 `scripts/strategy_config.py` 中 `BUY_SCORE`、`BREAKOUT_SCORE_MIN`
4. 在 `data/strategy_versions.json` 追加新版本记录
5. 开 PR，正文附影子轨 vs 生产对比
6. 验证通过后合并

当 `strategy_candidates.json` 中 **`shadowCandidate": true`** 时：

- **勿**直接改 `strategy_config.py`，继续观察 `shadow_reco.json`

当 GitHub Issue 带标签 `pipeline-health` 时：

1. 打开对应 workflow 日志
2. 修复 Cookie/脚本/依赖问题
3. 推送修复 PR，Issue 将在下次健康检查通过后自动关闭

## 问财自适应（无 LLM）

`fetch_wencai.py` 读取已有 `market.json` 的 `summary.mood`，轮换附加问句（见 `wencai_queries.WENCAI_MOOD_SCREENS`）。

## 推荐 Cursor 提示词

```
阅读 data/evolution_queue.json 与 data/shadow_reco.json。
若存在 shadow-upgrade-pr 任务，按 .github/EVOLUTION_PLAYBOOK.md 升级战术策略并开 PR。
若仅有 shadowCandidate，继续观察，勿直接改 strategy_config。
```

## 不做什么（控制成本）

- 不接入新付费 API
- 不用外部 Cron / 云函数
- 不部署后端服务
- 策略参数**不**由 Actions 直接改 `strategy_config.py`（必须经 PR，可回滚）
