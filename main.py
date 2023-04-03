from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import keybord
from Const import *


# Initialize bot and dispatcher
class FSMQuestion(StatesGroup):
    text = State()


# Обработчики
@dp.message_handler(state=FSMQuestion.text, content_types=['photo', 'text'])
async def newquestion(message: aiogram.types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['text'] = message.caption
        else:
            data['text'] = message.text
    await state.finish()
    if message.chat.username is None:
        who = "Ім'я користувача не встановлено"
    else:
        who = "@" + message.chat.username
    if message.content_type == 'photo':
        ph = message.photo[0].file_id
        await message.reply(f"{cfg['question_ur_question_sended_message']}",
                            parse_mode='Markdown')
        await bot.send_photo(cfg['teh_chat_id'], ph,
                             caption=f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}\n\n📝 Щоб відповісти "
                                     f"на запитання, введіть /відповідь {message.chat.id} Ваша відповідь",
                             parse_mode='Markdown')
    else:
        await message.reply(f"{cfg['question_ur_question_sended_message']}",
                            parse_mode='Markdown')
        await bot.send_message(cfg['teh_chat_id'],
                               f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}\n\n📝 Щоб відповісти "
                                     f"на запитання, введіть /відповідь {message.chat.id} Ваша відповідь",
                               parse_mode='Markdown')


def analytics(func: callable):
    total_messages = 0
    users = set()
    total_users = 0

    def analytics_wrapper(message):
        nonlocal total_messages, total_users
        total_messages += 1

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
    await message.answer(cfg['welcome_message'],
                         reply_markup=keybord.keyboard_menu)


@dp.message_handler(commands=['getchatid'])
async def client_getgroupid(message: aiogram.types.Message):
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*",
                             parse_mode='Markdown')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}",
                             parse_mode='Markdown')
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}",
                               parse_mode='Markdown')


@dp.message_handler(commands=['відповідь'])
async def admin_ot(message: aiogram.types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) >= 2:
            chatid = str(args[0])
            args.pop(0)
            answer = ""
            for ot in args:
                answer += ot + " "
            await message.reply('✅ Ви успішно відповіли на запитання!')
            await bot.send_message(chatid, f"✉ Нове повідомлення!\nВідповідь від технічної підтримки:\n\n{answer}",
                                   parse_mode='Markdown')
            return
        else:
            await message.reply('⚠ Вкажіть аргументи команди\nПриклад: /відповідь 516712732 Ваша відповідь',
                                parse_mode='Markdown')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}",
                             parse_mode='Markdown')
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}",
                               parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
@analytics
async def answer_to_the_question(message: aiogram.types.Message):
    try:
        if message.text == cfg['button_new_question']:
            await message.answer(f"{cfg['question_type_ur_question_message']}")
            await FSMQuestion.text.set()
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}",
                             parse_mode='Markdown')
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}",
                               parse_mode='Markdown')
    if message.text == 'Найчастіші запитання':
        await message.answer('Ось перелік найчастіших запитань...', reply_markup=keybord.mfaq)
    elif message.text == 'Фінанси':
        await message.answer('Ось перелік питань які стосуються фінансів...', reply_markup=keybord.finansy)
    elif message.text == 'Питання щодо навчання':
        await message.answer('Ось перелік питань які стосуються навчання...', reply_markup=keybord.regarding_training)
    elif message.text == 'Приймальна комісія':
        await message.answer('Ось перелік питань які стосуються примальної комісії...', reply_markup=keybord.admissions)


def extract_arg(arg):
    return arg.split()[1:]


@dp.callback_query_handler(lambda c: c.data == 'Specialty_FMKT')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute(
            "SELECT reply  FROM reply WHERE question = 'За якими спеціальностями відбувається набір?'"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'the_cost_of_the_hostel')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute(
            "SELECT reply  FROM reply WHERE question = 'Вартість проживання у гуртожитку 2022/2023 н.р. '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'documents')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Які потрібні документи для вступу? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'documents')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Умови вступу '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'terms_of_study')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Терміни навчання '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'tuition_fee')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply FROM reply WHERE question = 'Вартість навчання (денна/заочна) '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'faculty_dormitory')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Гуртожиток факультету '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'renewal')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Поновлення'"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'deduction')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Відрахування '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'email')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Електронна адреса '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'time')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Час роботи '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'location')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де знаходиться? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'academic_certificate')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Академічна довідка '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'student_id')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Студентський квиток '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'where_are_the_documents')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute(
            "SELECT reply  FROM reply WHERE question = 'Де знаходяться оригінали документів, на підставі яких Ви вступали до університету? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'wocftc')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute(
            "SELECT reply  FROM reply WHERE question = 'Де замовити довідку у територіальні центри комплектування та соціальної підтримки (ТЦК та СП, військкомат), форма 20 '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'wahtoac')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де і як замовити довідку? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'wFMKTdo')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де знаходиться деканат Факультету МКТ? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


@dp.callback_query_handler(lambda c: c.data == 'parents_must_be_present')
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT reply  FROM reply WHERE question = 'Де знаходиться деканат Факультету МКТ? '"):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"Якщо вступнику немає 18 так")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
