from contextlib import asynccontextmanager

from playwright.async_api import Playwright, BrowserContext, async_playwright

from crawler.src.core.config import HEADLESS, VIEWPORT_WIDTH, VIEWPORT_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, USERAGENT, \
    logger


async def _headless_browser(playwright_context: Playwright) -> BrowserContext:
    _browser = await playwright_context.chromium.launch(args=['--headless=new'], headless=False)
    browser = await _browser.new_context(user_agent=USERAGENT)
    return browser


async def _headful_browser(playwright_context: Playwright) -> BrowserContext:
    _browser = await playwright_context.chromium.launch(args=['--start-maximized'], headless=False)
    browser = await _browser.new_context(
        user_agent=USERAGENT,
        viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT},
        screen={'width': SCREEN_WIDTH, 'height': SCREEN_HEIGHT},
    )
    return browser


@asynccontextmanager
async def browser_context() -> BrowserContext:
    async with async_playwright() as pw_context:
        browser = await _headless_browser(pw_context) if HEADLESS else await _headful_browser(pw_context)
        logger.info('Created browser')
        try:
            logger.info('Opened browser')
            yield browser
        finally:
            await browser.close()
            logger.info('Closed browser')
