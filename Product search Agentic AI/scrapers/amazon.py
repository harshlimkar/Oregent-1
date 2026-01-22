from scrapers.base import get_browser
from scrapers.utils import human_scroll, wait_for_products

async def scrape_amazon(query, filters, limit=10):
    playwright = browser = context = None
    products = []

    try:
        playwright, browser, context = await get_browser()
        page = await context.new_page()

        url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"

        # ✅ DO NOT use networkidle on Amazon
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")

        # Allow JS to settle
        await page.wait_for_timeout(3000)

        # Scroll to trigger lazy loading
        await human_scroll(page, scrolls=5)

        # Explicitly wait for product cards
        found = await wait_for_products(
            page,
            "div[data-component-type='s-search-result']",
            timeout=20000
        )

        if not found:
            print("❌ Amazon: product cards not found")
            return []

        cards = await page.query_selector_all(
            "div[data-component-type='s-search-result']"
        )

        for card in cards:
            if len(products) >= limit:
                break

            try:
                title_el = await card.query_selector("h2 span")
                link_el = await card.query_selector("h2 a")

                if not title_el or not link_el:
                    continue

                title = (await title_el.inner_text()).strip()
                href = await link_el.get_attribute("href")

                if not href or not href.startswith("/"):
                    continue

                products.append({
                    "title": title,
                    "link": "https://www.amazon.in" + href,
                    "reviews": [],
                    "source": "Amazon"
                })
            except:
                continue

        # 🔍 DEBUG: keep browser open briefly
        await page.wait_for_timeout(4000)

    except Exception as e:
        print("Amazon error:", e)

    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

    return products
