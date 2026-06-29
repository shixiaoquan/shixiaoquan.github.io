# Truth Social 抓取配置

本模块镜像 [Truth Social @realDonaldTrump](https://truthsocial.com/@realDonaldTrump) 的公开帖子，抓取后自动翻译为中文，并写入 `data/trump_truth.json`。

## 无需配置即可使用（默认）

**不需要 Truth Social Token。** 工作流默认通过官方 Telegram 频道 RSS 镜像拉取内容（与 Truth Social 同步发布）：

```
https://rsshub.rssforever.com/telegram/channel/real_DonaldJTrump
```

站点 **Truth** Tab 会显示中文正文，点击「显示原文」可切换英文。

## 可选：Truth Social 直连（更高质量）

若你有 Truth Social 登录凭证，可配置 Secrets 优先使用 truthbrush 直连（含头像、互动数、媒体等完整字段）。

### 方式 A：Access Token

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

## 可选：自定义 RSS 地址

```
TRUTH_RSS_URL=https://你的-rss-镜像地址
```

## 工作流

`.github/workflows/update-truth-social.yml` — 每 **10 分钟** 运行一次。

```yaml
env:
  TRUTHSOCIAL_TOKEN: ${{ secrets.TRUTHSOCIAL_TOKEN }}      # 可选
  TRUTHSOCIAL_USERNAME: ${{ secrets.TRUTHSOCIAL_USERNAME }}  # 可选
  TRUTHSOCIAL_PASSWORD: ${{ secrets.TRUTHSOCIAL_PASSWORD }}  # 可选
  # TRUTH_RSS_URL: 自定义 RSS，不设置则用 Telegram 镜像
```

## 本地开发

```bash
pip install -r scripts/requirements.txt
python scripts/fetch_truth.py
```

有凭证时：

```bash
export TRUTHSOCIAL_TOKEN='你的token'
python scripts/fetch_truth.py
```

## 验证

`data/trump_truth.json` 中：

- `"status": "ok"`
- `posts` 数组含 `content`（原文）与 `contentZh`（中文）
- `source.dataSource` 为 `telegram_mirror`（默认）或 `truth_social`（有凭证时）

## 注意事项

- 非官方镜像，仅供个人阅读研究
- Telegram 镜像无需 Token，但不含 Truth Social 互动数据
- 若配置了 Token 且失效，会自动回退到 RSS 镜像
- 翻译使用 Google Translate（deep-translator），抓取时完成，前端无需联网翻译
