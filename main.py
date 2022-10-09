import aiogram
import sqlite3
import keybord
from Const import TOKEN

# Initialize bot and dispatcher
bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot)

con = sqlite3.connect("bd")
cur = con.cursor()


def analytics(func: callable):
    total_messages = 0
    users =set()
    total_users = 0

    def analytics_wrapper(message):
            nonlocal total_messages, total_users
            total_messages +=1

            if message.chat.id not in users:
                users.add(message.chat.id)
                total_users += 1
            data = [
                (
                    total_users, message.text, total_messages
                 )
            ]
            cur.executemany("INSERT INTO analytics VALUES(?, ?, ?)", data)
            con.commit()
            return func(message)

    return analytics_wrapper


@dp.message_handler(commands=['start'])
@analytics
async def hello(message: aiogram.types.Message):
    await message.answer("Вітаю, майбутній вступнику КНУТД❗️🧑‍🎓\n"
                         "Вступ на 1 курс завжди тривожний📚\n"
                         "І щоб бути впевненим в обраному шляху, завжди виникає безліч запитань💭\n"
                         "Тут ти знайдеш необхідну інформацію, яка допоможе тобі отримати відповіді на найпоширеніші запитання🔍\n"
                         "\n"
                         "P.S. Якщо виникнуть питання, на які не знайдеш відповідь, напиши його сюди👇🏻", reply_markup=keybord.keyboard_menu)


@dp.message_handler(content_types=['text'])
@analytics
async def answer_to_the_question(message: aiogram.types.Message):
    if message.text == 'Найчастіші запитання':
        await message.answer('Ось перелік найчастіших запитань...', reply_markup=keybord.mfaq)
    elif message.text == 'Фінанси':
        await message.answer('Ось перелік питань які стосуються фінансів...', reply_markup=keybord.finansy)
    elif message.text == 'Питання щодо навчання':
        await message.answer('Ось перелік питань які стосуються навчання...', reply_markup=keybord.regarding_training)
    elif message.text == 'Приймальна комісія':
        await message.answer('Ось перелік питань які стосуються примальної комісії...', reply_markup=keybord.admissions)




if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
