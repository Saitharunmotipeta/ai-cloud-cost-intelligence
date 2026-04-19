from app.domain.llm_explainer import LLMExplainer
import time


def llm_node(state):

    print("🔥 ENTERED LLM NODE")  # 🔥 DEBUG

    max_retries = 2
    delay = 1

    for attempt in range(max_retries + 1):
        try:
            llm = LLMExplainer()

            result = llm.generate_explanation(
                service=state["service"],
                cost=state["cost"],
                expected_cost=state["expected_cost"],
                deviation=state["deviation"],
                anomaly_type=state["anomaly_type"],
                trend=state["trend"],
                ratio=state["ratio"],
                historical_trend=state.get("historical_trend", "unknown"),
                repeat_anomaly=state.get("repeat_anomaly", False),
                context=state.get("context", []),
            )

            if not result:
                raise ValueError("Empty LLM response")

            return {
                "explanation": result.get("explanation"),
                "root_cause": result.get("root_cause"),
                "confidence": result.get("confidence"),
                "severity": state.get("severity"),  # 🔥 CRITICAL FIX
            }

        except Exception as e:
            print(f"⚠️ LLM attempt {attempt+1} failed:", str(e))

            if attempt < max_retries:
                time.sleep(delay)

    return {
        "explanation": "AI explanation unavailable",
        "root_cause": "LLM failed after retries",
        "confidence": "low",
        "severity": state.get("severity"),
    }