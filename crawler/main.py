import asyncio

from playwright.async_api import TimeoutError

from crawler.src.core.browser import browser_context
from crawler.src.core.config import settings, logger
from crawler.src.scraper import scrape_video_ids


async def worker(queue_in, queue_out):
    async with browser_context() as browser:
        page = await browser.new_page()

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
    # async with browser_context() as browser:
    #     tasks = [scrape_video_ids(browser, link) for link in links]
    #     async with BoundedTaskGroup(max_tasks=settings.browser.MAX_PAGES) as tg:
    #         results = [tg.create_task(task) for task in tasks]
    # logger.info("Все задачи завершены. Количество: %s." % len(results))

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
    queue = asyncio.Queue()
    for link in links:
        queue.put_nowait(link)

    output_queue = asyncio.Queue()

    page_workers = []
    for i in range(settings.browser.MAX_PAGES):
        page_worker = asyncio.create_task(worker(queue, output_queue))

    await queue.join()


if __name__ == '__main__':
    asyncio.run(main())
