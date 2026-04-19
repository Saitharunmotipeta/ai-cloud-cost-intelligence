from app.domain.rule_engine import RuleEngine

rule_engine = RuleEngine()


def rule_node(state):

    result = rule_engine.generate_recommendation(
        service=state["service"],
        cost=state["cost"],
        expected_cost=state["expected_cost"],
        anomaly_type=state["anomaly_type"],
        trend=state["trend"],
    )

    return {
        "recommendation": result["recommendation"],
        "impact": result["impact"],

        # 🔥 keep state consistent
        "service": state["service"],
        "cost": state["cost"],
        "expected_cost": state["expected_cost"],
        "deviation": state["deviation"],
    }