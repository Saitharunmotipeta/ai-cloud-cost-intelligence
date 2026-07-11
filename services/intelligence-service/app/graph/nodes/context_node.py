import app.domain.mock_data as mock_data
from shared.observability.metrics import (start_timer,stop_timer,)

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

    retrieval_timer = start_timer()

    # 🔥 FIX: use mock_db correctly
    results = [
        item for item in mock_data.mock_db
        if item["pattern"] == anomaly_type
    ]

    final_context = results if results else mock_data.mock_db[:2]

    retrieval_ms = stop_timer(
        retrieval_timer
    )

    print("\n🔍 DEBUG → Pattern:", anomaly_type)
    print("🔍 DEBUG → Available Patterns:", [r.get("pattern") for r in mock_data.mock_db])
    print("🔍 DEBUG → Selected Context:", final_context)
    print(f"⏱ Context Retrieval Time : {retrieval_ms:.2f} ms")

    return {
        "service": state["service"],
        "cost": cost,
        "expected_cost": expected,
        "deviation": state["deviation"],

        "ratio": ratio,
        "spike": spike,
        "trend": trend,

        "pattern": anomaly_type,
        "context": final_context,
        "context_retrieval_ms": round(retrieval_ms, 2)
    }