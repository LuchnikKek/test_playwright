import asyncio

from crawler.src.core.browser import browser_context
from crawler.src.core.config import settings
from crawler.src.worker import worker
from crawler.write_links import send_links


async def main():
    input_queue = asyncio.Queue()
    send_links(input_queue)

    output_queue = asyncio.Queue()

    async with browser_context() as browser, asyncio.TaskGroup() as tg:
        for i in range(settings.browser.MAX_PAGES):
            page_workers = [tg.create_task(worker(await browser.new_page(), input_queue, output_queue))]

    await input_queue.join()


if __name__ == '__main__':
    asyncio.run(main())
