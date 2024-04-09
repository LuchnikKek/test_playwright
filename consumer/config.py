import logging
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH: Path = Path(__file__).parent.parent
ENV_PATH: Path = ROOT_PATH / ".env"


class _PostgresSettings(BaseSettings):
    """Конфиг PostgreSQL."""
    DB: str
    USER: str
    PASS: str
    HOST: str
    PORT: int
    VIDEOS_TABLE: str

    @computed_field
    @property
    def DSN(self) -> str:  # noqa
        """Строка подключения. Пример: 'postgres://user:password@host:port/database'."""
        return f'postgres://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.DB}'

    model_config = SettingsConfigDict(env_prefix='PG_', env_file=ENV_PATH, extra='ignore')


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

        return f'amqp://{self.USER}:{self.PASS}@{self.HOST}/'

    model_config = SettingsConfigDict(env_prefix='RABBIT_', env_file=ENV_PATH, extra='ignore')


class _LoggerSettings(BaseSettings):
    """Конфиг Логгера."""
    FORMAT: str
    LEVEL: str

    model_config = SettingsConfigDict(env_prefix='LOG_', env_file=ENV_PATH, extra='ignore')


class _Settings(BaseSettings):
    """
    Основной конфиг приложения.
    Получение через экземпляр settings.
    """
    postgres: _PostgresSettings = _PostgresSettings()
    logger: _LoggerSettings = _LoggerSettings()
    rabbit: _RabbitSettings = _RabbitSettings()

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')


settings = _Settings()

logger = logging.getLogger('consumer')
logging.basicConfig(format=settings.logger.FORMAT, level=settings.logger.LEVEL)

logger.info(settings)
