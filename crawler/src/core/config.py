import logging
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH: Path = Path(__file__).parent.parent.parent.parent
ENV_PATH: Path = ROOT_PATH / ".env"


class _BrowserSettings(BaseSettings):
    """Конфиг браузера для PlayWright."""

    HEADLESS: bool
    MAX_PAGES: int
    PAGE_ADDITIONAL_LOADING_TIME_MS: int
    VIEWPORT_WIDTH: int
    VIEWPORT_HEIGHT: int
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    USERAGENT: str
    REQUEST_ABORTION_CODE: str

    model_config = SettingsConfigDict(env_prefix="BROWSER_", env_file=ENV_PATH, extra="ignore")


class _RabbitSettings(BaseSettings):
    """Конфиг RabbitMQ."""

    USER: str
    PASS: str
    HOST: str
    TOPIC: str

    @computed_field
    @property
    def DSN(self) -> str:  # noqa
        """Строка подключения. Пример: 'amqp://guest:guest@localhost/'."""

        return f"amqp://{self.USER}:{self.PASS}@{self.HOST}/"

    model_config = SettingsConfigDict(env_prefix="RABBIT_", env_file=ENV_PATH, extra="ignore")


class _LoggerSettings(BaseSettings):
    """Конфиг логгера."""

    FORMAT: str
    LEVEL: str

    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=ENV_PATH, extra="ignore")


class _Settings(BaseSettings):
    """
    Основной конфиг приложения.
    Доступен через экземпляр settings.
    """

    browser: _BrowserSettings = _BrowserSettings()
    logger: _LoggerSettings = _LoggerSettings()
    rabbit: _RabbitSettings = _RabbitSettings()

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")


settings = _Settings()

logger = logging.getLogger("crawler")
logging.basicConfig(format=settings.logger.FORMAT, level=settings.logger.LEVEL)
