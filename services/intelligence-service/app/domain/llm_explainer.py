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
        service: str,
        cost: float,
        expected_cost: float,
        deviation: float,
    ) -> str:

        prompt = f"""
You are a cloud FinOps expert.

Explain the following cloud cost anomaly in ONE short sentence.

Service: {service}
Expected Cost: {expected_cost}
Actual Cost: {cost}
Deviation: {deviation}

Focus on operational causes.
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