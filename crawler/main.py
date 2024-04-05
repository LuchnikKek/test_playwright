import asyncio


from playwright.async_api import Playwright, BrowserContext

from crawler.src.core.browser import browser_context
from crawler.src.core.config import *
from src.utils.bounded_task_group import BoundedTaskGroup


async def stub_task(browser: BrowserContext):
    page1 = await browser.new_page()
    await asyncio.sleep(5)
    await page1.close()


async def main():
    tasks = [stub_task, stub_task, stub_task, stub_task, stub_task, stub_task]
    async with browser_context() as browser, BoundedTaskGroup(max_tasks=4) as tg:
        results = [tg.create_task(task(browser)) for task in tasks]
    logger.info("Все задачи завершены. Количество: %s." % len(results))


if __name__ == '__main__':
    asyncio.run(main())
