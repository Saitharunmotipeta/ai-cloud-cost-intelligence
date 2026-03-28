from app.domain.rule_engine import RuleEngine

rule_engine = RuleEngine()


def rule_node(state):

    event = state["event"]

    result = rule_engine.generate_recommendation(
        event["service"],
        event["cost"],
        event["expected_cost"],
    )

    return {
        "recommendation": result["recommendation"],
        "service": event["service"],
        "cost": event["cost"],
        "expected_cost": event["expected_cost"],
        "deviation": event["deviation"],
    }