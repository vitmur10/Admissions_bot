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
        await message.reply(f"{cfg['question_ur_question_sended_message']}")
        await bot.send_photo(cfg['teh_chat_id'], ph,
                             caption=f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}\n\n📝 Щоб відповісти "
                                     f"на запитання, введіть ")
        await bot.send_message(cfg['teh_chat_id'], f"/відповідь {message.chat.id} Ваша відповідь")
    else:
        await message.reply(f"{cfg['question_ur_question_sended_message']}")
        await bot.send_message(cfg['teh_chat_id'],
                               f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}\n\n📝 Щоб відповісти ")
        await bot.send_message(cfg['teh_chat_id'],f"/відповідь {message.chat.id} Ваша відповідь")


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
            await bot.send_message(chatid, f"✉ Нове повідомлення!\nВідповідь від технічної підтримки:\n\n{answer}")
            return
        else:
            await message.reply('⚠ Вкажіть аргументи команди\nПриклад:')
            await bot.send_message(cfg['teh_chat_id'], f"/відповідь {message.chat.id} Ваша відповідь")
            return
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
        await message.answer('Ось перелік найчастіших запитань...', reply_markup=keybord.create_inline_keyboard(message.text))
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
async def independence_square(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    for reply in cur.execute("SELECT answer  FROM question_answer_Question WHERE text = ?", (callback_query.data,)):
        await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                            f"{q}\n"
                                                            f"{reply[0]}")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
