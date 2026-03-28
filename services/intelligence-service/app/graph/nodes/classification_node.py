def classification_node(state):

    ratio = state["ratio"]
    spike = state["spike"]
    trend = state["trend"]

    # 🔥 simple but effective rules
    if spike and ratio > 1:
        anomaly_type = "spike"

    elif ratio > 0.3 and trend == "moderate increase":
        anomaly_type = "drift"

    else:
        anomaly_type = "normal"

    return {
        "anomaly_type": anomaly_type
    }