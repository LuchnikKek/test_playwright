#!/bin/sh

wait_for_rabbit() {
    until nc -z "${RABBIT_HOST}" 5672; do
        echo "Ожидание доступности RabbitMQ..."
        sleep 1
    done
    echo "RabbitMQ доступен."
}

wait_for_rabbit

echo "Запуск Загрузчика..."
python run.py
