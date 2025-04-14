# Тестовое задание Avito

## Описание
API сервис для управления пунктами выдачи заказов (ПВЗ) и приёмки товаров.

## Технологии
- Python 3.12
- FastAPI
- PostgreSQL
- Docker
- Prometheus (для мониторинга)
- Pytest (для тестирования)

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd avito-test-spring
```

2. Переместиться в нужную папку
```bash
cd src
```

3. Для сборки проекта используется команда
```bash
docker compose up --build
```

4. Для остановки проекта
```bash
docker compose down -v
```