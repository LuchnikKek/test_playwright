#!/bin/sh

wait_for_rabbit() {
    until nc -z "${RABBIT_HOST}" 5672; do
        echo "Crawler: Ожидание доступности RabbitMQ..."
        sleep 1
    done
    echo "Crawler: RabbitMQ доступен."
}

wait_for_rabbit

echo "Запуск Crawler'а..."
python run.py
