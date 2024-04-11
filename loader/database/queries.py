__all__ = [
    "CREATE_VIDEOS_TEMP_TABLE",
    "MERGE_VIDEOS_TEMP_TABLE_TO_MAIN",
]

CREATE_VIDEOS_TEMP_TABLE = """
    CREATE TEMP TABLE _temp_videos_table (
        video_id VARCHAR(12) NOT NULL UNIQUE, 
        channel_username VARCHAR(50) NOT NULL, 
        video_href VARCHAR(50) NOT NULL UNIQUE
    )
    ON COMMIT DROP;
"""
"""Создание временной таблицы для Видео."""

MERGE_VIDEOS_TEMP_TABLE_TO_MAIN = """ 
    MERGE INTO videos v
    USING _temp_videos_table t ON v.video_id = t.video_id
    WHEN NOT MATCHED THEN 
       INSERT (video_id, channel_username, video_href)
       VALUES(t.video_id, t.channel_username, t.video_href);
"""
"""Вставка уникальных значений из временной таблицы в основную."""
