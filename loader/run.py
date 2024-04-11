import asyncio

import aio_pika
import asyncpg
import msgspec

from src.core.config import settings
from src.database.loader import load_to_db


async def on_message(message: aio_pika.abc.AbstractIncomingMessage, pool: asyncpg.Pool) -> None:
    """Функция обратного вызова для обработки сообщений.

    Args:
        message: Очередное сообщение.
        pool: Пул соединений с базой данных.
    """
    async with message.process():
        username: str = message.headers.get("username")
        video_ids: list[str] = msgspec.json.decode(message.body)

    await load_to_db(pool, username, video_ids)


async def run() -> None:
    """Точка входа Загрузчика сообщений из топика в базу.

    После открытия всех соединений, указывает Consumer'у очереди, callback-функцию on_message().
    Очередное сообщение вместе с пулом соединений будут поступать в этот callback.
    """
    db_pool = await asyncpg.create_pool(dsn=settings.postgres.DSN, min_size=1, max_size=settings.MAX_WORKERS + 1)

    rabbit_conn = await aio_pika.connect_robust(settings.rabbit.DSN)
    rabbit_channel = await rabbit_conn.channel()

    queue = await rabbit_channel.declare_queue(settings.rabbit.TOPIC, durable=True)

    await queue.consume(callback=lambda message: on_message(message, db_pool))

    try:
        await asyncio.Future()
    finally:
        await rabbit_conn.close()
        await db_pool.close()


if __name__ == "__main__":
    asyncio.run(run())
