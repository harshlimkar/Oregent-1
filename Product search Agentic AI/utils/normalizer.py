def normalize_product(product: dict) -> dict:
    """
    Normalize product structure across all sources
    so downstream analysis is stable and predictable.
    """

    return {
        "title": str(product.get("title", "")).strip(),
        "price": product.get("price"),
        "rating": float(product.get("rating", 3.5)) if product.get("rating") else 3.5,
        "reviews": product.get("reviews", []) or [],
        "link": product.get("link"),
        "source": product.get("source", "Unknown")
    }


def normalize_products(products: list) -> list:
    return [normalize_product(p) for p in products]
