import aiogram.types

from Const import cfg, cur

# Creating reply keyboard buttons
button_finansy = aiogram.types.KeyboardButton(text="Фінанси")
button_qat = aiogram.types.KeyboardButton(text="Питання щодо навчання")
button_admissions = aiogram.types.KeyboardButton(text='Питання щодо вступу')
button_mfaq = aiogram.types.KeyboardButton(text='Найчастіші запитання')
button_support = aiogram.types.KeyboardButton(cfg['button_new_question'])
button_back = aiogram.types.KeyboardButton("Змінити факультет")
# Creating a reply keyboard markup and adding buttons to it
keyboard_menu = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu.add(button_mfaq).row(button_qat).add(button_finansy, button_admissions).add(button_support, button_back)
# Creating a reply keyboard markup for faculty selection
menu_faculty = aiogram.types.ReplyKeyboardMarkup()
# Adding buttons for each faculty from the database
for name in cur.execute("SELECT name FROM question_answer_faculty"):
    button = aiogram.types.KeyboardButton(text=str(name[0]))
    menu_faculty.add(button)


def create_inline_keyboard(text, f_id):
    """Creating an inline keyboard markup for question selection"""

    menu_question = aiogram.types.InlineKeyboardMarkup()
    # Adding buttons for each question of the given type and faculty from the database
    for reply in cur.execute("SELECT text FROM question_answer_Question WHERE type = ? and faculty_id = ?",
                             (text, f_id)):
        button = aiogram.types.InlineKeyboardButton(text=reply[0], callback_data=reply[0])
        menu_question.add(button)
    return menu_question
