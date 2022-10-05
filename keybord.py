import aiogram
from main import bot, dp

# Кнопка почали
keyboard_start = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True)
button_3 = aiogram.types.InlineKeyboardButton(text="Почали", callback_data='Start')
keyboard_start.add(button_3)

# Кнопка меню
button_finansy = aiogram.types.KeyboardButton(text="Фінанси")
button_qat = aiogram.types.KeyboardButton(text="Питання щодо навчання")
button_admissions = aiogram.types.KeyboardButton(text='Приймальна комісія')
button_mfaq = aiogram.types.KeyboardButton(text='Найчастіші запитання')
keyboard_menu = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu.add(button_mfaq).row(button_qat).add(button_finansy, button_admissions)

rd = [button_finansy, button_admissions]





# Фінанси
what_is_the_tuition_fee = aiogram.types.InlineKeyboardButton(text='Яка вартість навчання?', callback_data='tuition_fee', url='https://knutd.edu.ua/files/pravila/2022/Dodatok_1_2022.pdf ')
the_cost_of_the_hostel = aiogram.types.InlineKeyboardButton(text='Яка вартість гуртожитку?', callback_data='the_cost_of_the_hostel', url='https://knutd.edu.ua/students/gurtozhitki/ ')
pay_for_tuition = aiogram.types.InlineKeyboardButton(text='Як сплачувати за навчання?', callback_data='pay_for_tuition', url="https://knutd.edu.ua/university/br/" )
the_cost_of_the_military_department = aiogram.types.InlineKeyboardButton(text='Яка вартість військової кафедри?', callback_data='military_department', url='https://knutd.edu.ua/admissions_main/obrati-profesiju/571/4936/ ')
finansy = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(what_is_the_tuition_fee).row(the_cost_of_the_hostel).row(the_cost_of_the_military_department).row(pay_for_tuition)

# Питання щодо навчання
terms_of_study = aiogram.types.InlineKeyboardButton(text='Терміни навчання', callback_data='terms_of_study', url='https://knutd.edu.ua/files/pravila/2022/Dodatok_1_2022.pdf ')
learning_offline_online = aiogram.types.InlineKeyboardButton(text='Навчання Офлайн/Онлайн?', callback_data='learning_offline_online', url='https://knutd.edu.ua/ekts/grafik/ ')
study_abroad_is_possible = aiogram.types.InlineKeyboardButton(text='Чи можливе навчання знаходячись закордоном?', callback_data='abroad_is_possible', url='https://drive.google.com/file/d/1kuo79jOR_TOavUXQV0c_oVnP6T_ePRvi/view ')
specialty = aiogram.types.InlineKeyboardButton(text='Які спеціальності пропонує університет?', url='https://knutd.edu.ua/admissions_main/perelik-osvitnikh-program-shho-proponuye-universitet/')
specialty_FMKT = aiogram.types.InlineKeyboardButton(text='Освітні програми ФМКТ', url='https://knutd.edu.ua/ekts/2022/op-fmkt/')
regarding_training = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(specialty).row(specialty_FMKT).row(study_abroad_is_possible).row(learning_offline_online).row(terms_of_study)

# Приймальна комісія
application_deadlines = aiogram.types.InlineKeyboardButton(text='Терміни подачі документів', callback_data='application_deadlines', url='https://knutd.edu.ua/admissions_main/admissions/ ')
parents_must_be_present = aiogram.types.InlineKeyboardButton(text='Чи повині батьки бути присутніми приподачі документів на контракт/бюджет?', callback_data='parents_must_be_present')
dormitory_documents = aiogram.types.InlineKeyboardButton(text='Які документи потрібні для заселення в гуртожиток?', callback_data='dormitory_documents', url='https://knutd.edu.ua/files/students/polozh-pro-koryst-gurt.pdf ')
documents = aiogram.types.InlineKeyboardButton(text='Які документи потрібно для подачі документів?', callback_data='documents')
admissions = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(parents_must_be_present).row(documents).row(dormitory_documents).row(application_deadlines)


mfaq = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(application_deadlines).row(documents).row(dormitory_documents).row(terms_of_study).add(specialty).row(specialty_FMKT).row(what_is_the_tuition_fee).row(the_cost_of_the_hostel)