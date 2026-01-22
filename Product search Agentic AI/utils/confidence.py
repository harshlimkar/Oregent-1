def compute_confidence(product: dict) -> float:
    """
    Confidence reflects reliability of the quality score,
    based on number of reviews and rating strength.
    """

    reviews = product.get("reviews", [])
    rating = product.get("rating", 0)

    review_factor = min(len(reviews) / 20.0, 1.0)   # max at 20 reviews
    rating_factor = min(rating / 5.0, 1.0)

    confidence = round((0.6 * review_factor) + (0.4 * rating_factor), 2)
    return confidence


def attach_confidence(products: list) -> list:
    for p in products:
        p["confidence"] = compute_confidence(p)
    return products
