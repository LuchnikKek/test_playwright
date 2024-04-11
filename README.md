# Тестовое задание (Playwright, RabbitMQ)

Парсер видео с каналов YouTube.

Стек:
- Python 3.11.
- Управление браузером: Playwright (асинхронный api).
- Хранилище: PostgreSQL (asyncpg).
- Брокер очередей: RabbitMQ (aio-pika).
- Запуск: Docker, Docker-compose.
- pydantic-settings, msgspec.
- Управление зависимостями: Poetry.
- Линтер, форматтер: ruff.


## Краткое описание

Архитектурно система делится на два компонента: **Crawler** и **Loader**.

**Crawler** (Сборщик) получает данные с YouTube и записывает их в Rabbit.

**Loader** (Загрузчик) читает данные из очереди и записывает в PostgreSQL.

Чтение и запись поддерживается в любом количестве вкладок (параметр **BROWSER_MAX_WORKERS**).
Он же отвечает за максимальное количество соединений в пуле PostgreSQL.

## Системные ограничения

Playwright поддерживает работу в докере **ТОЛЬКО** в **Headless** режиме. 
Для его включения параметр **BROWSER_HEADLESS** должен быть **True**.

## Quickstart

**Headless** (без браузерного окна):
1. `mv .env.template .env`
2. `docker compose up`
3. Долго-долго ждать. Playwright устанавливается в образ Докера около 3 минут.

**Headful** (с браузерным окном):
1. `mv .env.template .env`
2. Запустить loader командой `docker compose up loader_app`. В консоли будет сообщение 
3. Открыть **.env**. Выставить: 
   - `BROWSER_HEADLESS=False`
   - `PG_HOST=localhost`
   - `RABBIT_HOST=localhost`
4. Установить зависимости через poetry: `poetry install --no-root`
5. Установить playwright: `playwright install`
6. Запустить Crawler: `poetry run crawler/run.py`

## Изменение списка ссылок на каналы

Список ссылок можно посмотреть в [write_links.py](crawler%2Fwrite_links.py).
С причинами отсутствия гибкой конфигурации списка ссылок можно ознакомиться там же.
