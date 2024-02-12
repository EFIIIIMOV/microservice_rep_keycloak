FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_order

# Установка зависимостей проекта
COPY ./requirements.txt /app_order/
RUN pip install --no-cache-dir --upgrade -r /app_order/requirements.txt

# Перенос проекта в образ
COPY ./app /app_order/app
COPY .env /app_order

# Копирование файлов alembic
COPY ./migration /app_order/migration
COPY ./alembic.ini /app_order/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80"]

