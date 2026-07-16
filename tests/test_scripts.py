"""脚本单元测试 — attribution / decision / validate。"""

from __future__ import annotations

import json
import sys
import unittest
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
from validate_data import main as validate_main  # noqa: E402


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


class ValidateDataTests(unittest.TestCase):
    def test_schema_gate_passes(self):
        self.assertEqual(validate_main(), 0)


if __name__ == "__main__":
    unittest.main()
