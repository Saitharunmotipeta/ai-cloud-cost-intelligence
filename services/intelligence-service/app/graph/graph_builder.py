from langgraph.graph import StateGraph

from .state import IntelligenceState
from .nodes.rule_node import rule_node
from .nodes.llm_node import llm_node
from .nodes.severity_node import severity_node


def build_graph():

    builder = StateGraph(IntelligenceState)

    builder.add_node("rule", rule_node)
    builder.add_node("llm", llm_node)
    builder.add_node("severity_node", severity_node)

    builder.set_entry_point("rule")

    builder.add_edge("rule", "llm")
    builder.add_edge("llm", "severity_node")

    return builder.compile()