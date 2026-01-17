import requests
import json
import re
from smart_questions import SMART_QUESTIONS

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# ---------------- SAFE JSON PARSER ----------------
def extract_json(text: str) -> dict:
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError
        cleaned = re.sub(r",\s*}", "}", match.group())
        cleaned = re.sub(r",\s*]", "]", cleaned)
        return json.loads(cleaned)
    except Exception:
        return {
            "category": "unknown",
            "known_attributes": {}
        }

# ---------------- OLLAMA CALL ----------------
def ask_ollama(prompt: str) -> dict:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }
    )
    return extract_json(response.json().get("response", ""))

# ---------------- CATEGORY NORMALIZATION ----------------
def normalize_category(raw: str) -> str:
    raw = raw.lower()
    mapping = {
        "table": "home_kitchen",
        "chair": "home_kitchen",
        "bed": "home_kitchen",
        "sofa": "home_kitchen",
        "dress": "clothing_shoes_jewelry",
        "shirt": "clothing_shoes_jewelry",
        "pants": "clothing_shoes_jewelry",
        "rice": "grocery_gourmet_food",
        "food": "grocery_gourmet_food",
        "laptop": "electronics",
        "mobile": "electronics",
        "phone": "electronics"
    }
    return mapping.get(raw, raw)

# ---------------- SUPER-INTELLIGENT QUESTION LOGIC ----------------
def decide_next_question(category: str, known: dict) -> dict:
    questions = SMART_QUESTIONS.get(category)

    if not questions:
        return {
            "missing_attributes": ["clarification"],
            "next_question": "Can you tell me a bit more about what you’re looking for?"
        }

    for q in questions:
        if q["key"] not in known:
            return {
                "missing_attributes": [q["key"]],
                "next_question": q["question"]
            }

    return {
        "missing_attributes": [],
        "next_question": ""
    }

# ---------------- MAIN CONVERSATION AGENT ----------------
def conversation_agent(user_input: str) -> dict:
    prompt = f"""
You are a backend AI shopping assistant.
Return ONLY JSON.

Extract:
- category
- known_attributes

User input: "{user_input}"

JSON format:
{{ "category": "", "known_attributes": {{}} }}
"""

    data = ask_ollama(prompt)

    category = normalize_category(data.get("category", "unknown"))
    known_attributes = {
        k.lower(): str(v).lower()
        for k, v in data.get("known_attributes", {}).items()
    }

    qdata = decide_next_question(category, known_attributes)

    return {
        "category": category,
        "known_attributes": known_attributes,
        "missing_attributes": qdata["missing_attributes"],
        "next_question": qdata["next_question"]
    }
