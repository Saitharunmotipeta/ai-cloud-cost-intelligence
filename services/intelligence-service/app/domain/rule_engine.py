class RuleEngine:

    def generate_recommendation(
        self,
        service,
        cost,
        expected_cost,
        anomaly_type,
        trend,
    ):

        service = service.lower()

        # 🔥 derive signals
        deviation = cost - expected_cost
        ratio = (deviation / expected_cost) if expected_cost else 0

        # 🔥 impact classification (VERY IMPORTANT)
        if deviation > 1000 or ratio > 3:
            impact = "critical"
        elif deviation > 500 or ratio > 2:
            impact = "high"
        elif deviation > 100 or ratio > 1:
            impact = "medium"
        else:
            impact = "low"

        # 🔴 SPIKE
        if anomaly_type == "spike":

            if service == "ec2":
                recommendation = (
                    f"[{impact.upper()}] Sudden EC2 spike detected—check autoscaling, "
                    "recent instance launches, or burst workloads immediately."
                )

            else:
                recommendation = (
                    f"[{impact.upper()}] Sudden cost spike detected—investigate scaling or deployment changes."
                )

        # 🟡 DRIFT
        elif anomaly_type == "drift":

            recommendation = (
                f"[{impact.upper()}] Gradual cost increase—review long-running workloads and optimize usage."
            )

        # 🟢 NORMAL
        else:
            recommendation = "No significant anomaly detected—continue monitoring."

        return {
            "recommendation": recommendation,
            "impact": impact,   # ✅ NEW
            "ratio": ratio      # optional for downstream
        }