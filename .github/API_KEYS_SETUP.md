# FRED / Finnhub API Key 配置指南

宏观模块 `scripts/fetch_macro.py` 在免费源（Yahoo Finance、Frankfurter）之外，可选接入：

| Secret | 用途 | 注册地址 |
|--------|------|----------|
| `FRED_API_KEY` | 美国官方宏观序列（10Y-2Y 利差、失业率、CPI 等） | [FRED API Keys](https://fred.stlouisfed.org/docs/api/api_key.html) |
| `FINNHUB_API_KEY` | 全球/外汇新闻、财报日历 | [Finnhub 注册](https://finnhub.io/register) |

未配置时站点仍可正常运行，对应区块显示空状态或仅免费源数据。

## GitHub Actions 配置

1. 打开仓库 **Settings → Secrets and variables → Actions**
2. 新建 **Repository secret**：
   - Name: `FRED_API_KEY` — 粘贴 FRED 控制台生成的 Key
   - Name: `FINNHUB_API_KEY` — 粘贴 Finnhub Dashboard 中的 API Key
3. 保存后，以下工作流会自动注入环境变量：
   - `.github/workflows/update-market-data.yml`（每 5 分钟）
   - `.github/workflows/generate-investment-report.yml`（每日 9/12/16 点研报）

```yaml
env:
  FRED_API_KEY: ${{ secrets.FRED_API_KEY }}
  FINNHUB_API_KEY: ${{ secrets.FINNHUB_API_KEY }}
```

## 本地开发

```bash
export FRED_API_KEY='你的fred_key'
export FINNHUB_API_KEY='你的finnhub_key'
python scripts/fetch_macro.py
```

## 验证

成功时 `data/macro.json` 中：

- `sources` 里 `fred` / `finnhub` 的 `"cookieUsed": true`（表示 Key 已传入）
- `"fred"` 数组含 6 条官方序列（或 `status: partial`）
- `"finnhubNews"` 含宏观/外汇新闻
- `"earningsCalendar"` 含关注标的财报（AAPL、NVDA、1810.HK、0700.HK、688981.SS 等）
- `summary.yieldSpread10y2y` 有 10Y-2Y 利差数值

CI 在 `update-market-data` 工作流中会自动打印 `fred keyUsed` / `finnhub keyUsed` 日志。

## 注意事项

- FRED 免费层足够本项目使用；Finnhub 免费层有速率限制，本脚本已控制请求量
- Key 泄露请立即在对应平台轮换
- 问财 Cookie 配置见 [WENCAI_SETUP.md](./WENCAI_SETUP.md)
