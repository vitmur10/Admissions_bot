import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from asgiref.sync import sync_to_async

import keybord
from Const import *

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Introfon.settings')
application = get_wsgi_application()
from question_answer.models import Question
from analytics.views import analytics


# Initialize bot and dispatcher
class FSMQuestion(StatesGroup):
    text = State()


class Admin_ansver(StatesGroup):
    text = State()
    id_user = State()


class Add_mfaq(StatesGroup):
    text = State()
    answer = State()


faculty_id = None


# Обработчики

@dp.message_handler(state=Add_mfaq.text, content_types=['text'])
async def add_most_frequently_asked_questions(message: aiogram.types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text

        a = Question.objects.all()

        await sync_to_async(a.create)(text=data['text'], answer=data['answer'], type='Найчастіші запитання', faculty_id=1)


@dp.message_handler(state=FSMQuestion.text, content_types=['photo', 'text'])
async def newquestion(message: aiogram.types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Назад":
            await message.answer("Окей", reply_markup=keybord.keyboard_menu)
            await state.finish()
        else:
            if message.content_type == 'photo':
                data['text'] = message.caption
            else:
                data['text'] = message.text
            await state.finish()
            if message.chat.username is None:
                who = "Ім'я користувача не встановлено"
            else:
                who = "@" + message.chat.username
            c = message.chat.id
            add_most_frequently_asked_questions_button = aiogram.types.InlineKeyboardButton(text=f" Додати у "
                                                                                                 f"найчастіші "
                                                                                                 f"запитання",
                                                                                            callback_data="add_most_frequently_asked_questions")
            button_answer = aiogram.types.InlineKeyboardButton(text=f" Відповісти для {who}", callback_data=c)
            keyboard_answer = aiogram.types.InlineKeyboardMarkup().add(button_answer).add(
                add_most_frequently_asked_questions_button)
            if message.content_type == 'photo':
                ph = message.photo[0].file_id
                await message.reply(f"{cfg['question_ur_question_sended_message']}")
                await bot.send_photo(cfg['teh_chat_id'], ph,
                                     caption=f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}",
                                     reply_markup=keyboard_answer)
            else:
                await message.reply(f"{cfg['question_ur_question_sended_message']}", reply_markup=keybord.keyboard_menu)
                await bot.send_message(cfg['teh_chat_id'],
                                       f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}",
                                       reply_markup=keyboard_answer)


@dp.message_handler(state=Admin_ansver.text, content_types=['photo', 'text'])
async def newquestion(message: aiogram.types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            if message.content_type == 'photo':
                data['text'] = message.caption
            else:
                data['text'] = message.text
        await state.finish()
        await bot.send_message(data.get('id_user'),
                               f"✉ Нове повідомлення!\nВідповідь від технічної підтримки:\n\n{data['text']}")
        await message.reply('✅ Ви успішно відповіли на запитання!')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}")
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")


@dp.message_handler(commands=['start'])
@analytics
async def hello(message: aiogram.types.Message):
    await message.answer(cfg['welcome_message'],
                         reply_markup=keybord.menu_faculty)


@dp.message_handler(commands=['getchatid'])
async def client_getgroupid(message: aiogram.types.Message):
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*")
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}")
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")


@dp.message_handler(content_types=['text'])
@analytics
async def answer_to_the_question(message: aiogram.types.Message):
    global faculty_id
    if message.text == cfg['button_new_question']:
        try:
            button_back = aiogram.types.KeyboardButton("Назад")
            keybord_back = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)
            await message.answer(f"{cfg['question_type_ur_question_message']}", reply_markup=keybord_back)
            await FSMQuestion.text.set()
        except Exception as e:
            cid = message.chat.id
            await message.answer(f"{cfg['error_message']}")
            await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")
    if message.text == 'Найчастіші запитання':
        await message.answer('Ось перелік найчастіших запитань...',
                             reply_markup=keybord.create_inline_keyboard(message.text, faculty_id))
    elif message.text == 'Фінанси':
        await message.answer('Ось перелік питань які стосуються фінансів...',
                             reply_markup=keybord.create_inline_keyboard(message.text, faculty_id))
    elif message.text == 'Питання щодо навчання':
        await message.answer('Ось перелік питань які стосуються навчання...',
                             reply_markup=keybord.create_inline_keyboard(message.text, faculty_id))
    elif message.text == 'Питання щодо вступу':
        await message.answer('Ось перелік питань які стосуються вступу...',
                             reply_markup=keybord.create_inline_keyboard(message.text, faculty_id))
    elif message.text == 'Змінити факультет':
        await message.answer('Ось перелік факультетів',
                             reply_markup=keybord.menu_faculty)
    for id, name, social_media_link, website_link in cur.execute(
            "SELECT id ,name, social_media_link, website_link  FROM question_answer_faculty"):
        if message.text == name:
            faculty_id = id
            await message.answer(f"""{name}\nСоціальні мережі\n{social_media_link}Сайт- {website_link}""",
                                 reply_markup=keybord.keyboard_menu)


def extract_arg(arg):
    return arg.split()[1:]


@dp.callback_query_handler(lambda c: True)
async def admin_ot(callback_query: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.message.chat.id == cfg['teh_chat_id']:
        if callback_query.data == "c":
            await callback_query.message.answer(f"Напишіть відповідь")
            async with state.proxy() as data:
                data['id_user'] = callback_query.data
            await Admin_ansver.text.set()
        elif callback_query.data == "add_most_frequently_asked_questions":
            await callback_query.message.answer(f"Напишіть відповідь")
            message_index = callback_query.message.text.find('Питання:')
            message = callback_query.message.text[message_index + len("Питання:'"):]
            async with state.proxy() as data:
                data['text'] = message
            await Add_mfaq.text.set()
    else:
        for reply in cur.execute("SELECT answer FROM question_answer_Question WHERE text = ?",
                                 (callback_query.data,)):
            await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                                f"{q}\n"
                                                                f"{reply[0]}")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
