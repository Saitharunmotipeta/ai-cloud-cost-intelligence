import os
import json
from groq import Groq
import re


def safe_parse_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

        return {
            "explanation": "AI response parsing failed",
            "root_cause": "Unstructured output from model",
            "confidence": "low"
        }


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
        context=None,
    ):

        def build_context_text(context):
            if not context:
                return "No similar patterns available."

            lines = []
            for c in context[:3]:
                line = (
                    f"Pattern: {c.get('pattern')}, "
                    f"Cause: {c.get('root_cause')}, "
                    f"Insight: {c.get('explanation')}"
                )
                lines.append(line)

            return "\n".join(lines)

        context_text = build_context_text(context)

        prompt = f"""
        You are a senior cloud cost analyst.

        You MUST analyze the anomaly using NUMBERS and LOGIC.

        DATA:
        Service: {service}
        Actual Cost: {cost}
        Expected Cost: {expected_cost}
        Deviation: {deviation}
        Ratio: {ratio}
        Trend: {trend}
        Anomaly Type: {anomaly_type}

        REFERENCE PATTERNS:
        {context_text}

        INSTRUCTIONS:
        1. Calculate how significant the deviation is
        2. Explain what this deviation implies
        3. Compare with similar patterns if relevant
        4. Provide a SPECIFIC cause (not generic)
        5. Avoid vague phrases like "usage variation"

        OUTPUT STRICT JSON:
        {{
        "explanation": "...must include numbers and reasoning...",
        "root_cause": "...specific cause...",
        "confidence": "low | medium | high"
        }}
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=250,  # 🔥 increased
            )

            text = completion.choices[0].message.content.strip()
            print("🔎 RAW LLM OUTPUT:", text)

            data = safe_parse_json(text)

            print("✅ PARSED EXPLANATION:", data)
            
            return data

        except Exception as e:
            return {
                "explanation": "AI explanation unavailable",
                "root_cause": str(e),
                "confidence": "low"
            }