import re

def normalize_price(price):
    """
    Converts price like '₹1,999', 'Rs. 1999', None → int or None
    """
    if price is None:
        return None
    if isinstance(price, int):
        return price
    price = re.sub(r"[^\d]", "", str(price))
    return int(price) if price else None


def normalize_rating(rating):
    """
    Converts rating to float between 0 and 5
    """
    try:
        rating = float(rating)
        if 0 <= rating <= 5:
            return rating
    except:
        pass
    return None


def normalize_product(product: dict) -> dict:
    """
    Standardizes product fields
    """
    return {
        "title": product.get("title"),
        "price": normalize_price(product.get("price")),
        "rating": normalize_rating(product.get("rating")),
        "reviews": product.get("reviews", []),
        "source": product.get("source", "unknown"),
        "confidence": product.get("confidence", 0.5)
    }
