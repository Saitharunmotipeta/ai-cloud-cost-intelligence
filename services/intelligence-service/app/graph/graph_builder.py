from langgraph.graph import StateGraph, END

from .state import IntelligenceState
from .nodes.rule_node import rule_node
from .nodes.llm_node import llm_node
from .nodes.severity_node import severity_node
from .nodes.context_node import context_node
from .router import route_after_severity
from .nodes.classification_node import classification_node
from .nodes.historical_node import historical_node


def build_graph():

    builder = StateGraph(IntelligenceState)

    # ✅ nodes
    builder.add_node("context", context_node)
    builder.add_node("rule", rule_node)
    builder.add_node("severity_node", severity_node)
    builder.add_node("llm_node", llm_node)
    builder.add_node("classification", classification_node)
    builder.add_node("historical", historical_node)

    # ✅ NEW entry point
    builder.set_entry_point("context")


    # ✅ flow
    builder.add_edge("context", "historical")
    builder.add_edge("historical", "classification")
    builder.add_edge("classification", "rule")
    builder.add_edge("rule", "severity_node")

    # ✅ conditional flow
    builder.add_conditional_edges(
        "severity_node",
        route_after_severity,
        {
            "llm_node": "llm_node",
            "end": END
        }
    )

    return builder.compile()