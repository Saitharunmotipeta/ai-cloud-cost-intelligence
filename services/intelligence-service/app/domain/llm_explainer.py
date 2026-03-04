import os
from google import genai


class LLMExplainer:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable not set")

        self.client = genai.Client(api_key=api_key)

    def generate_explanation(
        self,
        service: str,
        cost: float,
        expected_cost: float,
        deviation: float,
    ) -> str:

        prompt = f"""
You are a cloud FinOps expert.

Explain the following cloud cost anomaly in ONE short sentence (max 25 words).

Service: {service}
Expected Cost: {expected_cost}
Actual Cost: {cost}
Deviation: {deviation}

Focus on likely operational causes.
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                request_options={"timeout": 5},
            )

            return response.text.strip()

        except Exception as e:
            return f"LLM explanation unavailable: {str(e)}"