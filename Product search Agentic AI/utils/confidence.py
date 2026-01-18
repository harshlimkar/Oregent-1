def explain_confidence(product):
    if product["confidence"] >= 0.85:
        return "High confidence (official data source)"
    if product["confidence"] >= 0.6:
        return "Medium confidence (search aggregation)"
    return "Low confidence (scraped fallback)"
