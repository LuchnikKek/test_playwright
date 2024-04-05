import asyncio


from playwright.async_api import BrowserContext

from crawler.src.core.browser import browser_context
from crawler.src.core.config import *
from src.utils.bounded_task_group import BoundedTaskGroup


async def parse(browser: BrowserContext, channel_link: str) -> set[str]:
    """
    Парсит страницу канала и возвращает все уникальные ссылки на видео.
    :param browser: Объект браузера.
    :param channel_link: Ссылка на канал.
    :return: set() со всеми уникальными ссылками на странице канала.
    """
    page = await browser.new_page()

    await page.goto(channel_link, wait_until='load')
    await page.wait_for_timeout(PAGE_ADDITIONAL_LOADING_TIME_MS)

    selectors = page.locator('css=a#thumbnail[href^="/watch?v="]')
    hrefs = await selectors.evaluate_all("list => list.map(element => element.href)")
    unique_hrefs = {href for href in hrefs}

    logger.info('Refs count: %s. Unique: %s.' % (len(hrefs), len(unique_hrefs)))
    await page.close()
    return unique_hrefs


async def stub_task(browser: BrowserContext):
    page1 = await browser.new_page()
    await asyncio.sleep(5)
    await page1.close()


async def main():
    links = ['https://www.youtube.com/@raily']

    async with browser_context() as browser, BoundedTaskGroup(max_tasks=MAX_PAGES) as tg:
        results = [tg.create_task(parse(browser, link)) for link in links]

    logger.info("Все задачи завершены. Количество: %s." % len(results))


if __name__ == '__main__':
    asyncio.run(main())
