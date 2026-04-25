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

        return None


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
        6.Do NOT include formulas like (x/y)*100
        7.Always return computed numbers

        STRICT RULES:

        - Output ONLY valid JSON
        - Do NOT truncate output
        - Ensure JSON is COMPLETE and CLOSED
        - Do NOT include markdown (```)
        - Do NOT include explanations outside JSON
        - If response is too long, SUMMARIZE instead of cutting off
        - Return ONLY valid JSON.
        - All numeric values must be fully computed numbers.
        - DO NOT include expressions like "1800/4200".
        - DO NOT include text outside JSON.

        FINAL OUTPUT FORMAT:

        {{  
        "explanation": "...",
        "root_cause": "...",
        "confidence": "low | medium | high"
        }}
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500,  # 🔥 increased
            )

            text = completion.choices[0].message.content.strip()
            print("🔎 RAW LLM OUTPUT:", text)

            data = safe_parse_json(text)

            print("✅ PARSED EXPLANATION:", data)

            return data

        except Exception as e:
            return None