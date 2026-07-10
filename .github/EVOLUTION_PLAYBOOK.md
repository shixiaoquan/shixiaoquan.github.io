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
| 进化事件日志 | `evolution_log.py` | 每次触发时追加 |
| 流水线健康 | `pipeline_health.py` | 每小时 |
| 看板汇总 | `build_site_status.py` | 每次数据更新后 |

## Cursor 负责什么

当 `data/strategy_candidates.json` 中 **`recommendUpgrade": true`** 时：

1. 读取 `upgradeReason` 与 `bestCandidate`
2. 创建分支 `cursor/strategy-vX-Y-93a1`
3. 更新 `scripts/strategy_config.py` 中 `BUY_SCORE`、`BREAKOUT_SCORE_MIN`
4. 在 `data/strategy_versions.json` 追加新版本记录
5. 开 PR，正文附回测对比表
6. 验证通过后合并（用户偏好可自动合并）

当 GitHub Issue 带标签 `pipeline-health` 时：

1. 打开对应 workflow 日志
2. 修复 Cookie/脚本/依赖问题
3. 推送修复 PR，Issue 将在下次健康检查通过后自动关闭

## 问财自适应（无 LLM）

`fetch_wencai.py` 读取已有 `market.json` 的 `summary.mood`，轮换附加问句（见 `wencai_queries.WENCAI_MOOD_SCREENS`）。

## 推荐 Cursor 提示词

```
阅读 data/strategy_candidates.json，若 recommendUpgrade 为 true，
请按 .github/EVOLUTION_PLAYBOOK.md 升级战术策略并开 PR。
```

## 不做什么（控制成本）

- 不接入新付费 API
- 不用外部 Cron / 云函数
- 不部署后端服务
- 策略参数**不**由 Actions 直接改 `strategy_config.py`（必须经 PR，可回滚）
