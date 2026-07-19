import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def test_gemini():
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Say Hello from Gemini."
    )
    return response.text


async def analyze_medical_report(report_text: str):
    prompt = f"""
You are an expert medical AI assistant.

Analyze the following medical report.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not write any explanation outside the JSON.

Return exactly in this format:

{{
  "summary": "...",
  "abnormal_findings": [
    "...",
    "..."
  ],
  "health_risks": [
    "...",
    "..."
  ],
  "recommendations": [
    "...",
    "..."
  ],
  "doctor_consultation": {{
    "required": true,
    "urgency": "Immediate / Within one week / Routine",
    "reason": "..."
  }}
}}

Medical Report:

{report_text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "summary": response.text,
            "abnormal_findings": [],
            "health_risks": [],
            "recommendations": [],
            "doctor_consultation": {
                "required": False,
                "urgency": "Unknown",
                "reason": "Unable to parse AI response."
            }
        }