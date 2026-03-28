import os
import json
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
        historical_trend,
        repeat_anomaly,
    ):

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
Historical Trend: {historical_trend}
Repeated Anomaly: {repeat_anomaly}

Return STRICT JSON (no extra text):

{{
  "explanation": "...",
  "root_cause": "...",
  "confidence": "low | medium | high"
}}

Rules:
- Use historical context if relevant
- Keep it concise
- No extra text
"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=80,
            )

            text = completion.choices[0].message.content.strip()

            # 🔥 SAFE PARSE
            try:
                data = json.loads(text)
            except Exception:
                data = {
                    "explanation": "AI response parsing failed",
                    "root_cause": "Unstructured output from model",
                    "confidence": "low"
                }

            return data

        except Exception as e:
            return {
                "explanation": "AI explanation unavailable",
                "root_cause": str(e),
                "confidence": "low"
            }