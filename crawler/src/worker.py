import asyncio

import aio_pika
import msgspec
from aio_pika.abc import AbstractRobustChannel
from playwright.async_api import Page, TimeoutError

from crawler.src.components.scraper import scrape_video_ids
from crawler.src.core.config import settings, logger
from crawler.src.utils.parse_username import parse_username


async def worker(page: Page, queue_in: asyncio.Queue, output_channel: AbstractRobustChannel):
    while True:
        channel_link = await queue_in.get()
        try:
            await page.goto(channel_link)
        except TimeoutError:
            pass
        await page.wait_for_timeout(settings.browser.PAGE_ADDITIONAL_LOADING_TIME_MS)

        video_ids = await scrape_video_ids(page)

        msg = aio_pika.Message(
            headers={'username': parse_username(channel_link)},
            body=msgspec.json.encode(video_ids),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await output_channel.default_exchange.publish(msg, routing_key=settings.rabbit.TOPIC)

        logger.info('По каналу %s получено %s ID.' % (msg.headers.get('username'), len(video_ids)))
        queue_in.task_done()
