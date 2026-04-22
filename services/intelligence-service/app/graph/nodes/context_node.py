import app.domain.mock_data as mock_data


def context_node(state):

    cost = state["cost"]
    expected = state["expected_cost"]

    ratio = (cost - expected) / expected if expected else 0
    spike = ratio > 1

    if ratio > 1:
        trend = "sharp increase"
    elif ratio > 0.3:
        trend = "moderate increase"
    else:
        trend = "stable"

    anomaly_type = state.get("anomaly_type", "unknown")

    # 🔥 FIX: use mock_db correctly
    results = [
        item for item in mock_data.mock_db
        if item["pattern"] == anomaly_type
    ]

    final_context = results if results else mock_data.mock_db[:2]

    print("\n🔍 DEBUG → Pattern:", anomaly_type)
    print("🔍 DEBUG → Available Patterns:", [r.get("pattern") for r in mock_data.mock_db])
    print("🔍 DEBUG → Selected Context:", final_context)

    return {
        "service": state["service"],
        "cost": cost,
        "expected_cost": expected,
        "deviation": state["deviation"],

        "ratio": ratio,
        "spike": spike,
        "trend": trend,

        "pattern": anomaly_type,
        "context": final_context
    }