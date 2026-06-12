# shixiaoquan.github.io

个人博客与站点源码，基于 Jekyll + Minima，通过 GitHub Pages 发布。

- 线上地址：<https://shixiaoquan.win>
- 自定义域名配置见 `CNAME`

## 本地开发

需要 Ruby 3.x 与 Bundler：

```bash
bundle install
bundle exec jekyll serve
```

浏览器访问 <http://127.0.0.1:4000>。

## 目录说明

| 路径 | 说明 |
|------|------|
| `_posts/` | 博客文章 |
| `_config.yml` | 站点配置 |
| `assets/` | 静态资源（图片、视频、样式） |
| `resume.html` | 在线简历 |
| `yuan.markdown` | 成长记录页面 |

## 发布

推送到 `master` 分支后，GitHub Actions / Pages 会自动构建站点。
