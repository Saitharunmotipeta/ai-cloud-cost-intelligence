def route_after_severity(state):

    severity = state["severity"]

    if severity in ["HIGH", "CRITICAL"]:
        return "llm_node"

    return "end"