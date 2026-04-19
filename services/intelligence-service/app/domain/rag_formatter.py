def format_anomaly_for_embedding(anomaly: dict) -> str:
    return f"""
    Pattern: {anomaly.get("anomaly_type")}
    Severity: {anomaly.get("severity")}
    Cost: {anomaly.get("cost")}
    Deviation: {anomaly.get("deviation")}
    """


def format_insight_for_embedding(insight: dict) -> str:
    return f"""
    Pattern: {insight.get("pattern")}
    Severity: {insight.get("severity")}
    Root Cause: {insight.get("root_cause")}
    Explanation: {insight.get("explanation")}
    """