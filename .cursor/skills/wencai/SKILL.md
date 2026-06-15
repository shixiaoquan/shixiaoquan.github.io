---
name: wencai
description: 同花顺问财数据查询 — 用自然语言拉取 A 股筛选、涨停跌停、人气榜、资金流向等，写入 data/wencai.json。在需要问财数据、A 股情绪、热股、修改问句或排查问财拉取失败时使用。
---

# 同花顺问财（pywencai）

## 架构定位

本项目为 **GitHub Pages 静态站**。问财数据通过 `scripts/fetch_wencai.py` 在 GitHub Actions 中离线拉取，结果写入 `data/wencai.json`，前端只读 JSON。

## 依赖

- Python：`pip install pywencai pandas`（见 `scripts/requirements.txt`）
- Node.js **v16+**（pywencai 内部执行 JS，CI 已配置 `setup-node`）

## Cookie（可选）

问财策略调整后，部分环境需登录 Cookie：

1. 浏览器打开 https://www.iwencai.com 并登录
2. F12 → Network → 任选请求 → 复制 `Cookie` 请求头
3. 本地：`export WENCAI_COOKIE='你的cookie'`
4. GitHub：仓库 Settings → Secrets → `WENCAI_COOKIE`

未配置时脚本仍会尝试无 Cookie 拉取；失败则写入 `status: "error"` 并保留上次有效数据。

## 修改问句

编辑 `scripts/wencai_queries.py` 中的 `WENCAI_SCREENS`：

```python
{
    "id": "hot",
    "title": "人气排行",
    "query": "人气排行",
    "query_type": "stock",
    "perpage": 10,
}
```

问句写法与同花顺问财网站搜索框一致，使用中文自然语言。

## 本地运行

```bash
pip install -r scripts/requirements.txt
# 可选
export WENCAI_COOKIE='...'
python scripts/fetch_wencai.py
```

## API 参考（pywencai）

```python
import pywencai

df = pywencai.get(
    query="今日涨停",
    query_type="stock",  # stock | zhishu | hkstock | usstock | fund ...
    perpage=10,          # 最大 100
    loop=False,          # True 可分页合并，慎用高频
    cookie=os.environ.get("WENCAI_COOKIE"),  # 可选
)
```

- 列表查询 → `pandas.DataFrame`
- 无结果 → `None`

## 注意事项

- **低频调用**：每 5 分钟已集成，勿再叠加高频问句
- 非官方接口，仅供学习研究，商用需自行评估风险
- 列名带日期后缀（如 `最新涨跌幅`），解析用 `scripts/fetch_wencai.py` 的 `normalize_row`

## 问财资讯

在 `wencai_queries.py` 的 `WENCAI_NEWS_QUERIES` 中配置。问句需返回含 `关键词资讯` 字段的结果（如「今日公告」「今日利好」），脚本会解析其中的公告链接与标题。

前端资讯 Tab 支持与 Yahoo 新闻合并展示，可按来源筛选。

| 文件 | 作用 |
|------|------|
| `scripts/wencai_queries.py` | 问句配置 |
| `scripts/fetch_wencai.py` | 拉取与写入 JSON |
| `data/wencai.json` | 前端数据源 |
| `js/app.js` | `renderWencai` 渲染 |
