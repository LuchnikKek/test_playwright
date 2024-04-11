import asyncio

import aio_pika
import msgspec
from aio_pika.abc import AbstractRobustChannel
from playwright.async_api import Page, TimeoutError

from src.components.scraper import scrape_video_ids
from src.core.config import settings, logger
from src.utils.parse_username import parse_username


async def worker(page: Page, queue_in: asyncio.Queue, output_channel: AbstractRobustChannel) -> None:
    """Воркер, непрерывно достающий ID видео по ссылке на канал.

    Основная рабочая единица Crawler (Сборщика).

    Бесконечно вычитывает входную очередь со ссылками на каналы.
    При получении ссылки открывает канал и получает список из всех video_id.
    Отправляет сообщение в выходную очередь.
    В конце сигнализирует входной очереди, что завершил с текущей ссылкой.

    Args:
        page: Объект страницы, на которой воркер будет открывать ссылки.
        queue_in: Асинхронная входная очередь со ссылками на каналы. В текущей реализации простая asyncio.Queue.
        output_channel: Асинхронная выходная очередь. В текущей реализации канал в RabbitMQ.
    """
    while True:
        channel_link = await queue_in.get()
        try:
            await page.goto(channel_link)
        except TimeoutError:
            pass
        await page.wait_for_timeout(settings.browser.PAGE_ADDITIONAL_LOADING_TIME_MS)

        video_ids = await scrape_video_ids(page)

        msg = _create_message(channel_link, video_ids)
        await output_channel.default_exchange.publish(msg, routing_key=settings.rabbit.TOPIC)

        logger.info("По каналу %s получено %s ID." % (msg.headers.get("username"), len(video_ids)))
        queue_in.task_done()


def _create_message(channel_link: str, video_ids: list[str]) -> aio_pika.Message:
    """Формирует сообщение для отправки в брокер.

    Args:
        channel_link: Ссылка на YouTube канал.
        video_ids: Список id видео.

    Returns:
        aio_pika.Message: Сообщение для отправки в брокер.
    """
    return aio_pika.Message(
        headers={"username": parse_username(channel_link)},
        body=msgspec.json.encode(video_ids),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )
