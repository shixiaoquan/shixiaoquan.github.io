# 站点持续进化 · GitHub Actions 自动化

本仓库是**纯静态站 + 数据构建流水线**：前端 HTML/JS/CSS 与 `data/*.json` 一同部署到 GitHub Pages。所有行情、荐股、研报、策略学习均由 Actions 定时写入数据文件，站点无需后端即可持续更新。

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions（定时 / 手动 / 代码推送触发）                  │
├─────────────────────────────────────────────────────────────┤
│  update-market-data      交易日高频   行情·宏观·荐股·影子轨    │
│  update-truth-social     每 10 分钟  Truth 镜像 + 中文翻译   │
│  update-wencai-data      每小时      问财自然语言筛选         │
│  generate-investment-report  每日 3 次  投资决策研报           │
│  weekly-backtest         每周日      回测·归因·参数搜索     │
│  evolution-followup      事件驱动    影子轨·配对归因·队列     │
│  continuous-evolution    每小时      进化看板·健康·队列 Issue │
│  scripts-test            PR/推送     脚本单元测试             │
└──────────────────────────────┬──────────────────────────────┘
                               │ git commit → master
                               ▼
                    GitHub Pages（shixiaoquan.win）
                               │
                               ▼
              前端 SWR 缓存 + PollScheduler 局部刷新
```

## 工作流一览

| 工作流 | 频率 | 产出 | 说明 |
|--------|------|------|------|
| `update-market-data.yml` | 5min（交易日历降频） | `market_core.json` / `market_reco.json` 等 | 含决策分、影子轨、进化队列 |
| `update-truth-social.yml` | 10min | `trump_truth.json` | Telegram RSS 降级 |
| `update-wencai-data.yml` | 每小时 | `wencai.json` | 需 `WENCAI_COOKIE` |
| `generate-investment-report.yml` | UTC 1/4/8 | `data/reports/*.md` | 含进化状态章节 |
| `weekly-backtest.yml` | 周日 | `backtest.json`、归因、影子轨 | 含配对归因 |
| `evolution-followup.yml` | 事件驱动 | `shadow_reco.json`、队列 | 行情/回测成功后 |
| `continuous-evolution.yml` | 每小时 | `site_status.json`、Issue | 流水线 + 进化队列告警 |
| `scripts-test.yml` | PR | 单元测试 | attribution / decision / validate |
| `pipeline-failure-alert.yml` | 失败时 | GitHub Issue | 零成本告警 |

## 策略「进化」机制

1. **战术荐股**：`strategy_config.py` v1.3 + `tactic_tune.json` 归因反哺门槛
2. **决策质量分**：`decision_score.py` 四维加权，写入 history 快照（含 `decisionComponents`）
3. **影子轨**：`shadow_reco.py` 并行 forward 验证，满 4 周 + 配对归因优于生产才可升 PR
4. **配对归因**：`paired_attribution.py` 同日复盘同标的 T+5 对比
5. **荐股归因**：`reco_attribution.py` 按信号/市场/决策分/Regime 分桶
6. **参数搜索**：`strategy_param_sweep.py` → `strategy_candidates.json` → 影子轨
7. **进化队列**：`evolution_queue.json` 单入口待办，高优任务自动开 Issue（`evolution-queue` 标签）
8. **Schema Gate**：`validate_data.py` ERROR 时 CI 失败
9. **大师学习**：`master_strategy_learn.py` 按 regime 微调权重
10. **Dependabot + Cursor PR**：依赖与策略升级可审计

## 前端刷新

- `js/data-cache.js`：sessionStorage stale-while-revalidate
- `js/poll-scheduler.js`：标签页隐藏降频
- `js/app.js`：行情、历史、站点状态均走 DataCache

## 本地验证

```bash
pip install -r scripts/requirements.txt
python scripts/fetch_data.py
python scripts/reco_attribution.py
python scripts/paired_attribution.py
python scripts/build_evolution_queue.py
python scripts/build_site_status.py
python scripts/validate_data.py
python -m unittest discover -s tests -p "test_*.py" -v
```

## Cursor 协作

详见 `.github/EVOLUTION_PLAYBOOK.md`：机器产出候选 → 影子轨验证 → Cursor 审阅开 PR → 合并发布。
