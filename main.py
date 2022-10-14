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


@dp.callback_query_handler(lambda c: c.data == 'Specialty_FMKT')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'За якими спеціальностями відбувається набір?'"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'the_cost_of_the_hostel')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Вартість проживання у гуртожитку 2022/2023 н.р. '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'documents')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Які потрібні документи для вступу? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'documents')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Умови вступу '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'terms_of_study')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Терміни навчання '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'tuition_fee')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply FROM reply WHERE question = 'Вартість навчання (денна/заочна) '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'faculty_dormitory')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Гуртожиток факультету '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'renewal')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Поновлення'"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'deduction')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Відрахування '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'email')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Електронна адреса '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'time')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Час роботи '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")



@dp.callback_query_handler(lambda c: c.data == 'location')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де знаходиться? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'academic_certificate')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Академічна довідка '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")



@dp.callback_query_handler(lambda c: c.data == 'student_id')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Студентський квиток '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")



@dp.callback_query_handler(lambda c: c.data == 'where_are_the_documents')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де знаходяться оригінали документів, на підставі яких Ви вступали до університету? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'wocftc')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де замовити довідку у територіальні центри комплектування та соціальної підтримки (ТЦК та СП, військкомат), форма 20 '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'wahtoac')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де і як замовити довідку? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")


@dp.callback_query_handler(lambda c: c.data == 'wFMKTdo')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де знаходиться деканат Факультету МКТ? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{reply}")

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
