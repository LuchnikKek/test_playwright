import asyncio

import aio_pika
import msgspec

from config import settings
from database.loader import init_db, load_to_db


async def on_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Обработчик сообщений."""
    async with message.process():
        username: str = message.headers.get('username')
        video_ids: list[str] = msgspec.json.decode(message.body)

    await load_to_db(username, video_ids)


async def main() -> None:
    """Точка входа загрузчика сообщений из топика в базу."""
    await init_db()

    rabbit_conn = await aio_pika.connect_robust(settings.rabbit.DSN)
    rabbit_channel = await rabbit_conn.channel()

    queue = await rabbit_channel.declare_queue(settings.rabbit.TOPIC, durable=True)
    await queue.consume(callback=on_message)

    try:
        await asyncio.Future()
    finally:
        await rabbit_conn.close()


if __name__ == "__main__":
    asyncio.run(main())
