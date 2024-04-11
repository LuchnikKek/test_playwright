import src.database.queries as db_queries
from src.core.config import logger

from asyncpg import Pool


async def load_to_db(pool: Pool, username: str, video_ids: list[str]) -> None:
    """Функция для асинхронной загрузки данных в базу.

    Получает соединение из Пула. В транзакции:
    1. Копирует записи во временную таблицу (использует binary COPY, поэтому работает быстро).
    2. Мёрджит (то же, что INSERT INTO) временную таблицу в оригинальную, добавляя только новые записи.
    3. Временная таблица создана с 'ON COMMIT DROP', так что автоматически удаляется после транзакции.

    Args:
        pool: Пул соединений к PostgreSQL.
        username: Имя пользователя владельца канала, начиная с символа "@".
        video_ids: Список ID видео. Только ID, без параметра "v=".
    """
    columns = ["video_id", "channel_username", "video_href"]
    records = ((video_id, username, f"https://www.youtube.com/watch?v={video_id}") for video_id in video_ids)

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(db_queries.CREATE_VIDEOS_TEMP_TABLE)
            await connection.copy_records_to_table("_temp_videos_table", records=records, columns=columns)
            result = await connection.execute(db_queries.MERGE_VIDEOS_TEMP_TABLE_TO_MAIN)
        logger.info(result)
