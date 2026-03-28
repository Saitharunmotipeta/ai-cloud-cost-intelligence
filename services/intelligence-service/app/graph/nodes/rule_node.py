from app.domain.rule_engine import RuleEngine

rule_engine = RuleEngine()


def rule_node(state):

    event = state["event"]

    result = rule_engine.generate_recommendation(
        service=event["service"],
        cost=event["cost"],
        expected_cost=event["expected_cost"],
        anomaly_type=state["anomaly_type"],   # ✅ NEW
        trend=state["trend"],                 # ✅ NEW
    )

    return {
        "recommendation": result["recommendation"],
        "service": event["service"],
        "impacct":result["impact"],
        "cost": event["cost"],
        "expected_cost": event["expected_cost"],
        "deviation": event["deviation"],
    }