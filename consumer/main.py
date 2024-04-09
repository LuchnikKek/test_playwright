import asyncio

import aio_pika
import msgspec


async def on_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Обработчик сообщений."""
    async with message.process():
        msg_body = msgspec.json.decode(message.body)
        print("Received message body: %s" % msg_body)

        msg_headers = message.headers
        print("Received message headers: %s" % msg_headers)


async def main() -> None:
    """Функция запуска Consumer'а сообщений."""
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    channel = await connection.channel()
    queue = await channel.declare_queue('video_ids', durable=True)
    await queue.consume(callback=on_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
