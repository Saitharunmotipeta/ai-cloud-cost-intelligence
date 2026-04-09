import os
from dotenv import load_dotenv

# ✅ Load env
load_dotenv(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../infrastructure/docker/.env")
    )
)

from app.graph.graph_builder import build_graph
from app.domain.rag_store import vector_store
from app.domain.embedding import get_embedding
from app.domain.rag_formatter import format_insight


# 🔥 STEP 1: Load mock RAG data
def load_test_data():
    print("📦 Loading mock RAG data...\n")

    mock_insights = [
        {
            "service": "EC2",
            "anomaly_type": "spike",
            "severity": "high",
            "root_cause": "AUTO_SCALING_BUG_UNIQUE",
            "explanation": "Instances scaled aggressively due to low threshold"
        },
        {
            "service": "EC2",
            "anomaly_type": "spike",
            "severity": "high",
            "root_cause": "TRAFFIC_SPIKE_UNIQUE",
            "explanation": "High incoming traffic caused sudden scaling"
        }
    ]

    for insight in mock_insights:
        text = format_insight(insight)
        emb = get_embedding(text)
        vector_store.add(emb, insight)

    print("✅ Mock data loaded into vector store\n")


# 🔥 STEP 2: Run test cases
def run_test():
    print("\n🚀 Starting Intelligence Graph RAG Test\n")

    # 👉 Load RAG memory FIRST
    load_test_data()

    print("⚙️ Building graph...")
    graph = build_graph()
    print("✅ Graph built successfully\n")

    test_cases = [
        {
            "name": "🔥 EC2 Spike (Should MATCH RAG)",
            "event": {
                "account_id": "test-1",
                "service": "EC2",
                "cost": 300,
                "expected_cost": 100,
                "deviation": 200,
            }
        },
        {
            "name": "⚡ EC2 Moderate (Partial Match)",
            "event": {
                "account_id": "test-2",
                "service": "EC2",
                "cost": 500,
                "expected_cost": 100,
                "deviation": 400,
            }
        },
        {
            "name": "🧊 S3 Spike (Should NOT match EC2 context)",
            "event": {
                "account_id": "test-3",
                "service": "S3",
                "cost": 600,
                "expected_cost": 100,
                "deviation": 500,
            }
        }
    ]

    for idx, test in enumerate(test_cases, 1):
        print("\n" + "=" * 60)
        print(f"🧪 TEST {idx}: {test['name']}")
        print("=" * 60)

        try:
            print("⚡ Running graph...\n")

            result = graph.invoke({
                "event": test["event"]
            })

            print("✅ Graph executed successfully\n")

            # 🔍 RAG Context
            context = result.get("context", [])
            print("🔍 RAG CONTEXT:")
            if context:
                for i, c in enumerate(context, 1):
                    print(f"  {i}. {c}")
            else:
                print("  ❌ No context retrieved")

            # 🧠 Explanation
            print("\n🧠 EXPLANATION:")
            print(result.get("explanation", "❌ Missing"))

            # 🎯 Root Cause
            print("\n🎯 ROOT CAUSE:")
            print(result.get("root_cause", "❌ Missing"))

            # 📊 Confidence
            print("\n📊 CONFIDENCE:")
            print(result.get("confidence", "❌ Missing"))

            # 🔥 Validation
            print("\n🧪 VALIDATION CHECK:")
            if context:
                print("  ✅ Context retrieved → RAG working")
            else:
                print("  ❌ No context → RAG NOT working")

        except Exception as e:
            print("\n❌ ERROR DURING TEST:")
            print(str(e))

    print("\n🏁 TEST RUN COMPLETE\n")


if __name__ == "__main__":
    run_test()