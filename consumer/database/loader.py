import asyncpg
from asyncpg import Connection

import consumer.database.queries as qs
from consumer.config import settings, logger

db: Connection | None = None


async def init_db():
    """DDL-команды для инициализации базы данных."""
    global db
    db = await asyncpg.connect(settings.postgres.DSN)

    await db.execute(qs.CREATE_VIDEOS_TABLE)
    await db.execute(qs.CREATE_UPDATE_FUNCTION)
    await db.execute(qs.CREATE_VIDEOS_TABLE_TRIGGER)
    await db.execute(qs.CREATE_TEMP_TABLE)


async def load_to_db(username: str, video_ids: list[str]):
    columns = ["video_id", "channel_username", "video_href"]
    records = ((video_id, username, f"https://www.youtube.com/watch?v={video_id}") for video_id in video_ids)

    async with db.transaction():
        await db.copy_records_to_table("_temp_table", records=records, columns=columns)
        result = await db.execute(qs.INSERT_TEMP_TABLE_TO_MAIN)
        await db.execute("""TRUNCATE TABLE _temp_table""")

        logger.debug(result)
