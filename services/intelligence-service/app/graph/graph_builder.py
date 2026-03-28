from langgraph.graph import StateGraph, END

from .state import IntelligenceState
from .nodes.rule_node import rule_node
from .nodes.llm_node import llm_node
from .nodes.severity_node import severity_node
from .router import route_after_severity


def build_graph():

    builder = StateGraph(IntelligenceState)

    builder.add_node("rule", rule_node)
    builder.add_node("severity_node", severity_node)
    builder.add_node("llm_node", llm_node)

    builder.set_entry_point("rule")

    # flow
    builder.add_edge("rule", "severity_node")

    # 🔥 conditional edge
    builder.add_conditional_edges(
        "severity_node",
        route_after_severity,
        {
            "llm_node": "llm_node",
            "end": END
        }
    )

    return builder.compile()