import asyncio

import aio_pika

from crawler.src.core.browser import browser_context
from crawler.src.core.config import settings
from crawler.src.worker import worker
from crawler.write_links import send_links


async def main():
    input_queue = asyncio.Queue()
    send_links(input_queue)

    rabbit_connection = await aio_pika.connect_robust(settings.rabbit.DSN)

    async with rabbit_connection.channel() as channel:
        async with browser_context() as browser:
            async with asyncio.TaskGroup() as tg:
                for i in range(settings.browser.MAX_PAGES):
                    page = await browser.new_page()

                    tg.create_task(worker(page, input_queue, channel))

    await input_queue.join()


if __name__ == '__main__':
    asyncio.run(main())
