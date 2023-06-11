import aiogram
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage

cfg = {
    'token': '6075826339:AAF-yGH627OMzQcZAQuQes0PC3K3dB3PUd4',
    'teh_chat_id': -919047324,
    'db_name': 'Introfon/db.sqlite3',

    'button_new_question': '✉ Поставити питання',

    'welcome_message': "Вітаю, майбутній вступнику КНУТД❗️🧑‍🎓\n"
                         "Вступ на 1 курс завжди тривожний📚\n"
                         "І щоб бути впевненим в обраному шляху, завжди виникає безліч запитань💭\n"
                         "Тут ти знайдеш необхідну інформацію, яка допоможе тобі отримати відповіді на найпоширеніші запитання🔍\n"
                         "\n"
                         "P.S. Якщо виникнуть питання, на які не знайдеш відповідь, напиши його сюди👇🏻",
    'error_message': 'Упс! Помилка! Не хвилюйтеся, помилку вже відправлено розробникам.',
    'ban_message': '⚠ Ви заблоковані в боті!',
    'question_type_ur_question_message': '📝 Введіть своє запитання (можна додати фото):',
    'question_ur_question_sended_message': '✉ Ваш запит був відправлений! Очікуйте відповіді від служби підтримки.',
}
bot = aiogram.Bot(token=cfg['token'])


con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)

q = ('*' * 30)
