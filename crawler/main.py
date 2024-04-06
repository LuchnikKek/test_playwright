import asyncio

from crawler.src.core.browser import browser_context
from crawler.src.core.config import settings, logger
from crawler.src.scraper import scrape_video_ids
from src.utils.bounded_task_group import BoundedTaskGroup


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

    async with browser_context() as browser:
        tasks = [scrape_video_ids(browser, link) for link in links]
        async with BoundedTaskGroup(max_tasks=settings.browser.MAX_PAGES) as tg:
            results = [tg.create_task(task) for task in tasks]

    logger.info("Все задачи завершены. Количество: %s." % len(results))


if __name__ == '__main__':
    asyncio.run(main())
