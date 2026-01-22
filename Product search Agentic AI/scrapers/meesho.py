from scrapers.base import get_browser
from scrapers.utils import human_scroll

async def scrape_meesho(query, filters, limit=10):
    playwright = browser = context = None
    products = []

    try:
        playwright, browser, context = await get_browser()
        page = await context.new_page()

        url = f"https://www.meesho.com/search?q={query.replace(' ', '%20')}"
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        await human_scroll(page)

        cards = await page.query_selector_all("a")

        for card in cards:
            if len(products) >= limit:
                break

            try:
                link = await card.get_attribute("href")
                title = (await card.inner_text()).strip()

                if not link or not title or "meesho.com" not in link:
                    continue

                products.append({
                    "title": title,
                    "link": link,
                    "reviews": [],
                    "source": "Meesho"
                })
            except:
                continue

    except Exception as e:
        print("Meesho blocked:", e)

    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

    return products
