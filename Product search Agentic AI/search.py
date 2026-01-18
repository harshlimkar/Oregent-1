import sys
import json
import asyncio
import os
from dotenv import load_dotenv

from apis.flipkart_api import search_flipkart_api
from discovery.search_engine import search_engine_discovery
from quality import rank_products

load_dotenv()

CACHE_FILE = "cache.json"

async def run_search(query: str):
    print(f"\n🔍 Searching for: {query}\n")
    products = []

    # 1️⃣ Flipkart Affiliate API (primary)
    products = search_flipkart_api(query)
    if products:
        print("✅ Found via Flipkart Affiliate API")

    # 2️⃣ Search engine fallback
    if not products:
        print("🔁 Falling back to search-engine discovery")
        products = await search_engine_discovery(query)

    # 3️⃣ Cache fallback
    if not products and os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
            products = cache.get(query, [])
            if products:
                print("📦 Using cached historical data")

    if not products:
        print("❌ No products found")
        return

    ranked = rank_products(products)

    print("\n🏆 BEST QUALITY PRODUCTS (Top 10)\n")

    for idx, p in enumerate(ranked, start=1):
        print(f"{idx}️⃣ {p['title']}")
        print(f"   Platform : {p.get('source')}")
        print(f"   Quality Score : {p['final_score']}\n")

        print("   Key Qualities:")
        for q in p["key_qualities"]:
            print(f"   • {q}")

        print(f"\n   Why Ranked #{idx}:")
        print(f"   {p['rank_reason']}")

        print("\n   Buy Link:")
        print(f"   {p.get('link')}")
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    arg = sys.argv[1]

    try:
        with open(arg, "r", encoding="utf-8") as f:
            data = json.load(f)
            query = data.get("query")
    except:
        query = arg

    asyncio.run(run_search(query))
