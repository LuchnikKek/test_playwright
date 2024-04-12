FROM python:3.11-bookworm as build

WORKDIR /opt/crawler

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd curl

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium --with-deps

COPY . .

RUN chmod +x /opt/crawler/entrypoint.sh

ENTRYPOINT ["/opt/crawler/entrypoint.sh"]