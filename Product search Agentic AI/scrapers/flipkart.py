from scrapers.base import get_browser
from scrapers.utils import human_scroll, wait_for_products

async def scrape_flipkart(query, filters, limit=10):
    playwright, browser, context = await get_browser()
    page = await context.new_page()
    products = []

    try:
        await page.goto(
            f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}",
            timeout=60000,
            wait_until="networkidle"
        )

        # 🔥 CLOSE LOGIN POPUP
        try:
            close_btn = await page.wait_for_selector(
                "button._2KpZ6l._2doB4z", timeout=5000
            )
            await close_btn.click()
        except:
            pass

        await human_scroll(page)

        found = await wait_for_products(page, "a._1fQZEK")

        if not found:
            print("❌ Flipkart: products not loaded")
            return []

        cards = await page.query_selector_all("a._1fQZEK")

        for card in cards:
            if len(products) >= limit:
                break

            title_el = await card.query_selector("div._4rR01T")
            link = await card.get_attribute("href")

            if not title_el or not link:
                continue

            products.append({
                "title": (await title_el.inner_text()).strip(),
                "link": "https://www.flipkart.com" + link,
                "reviews": [],
                "source": "Flipkart"
            })

        await page.wait_for_timeout(5000)

    finally:
        await browser.close()
        await playwright.stop()

    return products
