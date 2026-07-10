"""问财预置问句 — 修改此处即可扩展数据源。"""

WENCAI_SCREENS = [
    {
        "id": "limit_up",
        "title": "今日涨停",
        "query": "今日涨停",
        "query_type": "stock",
        "perpage": 100,
        "display": 12,
    },
    {
        "id": "limit_down",
        "title": "今日跌停",
        "query": "今日跌停",
        "query_type": "stock",
        "perpage": 100,
        "display": 12,
    },
    {
        "id": "hot",
        "title": "人气排行",
        "query": "人气排行",
        "query_type": "stock",
        "perpage": 10,
    },
    {
        "id": "main_flow",
        "title": "主力资金净流入",
        "query": "主力资金净流入",
        "query_type": "stock",
        "perpage": 8,
    },
]

# 按驾驶舱市场情绪轮换的附加问句（无需 LLM，读 market.json 即可）
WENCAI_MOOD_SCREENS = {
    "偏多": {
        "id": "breakout",
        "title": "突破年线",
        "query": "突破年线且成交量放大",
        "query_type": "stock",
        "perpage": 8,
    },
    "偏空": {
        "id": "low_pe",
        "title": "低估值防御",
        "query": "市盈率低于行业均值且股息率大于3%",
        "query_type": "stock",
        "perpage": 8,
    },
    "震荡": {
        "id": "range",
        "title": "箱体震荡",
        "query": "60日内振幅小于15%且今日放量",
        "query_type": "stock",
        "perpage": 8,
    },
}

# 问财资讯问句（关键词资讯字段含公告/利好链接）
WENCAI_NEWS_QUERIES = [
    {
        "id": "announce",
        "title": "今日公告",
        "query": "今日公告",
        "query_type": "stock",
        "category": "公告",
        "perpage": 15,
    },
    {
        "id": "positive",
        "title": "今日利好",
        "query": "今日利好",
        "query_type": "stock",
        "category": "利好",
        "perpage": 10,
    },
]
