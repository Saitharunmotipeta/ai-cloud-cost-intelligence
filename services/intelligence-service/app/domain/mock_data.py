mock_db = []


def load_mock_data():
    global mock_db

    mock_db = [
        {
            "pattern": "cost_spike",
            "severity": "high",
            "root_cause": "Sudden increase in usage",
            "explanation": "Sudden spike leads to cost increase."
        },
        {
            "pattern": "gradual_increase",
            "severity": "medium",
            "root_cause": "Steady workload growth",
            "explanation": "Gradual scaling increases cost."
        },
        {
            "pattern": "low_usage",
            "severity": "low",
            "root_cause": "Normal behavior",
            "explanation": "Usage is within expected limits."
        }
    ]