from playwright.async_api import Page

from crawler.src.core.config import logger


async def infinite_wait(page: Page):
    logger.info("INFINITE WAITING ENABLED!")
    while True:
        await page.wait_for_timeout(29000)
