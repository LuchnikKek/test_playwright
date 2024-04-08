import asyncio

import aio_pika

from crawler.src.core.browser import browser_context
from crawler.src.core.config import settings
from crawler.src.worker import worker
from crawler.write_links import send_links


async def main():
    input_queue = asyncio.Queue()
    send_links(input_queue)

    rabbit_connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    async with browser_context() as browser, asyncio.TaskGroup() as tg, rabbit_connection:
        for i in range(settings.browser.MAX_PAGES):
            page = await browser.new_page()
            channel = await rabbit_connection.channel()
            tg.create_task(worker(page, input_queue, channel))

    await input_queue.join()


if __name__ == '__main__':
    asyncio.run(main())
