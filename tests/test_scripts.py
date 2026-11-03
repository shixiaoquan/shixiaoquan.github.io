"""脚本单元测试 — attribution / decision / validate。"""

from __future__ import annotations

import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from attribution_lib import (  # noqa: E402
    backfill_decision_labels,
    backfill_market_context,
    decision_label,
    summarize_items,
)
from decision_score import score_pick  # noqa: E402
from market_regime import detect_market_regime, regime_label  # noqa: E402
from paired_attribution import build_paired_attribution, _summarize_pairs  # noqa: E402
from shadow_reco import _calendar_weeks  # noqa: E402
from hk01810_box import decide as hk01810_decide  # noqa: E402
from validate_data import main as validate_main  # noqa: E402
from xiaomi_radar import build_radar  # noqa: E402
from xiaomi_trader import (  # noqa: E402
    build_catalyst_gate,
    build_payload,
    build_position_gate,
    build_valuation_gate,
    expand_calendar,
    implied_pe,
)


class DecisionScoreTests(unittest.TestCase):
    def test_score_pick_has_label(self):
        result = score_pick(
            {"symbol": "AAPL", "market": "美股", "sector": "消费电子"},
            market_summary={"mood": "偏多"},
            macro=None,
            wencai=None,
            master_reco=None,
            truth=None,
        )
        self.assertIn(result["decisionLabel"], ("高", "中", "低"))
        self.assertGreaterEqual(result["decisionScore"], 0)
        self.assertLessEqual(result["decisionScore"], 100)
        self.assertIn("macro", result["decisionComponents"])


class AttributionLibTests(unittest.TestCase):
    def test_decision_label_from_score(self):
        self.assertEqual(decision_label({"decisionScore": 75}), "高")
        self.assertEqual(decision_label({"decisionScore": 55}), "中")
        self.assertEqual(decision_label({"decisionScore": 40}), "低")

    def test_summarize_by_regime(self):
        items = {
            "a": {
                "returns": {"t5": 2.0},
                "signal": "buy",
                "market": "美股",
                "decisionLabel": "高",
                "marketRegime": "risk_on",
            },
            "b": {
                "returns": {"t5": -1.0},
                "signal": "watch",
                "market": "A股",
                "decisionLabel": "低",
                "marketRegime": "risk_off",
            },
        }
        summary = summarize_items(items)
        self.assertEqual(summary["maturedT5"], 2)
        self.assertIn("risk_on", summary["byRegime"])
        self.assertIn("risk_off", summary["byRegime"])


class MarketRegimeTests(unittest.TestCase):
    def test_detect_risk_off(self):
        self.assertEqual(detect_market_regime({"mood": "偏空"}, {"vix": 25}), "risk_off")

    def test_detect_risk_on(self):
        self.assertEqual(detect_market_regime({"mood": "偏多"}, {"vix": 14}), "risk_on")

    def test_regime_label(self):
        self.assertEqual(regime_label("risk_on"), "偏多")


class PairedAttributionTests(unittest.TestCase):
    def test_build_paired_runs(self):
        payload = build_paired_attribution()
        self.assertIn("summary", payload)
        self.assertIn("pairs", payload)
        self.assertIn("marketPairs", payload)
        self.assertIn("marketPairedCount", payload["summary"])

    def test_summarize_pairs(self):
        summary = _summarize_pairs(
            [
                {"edgeT5": 1.0, "prodReturnT5": 0.5, "shadowReturnT5": 1.5, "shadowWins": True},
                {"edgeT5": -0.5, "prodReturnT5": 1.0, "shadowReturnT5": 0.5, "shadowWins": False},
            ]
        )
        self.assertEqual(summary["pairedCount"], 2)
        self.assertEqual(summary["shadowWinRate"], 50.0)


class ShadowTrackTests(unittest.TestCase):
    def test_calendar_weeks_span(self):
        weeks, days = _calendar_weeks(
            [
                {"recordedAt": "2026-07-10T10:00:00+08:00"},
                {"recordedAt": "2026-07-10T16:00:00+08:00"},
                {"recordedAt": "2026-07-17T10:00:00+08:00"},
            ]
        )
        self.assertEqual(days, 2)
        self.assertEqual(weeks, 1.0)

    def test_calendar_weeks_empty(self):
        weeks, days = _calendar_weeks([])
        self.assertEqual(weeks, 0.0)
        self.assertEqual(days, 0)


class BackfillTests(unittest.TestCase):
    def test_backfill_market_context(self):
        items = {
            "2026-03-10T00:00:00:AAPL": {
                "marketRegime": "unknown",
                "marketMood": None,
            }
        }
        records = [
            {
                "id": "2026-03-10T00:00:00",
                "recordedAt": "2026-03-10T00:00:00",
                "marketContext": {"regime": "risk_on", "mood": "偏多"},
                "picks": [{"symbol": "AAPL"}],
            }
        ]
        backfill_market_context(items, records)
        self.assertEqual(items["2026-03-10T00:00:00:AAPL"]["marketRegime"], "risk_on")
        self.assertEqual(items["2026-03-10T00:00:00:AAPL"]["marketMood"], "偏多")

    def test_backfill_decision_labels(self):
        items = {"r1:MSFT": {"decisionLabel": "未知", "decisionScore": None}}
        records = [
            {
                "id": "r1",
                "picks": [{"symbol": "MSFT", "decisionScore": 72}],
            }
        ]
        backfill_decision_labels(items, records)
        self.assertEqual(items["r1:MSFT"]["decisionLabel"], "高")
        self.assertEqual(items["r1:MSFT"]["decisionScore"], 72)


