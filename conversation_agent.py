import requests
import json
import re
from smart_questions import SMART_QUESTIONS
from image_to_prompt import image_to_text

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# ================= SESSION MEMORY =================
SESSION_MEMORY = {}

def get_session_memory(session_id: str) -> dict:
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "product": None,
            "category": None,
            "known_attributes": {}
        }
    return SESSION_MEMORY[session_id]

# ================= SAFE JSON =================
def extract_json(text: str) -> dict:
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError
        cleaned = re.sub(r",\s*}", "}", match.group())
        cleaned = re.sub(r",\s*]", "]", cleaned)
        return json.loads(cleaned)
    except Exception:
        return {"category": "unknown", "known_attributes": {}}

# ================= OLLAMA =================
def ask_ollama(prompt: str) -> dict:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }
    )
    return extract_json(res.json().get("response", ""))

# ================= PRIMARY PRODUCT (TEXT FIRST) =================
def extract_primary_product(text: str) -> str:
    text = text.lower()
    if any(w in text for w in ["pant", "pants", "trouser"]):
        return "pants"
    if "shirt" in text:
        return "shirt"
    if "dress" in text:
        return "dress"
    if "table" in text:
        return "table"
    return "product"

# ================= CATEGORY =================
def normalize_category(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["pant", "pants", "shirt", "dress", "clothing", "men", "women"]):
        return "clothing_shoes_jewelry"
    if any(w in text for w in ["table", "chair", "bed", "sofa"]):
        return "home_kitchen"
    if any(w in text for w in ["rice", "food", "grocery"]):
        return "grocery_gourmet_food"
    if any(w in text for w in ["laptop", "phone", "mobile"]):
        return "electronics"

    return "unknown"

# ================= IMAGE FILTER =================
def filter_image_text(text: str, product: str) -> str:
    text = text.lower()
    if product == "pants":
        return re.sub(r"\bshirt\b|\bt-shirt\b", "", text)
    if product == "shirt":
        return re.sub(r"\bpants\b|\btrousers\b", "", text)
    return text

# ================= CLEAN ATTRIBUTES =================
def clean_known_attributes(attrs: dict) -> dict:
    cleaned = {}
    for k, v in attrs.items():
        val = str(v).lower().strip()

        if val in ["unknown", "none", "", "[]", "['unknown']"] or "unknown" in val:
            continue

        # Clean color lists
        if "color" in k and "[" in val:
            colors = (
                val.replace("[", "")
                   .replace("]", "")
                   .replace("'", "")
                   .split(",")
            )
            cleaned["color"] = [c.strip() for c in colors if c.strip()]
        else:
            cleaned[k] = val

    return cleaned

# ================= ATTRIBUTE INFERENCE =================
def infer_attributes(known: dict) -> dict:
    inferred = {}

    style = known.get("style", "")

    if "office" in style:
        inferred["occasion"] = "office"
    elif "formal" in style:
        inferred["occasion"] = "formal"
    elif "casual" in style:
        inferred["occasion"] = "casual"
    elif "party" in style:
        inferred["occasion"] = "party"

    return inferred

# ================= QUESTIONS =================
def decide_next_question(category: str, known: dict) -> dict:
    questions = SMART_QUESTIONS.get(category)

    if not questions:
        return {
            "missing_attributes": [],
            "next_question": ""
        }

    for q in questions:
        if q["key"] not in known:
            return {
                "missing_attributes": [q["key"]],
                "next_question": q["question"]
            }

    return {"missing_attributes": [], "next_question": ""}

# ================= MAIN AGENT (STATEFUL + SMART) =================
def conversation_agent(
    user_input: str,
    image_path: str | None = None,
    session_id: str = "default"
) -> dict:
    # 🧠 Load session memory
    memory = get_session_memory(session_id)

    # 🔒 Product locking (TEXT FIRST)
    new_product = extract_primary_product(user_input)
    if new_product != "product":
        memory["product"] = new_product

    product = memory["product"]

    # 🧠 Category once
    if memory["category"] is None and product:
        memory["category"] = normalize_category(product)

    category = memory["category"]

    # 🖼️ Image → prompt refinement
    image_description = ""
    if image_path:
        try:
            raw = image_to_text(image_path)
            image_description = filter_image_text(raw, product)
        except Exception:
            pass

    # 🧠 Grounded prompt
    prompt = f"""
You are an AI shopping assistant.

IMPORTANT:
The user is buying ONLY: {product}.
Do NOT change product unless explicitly stated.

User message:
"{user_input}"
"""

    if image_description:
        prompt += f'\nImage description:\n"{image_description}"\n'

    prompt += """
Return ONLY JSON:
{
  "known_attributes": {}
}
"""

    data = ask_ollama(prompt)

    # 🧼 Merge attributes
    new_attrs = clean_known_attributes(
        {k.lower(): v for k, v in data.get("known_attributes", {}).items()}
    )
    memory["known_attributes"].update(new_attrs)

    # 🧠 Infer missing attributes
    inferred = infer_attributes(memory["known_attributes"])
    memory["known_attributes"].update(inferred)

    # ❓ Ask ONLY if truly missing
    qdata = decide_next_question(category, memory["known_attributes"])

    return {
        "session_id": session_id,
        "product": product,
        "category": category,
        "known_attributes": memory["known_attributes"],
        "missing_attributes": qdata["missing_attributes"],
        "next_question": qdata["next_question"],
        "image_description": image_description
    }
