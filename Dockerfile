# Використовуємо базовий образ Python
FROM python:3.11

# Встановлюємо залежності
RUN apt-get update && apt-get install -y \
    build-essential \
    git

# Встановлюємо необхідні бібліотеки
RUN pip install\
    Django \
    python-dotenv\
    aiogram\
    django-grappelli \
    asyncio

# Копіюємо код у контейнер
WORKDIR /usr/src/app
COPY . .

# Виконуємо міграції бази даних Django
RUN python Introfon/manage.py migrate

# Вказуємо порт, який відкривається для доступу до додатку
EXPOSE 8000

# Вказуємо команду для запуску додатку
CMD ["bash", "-c","python main.py & python Introfon/manage.py runserver"]
