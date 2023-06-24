# Dockerfile

# Устанавливаем базовый образ
FROM python:3.10
# import from .env APP_PORT
ARG APP_PORT

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости проекта в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код в рабочую директорию
COPY . /app

EXPOSE $APP_PORT

# Запускаем приложение
CMD ["python", "main.py"]