import json
from pydantic import ValidationError
from src.schemas import Demographics

PROMPT_TEMPLATE = """Extract patient demographics from the clinical note below.

Return ONLY a JSON object with these exact fields:
- "sex": "male" or "female", or null if not stated
- "age": age in years as a number, or null if not stated
- "weight_kg": weight in kilograms as a number, or null if not stated
- "height_cm": height in centimeters as a number, or null if not stated
- "bmi": body mass index as a number, or null if not stated

Return nothing but the JSON — no explanation, no markdown fences.

Clinical note:
{note}
"""


def extract_demographics(note: str, client) -> dict:
    """Return a dict describing the outcome so failures can be surveyed:
    success -> {"status": "ok", "data": {...}}
    failure -> {"status": "error", "stage": ..., "error": ..., "raw": ...}
    """
    prompt = PROMPT_TEMPLATE.format(note=note)
    raw_response = client.complete(prompt)

    # clean markdown fences
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json") :]
        cleaned = cleaned.strip()

    # parse JSON
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "stage": "json_parse",
            "error": str(e),
            "raw": raw_response,
        }

    # validate against schema
    try:
        demo = Demographics(**data)
        return {"status": "ok", "data": demo.model_dump()}
    except ValidationError as e:
        return {
            "status": "error",
            "stage": "validation",
            "error": str(e),
            "raw": raw_response,
        }
