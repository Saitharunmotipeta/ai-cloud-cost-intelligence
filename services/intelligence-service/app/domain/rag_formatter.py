def format_anomaly(anomaly: dict) -> str:
    return f"""
    Pattern: {anomaly.get("anomaly_type")}
    PatternType: {anomaly.get("anomaly_type")}   # 🔥 boost match

    Severity: {anomaly.get("severity")}

    Cost: {anomaly.get("cost")}
    Deviation: {anomaly.get("deviation")}
    """


def format_insight(insight: dict) -> str:
    return f"""
    Pattern: {insight.get("pattern")}
    PatternType: {insight.get("pattern")}   # 🔥 boost embedding weight

    Severity: {insight.get("severity")}

    Root Cause: {insight.get("root_cause")}
    Explanation: {insight.get("explanation")}
    """