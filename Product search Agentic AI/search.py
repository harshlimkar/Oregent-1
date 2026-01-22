import asyncio
from discovery.search_engine import search_engine_fetch
from quality import rank_products


async def main():
    query = "smart watch"

    print(f"\n🔍 Searching for: {query}\n")

    products = []

    # Scraping stage skipped (unreliable)
    if not products:
        print("⚠️ Using search-engine discovery (reliable fallback)\n")
        products = search_engine_fetch(query, limit=15)

    if not products:
        print("❌ No products found from any source.")
        return

    ranked_products = rank_products(products, top_n=10)

    print("\n🏆 BEST QUALITY PRODUCTS (Top 10)\n")

    for idx, p in enumerate(ranked_products, 1):
        print(f"{idx}️⃣ {p['title']}")
        print(f"   Platform      : {p['source']}")
        print(f"   Quality Score : {p['final_score']}")
        print(f"   Why Ranked    : {p['rank_reason']}")
        print(f"   Buy Link      : {p['link']}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
