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
