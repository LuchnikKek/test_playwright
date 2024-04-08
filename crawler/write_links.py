import asyncio

links = [
    'https://www.youtube.com/@raily',
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


def send_links(queue: asyncio.Queue):
    for link in links:
        queue.put_nowait(link)
