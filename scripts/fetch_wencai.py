#!/usr/bin/env python3
"""同花顺问财 — 离线拉取 A 股洞察，写入 data/wencai.json。"""

from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from wencai_queries import WENCAI_NEWS_QUERIES, WENCAI_SCREENS

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "wencai.json"

CODE_KEYS = ("股票代码", "code")
NAME_KEYS = ("股票简称", "名称", "股票名称")
PRICE_KEYS = ("最新价", "现价")
CHANGE_KEYS = ("最新涨跌幅", "涨跌幅", "涨跌幅:前复权")
FLOW_KEYS = ("主力资金流向", "陆股通净买入额", "主力净流入")
RANK_KEYS = ("个股热度排名", "排名")
NEWS_FIELD_KEYS = ("关键词资讯", "资讯", "新闻")


def decode_news_payload(raw: Any) -> list[dict]:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    text = str(raw).strip()
    if not text or text.lower() == "nan":
        return []
    try:
        decoded = base64.b64decode(text)
        data = json.loads(decoded)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError, TypeError):
        return []


def pick_news_column(columns: list[str]) -> str | None:
    for col in columns:
        for key in NEWS_FIELD_KEYS:
            if key in col:
                return col
    return None


def article_to_news_item(
    article: dict,
    *,
    stock_code: str,
    stock_name: str,
    category: str,
) -> dict | None:
    title = (article.get("PageRawTitle") or article.get("title") or "").strip()
    if not title:
        return None
    link = (article.get("URL") or article.get("url") or "").strip()
    uid = article.get("UID") or article.get("uid") or title
    published = article.get("PublishTime") or article.get("publishTime")
    published_iso = None
    if published:
        try:
            published_iso = datetime.fromtimestamp(int(published), tz=timezone.utc).astimezone().isoformat(
                timespec="seconds"
            )
        except (TypeError, ValueError, OSError):
            published_iso = None

    related = stock_name or stock_code or "A股"
    if stock_code and stock_name:
        related = f"{stock_name} ({stock_code})"

    return {
        "id": f"wencai:{uid}",
        "title": title,
        "link": link,
        "publisher": "同花顺问财",
        "related": related,
        "publishedAt": published_iso,
        "summary": category,
        "source": "wencai",
        "category": category,
    }


def extract_news_from_df(df: pd.DataFrame, category: str, limit: int) -> list[dict]:
    columns = [str(c) for c in df.columns.tolist()]
    news_col = pick_news_column(columns)
    if not news_col:
        return []

    code_col = pick_column(columns, CODE_KEYS)
    name_col = pick_column(columns, NAME_KEYS)
    articles: list[dict] = []
    seen: set[str] = set()

    for _, row in df.head(limit).iterrows():
        stock_code = str(row.get(code_col, "")).strip() if code_col else ""
        stock_name = str(row.get(name_col, "")).strip() if name_col else ""
        for article in decode_news_payload(row.get(news_col)):
            item = article_to_news_item(
                article,
                stock_code=stock_code,
                stock_name=stock_name,
                category=category,
            )
            if not item or item["id"] in seen:
                continue
            seen.add(item["id"])
            articles.append(item)
    return articles


def fetch_wencai_news(cookie: str | None) -> list[dict]:
    import pywencai

    all_news: list[dict] = []
    seen: set[str] = set()

    for spec in WENCAI_NEWS_QUERIES:
        kwargs: dict[str, Any] = {
            "query": spec["query"],
            "query_type": spec.get("query_type", "stock"),
            "perpage": min(spec.get("perpage", 10), 100),
            "no_detail": True,
        }
        if cookie:
            kwargs["cookie"] = cookie
        try:
            result = pywencai.get(**kwargs)
        except Exception:
            continue
        if not isinstance(result, pd.DataFrame) or result.empty:
            continue
        for item in extract_news_from_df(result, spec.get("category", "资讯"), spec.get("perpage", 10)):
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            all_news.append(item)

    all_news.sort(key=lambda x: x.get("publishedAt") or "", reverse=True)
    return all_news[:40]


