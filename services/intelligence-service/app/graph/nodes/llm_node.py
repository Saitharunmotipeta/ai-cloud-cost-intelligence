from app.domain.llm_explainer import LLMExplainer
import time


def llm_node(state):

    print("🔥 ENTERED LLM NODE")

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

            # -------------------------
            # 🔥 NORMALIZATION (KEY FIX)
            # -------------------------
            if not result:
                raise ValueError("Empty LLM response")

            data = result  # LLM already returns structured dict

            # Extract correct fields (REAL FIX)
            explanation = data.get("deviation_implication")
            root_cause = data.get("root_cause") or data.get("specific_cause")
            confidence = data.get("confidence")

            # -------------------------
            # 🔥 VALIDATION (RELAXED + CORRECT)
            # -------------------------
            if not explanation:
                raise ValueError("Missing explanation")

            if not root_cause:
                raise ValueError("Missing root cause")

            # -------------------------
            # ✅ SUCCESS RETURN
            # -------------------------
            return {
                "explanation": data,  # pass full structured object
                "root_cause": root_cause,
                "confidence": confidence or "medium",
                "severity": state.get("severity"),
            }

        except Exception as e:
            print(f"⚠️ LLM attempt {attempt+1} failed:", str(e))

            if attempt < max_retries:
                time.sleep(delay)

    # -------------------------
    # 🔥 FINAL FALLBACK (SAFE)
    # -------------------------
    fallback_cause = state.get("anomaly_type", "unknown anomaly")

    return {
        "explanation": None,
        "root_cause": f"Detected {fallback_cause}, requires investigation",
        "confidence": "low",
        "severity": state.get("severity"),
    }