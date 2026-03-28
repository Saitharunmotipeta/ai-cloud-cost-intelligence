import os
from groq import Groq

class LLMExplainer:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)

        self.model = "llama-3.1-8b-instant"

    def generate_explanation(
        self,
        service,
        cost,
        expected_cost,
        deviation,
        anomaly_type,
        trend,
        ratio,
    )->str:

        prompt = f"""
        You are a cloud cost optimization expert.

        Analyze the anomaly:

        Service: {service}
        Actual Cost: {cost}
        Expected Cost: {expected_cost}
        Deviation: {deviation}
        Anomaly Type: {anomaly_type}
        Trend: {trend}
        Change Ratio: {ratio}

        Instructions:
        - Explain clearly in 2 sentences MAX
        - Mention anomaly type
        - Mention likely root cause
        - Keep it concise and complete
        - Do NOT exceed 50 words

        Output:
        """
        try:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=60,
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:

            return f"LLM explanation unavailable: {str(e)}"