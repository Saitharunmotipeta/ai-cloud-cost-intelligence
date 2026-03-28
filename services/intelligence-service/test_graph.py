import os
from dotenv import load_dotenv

# ✅ Load env (for local testing)
load_dotenv(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../infrastructure/docker/.env")
    )
)

from app.graph.graph_builder import build_graph


def run_test():

    graph = build_graph()

    result = graph.invoke({
        "event": {
            "account_id": "test-123",
            "service": "EC2",
            "cost": 100,
            "expected_cost": 100,
            "deviation": 10,
        }
    })

    print("\n🔥 GRAPH OUTPUT:\n")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    run_test()