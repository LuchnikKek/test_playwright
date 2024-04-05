import asyncio


from playwright.async_api import BrowserContext

from crawler.src.core.browser import browser_context
from crawler.src.core.config import *
from src.utils.bounded_task_group import BoundedTaskGroup


async def parse(browser: BrowserContext, channel_link: str):

    page = await browser.new_page()

    await page.goto(channel_link, wait_until='load')
    await page.wait_for_timeout(PAGE_ADDITIONAL_LOADING_TIME_MS)
    # await wait_func(page)

    selectors = page.locator('css=a#thumbnail[href^="/watch?v="]')
    count = await selectors.count()
    hrefs = {await selectors.nth(i).get_attribute('href') for i in range(count)}

    logger.info('All count: %s. Unique: %s.' % (count, len(hrefs)))

    await page.close()


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