def load_existing() -> dict:
    if OUTPUT_FILE.exists():
        try:
            return json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def pick_column(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    for key in candidates:
        for col in columns:
            if col == key or col.startswith(key):
                return col
    return None


def to_float(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def normalize_row(row: dict, columns: list[str]) -> dict:
    code_col = pick_column(columns, CODE_KEYS)
    name_col = pick_column(columns, NAME_KEYS)
    price_col = pick_column(columns, PRICE_KEYS)
    change_col = pick_column(columns, CHANGE_KEYS)
    flow_col = pick_column(columns, FLOW_KEYS)
    rank_col = pick_column(columns, RANK_KEYS)

    item: dict[str, Any] = {
        "code": str(row.get(code_col, "")).strip() if code_col else "",
        "name": str(row.get(name_col, "")).strip() if name_col else "",
        "price": to_float(row.get(price_col)) if price_col else None,
        "changePct": to_float(row.get(change_col)) if change_col else None,
    }
    if flow_col:
        flow = row.get(flow_col)
        if flow is not None and not (isinstance(flow, float) and pd.isna(flow)):
            try:
                item["flow"] = int(float(flow))
            except (TypeError, ValueError):
                pass
    if rank_col:
        rank = row.get(rank_col)
        if rank is not None and not (isinstance(rank, float) and pd.isna(rank)):
            item["rank"] = str(rank)
    return item


def dataframe_to_items(df: pd.DataFrame, limit: int) -> list[dict]:
    columns = [str(c) for c in df.columns.tolist()]
    items = []
    for _, row in df.head(limit).iterrows():
        item = normalize_row(row.to_dict(), columns)
        if item.get("code") or item.get("name"):
            items.append(item)
    return items


def fetch_screen(screen: dict, cookie: str | None) -> dict:
    import pywencai

    fetch_perpage = min(screen.get("perpage", 10), 100)
    display = screen.get("display") or min(screen.get("perpage", 10), 100)

    kwargs: dict[str, Any] = {
        "query": screen["query"],
        "query_type": screen.get("query_type", "stock"),
        "perpage": fetch_perpage,
    }
    if cookie:
        kwargs["cookie"] = cookie

    result = pywencai.get(**kwargs)
    payload: dict[str, Any] = {
        "id": screen["id"],
        "title": screen["title"],
        "query": screen["query"],
        "status": "ok",
        "items": [],
    }

    if result is None:
        payload["status"] = "empty"
        return payload

    if isinstance(result, pd.DataFrame):
        if result.empty:
            payload["status"] = "empty"
            return payload
        if screen.get("display"):
            payload["count"] = len(result)
            if len(result) >= fetch_perpage:
                payload["countNote"] = f"{fetch_perpage}+"
        payload["items"] = dataframe_to_items(result, display)
        return payload

    if isinstance(result, dict):
        for value in result.values():
            if isinstance(value, pd.DataFrame) and not value.empty:
                payload["items"] = dataframe_to_items(value, display)
                return payload
    payload["status"] = "empty"
    return payload


def fetch_screen_resilient(screen: dict, cookie: str | None) -> dict:
    """拉取问句，涨停榜失败时尝试备用问句。"""
    try:
        return fetch_screen(screen, cookie)
    except Exception as primary_exc:
        if screen.get("id") != "limit_up":
            raise
        fallback = {
            **screen,
            "query": "非ST今日涨停",
            "title": screen.get("title", "今日涨停"),
        }
        try:
            payload = fetch_screen(fallback, cookie)
            payload["fallbackQuery"] = True
            payload["query"] = f"{screen['query']}（备用：非ST今日涨停）"
            return payload
        except Exception:
            raise primary_exc


def merge_screen_result(screen: dict, existing_screens: list[dict]) -> dict:
    """失败时复用上次成功数据，避免整块空白。"""
    has_data = screen.get("status") == "ok" and (
        screen.get("items") or screen.get("count") is not None
    )
    if has_data:
        return screen

    prev = next((s for s in existing_screens if s.get("id") == screen["id"]), None)
    if not prev or not (prev.get("items") or prev.get("count") is not None):
        return screen

    merged = dict(prev)
    merged["status"] = "stale"
    merged["stale"] = True
    merged["staleMessage"] = "沿用上次数据"
    if screen.get("error"):
        merged["error"] = screen["error"]
    return merged


def build_sentiment(screens: list[dict], existing: dict | None = None) -> dict:
    existing = existing or {}
    limit_up = next((s for s in screens if s["id"] == "limit_up"), {})
    limit_down = next((s for s in screens if s["id"] == "limit_down"), {})
    up_count = limit_up.get("count")
    down_count = limit_down.get("count")

    if up_count is None:
        up_count = existing.get("limitUp")
    if down_count is None:
        down_count = existing.get("limitDown")

    mood = existing.get("mood", "震荡")
    if up_count is not None and down_count is not None:
        if up_count > down_count * 3:
            mood = "偏多"
        elif down_count > up_count * 2:
            mood = "偏空"
        else:
            mood = "震荡"

    return {
        "limitUp": up_count,
        "limitDown": down_count,
        "limitUpNote": limit_up.get("countNote") or existing.get("limitUpNote"),
        "limitDownNote": limit_down.get("countNote") or existing.get("limitDownNote"),
        "mood": mood,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cookie = os.environ.get("WENCAI_COOKIE") or None
    now = datetime.now(timezone.utc).astimezone()
    existing = load_existing()

    screens: list[dict] = []
    errors: list[str] = []

    for screen in WENCAI_SCREENS:
        try:
            screens.append(fetch_screen_resilient(screen, cookie))
        except Exception as exc:
            errors.append(f"{screen['id']}: {exc}")
            screens.append(
                {
                    "id": screen["id"],
                    "title": screen["title"],
                    "query": screen["query"],
                    "status": "error",
                    "items": [],
                    "error": str(exc)[:200],
                }
            )

    screens = [merge_screen_result(s, existing.get("screens", [])) for s in screens]

    ok_count = sum(
        1
        for s in screens
        if s.get("status") in ("ok", "stale") and (s.get("items") or s.get("count") is not None)
    )
    news = fetch_wencai_news(cookie)
    if not news and existing.get("news"):
        news = existing["news"]
        stale_news = True
    else:
        stale_news = False

    if ok_count == 0 and errors and not news:
        status = "error"
        message = "问财拉取失败，部分数据可能为上次缓存"
    elif ok_count == 0 and not news:
        status = "empty"
        message = "问财暂无数据（可能非交易时段）"
    else:
        status = "ok"
        parts = []
        if ok_count:
            parts.append(f"{ok_count} 个市场问句")
        if news:
            parts.append(f"{len(news)} 条资讯")
        message = f"已更新 {' · '.join(parts)}" if parts else "已更新"
        if any(s.get("stale") for s in screens):
            message += " · 部分沿用缓存"

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "source": "同花顺问财",
        "status": status,
        "message": message,
        "cookieUsed": bool(cookie),
        "sentiment": build_sentiment(screens, existing.get("sentiment")),
        "screens": screens,
        "news": news,
    }
    if errors:
        payload["errors"] = errors
    if stale_news:
        payload["newsStale"] = True

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({status}, {ok_count} screens, {len(news)} news)")


if __name__ == "__main__":
    main()
