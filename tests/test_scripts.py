"""脚本单元测试 — attribution / decision / validate。"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from attribution_lib import decision_label, summarize_items  # noqa: E402
from decision_score import score_pick  # noqa: E402
from market_regime import detect_market_regime, regime_label  # noqa: E402
from paired_attribution import build_paired_attribution  # noqa: E402
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


class ValidateDataTests(unittest.TestCase):
    def test_schema_gate_passes(self):
        self.assertEqual(validate_main(), 0)


if __name__ == "__main__":
    unittest.main()
