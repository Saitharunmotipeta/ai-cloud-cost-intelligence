from app.domain.llm_explainer import LLMExplainer
import time


def llm_node(state):

    max_retries = 2
    delay = 1

    for attempt in range(max_retries + 1):
        try:
            llm = LLMExplainer()

            explanation = llm.generate_explanation(
                service=state["service"],
                cost=state["cost"],
                expected_cost=state["expected_cost"],
                deviation=state["deviation"],
                anomaly_type=state["anomaly_type"],
                trend=state["trend"],
                ratio=state["ratio"],
            )

            return {"message": explanation}

        except Exception as e:
            print(f"⚠️ LLM attempt {attempt+1} failed:", str(e))

            if attempt < max_retries:
                time.sleep(delay)
            else:
                break

    # 🔥 fallback response
    return {
        "message": "Unable to generate AI explanation. Please review resource usage manually."
    }