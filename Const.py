import aiogram
import psycopg2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

cfg = {
    'token': '6075826339:AAF-yGH627OMzQcZAQuQes0PC3K3dB3PUd4',
    'teh_chat_id': -842742159,
    'db_name': 'Infotron_bd',  # Замініть на ім'я вашої PostgreSQL бази даних
    'db_user': 'vitmur',  # Замініть на користувача PostgreSQL бази даних
    'db_password': 'uaknutd',  # Замініть на пароль користувача PostgreSQL бази даних

    'button_new_question': '✉ Поставити питання',
    'welcome_message': "Вітаю, майбутній вступнику КНУТД❗️🧑‍🎓\n"
                       "Вступ на 1 курс завжди тривожний📚\n"
                       "І щоб бути впевненим в обраному шляху, завжди виникає безліч запитань💭\n"
                       "Тут ти знайдеш необхідну інформацію, яка допоможе тобі отримати відповіді на найпоширеніші "
                       "запитання🔍\n "
                       "\n"
                       "P.S. Якщо виникнуть питання, на які не знайдеш відповідь, напиши його сюди👇🏻",
    'error_message': 'Упс! Помилка! Не хвилюйтеся, помилку вже відправлено розробникам.',
    'ban_message': '⚠ Ви заблоковані в боті!',
    'question_type_ur_question_message': '📝 Введіть своє запитання (можна додати фото):',
    'question_ur_question_sended_message': '✉ Ваш запит був відправлений! Очікуйте відповіді від служби підтримки.',
}

bot = aiogram.Bot(token=cfg['token'])

# Змінено підключення до PostgreSQL
con = psycopg2.connect(
    dbname=cfg['db_name'],
    user=cfg['db_user'],
    password=cfg['db_password'],
    host='infotron_postgres',  # Залиште як є, оскільки це ім'я сервісу з Docker Compose
    port='5432'  # Залиште як є, порт за замовчуванням для PostgreSQL
)
cur = con.cursor()
order = {}
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)

q = '*' * 30
cur.execute("SELECT id FROM cafe_order")
try:
    max_id = cur.fetchone()[0]  # Отримати максимальне значення id
except TypeError:
    max_id = 0
dict_order = {'my_basket': f"Ось список товарів у вашому кошику:\n{', '.join([f'{key} - {cost}' for key, cost in order.items()])}",
              'confirm_order': f"""Номер замовлення {max_id + 1} заберіть і оплатіть його у кафе""" if len(
                  order) > 0 else f"Виберіть продукти",
              }

dict_answer = {'Найчастіші запитання': 'Ось перелік найчастіших запитань...',
               'Фінанси': 'Ось перелік питань які стосуються фінансів...',
               'Питання щодо навчання': 'Ось перелік питань які стосуються навчання...',
               'Питання щодо вступу': 'Ось перелік питань які стосуються вступу...'}
