.PHONY: down up_loader up_crawler up_clean up local local_clean

# Очистка базы. Удаляет все контейнеры и Volume.
down:
	@docker compose down -v

# Запуск Loader (загрузчик распаршенных ссылок в базу).
up_loader:
	@docker compose up -d loader_app

# Запуск Crawler В ДОКЕРЕ.
up_crawler:
	@docker compose up -d crawler_app

# Запуск Crawler В ДОКЕРЕ и Loader в Докере С ОЧИСТКОЙ бд.
up_clean: down up_loader up_crawler
	@docker compose logs -f crawler_app loader_app

# Запуск Crawler В ДОКЕРЕ и Loader в Докере БЕЗ ОЧИСТКИ бд. \
Пойдёт по всем ссылкам с самого начала, но вставлять в базу будет только новые. \
Количество новых вставленных записей можно видеть в логах "MERGE 0 N".
up: up_loader up_crawler
	@docker compose logs -f crawler_app loader_app



# Запуск Crawler ЛОКАЛЬНО и Loader в Докере БЕЗ ОЧИСТКИ бд. \
Пойдёт по всем ссылкам с самого начала, но вставлять в базу будет только новые. \
Количество новых вставленных записей можно видеть в логах "MERGE 0 N".
local: up_loader
	poetry install --no-root -n --without=dev \
	&& playwright install \
	&& export RABBIT_HOST="localhost" \
	&& cd crawler \
	&& poetry run sh ./entrypoint.sh


# Запуск Crawler ЛОКАЛЬНО и Loader в Докере С ОЧИСТКОЙ бд.
local_clean: down local








