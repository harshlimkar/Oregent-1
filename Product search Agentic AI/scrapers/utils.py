# scrapers/utils.py

async def human_scroll(page, scrolls=5, delay=1200):
    """
    Simulate human-like scrolling to trigger lazy loading
    """
    for _ in range(scrolls):
        await page.mouse.wheel(0, 1500)
        await page.wait_for_timeout(delay)


async def wait_for_products(page, selector, timeout=20000):
    """
    Wait until product cards appear on the page
    """
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        return True
    except:
        return False
