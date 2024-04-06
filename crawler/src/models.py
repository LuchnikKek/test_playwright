import msgspec


class VideoRecord(msgspec.Struct):
    """Структура для передачи данных из Crawler."""

    video_id: list[str]
    channel_username: str
