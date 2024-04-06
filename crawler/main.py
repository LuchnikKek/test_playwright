import asyncio

from crawler.src.core.browser import browser_context
from crawler.src.core.config import *
from crawler.src.scraper import scrape_video_links
from src.utils.bounded_task_group import BoundedTaskGroup


async def main():
    links = ['https://www.youtube.com/@raily']

    async with browser_context() as browser, BoundedTaskGroup(max_tasks=settings.browser.MAX_PAGES) as tg:
        results = [tg.create_task(scrape_video_links(browser, link)) for link in links]

    logger.info("Все задачи завершены. Количество: %s." % len(results))


if __name__ == '__main__':
    asyncio.run(main())
