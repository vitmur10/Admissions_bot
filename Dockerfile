# Використовуємо базовий образ Python
FROM python:3.11

# Встановлюємо залежності
RUN apt-get update && apt-get install -y \
    build-essential \
    git && \
    pip install \
    Django \
    python-dotenv \
    aiogram \
    asyncio \
    psycopg2


# Копіюємо код у контейнер
WORKDIR /usr/src/app

COPY . /usr/src/app/



# Вказуємо порт, який відкривається для доступу до додатку
EXPOSE 8000

# Вказуємо команду для запуску додатку
CMD ["bash", "-c","python manage.py makemigrations & python manage.py migrate & python manage.py runserver 0.0.0.0:8000 & python main.py"]
