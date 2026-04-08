from app.domain.embedding import get_embedding
from app.domain.rag_store import vector_store
from app.domain.rag_formatter import format_anomaly


def context_node(state):

    event = state["event"]

    cost = event["cost"]
    expected = event["expected_cost"]

    # 🔥 existing logic (KEEP THIS)
    ratio = (cost - expected) / expected if expected else 0
    spike = ratio > 1

    if ratio > 1:
        trend = "sharp increase"
    elif ratio > 0.3:
        trend = "moderate increase"
    else:
        trend = "stable"

    # 🔥 NEW: RAG retrieval
    query_text = format_anomaly({
        "service": event["service"],
        "anomaly_type": state.get("anomaly_type", "unknown"),
        "region": event.get("region", "unknown"),
        "severity": state.get("severity", "unknown"),
        "description": f"Cost deviation {event['deviation']}"
    })

    query_embedding = get_embedding(query_text)

    results = vector_store.search(query_embedding, top_k=5)

    # 🔥 filter by same service
    filtered = [
        r for r in results
        if r.get("service") == event["service"]
    ]

    # fallback if nothing matches
    state["context"] = filtered if filtered else []

    return {
        # existing
        "service": event["service"],
        "cost": cost,
        "expected_cost": expected,
        "deviation": event["deviation"],

        "ratio": ratio,
        "spike": spike,
        "trend": trend,

        # 🔥 NEW
        "context": results
    }