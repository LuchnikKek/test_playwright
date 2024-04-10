def parse_username(channel_link: str) -> str:
    """Парсит username из ссылки на канал."""

    return "@%s" % channel_link.partition("@")[2]
