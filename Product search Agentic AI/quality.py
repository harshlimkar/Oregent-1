import re
from typing import List, Dict
import spacy

# -----------------------------
# Safe spaCy load
# -----------------------------
def load_spacy():
    try:
        return spacy.load("en_core_web_sm")
    except:
        return spacy.blank("en")

nlp = load_spacy()

# -----------------------------
# Optional Ollama (safe)
# -----------------------------
def ask_ollama(prompt: str):
    try:
        import ollama
        r = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        return r["message"]["content"]
    except:
        return None

# -----------------------------
# Generic aspect keywords (category-agnostic)
# -----------------------------
ASPECTS = {
    "performance": ["fast", "smooth", "accurate", "responsive"],
    "durability": ["durable", "broken", "stopped", "long lasting"],
    "comfort": ["comfortable", "fit", "grip", "lightweight"],
    "quality": ["quality", "material", "build"],
    "value": ["worth", "price", "value", "money"],
    "battery": ["battery", "backup", "charge"]
}

POSITIVE = ["good", "great", "excellent", "amazing", "best", "nice"]
NEGATIVE = ["bad", "poor", "worst", "issue", "problem", "broken"]

# -----------------------------
# Review cleaning
# -----------------------------
def clean_reviews(reviews: List[str]) -> List[str]:
    cleaned = []
    for r in reviews:
        r = r.lower()
        r = re.sub(r"[^a-z0-9\s]", " ", r)
        r = re.sub(r"\s+", " ", r).strip()
        if len(r) > 10:
            cleaned.append(r)
    return cleaned

# -----------------------------
# Aspect sentiment analysis
# -----------------------------
def aspect_analysis(reviews: List[str]) -> Dict[str, float]:
    score = {a: 0 for a in ASPECTS}
    count = {a: 0 for a in ASPECTS}

    for r in reviews:
        for aspect, keywords in ASPECTS.items():
            if any(k in r for k in keywords):
                count[aspect] += 1
                if any(p in r for p in POSITIVE):
                    score[aspect] += 1
                if any(n in r for n in NEGATIVE):
                    score[aspect] -= 1

    return {
        a: (score[a] / count[a] if count[a] else 0)
        for a in ASPECTS
    }

# -----------------------------
# Convert aspects → qualities (GENERIC)
# -----------------------------
def aspects_to_qualities(aspect_scores: Dict[str, float]) -> List[str]:
    qualities = []

    for aspect, val in aspect_scores.items():
        if val > 0.35:
            qualities.append(f"Strong {aspect.replace('_', ' ')}")
        elif val < -0.35:
            qualities.append(f"Weak {aspect.replace('_', ' ')}")

    if not qualities:
        qualities.append("Balanced overall quality")

    return qualities[:4]

# -----------------------------
# Generate rank explanation (GENERIC)
# -----------------------------
def generate_rank_reason(rank: int, product: dict, prev_product: dict | None):
    if rank == 1:
        return (
            "This product ranks first because it has the highest overall quality score, "
            "driven by strong performance across multiple quality aspects and consistently "
            "positive user feedback."
        )

    if prev_product:
        diff = round(prev_product["final_score"] - product["final_score"], 3)
        return (
            f"This product ranks #{rank} because its overall quality score is slightly "
            f"lower than the higher-ranked option by {diff}. While it performs well, it shows "
            f"comparatively fewer strong positive signals in certain quality aspects."
        )

    return f"This product ranks #{rank} due to moderate overall quality."

# -----------------------------
# Main ranking engine (GENERIC)
# -----------------------------
def rank_products(products: List[Dict], top_n: int = 10) -> List[Dict]:
    ranked = []

    for p in products:
        reviews = clean_reviews(p.get("reviews", []))
        aspect_scores = aspect_analysis(reviews)

        # Optional LLM signal
        llm_score = 0.6
        llm_text = ask_ollama(
            f"Give an overall quality score between 0 and 1:\n{reviews[:8]}"
        ) if reviews else None

        if llm_text:
            for t in llm_text.split():
                try:
                    v = float(t)
                    if 0 <= v <= 1:
                        llm_score = v
                        break
                except:
                    pass

        rating_score = (p.get("rating") or 3.5) / 5
        aspect_score = sum((v + 1) / 2 for v in aspect_scores.values()) / len(aspect_scores)

        final_score = round(
            0.4 * rating_score +
            0.3 * aspect_score +
            0.3 * llm_score,
            3
        )

        ranked.append({
            **p,
            "final_score": final_score,
            "key_qualities": aspects_to_qualities(aspect_scores),
            "aspect_scores": aspect_scores
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)

    output = []
    for i, p in enumerate(ranked[:top_n]):
        prev = ranked[i - 1] if i > 0 else None
        p["rank_reason"] = generate_rank_reason(i + 1, p, prev)
        output.append(p)

    return output
