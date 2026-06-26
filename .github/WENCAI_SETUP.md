# 问财 Cookie 配置指南

问财（同花顺 iWencai）为非官方接口，部分问句（尤其是「今日涨停」）在无 Cookie 时可能失败。本项目已实现**失败降级**（复用上次缓存数据），但配置 Cookie 可显著提升稳定性。

## GitHub Actions 配置（推荐）

1. 浏览器打开 [https://www.iwencai.com](https://www.iwencai.com) 并登录
2. F12 → Network → 任选请求 → 复制请求头中的 `Cookie` 完整值
3. 打开仓库 **Settings → Secrets and variables → Actions**
4. 点击 **New repository secret**
5. Name: `WENCAI_COOKIE`
6. Value: 粘贴 Cookie 字符串
7. 保存后，下次 `update-wencai-data` 工作流运行时会自动使用

工作流文件：`.github/workflows/update-wencai-data.yml`

```yaml
env:
  WENCAI_COOKIE: ${{ secrets.WENCAI_COOKIE }}
```

## 本地开发

```bash
export WENCAI_COOKIE='你的cookie'
python scripts/fetch_wencai.py
```

## 验证

成功时 `data/wencai.json` 中：

- `"cookieUsed": true`
- `"status": "ok"`
- 各 screen 的 `"status"` 为 `"ok"` 而非 `"error"` / `"stale"`

## 注意事项

- Cookie 会过期，若涨停榜再次失败请重新获取并更新 Secret
- 问财工作流为**每小时**运行一次，请勿提高频率
- 未配置 Cookie 时站点仍可正常访问，只是部分 A 股情绪数据可能显示缓存或 `--`
