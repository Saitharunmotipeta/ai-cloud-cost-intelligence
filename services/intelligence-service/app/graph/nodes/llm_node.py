from app.domain.llm_explainer import LLMExplainer

llm = LLMExplainer()


def llm_node(state):

    explanation = llm.generate_explanation(
        state["service"],
        state["cost"],
        state["expected_cost"],
        state["deviation"],
    )

    return {
        "message": explanation
    }