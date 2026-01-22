"""
quality.py
----------
Analyzes product quality using text-based signals
(reviews, snippets, descriptions).
"""

import re


POSITIVE_WORDS = [
    "best", "excellent", "great", "recommended", "top",
    "reliable", "amazing", "good", "worth", "value"
]

NEGATIVE_WORDS = [
    "bad", "poor", "worst", "issue", "problem",
    "complaint", "damage", "fake"
]

ASPECT_KEYWORDS = {
    "battery": ["battery", "backup", "charge"],
    "performance": ["performance", "fast", "smooth", "accurate"],
    "design": ["design", "build", "comfortable", "look"],
    "value": ["price", "value", "worth", "budget"]
}


def analyze_text_quality(texts):
    """
    Given list of review/snippet texts, return:
    - quality score
    - key qualities
    """
    score = 0.4  # base score
    aspects_found = set()

    for text in texts:
        t = text.lower()

        for w in POSITIVE_WORDS:
            if w in t:
                score += 0.05

        for w in NEGATIVE_WORDS:
            if w in t:
                score -= 0.05

        for aspect, keywords in ASPECT_KEYWORDS.items():
            for k in keywords:
                if k in t:
                    aspects_found.add(aspect)

    score = max(0.1, min(score, 0.95))

    return score, aspects_found


def rank_products(products, top_n=10):
    ranked = []

    for product in products:
        texts = product.get("reviews", [])

        score, aspects = analyze_text_quality(texts)

        if aspects:
            reason = (
                f"Strong performance in "
                + ", ".join(sorted(aspects))
                + " based on user feedback."
            )
        else:
            reason = (
                "Consistently positive mentions and balanced overall quality "
                "across multiple sources."
            )

        ranked.append({
            "title": product["title"],
            "link": product["link"],
            "source": product["source"],
            "final_score": round(score, 2),
            "rank_reason": reason
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked[:top_n]
