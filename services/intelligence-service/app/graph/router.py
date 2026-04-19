# def route_after_severity(state):

#     severity = state["severity"]

#     if severity in ["HIGH", "CRITICAL"]:
#         return "llm_node"

#     return "end"

def route_after_severity(state):
    print("🚨 ROUTER SEVERITY:", state.get("severity"))
    print("🚨 FORCING LLM NODE")

    return "llm_node"