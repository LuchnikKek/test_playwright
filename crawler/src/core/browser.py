from contextlib import asynccontextmanager

from playwright.async_api import Playwright, BrowserContext, async_playwright

from crawler.src.core.config import settings, logger


async def _headless_browser(playwright_context: Playwright) -> BrowserContext:
    _browser = await playwright_context.chromium.launch(args=['--headless=new'], headless=False)
    browser = await _browser.new_context(user_agent=settings.browser.USERAGENT)
    return browser


async def _headful_browser(playwright_context: Playwright) -> BrowserContext:
    _browser = await playwright_context.chromium.launch(args=['--start-maximized'], headless=False)
    browser = await _browser.new_context(
        user_agent=settings.browser.USERAGENT,
        viewport={'width': settings.browser.VIEWPORT_WIDTH, 'height': settings.browser.VIEWPORT_HEIGHT},
        screen={'width': settings.browser.SCREEN_WIDTH, 'height': settings.browser.SCREEN_HEIGHT},
    )
    return browser


@asynccontextmanager
async def browser_context() -> BrowserContext:
    async with async_playwright() as context:
        browser = await _headless_browser(context) if settings.browser.HEADLESS else await _headful_browser(context)
        try:
            logger.info('Открыл браузер.')
            yield browser
        finally:
            await browser.close()
            logger.info('Закрыл браузер.')
