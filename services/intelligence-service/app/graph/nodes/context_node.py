def context_node(state):

    event = state["event"]

    cost = event["cost"]
    expected = event["expected_cost"]

    # 🔥 core signal
    ratio = (cost - expected) / expected if expected else 0

    # 🔥 spike detection
    spike = ratio > 1  # >100% increase

    # 🔥 simple trend (for now static)
    if ratio > 1:
        trend = "sharp increase"
    elif ratio > 0.3:
        trend = "moderate increase"
    else:
        trend = "stable"

    return {
        "service": event["service"],
        "cost": cost,
        "expected_cost": expected,
        "deviation": event["deviation"],

        "ratio": ratio,
        "spike": spike,
        "trend": trend,
    }