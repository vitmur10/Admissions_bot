from Const import *

from main import *

# Кнопка меню
button_finansy = aiogram.types.KeyboardButton(text="Фінанси")
button_qat = aiogram.types.KeyboardButton(text="Питання щодо навчання")
button_admissions = aiogram.types.KeyboardButton(text='Приймальна комісія')
button_mfaq = aiogram.types.KeyboardButton(text='Найчастіші запитання')
button_support = aiogram.types.KeyboardButton(cfg['button_new_question'])
keyboard_menu = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu.add(button_mfaq).row(button_qat).add(button_finansy, button_admissions).add(button_support)


def create_inline_keyboard(text):
    menu_reply = aiogram.types.InlineKeyboardMarkup()
    for reply in cur.execute("SELECT text  FROM question_answer_Question WHERE type = ?", (text,)):
        button = aiogram.types.InlineKeyboardButton(text=reply[0], callback_data=reply[0])
        menu_reply.add(button)
    return menu_reply
