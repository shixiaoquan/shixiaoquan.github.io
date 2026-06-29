# Truth Social 抓取配置

本模块镜像 [Truth Social @realDonaldTrump](https://truthsocial.com/@realDonaldTrump) 的公开帖子，抓取后自动翻译为中文，并写入 `data/trump_truth.json`。

## GitHub Actions 配置

Truth Social 有 Cloudflare 防护，需使用 **truthbrush** 登录凭证。

### 方式 A：Access Token（推荐）

1. 浏览器登录 Truth Social
2. F12 → Application / Network → 找到 API 请求中的 `Authorization: Bearer <token>`
3. 仓库 **Settings → Secrets → Actions** 新建：
   - Name: `TRUTHSOCIAL_TOKEN`
   - Value: token 字符串（不含 `Bearer ` 前缀）

### 方式 B：账号密码

```
TRUTHSOCIAL_USERNAME=你的用户名
TRUTHSOCIAL_PASSWORD=你的密码
```

## 工作流

`.github/workflows/update-truth-social.yml` — 每 **10 分钟** 运行一次。

```yaml
env:
  TRUTHSOCIAL_TOKEN: ${{ secrets.TRUTHSOCIAL_TOKEN }}
  TRUTHSOCIAL_USERNAME: ${{ secrets.TRUTHSOCIAL_USERNAME }}
  TRUTHSOCIAL_PASSWORD: ${{ secrets.TRUTHSOCIAL_PASSWORD }}
```

## 本地开发

```bash
export TRUTHSOCIAL_TOKEN='你的token'
pip install -r scripts/requirements.txt
python scripts/fetch_truth.py
```

## 验证

`data/trump_truth.json` 中：

- `"credentialUsed": true`
- `"status": "ok"`
- `posts` 数组含 `content`（原文）与 `contentZh`（中文）

## 前端

站点 **Truth** Tab：默认显示中文正文，点击「显示原文」可切换英文原文。

## 注意事项

- 非官方镜像，仅供个人阅读研究
- Token 会过期，失效后请重新获取
- 翻译使用 Google Translate（deep-translator），抓取时完成，前端无需联网翻译
