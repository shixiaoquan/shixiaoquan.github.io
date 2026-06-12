# 投资分析大盘

GitHub Pages 静态投资看板，展示全球主要指数、重点个股与财经资讯。

## 功能

- 全球主要指数每日走势（标普 500、道琼斯、纳斯达克、恒生、日经、上证）
- 重点个股分析：小米集团、泡泡玛特、SK 海力士
- 重要财经资讯聚合
- GitHub Actions 每日自动更新数据

## 本地开发

```bash
pip install -r scripts/requirements.txt
python scripts/fetch_data.py
python3 -m http.server 8080
```

浏览器访问 `http://localhost:8080`。

## 原站点

原 Jekyll 个人博客已备份至 `backup/jekyll-personal-site/`。
