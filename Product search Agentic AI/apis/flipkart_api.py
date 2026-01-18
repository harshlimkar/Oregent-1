import os
import requests

FLIPKART_API_KEY = os.getenv("FLIPKART_API_KEY")

def search_flipkart_api(query, limit=10):
    """
    REAL Flipkart Affiliate API should be plugged here.
    This is a safe stub structure.
    """
    if not FLIPKART_API_KEY:
        return []

    # Simulated response (replace with real API response parsing)
    return [{
        "title": "Logitech G102 Gaming Mouse",
        "price": 1799,
        "rating": 4.5,
        "reviews": [
            "Very smooth and accurate",
            "Great for gaming",
            "Build quality is decent"
        ],
        "link": "https://www.flipkart.com/affiliate-link",
        "source": "Flipkart API",
        "confidence": 0.9
    }]
