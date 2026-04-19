from app.domain.embedding import get_embedding
from app.domain.rag_store import vector_store
from app.domain.rag_formatter import format_anomaly_for_embedding


def context_node(state):

    cost = state["cost"]
    expected = state["expected_cost"]

    # 🔥 ratio + trend logic
    ratio = (cost - expected) / expected if expected else 0
    spike = ratio > 1

    if ratio > 1:
        trend = "sharp increase"
    elif ratio > 0.3:
        trend = "moderate increase"
    else:
        trend = "stable"

    anomaly_type = state.get("anomaly_type", "unknown")

    # 🔥 RAG query
    query_text = format_anomaly_for_embedding({
        "anomaly_type": anomaly_type,
        "severity": state.get("severity", "unknown"),
        "cost": cost,
        "deviation": state["deviation"]   # ✅ FIXED
    })

    query_embedding = get_embedding(query_text)

    results = vector_store.search(query_embedding, top_k=5)

    # 🔥 filter by pattern
    filtered = [
        r for r in results
        if r.get("pattern") == anomaly_type
    ]

    final_context = filtered if filtered else results[:2]

    # 🔥 DEBUG
    print("\n🔍 DEBUG → Pattern:", anomaly_type)
    print("🔍 DEBUG → Retrieved Patterns:", [r.get("pattern") for r in results])
    print("🔍 DEBUG → Filtered Patterns:", [r.get("pattern") for r in filtered])

    return {
        "service": state["service"],   # ✅ FIXED
        "cost": cost,
        "expected_cost": expected,
        "deviation": state["deviation"],

        "ratio": ratio,
        "spike": spike,
        "trend": trend,

        "pattern": anomaly_type,
        "context": final_context
    }