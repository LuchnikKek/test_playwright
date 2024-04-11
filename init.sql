-- Таблица для хранения видео
CREATE TABLE IF NOT EXISTS videos
(
    video_id         VARCHAR(12) NOT NULL PRIMARY KEY,
    channel_username VARCHAR(50) NOT NULL,
    video_href       VARCHAR(50) NOT NULL UNIQUE,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);


-- Функция, вызываемая триггером при обновлении записи (актуализирует updated_at)
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS
$$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Триггер, вызываемый при обновлении записи
CREATE OR REPLACE TRIGGER set_timestamp
    BEFORE UPDATE
    ON videos
    FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();
