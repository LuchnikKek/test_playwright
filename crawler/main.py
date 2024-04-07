import asyncio

from playwright.async_api import TimeoutError, Page

from crawler.src.core.browser import browser_context
from crawler.src.core.config import settings, logger
from crawler.src.scraper import scrape_video_ids


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
        logger.info(ids)
        queue_in.task_done()


async def main():
    links = [
        'https://www.youtube.com/@raily',
        "https://www.youtube.com/@adorplayer",
        "https://www.youtube.com/@soderlingoc",
        "https://www.youtube.com/@sodyan",
        "https://www.youtube.com/@restlgamer",
        "https://www.youtube.com/@drozhzhin",
        "https://www.youtube.com/@empatia_manuchi",
        "https://www.youtube.com/@barsikofficial",
        "https://www.youtube.com/@diodand",
        "https://www.youtube.com/@nedohackerslite",
    ]

    input_queue = asyncio.Queue()
    for link in links:
        input_queue.put_nowait(link)

    output_queue = asyncio.Queue()

    async with browser_context() as browser:
        async with asyncio.TaskGroup() as tg:
            for i in range(settings.browser.MAX_PAGES):
                page_workers = [tg.create_task(worker(await browser.new_page(), input_queue, output_queue))]

    await input_queue.join()


if __name__ == '__main__':
    asyncio.run(main())
