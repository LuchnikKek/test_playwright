import database.queries as db_queries
from asyncpg import Pool
from config import logger


async def load_to_db(pool: Pool, username: str, video_ids: list[str]) -> None:
    columns = ["video_id", "channel_username", "video_href"]
    records = ((video_id, username, f"https://www.youtube.com/watch?v={video_id}") for video_id in video_ids)

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(db_queries.CREATE_VIDEOS_TEMP_TABLE)
            await connection.copy_records_to_table("_temp_videos_table", records=records, columns=columns)
            result = await connection.execute(db_queries.MERGE_VIDEOS_TEMP_TABLE_TO_MAIN)
        logger.debug(result)
