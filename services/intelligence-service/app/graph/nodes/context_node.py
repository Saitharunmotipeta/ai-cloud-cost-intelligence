from app.domain.embedding import get_embedding
from app.domain.rag_store import vector_store
from app.domain.rag_formatter import format_anomaly


def context_node(state):

    event = state["event"]

    cost = event["cost"]
    expected = event["expected_cost"]

    # 🔥 ratio + trend logic (keep)
    ratio = (cost - expected) / expected if expected else 0
    spike = ratio > 1

    if ratio > 1:
        trend = "sharp increase"
    elif ratio > 0.3:
        trend = "moderate increase"
    else:
        trend = "stable"

    # 🔥 Use pattern instead of service
    anomaly_type = state.get("anomaly_type", "unknown")

    # 🔥 RAG query (pattern-driven)
    query_text = format_anomaly({
        "anomaly_type": anomaly_type,
        "severity": state.get("severity", "unknown"),
        "cost": cost,
        "deviation": event["deviation"]
    })

    query_embedding = get_embedding(query_text)

    results = vector_store.search(query_embedding, top_k=5)

    # 🔥 NEW FILTER: match by pattern
    filtered = [
        r for r in results
        if r.get("pattern") == anomaly_type
    ]

    # 🔥 fallback: if no exact match, use top results
    final_context = filtered if filtered else results[:2]

    # 🔥 DEBUG
    print("\n🔍 DEBUG → Pattern:", anomaly_type)
    print("🔍 DEBUG → Retrieved Patterns:", [r.get("pattern") for r in results])
    print("🔍 DEBUG → Filtered Patterns:", [r.get("pattern") for r in filtered])

    return {
        "service": event["service"],
        "cost": cost,
        "expected_cost": expected,
        "deviation": event["deviation"],

        "ratio": ratio,
        "spike": spike,
        "trend": trend,

        "pattern": anomaly_type,   # 🔥 important for LLM
        "context": final_context
    }