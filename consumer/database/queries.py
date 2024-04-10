__all__ = [
    "CREATE_VIDEOS_TABLE",
    "CREATE_UPDATE_FUNCTION",
    "CREATE_VIDEOS_TABLE_TRIGGER",
    "CREATE_TEMP_TABLE",
    "INSERT_TEMP_TABLE_TO_MAIN",
]

"""
Базовая таблица
"""
CREATE_VIDEOS_TABLE = """
    CREATE TABLE IF NOT EXISTS videos (
        video_id VARCHAR(12) NOT NULL PRIMARY KEY,
        channel_username VARCHAR(50) NOT NULL,
        video_href VARCHAR(50) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
"""

"""
Создание триггера для поля `updated_at`
"""
CREATE_UPDATE_FUNCTION = """
    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
"""
CREATE_VIDEOS_TABLE_TRIGGER = """
    CREATE OR REPLACE TRIGGER set_timestamp
    BEFORE UPDATE ON videos
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_timestamp();
"""

"""
Временная таблица для вставки данных.
"""
CREATE_TEMP_TABLE = """
    CREATE TEMPORARY TABLE IF NOT EXISTS _temp_table (
        video_id VARCHAR(12), 
        channel_username VARCHAR(50), 
        video_href VARCHAR(50)
    )
"""

INSERT_TEMP_TABLE_TO_MAIN = """
    INSERT INTO videos (video_id, channel_username, video_href)
    SELECT * FROM _temp_table
    ON CONFLICT (video_id) DO NOTHING 
"""
