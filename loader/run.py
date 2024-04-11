import asyncio

import aio_pika
import asyncpg
import msgspec

from config import settings
from database.loader import load_to_db


async def on_message(message: aio_pika.abc.AbstractIncomingMessage, pool: asyncpg.Pool) -> None:
    """Обработчик сообщений."""
    async with message.process():
        username: str = message.headers.get("username")
        video_ids: list[str] = msgspec.json.decode(message.body)

    await load_to_db(pool, username, video_ids)


async def run() -> None:
    """Точка входа загрузчика сообщений из топика в базу."""
    db_pool = await asyncpg.create_pool(dsn=settings.postgres.DSN, min_size=1, max_size=settings.MAX_WORKERS)

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
