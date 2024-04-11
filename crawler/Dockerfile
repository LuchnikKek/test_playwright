FROM python:3.11-bookworm as build

WORKDIR /opt/crawler
ENV PATH /opt/crawler/.venv/bin/:$PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd curl

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir playwright==1.42.0 poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi \
    && playwright install --with-deps

COPY . .

RUN chmod +x /opt/crawler/entrypoint.sh

ENTRYPOINT ["/opt/crawler/entrypoint.sh"]