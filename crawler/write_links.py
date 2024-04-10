"""
Модуль, записывающий в очередь ссылки на каналы.

Это тестовое задание, поэтому я не стал заморачиваться с появлением ссылок в системе.

Этот скрипт вне директории `src/`, чтобы подчеркнуть:
_в рамках тестового появление ссылок на каналы в очереди не важно и не является частью системы_.
Важнее то, что в `run.py` у нас уже есть некоторая очередь, из которой мы их читаем.

Будь это production решение, ссылки вводились бы в систему каким-то иным, корректным способом.
"""

import asyncio

links = [
    "https://www.youtube.com/@raily",
    "https://www.youtube.com/@adorplayer",
    "https://www.youtube.com/@soderlingoc",
    "https://www.youtube.com/@sodyan",
    "https://www.youtube.com/@restlgamer",
    "https://www.youtube.com/@drozhzhin",
    "https://www.youtube.com/@empatia_manuchi",
    "https://www.youtube.com/@barsikofficial",
    "https://www.youtube.com/@diodand",
    "https://www.youtube.com/@nedohackerslite",
]


def send_links(queue: asyncio.Queue) -> None:
    """Записывает ссылки на канал в очередь.

    Args:
        queue: Очередь, в которую записываются ссылки.
    """
    for link in links:
        queue.put_nowait(link)
