#!/usr/bin/env python3
"""交易日历 — 判断行情流水线强度（high / low / closed）。"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

BJT = ZoneInfo("Asia/Shanghai")


def market_intensity(now: datetime | None = None) -> str:
    """返回 high | low | closed。"""
    now = now or datetime.now(BJT)
    if now.tzinfo is None:
        now = now.replace(tzinfo=BJT)
    else:
        now = now.astimezone(BJT)

    wd = now.weekday()  # 0=Mon
    if wd >= 5:
        return "closed"

    hour = now.hour + now.minute / 60
    # A 股 9:15–15:00；港股 9:30–16:00；美股夏令约 21:30–04:00 BJT
    if 9.25 <= hour <= 15.0:
        return "high"
    if 21.5 <= hour or hour <= 4.5:
        return "high"
    return "low"


def main() -> int:
    intensity = market_intensity()
    print(f"market_intensity={intensity}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"intensity={intensity}\n")

    # closed 时仍允许轻量任务，但可跳过重型 fetch
    return 0


if __name__ == "__main__":
    sys.exit(main())
