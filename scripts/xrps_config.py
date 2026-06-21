"""XRPS-X 小米滚动仓交易系统 — 参数配置。"""

STRATEGY_VERSION = "XRPS-X-1.0"
STRATEGY_NAME = "小米滚动仓交易系统"
STRATEGY_CODE = "XRPS-X"

PAPER_SYMBOL = "1810.HK"
PAPER_SYMBOL_NAME = "小米集团"
PAPER_SYMBOL_MARKET = "港股"
PAPER_SYMBOL_HK_CODE = "01810"
PAPER_INITIAL_CASH = 1_000_000.0
PAPER_IPO_DATE = "2018-07-09"

# 三仓目标比例
CORE_PCT = 0.40
ROLLING_PCT = 0.40
CASH_PCT = 0.20
MAX_POSITION_PCT = 0.80

# 滚动卖出（仅滚动仓，相对滚动成本价涨幅）
ROLLING_SELL_LEVELS = (
    (0.15, 0.10),
    (0.25, 0.10),
    (0.40, 0.10),
    (0.60, 0.10),
)

# 滚动买回（相对近 60 日高点回撤，用现金买入滚动仓）
ROLLING_BUY_DRAWDOWNS = (
    (-0.10, 0.10),
    (-0.20, 0.10),
    (-0.30, 0.10),
)

# 月线加仓（连阴月数 → 用现金增核心仓，占当时净值比例）
MONTHLY_DOWN_CORE_BUY = (
    (5, 0.05),
    (6, 0.08),
    (7, 0.12),
)

# 月线减仓（仅减滚动仓）
MONTHLY_UP_REDUCE = (
    (0.20, 0.15),   # 单月涨幅 ≥20%
    (0.50, 0.25),   # 近两月累计 ≥50%
)

# 三月翻倍 → 清空滚动仓
MONTHLY_TRIPLE_REDUCE_ROLLING = True

PEAK_LOOKBACK_DAYS = 60
MIN_CASH_RESERVE_PCT = 0.10
