from aiogram import types

kb = [
    [types.KeyboardButton(text='➕ Заказать поездку'), types.KeyboardButton(text='🚕 Для водителей')],
    [types.KeyboardButton(text='🏠 Личный кабинет')],
    [types.KeyboardButton(text='💻 Тех. поддержка'), types.KeyboardButton(text='📱 О нас')]
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

sit_kb = [[types.InlineKeyboardButton(text='🚗 Я сел', callback_data='isit')]]

sit_keyboard = types.InlineKeyboardMarkup(inline_keyboard=sit_kb)

cabinet_kb = [
    [types.InlineKeyboardButton(text='💵 Пополнить баланс', callback_data='pay')]
    ]

cabinet_keyboard = types.InlineKeyboardMarkup(inline_keyboard=cabinet_kb)

check_pay_kb = [[types.InlineKeyboardButton(text='💳 Оплатил', callback_data='check_pay')]]

check_pay_keyboard = types.InlineKeyboardMarkup(inline_keyboard=check_pay_kb)

driver_kb = [[types.KeyboardButton(text='🚀 Работа')], [types.KeyboardButton(text='🚕 Стать водителем')], [types.KeyboardButton(text='🔙 Вернуться в меню')]]

driver_keyboard = types.ReplyKeyboardMarkup(keyboard=driver_kb, resize_keyboard=True)

stop_work_kb = [[types.KeyboardButton(text='⛔ Прекратить работу')]]

stop_work_keyboard = types.ReplyKeyboardMarkup(keyboard=stop_work_kb, resize_keyboard=True)

stop_app_kb = [[types.InlineKeyboardButton(text='✅ Завершить заказ', callback_data='finish_app')]]

stop_app_keyboard = types.InlineKeyboardMarkup(inline_keyboard=stop_app_kb)

stop_app_us_kb = [[types.KeyboardButton(text='✅ Прибыл')]]

stop_app_us_keyboard = types.ReplyKeyboardMarkup(keyboard=stop_app_us_kb, resize_keyboard=True)

i_drive_kb = [[types.InlineKeyboardButton(text='🚗 Приехал', callback_data='idrive')]]

i_drive_keyboard = types.InlineKeyboardMarkup(inline_keyboard=i_drive_kb)

back_kb = [
    [types.KeyboardButton(text='🔙 Вернуться в меню')]
]

back_keyboard = types.ReplyKeyboardMarkup(keyboard=back_kb, resize_keyboard=True)

num_kb = [
    [types.KeyboardButton(text='📱 Поделиться номером телефона', request_contact=True)],
    [types.KeyboardButton(text='🔙 Вернуться в меню')]
]

num_keyboard = types.ReplyKeyboardMarkup(keyboard=num_kb, resize_keyboard=True)

geo_kb = [
    [types.KeyboardButton(text='📡Поделиться геопозицией', request_location=True)],
    [types.KeyboardButton(text='🔙 Вернуться в меню')]
]

geo_keyboard = types.ReplyKeyboardMarkup(keyboard=geo_kb, resize_keyboard=True)

applic_kb = [
    [types.KeyboardButton(text='Создать заказ 🏁')],
    [types.KeyboardButton(text='🚫 Отменить заказ')]
]

applic_keyboard = types.ReplyKeyboardMarkup(keyboard=applic_kb, resize_keyboard=True)

reg_kb = [
    [types.InlineKeyboardButton(text='🪪 Написать админу', url='https://t.me/Tech_support_taxi_nubira')],
]

reg_keyboard = types.InlineKeyboardMarkup(inline_keyboard=reg_kb, resize_keyboard=True)

canal_kb = [
    [types.InlineKeyboardButton(text='📢 Подписаться на канал', url='https://t.me/taxinubira')],
]

canal_keyboard = types.InlineKeyboardMarkup(inline_keyboard=canal_kb)

finish_kb = [
    [types.KeyboardButton(text='Завершить 🏁')]
]

finish_keyboard = types.ReplyKeyboardMarkup(keyboard=finish_kb, resize_keyboard=True)

continue_kb = [
    [types.KeyboardButton(text='Далее')],
    [types.KeyboardButton(text='🔙 Вернуться в меню')]
]

continue_keyboard = types.ReplyKeyboardMarkup(keyboard=continue_kb, resize_keyboard=True)

admin_kb = [
    [types.InlineKeyboardButton(text='Рассылка', callback_data='news')], [types.InlineKeyboardButton(text='Статистика', callback_data='stat')],
    [types.InlineKeyboardButton(text='Заявки', callback_data='request')], [types.InlineKeyboardButton(text='Обратная связь', callback_data='quest')]
]

admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard=admin_kb)

back_in_kb = [
    [types.InlineKeyboardButton(text='Назад', callback_data='back')]
]

back_in_keyboard = types.InlineKeyboardMarkup(inline_keyboard=back_in_kb)

work_kb = [
    [types.InlineKeyboardButton(text='Поехал!', callback_data='work')]
]

work_keyboard = types.InlineKeyboardMarkup(inline_keyboard=work_kb)