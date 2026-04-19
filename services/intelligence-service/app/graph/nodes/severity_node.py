def severity_node(state):

    # cost = state["cost"]
    # expected_cost = state["expected_cost"]

    # ratio = (cost - expected_cost) / expected_cost if expected_cost else 0

    # if ratio > 2:
    #     severity = "CRITICAL"
    # elif ratio > 1:
    #     severity = "HIGH"
    # elif ratio > 0.5:
    #     severity = "MEDIUM"
    # else:
    #     severity = "LOW"

    return {
        "severity": state.get("severity", "LOW")  # trust analytics
    }