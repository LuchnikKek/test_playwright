import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH: Path = Path(__file__).parent.parent.parent.parent
ENV_PATH: Path = ROOT_PATH / ".env"


class _BrowserSettings(BaseSettings):
    HEADLESS: bool
    MAX_PAGES: int
    PAGE_ADDITIONAL_LOADING_TIME_MS: int
    VIEWPORT_WIDTH: int
    VIEWPORT_HEIGHT: int
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    USERAGENT: str
    REQUEST_ABORTION_CODE: str

    model_config = SettingsConfigDict(env_prefix='BROWSER_', env_file=ENV_PATH, extra='ignore')


class _LoggerSettings(BaseSettings):
    FORMAT: str
    LEVEL: str

    model_config = SettingsConfigDict(env_prefix='LOG_', env_file=ENV_PATH, extra='ignore')


class _Settings(BaseSettings):
    """
    Основной конфиг приложения.
        browser - настройки браузера.
        logger - настройки логгера.
    Получение через экземпляр settings.
    """
    browser: _BrowserSettings = _BrowserSettings()
    logger: _LoggerSettings = _LoggerSettings()

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')


settings = _Settings()

logger = logging.getLogger('crawler')
logging.basicConfig(format=settings.logger.FORMAT, level=settings.logger.LEVEL)
