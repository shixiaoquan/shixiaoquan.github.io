# 站点持续进化 · GitHub Actions 自动化

本仓库是**纯静态站 + 数据构建流水线**：前端 HTML/JS/CSS 与 `data/*.json` 一同部署到 GitHub Pages。所有行情、荐股、研报、策略学习均由 Actions 定时写入数据文件，站点无需后端即可持续更新。

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions（定时 / 手动 / 代码推送触发）                  │
├─────────────────────────────────────────────────────────────┤
│  update-market-data      每 5 分钟   行情·宏观·荐股·模拟盘    │
│  update-truth-social     每 10 分钟  Truth 镜像 + 中文翻译   │
│  update-wencai-data      每小时      问财自然语言筛选         │
│  generate-investment-report  每日 3 次  投资决策研报           │
│  weekly-backtest         每周日      策略与模拟盘回测         │
│  continuous-evolution    每小时      进化看板 site_status     │
└──────────────────────────────┬──────────────────────────────┘
                               │ git commit → master
                               ▼
                    GitHub Pages（shixiaoquan.win）
                               │
                               ▼
              前端每 5 分钟轮询 JSON，局部刷新无整页重载
```

## 工作流一览

| 工作流 | 频率 | 产出 | 说明 |
|--------|------|------|------|
| `update-market-data.yml` | `*/5 * * * *` | `data/market.json` 等 | 含 FRED/Finnhub 宏观、交易引擎、大师荐股在线学习 |
| `update-truth-social.yml` | `*/10 * * * *` | `data/trump_truth.json` | 默认 Telegram RSS，无需 Token |
| `update-wencai-data.yml` | `15 * * * *` | `data/wencai.json` | 需 `WENCAI_COOKIE` Secret |
| `generate-investment-report.yml` | UTC 1/4/8 点 | `data/reports/*.md` | 晨会 / 午间 / 收盘三份日报 |
| `weekly-backtest.yml` | 周日 02:00 UTC | `data/backtest.json` | 战术策略与小米 XRPS 回测 |
| `continuous-evolution.yml` | `30 * * * *` + push | `data/site_status.json` | 汇总新鲜度与策略进化指标 |
| `pipeline-failure-alert.yml` | 工作流失败时 | GitHub Issue | 零成本告警 |
| `weekly-backtest.yml`（扩展） | 周日 | `reco_attribution.json` / `strategy_candidates.json` | 荐股归因 + 参数搜索 |

## 策略「进化」机制

1. **战术荐股**：`strategy_config.py` 定义版本（当前 v1.3），`fetch_data.py` 每 5 分钟重算信号并写入 `reco_history.json` 存档。
2. **投资大师**：`master_strategy_learn.py` 根据历史荐股胜率微调 7 位大师权重，`revision` 随每次行情更新递增；变更写入 `evolution_log.json`。
3. **荐股归因**：`reco_attribution.py` 每周计算 T+1/5/20 收益（yfinance，无新 API）。
4. **参数搜索**：`strategy_param_sweep.py` 每周网格搜索，产出 `strategy_candidates.json`；若优于当前则 **Cursor 开 PR** 升级（见 `EVOLUTION_PLAYBOOK.md`）。
5. **问财自适应**：`fetch_wencai.py` 按 `market.json` 情绪轮换附加问句。
6. **周度回测**：`weekly-backtest.yml` 刷新 `backtest.json`，实验室 Tab 对比各策略版本。
7. **进化看板**：`build_site_status.py` 聚合上述指标 → `site_status.json`，驾驶舱展示流水线健康度。
8. **健康告警**：`pipeline_health.py` + GitHub Issues（`pipeline-health` 标签），失败工作流由 `pipeline-failure-alert.yml` 通知。
9. **Dependabot**：每周检查 pip / Actions 依赖，PR 由 Cursor 或人工合并。

## 前端刷新

- `js/app.js`：每 5 分钟拉取 `market.json`、`macro.json`、`wencai.json`、交易数据
- `js/truth.js`：每 5 分钟拉取 `trump_truth.json`
- 有变更才重绘 DOM，避免闪烁

## 本地验证

```bash
pip install -r scripts/requirements.txt
python scripts/fetch_data.py
python scripts/build_site_status.py
# 打开 index.html 或 python -m http.server
```

## 手动触发

仓库 **Actions** 页 → 选择对应工作流 → **Run workflow**。

## Secrets（均可选）

| Secret | 用途 |
|--------|------|
| `FRED_API_KEY` | 美国宏观序列 |
| `FINNHUB_API_KEY` | 宏观新闻与财报日历 |
| `WENCAI_COOKIE` | 问财筛选 |
| `TRUTHSOCIAL_TOKEN` | Truth 直连（无则走 RSS） |

未配置的模块会降级或跳过，不影响其余流水线。

## Cursor 协作

详见 `.github/EVOLUTION_PLAYBOOK.md`：机器产出候选 → Cursor 审阅开 PR → 合并发布，全程不增加外部资源。

## 近期优化（P0–P3）

- **P0**：修复 `generate_report.py` 空指针；参数搜索探索模式（2y+放宽过滤）；研报失败自动开 Issue
- **P1**：`market_core.json` / `market_reco.json` 拆分；`reco_history` 归档；pip cache 复用；研报默认不重复 fetch
- **P2**：`tactic_tune.json` 归因反哺门槛；`poll-scheduler.js` 标签页隐藏降频；进化面板链到 Actions
- **P3**：`paper_ab.json` 战术 A/B；Truth 帖子舆情标签
