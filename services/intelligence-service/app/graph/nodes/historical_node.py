def historical_node(state):

    # event = state["event"]

    current_cost = state["cost"]

    # 🔥 MOCK (replace later with DB/service call)
    past_costs = [95, 100, 105, 98, 102]

    past_avg = sum(past_costs) / len(past_costs)

    # 🔥 trend detection
    if current_cost > past_avg * 1.5:
        historical_trend = "abnormal spike"
    elif current_cost > past_avg * 1.1:
        historical_trend = "increasing trend"
    else:
        historical_trend = "stable"

    # 🔥 repeat anomaly detection
    repeat_anomaly = current_cost > past_avg * 1.3

    return {
        "past_avg_cost": past_avg,
        "historical_trend": historical_trend,
        "repeat_anomaly": repeat_anomaly,
    }