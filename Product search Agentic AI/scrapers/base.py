from playwright.async_api import async_playwright

async def get_browser():
    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=False,   # 🔥 MUST be False
        slow_mo=100,      # 🔥 Human-like delay
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ]
    )

    context = await browser.new_context(
        viewport=None,   # real window size
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        locale="en-IN"
    )

    return playwright, browser, context
