from typing import Dict


class RuleEngine:

    def generate_recommendation(
        self,
        service: str,
        cost: float,
        expected_cost: float,
    ) -> Dict[str, str]:

        service = service.upper()

        # Default recommendation
        recommendation = "Review recent resource usage and configuration changes."

        if service == "EC2":
            recommendation = (
                "Check autoscaling groups, recently launched EC2 instances, "
                "or unexpected workload spikes."
            )

        elif service == "S3":
            recommendation = (
                "Check S3 storage growth, large uploads, or lifecycle policy configuration."
            )

        elif service == "RDS":
            recommendation = (
                "Review database query load, instance scaling events, "
                "or long-running queries."
            )

        elif service == "LAMBDA":
            recommendation = (
                "Check Lambda invocation spikes, retry storms, or new deployments."
            )

        elif service == "CLOUDFRONT":
            recommendation = (
                "Check traffic spikes, caching behavior, or large content delivery."
            )

        elif service == "EKS":
            recommendation = (
                "Check Kubernetes cluster scaling, pod autoscaling, "
                "or increased container workloads."
            )

        return {
            "recommendation": recommendation
        }