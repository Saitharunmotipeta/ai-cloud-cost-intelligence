def format_anomaly(anomaly: dict) -> str:
    return f"""
    Service: {anomaly.get("service")}
    ServiceType: {anomaly.get("service")}   # 🔥 boost importance
    Type: {anomaly.get("anomaly_type")}
    Severity: {anomaly.get("severity")}
    Description: {anomaly.get("description")}
    """


def format_insight(insight: dict) -> str:
    return f"""
    Service: {insight.get("service")}
    Type: {insight.get("anomaly_type")}
    Severity: {insight.get("severity")}
    Root Cause: {insight.get("root_cause")}
    Explanation: {insight.get("explanation")}
    """