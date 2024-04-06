import re

from crawler.src.core.exceptions import ParsingException


async def parse_video_id(video_link: str) -> str | None:
    """
    Парсит ID видео из параметра в ссылке.
    Паттерн ищет query-параметр, который состоит из: ('?' или '&') + ('v=') + (буквы, цифры, '-', '_').

    :param video_link: Ссылка на видео.
    :return: Строковый ID видео без имени параметра.
    :raise ParsingException: Если ссылка не содержит ID для видео.
    """
    video_id = re.search('[?&]v=[A-z0-9-_]*', video_link)

    if not video_id:
        raise ParsingException(video_link)

    return video_id.group(0)[3:]
