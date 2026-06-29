#!/usr/bin/env python3
"""抓取 Truth Social @realDonaldTrump 帖子，翻译为中文并写入 data/trump_truth.json。"""

from __future__ import annotations

import html
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "trump_truth.json"
ACCOUNT_HANDLE = "realDonaldTrump"
MAX_POSTS = 40
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def strip_html(content: str) -> str:
    if not content:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", content, flags=re.I)
    text = re.sub(r"</p>", "\n\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def translate_to_zh(text: str) -> tuple[str, str]:
    """返回 (译文, status: ok|same|error)。"""
    if not text or not text.strip():
        return text, "same"
    try:
        from deep_translator import GoogleTranslator

        chunk = text[:4500]
        translated = GoogleTranslator(source="auto", target="zh-CN").translate(chunk)
        if not translated:
            return text, "error"
        if translated.strip() == chunk.strip():
            return translated, "same"
        return translated.strip(), "ok"
    except Exception:
        return text, "error"


def load_existing() -> dict:
    if OUTPUT_FILE.exists():
        try:
            data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "updatedAt": None,
        "status": "empty",
        "account": {
            "username": ACCOUNT_HANDLE,
            "displayName": "Donald J. Trump",
            "profileUrl": f"https://truthsocial.com/@{ACCOUNT_HANDLE}",
        },
        "posts": [],
    }


def fetch_posts() -> tuple[list[dict], dict, str]:
    """返回 (posts, account_meta, status)。"""
    token = os.environ.get("TRUTHSOCIAL_TOKEN")
    username = os.environ.get("TRUTHSOCIAL_USERNAME")
    password = os.environ.get("TRUTHSOCIAL_PASSWORD")

    if not token and not (username and password):
        return [], {}, "missing_credentials"

    try:
        from truthbrush.api import Api

        api = Api(username=username, password=password, token=token)
        account = api.lookup(ACCOUNT_HANDLE)
        if not account:
            return [], {}, "error"

        raw_posts = list(api.pull_statuses(ACCOUNT_HANDLE, replies=False, verbose=False))
        if not raw_posts:
            return [], account, "empty"

        posts = []
        for item in raw_posts[:MAX_POSTS]:
            post_id = str(item.get("id", ""))
            if not post_id:
                continue
            content_html = item.get("content") or ""
            plain = strip_html(content_html)
            media = []
            for att in item.get("media_attachments") or []:
                media.append(
                    {
                        "type": att.get("type") or "image",
                        "url": att.get("url") or "",
                        "previewUrl": att.get("preview_url") or att.get("url") or "",
                        "description": att.get("description") or "",
                    }
                )

            posts.append(
                {
                    "id": post_id,
                    "url": item.get("url") or f"https://truthsocial.com/@{ACCOUNT_HANDLE}/posts/{post_id}",
                    "publishedAt": item.get("created_at"),
                    "content": plain,
                    "contentHtml": content_html,
                    "media": media,
                    "reblogsCount": item.get("reblogs_count") or 0,
                    "favouritesCount": item.get("favourites_count") or 0,
                    "repliesCount": item.get("replies_count") or 0,
                }
            )

        account_meta = {
            "id": str(account.get("id", "")),
            "username": account.get("username") or ACCOUNT_HANDLE,
            "displayName": account.get("display_name") or "Donald J. Trump",
            "avatar": account.get("avatar") or account.get("avatar_static") or "",
            "header": account.get("header") or account.get("header_static") or "",
            "followersCount": account.get("followers_count"),
            "statusesCount": account.get("statuses_count"),
            "profileUrl": account.get("url") or f"https://truthsocial.com/@{ACCOUNT_HANDLE}",
            "note": strip_html(account.get("note") or ""),
        }
        return posts, account_meta, "ok"
    except Exception as exc:
        print(f"Truth Social fetch error: {exc}")
        return [], {}, "error"


def merge_translations(new_posts: list[dict], existing_posts: list[dict]) -> list[dict]:
    by_id = {p["id"]: p for p in existing_posts if p.get("id")}
    merged = []
    for post in new_posts:
        old = by_id.get(post["id"], {})
        content = post.get("content") or ""
        if old.get("content") == content and old.get("contentZh"):
            post["contentZh"] = old["contentZh"]
            post["translationStatus"] = old.get("translationStatus", "ok")
        else:
            zh, status = translate_to_zh(content)
            post["contentZh"] = zh
            post["translationStatus"] = status
        merged.append(post)
    return merged


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone()
    existing = load_existing()
    cred_used = bool(
        os.environ.get("TRUTHSOCIAL_TOKEN")
        or (os.environ.get("TRUTHSOCIAL_USERNAME") and os.environ.get("TRUTHSOCIAL_PASSWORD"))
    )

    posts, account, status = fetch_posts()

    if posts:
        posts = merge_translations(posts, existing.get("posts") or [])
        payload = {
            "updatedAt": now.isoformat(timespec="seconds"),
            "status": status,
            "credentialUsed": cred_used,
            "account": account,
            "posts": posts,
            "source": {
                "platform": "Truth Social",
                "handle": f"@{ACCOUNT_HANDLE}",
                "profileUrl": f"https://truthsocial.com/@{ACCOUNT_HANDLE}",
            },
            "disclaimer": "非官方镜像，仅供阅读；版权归原发布者与 Truth Social 所有。",
        }
    elif existing.get("posts"):
        payload = {**existing}
        payload["updatedAt"] = now.isoformat(timespec="seconds")
        payload["credentialUsed"] = cred_used
        payload["status"] = status if status != "ok" else "stale"
        print(f"Fetch failed ({status}), keeping {len(existing.get('posts', []))} cached posts.")
    else:
        payload = {
            "updatedAt": now.isoformat(timespec="seconds"),
            "status": status,
            "credentialUsed": cred_used,
            "account": existing.get("account")
            or {
                "username": ACCOUNT_HANDLE,
                "displayName": "Donald J. Trump",
                "profileUrl": f"https://truthsocial.com/@{ACCOUNT_HANDLE}",
            },
            "posts": [],
            "source": {
                "platform": "Truth Social",
                "handle": f"@{ACCOUNT_HANDLE}",
                "profileUrl": f"https://truthsocial.com/@{ACCOUNT_HANDLE}",
            },
            "disclaimer": "非官方镜像，仅供阅读；版权归原发布者与 Truth Social 所有。",
            "setupHint": "请在 GitHub Secrets 配置 TRUTHSOCIAL_TOKEN 或 TRUTHSOCIAL_USERNAME/PASSWORD",
        }

    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({len(payload.get('posts', []))} posts, status={payload.get('status')})")


if __name__ == "__main__":
    main()
