import asyncio

from playwright.async_api import Page, TimeoutError

from crawler.src.components.scraper import scrape_video_ids
from crawler.src.core.config import settings


async def worker(page: Page, queue_in: asyncio.Queue, queue_out: asyncio.Queue):
    while True:
        channel_link = await queue_in.get()
        try:
            await page.goto(channel_link)
        except TimeoutError:
            pass
        await page.wait_for_timeout(settings.browser.PAGE_ADDITIONAL_LOADING_TIME_MS)
        ids = await scrape_video_ids(page, channel_link)

        queue_out.put_nowait(ids)
        queue_in.task_done()
