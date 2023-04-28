from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import keybord
from Const import *


# Initialize bot and dispatcher
class FSMQuestion(StatesGroup):
    text = State()


class Admin_ansver(StatesGroup):
    text = State()
    id_user = State()


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
    c = message.chat.id
    button_ansver = aiogram.types.InlineKeyboardButton(text=f" Відповісти для {who}", callback_data=c)
    keyboard_ansver = aiogram.types.InlineKeyboardMarkup().add(button_ansver)
    if message.content_type == 'photo':
        ph = message.photo[0].file_id
        await message.reply(f"{cfg['question_ur_question_sended_message']}")
        await bot.send_photo(cfg['teh_chat_id'], ph,
                             caption=f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}",
                             reply_markup=keyboard_ansver)
    else:
        await message.reply(f"{cfg['question_ur_question_sended_message']}")
        await bot.send_message(cfg['teh_chat_id'],
                               f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}",
                               reply_markup=keyboard_ansver)


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
async def hello(message: aiogram.types.Message):
    await message.answer(cfg['welcome_message'],
                         reply_markup=keybord.keyboard_menu)


@dp.message_handler(commands=['getchatid'])
async def client_getgroupid(message: aiogram.types.Message):
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*")
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}")
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")


@dp.message_handler(content_types=['text'])
async def answer_to_the_question(message: aiogram.types.Message):
    try:
        if message.text == cfg['button_new_question']:
            await message.answer(f"{cfg['question_type_ur_question_message']}")
            await FSMQuestion.text.set()
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}")
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")
    if message.text == 'Найчастіші запитання':
        await message.answer('Ось перелік найчастіших запитань...',
                             reply_markup=keybord.create_inline_keyboard(message.text))
    elif message.text == 'Фінанси':
        await message.answer('Ось перелік питань які стосуються фінансів...',
                             reply_markup=keybord.create_inline_keyboard(message.text))
    elif message.text == 'Питання щодо навчання':
        await message.answer('Ось перелік питань які стосуються навчання...',
                             reply_markup=keybord.create_inline_keyboard(message.text))
    elif message.text == 'Приймальна комісія':
        await message.answer('Ось перелік питань які стосуються примальної комісії...',
                             reply_markup=keybord.create_inline_keyboard(message.text))


def extract_arg(arg):
    return arg.split()[1:]


@dp.callback_query_handler(lambda c: True)
async def admin_ot(callback_query: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.message.chat.id == cfg['teh_chat_id']:
        await callback_query.message.answer(f"Напишіть відповідь")
        async with state.proxy() as data:
            data['id_user'] = callback_query.data
        await Admin_ansver.text.set()
    else:
        for reply in cur.execute("SELECT answer FROM question_answer_Question WHERE text = ?",
                                 (callback_query.data,)):
            await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                                f"{q}\n"
                                                                f"{reply[0]}")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
