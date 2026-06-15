#!/usr/bin/env python3
"""同花顺问财 — 离线拉取 A 股洞察，写入 data/wencai.json。"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from wencai_queries import WENCAI_SCREENS

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "wencai.json"

CODE_KEYS = ("股票代码", "code")
NAME_KEYS = ("股票简称", "名称", "股票名称")
PRICE_KEYS = ("最新价", "现价")
CHANGE_KEYS = ("最新涨跌幅", "涨跌幅", "涨跌幅:前复权")
FLOW_KEYS = ("主力资金流向", "陆股通净买入额", "主力净流入")
RANK_KEYS = ("个股热度排名", "排名")


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


def build_sentiment(screens: list[dict]) -> dict:
    limit_up = next((s for s in screens if s["id"] == "limit_up"), {})
    limit_down = next((s for s in screens if s["id"] == "limit_down"), {})
    up_count = limit_up.get("count")
    down_count = limit_down.get("count")

    mood = "震荡"
    if up_count is not None and down_count is not None:
        if up_count > down_count * 3:
            mood = "偏多"
        elif down_count > up_count * 2:
            mood = "偏空"

    return {
        "limitUp": up_count,
        "limitDown": down_count,
        "limitUpNote": limit_up.get("countNote"),
        "limitDownNote": limit_down.get("countNote"),
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
            screens.append(fetch_screen(screen, cookie))
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

    ok_count = sum(1 for s in screens if s.get("status") == "ok" and s.get("items"))
    if ok_count == 0 and errors:
        status = "error"
        message = "问财拉取失败，请检查 Cookie 或问句。详见 .cursor/skills/wencai/SKILL.md"
    elif ok_count == 0:
        status = "empty"
        message = "问财暂无数据（可能非交易时段）"
    else:
        status = "ok"
        message = f"已更新 {ok_count} 个问句结果"

    payload = {
        "updatedAt": now.isoformat(timespec="seconds"),
        "source": "同花顺问财",
        "status": status,
        "message": message,
        "cookieUsed": bool(cookie),
        "sentiment": build_sentiment(screens),
        "screens": screens,
    }
    if errors:
        payload["errors"] = errors

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({status}, {ok_count} screens with data)")


if __name__ == "__main__":
    main()
