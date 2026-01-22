from scrapers.base import get_browser
from scrapers.utils import human_scroll

async def scrape_myntra(query, filters, limit=10):
    playwright = browser = context = None
    products = []

    try:
        playwright, browser, context = await get_browser()
        page = await context.new_page()

        url = f"https://www.myntra.com/{query.replace(' ', '-')}"
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        await human_scroll(page)

        cards = await page.query_selector_all("li.product-base")

        for card in cards:
            if len(products) >= limit:
                break

            try:
                brand_el = await card.query_selector("h3.product-brand")
                name_el = await card.query_selector("h4.product-product")
                link_el = await card.query_selector("a")

                if not brand_el or not name_el or not link_el:
                    continue

                title = f"{(await brand_el.inner_text()).strip()} {(await name_el.inner_text()).strip()}"
                link = await link_el.get_attribute("href")

                products.append({
                    "title": title,
                    "link": link,
                    "reviews": [],
                    "source": "Myntra"
                })
            except:
                continue

    except Exception as e:
        print("Myntra blocked:", e)

    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

    return products