class Hk01810BoxTests(unittest.TestCase):
    def test_mid_box_wait(self):
        advice = hk01810_decide(26.18)
        self.assertEqual(advice["action"], "wait")
        self.assertFalse(advice["operate"])

    def test_buy_and_sell_zones(self):
        self.assertEqual(hk01810_decide(25.7)["action"], "buy")
        self.assertEqual(hk01810_decide(25.7)["zoneId"], "t1")
        self.assertEqual(hk01810_decide(23.5)["zoneId"], "t2")
        self.assertEqual(hk01810_decide(22.0)["zoneId"], "t3")
        self.assertEqual(hk01810_decide(28.5)["action"], "sell")
        self.assertEqual(hk01810_decide(29.05)["zoneId"], "s2")

    def test_invalidation_and_breakout(self):
        self.assertEqual(hk01810_decide(21.2)["action"], "exit")
        self.assertEqual(hk01810_decide(29.5)["action"], "breakout_up")


class XiaomiTraderTests(unittest.TestCase):
    def test_calendar_windows_from_nov_3(self):
        events = [
            {"id": "q3", "kind": "earnings", "title": "三季报", "date": "2026-11-24"},
            {
                "id": "m",
                "kind": "delivery",
                "title": "汽车月度交付",
                "recurrence": "monthly",
                "dayOfMonth": 1,
            },
            {"id": "u", "kind": "data", "title": "待定", "date": None},
        ]
        calendar = expand_calendar(events, date(2026, 11, 3), 60)
        by_date = {row["date"]: row for row in calendar["upcoming"]}
        self.assertEqual(by_date["2026-11-24"]["daysUntil"], 21)
        self.assertTrue(by_date["2026-11-24"]["within30"])
        self.assertEqual(by_date["2026-12-01"]["daysUntil"], 28)
        self.assertEqual(by_date["2027-01-01"]["daysUntil"], 59)
        self.assertFalse(by_date["2027-01-01"]["within30"])
        self.assertNotIn("2026-11-01", by_date)
        self.assertEqual(len(calendar["undated"]), 1)

    def test_monthly_clamps_short_month(self):
        events = [
            {"id": "m", "kind": "delivery", "title": "交付", "recurrence": "monthly", "dayOfMonth": 31}
        ]
        calendar = expand_calendar(events, date(2026, 1, 31), 60)
        dates = [row["date"] for row in calendar["upcoming"]]
        self.assertIn("2026-02-28", dates)
        self.assertIn("2026-03-31", dates)

    def test_sell_zone_blocks_new_long(self):
        status, summary = build_valuation_gate(
            28.5, {"action": "sell", "actionLabel": "卖出2份"}, 25.2
        )
        self.assertEqual(status, "block")
        self.assertIn("不新开多", summary)

    def test_missing_price_has_no_multiple(self):
        self.assertIsNone(implied_pe(None, 246))

    def test_payload_labels_assumptions_and_four_gates(self):
        seed = json.loads((ROOT / "data" / "xiaomi_trader_seed.json").read_text(encoding="utf-8"))
        box = {
            "quote": {"price": 28.5, "asOf": "2026-11-03"},
            "levels": {"boxLow": 25.44, "boxHigh": 29.1, "bottom": 21.3},
        }
        macro = {
            "fx": [
                {"symbol": "USDCNY=X", "price": 6.65},
                {"symbol": "USDHKD=X", "price": 7.85},
            ]
        }
        paper = {"strategyCode": "XRPS-X", "positionPct": 47.4, "equity": 1_000_000, "cash": 200_000}
        payload = build_payload(
            seed,
            box=box,
            macro=macro,
            paper=paper,
            radar={"items": []},
            as_of=date(2026, 11, 3),
        )
        self.assertIn("不构成投资建议", payload["disclaimer"])
        self.assertEqual([row["id"] for row in payload["scenarios"]["items"]], ["bull", "base", "bear"])
        self.assertIn("假设", payload["scenarios"]["assumptionLabel"])
        self.assertEqual(payload["scenarios"]["items"][1]["profitMetric"], "adjusted_net_profit")
        base_pe = payload["scenarios"]["items"][1]["impliedPe"]
        self.assertIsNotNone(base_pe)
        self.assertGreater(base_pe, 15)
        self.assertLess(base_pe, 40)
        gates = {row["id"]: row for row in payload["checklist"]["gates"]}
        self.assertEqual(gates["valuation"]["status"], "block")
        self.assertEqual(gates["catalyst"]["status"], "caution")
        self.assertTrue(gates["catalyst"]["humanNote"].strip())
        self.assertEqual(gates["position"]["status"], "block")
        self.assertEqual(gates["exit"]["status"], "pass")
        self.assertIn("箱体底部", gates["exit"]["humanNote"])
        self.assertIn("不新开多", payload["stance"]["headline"])
        self.assertIn("加仓", "".join(payload["stance"]["forbidden"]))
        self.assertTrue(payload["indicators"]["phone"]["placeholder"])
        self.assertTrue(payload["indicators"]["iotMargin"]["placeholder"])
        self.assertFalse(payload["indicators"]["phone"]["available"])
        self.assertGreaterEqual(len(payload["weeklyReview"]["rows"]), 4)
        self.assertNotIn("trades", payload["publicSim"])
        self.assertEqual(payload["calendar"]["next"]["date"], "2026-11-24")
        self.assertFalse(payload["checklist"]["readyToOpen"])

    def test_valuation_uses_multiple_not_only_box(self):
        blocked, _ = build_valuation_gate(
            25.7, {"action": "buy", "actionLabel": "买入第1份"}, 25.2
        )
        self.assertEqual(blocked, "block")
        opened, summary = build_valuation_gate(
            25.7, {"action": "buy", "actionLabel": "买入第1份"}, 18
        )
        self.assertEqual(opened, "pass")
        self.assertIn("买区", summary)

    def test_position_above_add_ceiling_blocks_add_narrative(self):
        status, summary = build_position_gate(
            {"positionPct": 47.4, "equityHkd": 1_000_000, "cashHkd": 200_000},
            0.84,
            {"addCeilingPct": 40, "maxPositionPct": 80},
        )
        self.assertEqual(status, "block")
        self.assertIn("加仓", summary)

    def test_catalyst_blocks_into_an_unwritten_print(self):
        calendar = expand_calendar(
            [{"id": "q3", "kind": "earnings", "title": "三季报", "date": "2026-11-24"}],
            date(2026, 11, 3),
            60,
        )
        blocked, _ = build_catalyst_gate(calendar, human_note="", block_within_days=21)
        self.assertEqual(blocked, "block")
        noted, _ = build_catalyst_gate(
            calendar, human_note="赌的是交付，不是利润", block_within_days=21
        )
        self.assertEqual(noted, "caution")

    def test_blank_notes_keep_catalyst_blocked_and_exit_unpassed(self):
        seed = json.loads((ROOT / "data" / "xiaomi_trader_seed.json").read_text(encoding="utf-8"))
        for gate in seed["checklist"]["gates"]:
            gate["humanNote"] = ""
        box = {
            "quote": {"price": 28.5, "asOf": "2026-11-03"},
            "levels": {"boxLow": 25.44, "boxHigh": 29.1, "bottom": 21.3},
        }
        macro = {
            "fx": [
                {"symbol": "USDCNY=X", "price": 6.65},
                {"symbol": "USDHKD=X", "price": 7.85},
            ]
        }
        paper = {"strategyCode": "XRPS-X", "positionPct": 47.4, "equity": 1_000_000, "cash": 200_000}
        payload = build_payload(
            seed,
            box=box,
            macro=macro,
            paper=paper,
            radar={"items": []},
            as_of=date(2026, 11, 3),
        )
        gates = {row["id"]: row for row in payload["checklist"]["gates"]}
        self.assertEqual(gates["catalyst"]["status"], "block")
        self.assertEqual(gates["exit"]["status"], "caution")
        self.assertEqual(gates["exit"]["humanNote"], "")

    def test_radar_clusters_require_source_date_confidence(self):
        inbox = json.loads((ROOT / "data" / "xiaomi_radar_inbox.json").read_text(encoding="utf-8"))
        radar = build_radar(inbox, as_of=date(2026, 11, 3))
        self.assertGreaterEqual(len(radar["clusters"]), 3)
        flat = {row["id"]: row for row in radar["items"]}
        self.assertEqual(flat["h1-profit"]["confidence"], "high")
        self.assertFalse(flat["h1-profit"]["stale"])
        self.assertTrue(flat["skynomad"]["stale"])
        self.assertIn("source", flat["oct-deliveries"])
        self.assertEqual(flat["oct-deliveries"]["date"], "2026-11-01")
        self.assertEqual(flat["phone-asp-gap"]["clusterId"], "data-gaps")
        self.assertNotEqual(radar["clusters"][0]["id"], "data-gaps")
        self.assertEqual(radar["clusters"][-1]["id"], "data-gaps")
        self.assertTrue(str(flat["oct-deliveries"].get("sourceUrl") or "").startswith("https://"))
        self.assertEqual(flat["buyback-oct28"]["confidence"], "high")
        self.assertTrue(str(flat["buyback-oct28"].get("sourceUrl") or "").startswith("https://"))
        dropped = build_radar({"items": [{"title": "无来源"}]}, as_of=date(2026, 11, 3))
        self.assertEqual(dropped["feed"]["dropped"], 1)
        self.assertEqual(dropped["items"], [])


class ValidateDataTests(unittest.TestCase):
    def test_schema_gate_passes(self):
        self.assertEqual(validate_main(), 0)


if __name__ == "__main__":
    unittest.main()
