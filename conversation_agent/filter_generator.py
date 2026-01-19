import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# ---------- SAFE JSON ----------
def extract_json(text: str) -> dict:
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError
        cleaned = re.sub(r",\s*}", "}", match.group())
        cleaned = re.sub(r",\s*]", "]", cleaned)
        return json.loads(cleaned)
    except Exception:
        return {"filters": []}

# ---------- OLLAMA ----------
def ask_ollama(prompt: str) -> dict:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        }
    )
    return extract_json(res.json().get("response", ""))

# ---------- AI FILTER GENERATOR ----------
def generate_filter_box(
    product: str,
    category: str,
    known_attributes: dict
) -> dict:
    prompt = f"""
You are an AI that designs e-commerce FILTER BOXES.

Product: {product}
Category: {category}

Already known attributes:
{json.dumps(known_attributes, indent=2)}

TASK:
- Generate ONLY relevant filters for this product
- Do NOT include already known attributes as selectable
- Choose correct filter types:
  - checkbox (multiple options)
  - button (sizes)
  - range (price)
  - rating (stars)
- Keep filters simple and useful
- Return ONLY JSON

JSON FORMAT:
{{
  "filters": [
    {{
      "key": "",
      "label": "",
      "type": "",
      "options": [] | null,
      "min": null,
      "max": null
    }}
  ]
}}
"""

    return ask_ollama(prompt)
