from main import *

# Кнопка почали
keyboard_start = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True)
button_3 = aiogram.types.InlineKeyboardButton(text="Почали", callback_data='Start')
keyboard_start.add(button_3)

# Кнопка меню
button_finansy = aiogram.types.KeyboardButton(text="Фінанси")
button_qat = aiogram.types.KeyboardButton(text="Питання щодо навчання")
button_admissions = aiogram.types.KeyboardButton(text='Приймальна комісія')
button_mfaq = aiogram.types.KeyboardButton(text='Найчастіші запитання')
button_support = aiogram.types.KeyboardButton(cfg['button_new_question'])
keyboard_menu = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu.add(button_mfaq).row(button_qat).add(button_finansy, button_admissions).add(button_support)

rd = [button_finansy, button_admissions]





# Фінанси
what_is_the_tuition_fee = aiogram.types.InlineKeyboardButton(text='Яка вартість навчання?', callback_data='tuition_fee')
the_cost_of_the_hostel = aiogram.types.InlineKeyboardButton(text='Яка вартість гуртожитку?', callback_data='the_cost_of_the_hostel')
pay_for_tuition = aiogram.types.InlineKeyboardButton(text='Як сплачувати за навчання?', callback_data='pay_for_tuition', url="https://knutd.edu.ua/university/br/" )
the_cost_of_the_military_department = aiogram.types.InlineKeyboardButton(text='Яка вартість військової кафедри?', callback_data='military_department', url='https://knutd.edu.ua/admissions_main/obrati-profesiju/571/4936/ ')
finansy = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(what_is_the_tuition_fee).row(the_cost_of_the_hostel).row(the_cost_of_the_military_department).row(pay_for_tuition)

# Питання щодо навчання
faculty_dormitory = aiogram.types.InlineKeyboardButton(text='Гуртожиток факультету', callback_data='faculty_dormitory')
terms_of_study = aiogram.types.InlineKeyboardButton(text='Терміни навчання', callback_data='terms_of_study')
learning_offline_online = aiogram.types.InlineKeyboardButton(text='Навчання Офлайн/Онлайн?', callback_data='learning_offline_online', url='https://knutd.edu.ua/ekts/grafik/ ')
study_abroad_is_possible = aiogram.types.InlineKeyboardButton(text='Чи можливе навчання знаходячись закордоном?', callback_data='abroad_is_possible', url='https://drive.google.com/file/d/1kuo79jOR_TOavUXQV0c_oVnP6T_ePRvi/view ')
specialty = aiogram.types.InlineKeyboardButton(text='Які спеціальності пропонує університет?', url='https://knutd.edu.ua/admissions_main/perelik-osvitnikh-program-shho-proponuye-universitet/')
specialty_FMKT = aiogram.types.InlineKeyboardButton(text='Освітні програми ФМКТ', callback_data='Specialty_FMKT')
regarding_training = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(specialty).row(specialty_FMKT).row(study_abroad_is_possible).row(learning_offline_online).row(terms_of_study).row(faculty_dormitory)

email = aiogram.types.InlineKeyboardButton(text='Електронна адреса ', callback_data='email')
timee = aiogram.types.InlineKeyboardButton(text='Час роботи ', callback_data='time')
location = aiogram.types.InlineKeyboardButton(text='Де знаходиться? ', callback_data='location')
academic_certificate = aiogram.types.InlineKeyboardButton(text='Академічна довідка ', callback_data='academic_certificate')
student_id = aiogram.types.InlineKeyboardButton(text='Студентський квиток ', callback_data='student_id')
where_are_the_documents = aiogram.types.InlineKeyboardButton(text='Де знаходяться документи які я подавав?', callback_data='where_are_the_documents')
wocftc = aiogram.types.InlineKeyboardButton(text='Де замовити довідку у територіальні центри комплектування та соціальної підтримки (ТЦК та СП, військкомат), форма 20 ', callback_data='wocftc')
wahtoac = aiogram.types.InlineKeyboardButton(text='Де і як замовити довідку? ', callback_data='wahtoac')
wFMKTdo = aiogram.types.InlineKeyboardButton(text='Де знаходиться деканат Факультету МКТ? ', callback_data='wFMKTdo')
# Приймальна комісія
application_deadlines = aiogram.types.InlineKeyboardButton(text='Терміни подачі документів', callback_data='application_deadlines', url='https://knutd.edu.ua/admissions_main/admissions/ ')
parents_must_be_present = aiogram.types.InlineKeyboardButton(text='Чи повині батьки бути присутніми приподачі документів на контракт/бюджет?', callback_data='parents_must_be_present')
dormitory_documents = aiogram.types.InlineKeyboardButton(text='Які документи потрібні для заселення в гуртожиток?', callback_data='dormitory_documents', url='https://knutd.edu.ua/files/students/polozh-pro-koryst-gurt.pdf ')
documents = aiogram.types.InlineKeyboardButton(text='Які потрібні документи для вступу?', callback_data='documents')
renewal = aiogram.types.InlineKeyboardButton(text='Поновлення', callback_data='renewal')
deduction = aiogram.types.InlineKeyboardButton(text= 'Відрахування', callback_data='deduction')
admissions = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(parents_must_be_present).row(documents).row(dormitory_documents).row(application_deadlines).row(
    renewal).row(deduction).row(email).row(timee).row(location).row(academic_certificate).row(student_id).row(where_are_the_documents).row(
    wahtoac).row(wFMKTdo)


mfaq = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True).add(application_deadlines).row(documents).row(dormitory_documents).row(terms_of_study).add(specialty).row(specialty_FMKT).row(what_is_the_tuition_fee).row(the_cost_of_the_hostel)