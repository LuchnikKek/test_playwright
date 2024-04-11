import asyncio

import aio_pika

from src.core.browser import browser_context
from src.core.config import settings
from src.core.worker import worker
from write_links import send_links


async def run():
    """Точка входа сборщика данных по каналам."""
    input_queue = asyncio.Queue()
    send_links(input_queue)

    rabbit_connection = await aio_pika.connect_robust(settings.rabbit.DSN)

    async with rabbit_connection.channel() as channel:
        async with browser_context() as browser:
            async with asyncio.TaskGroup() as tg:
                for i in range(settings.browser.MAX_WORKERS):
                    page = await browser.new_page()

                    tg.create_task(worker(page, input_queue, channel))

    await input_queue.join()


if __name__ == "__main__":
    asyncio.run(run())
