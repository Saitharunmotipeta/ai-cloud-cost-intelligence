from datetime import datetime, timezone

from .rule_engine import RuleEngine
from .llm_explainer import LLMExplainer


class InsightEngine:

    def __init__(self):

        self.rule_engine = RuleEngine()
        self.llm = LLMExplainer()

    def generate_insight(
        self,
        account_id: str,
        service: str,
        cost: float,
        expected_cost: float,
        deviation: float,
    ):

        # Rule-based recommendation
        rule_result = self.rule_engine.generate_recommendation(
            service,
            cost,
            expected_cost,
        )

        recommendation = rule_result["recommendation"]

        # LLM explanation
        explanation = self.llm.generate_explanation(
            service,
            cost,
            expected_cost,
            deviation,
        )

        # Severity calculation
        ratio = (cost - expected_cost) / expected_cost if expected_cost else 0

        if ratio > 2:
            severity = "CRITICAL"
        elif ratio > 1:
            severity = "HIGH"
        elif ratio > 0.5:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return {
            "account_id": account_id,
            "service": service,
            "severity": severity,
            "message": explanation,
            "recommendation": recommendation,
            "generated_at": datetime.now(timezone.utc),
        }