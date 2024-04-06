class BaseCrawlerException(Exception):
    """Базовое исключение для модуля crawler."""


class ScrapingException(BaseCrawlerException):
    """Исключение, вызываемое при ошибках веб-скрапинга (Playwright)."""


class ParsingException(BaseCrawlerException):
    """Исключение, вызываемое при ошибках парсинга полученных данных."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Недопустимое значение для парсинга: %s" % self.value
