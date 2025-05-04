from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from keyboards.keyboard import * 
from states.dispatcher import UserState
from config.config import *
import html, asyncio, aiosqlite

applic_num = 0
router = Router()
sent_messages_1 = {}
sent_messages_2 = {}
sent_messages_3 = {}

@router.message(F.text == '➕ Заказать поездку')
async def first_step(message: types.Message, state: FSMContext) -> None:
    await state.set_state(UserState.begin_adress)
    await message.answer(f'Укажите <b>{html.escape('АДРЕС')}</b> или <b>{html.escape('МЕСТО')}</b> откуда вас нужно забрать\n\n<i>Напишите как можно более подробно</i>', reply_markup=back_keyboard)

@router.message(UserState.begin_adress)
async def second_step(message: types.Message, state: FSMContext) -> None:
    await state.update_data(begin=message.text)
    await state.set_state(UserState.finish_adress)
    await message.answer(f'Укажите <b>АДРЕС</b>, <b>КУДА</b> вас нужно отвезти', reply_markup=back_keyboard)

@router.message(UserState.finish_adress)
async def third_step(message: types.Message, state: FSMContext) -> None:
    await state.update_data(finish=message.text)
    await state.set_state(UserState.comment)
    await message.answer('Напишите комментарии для водителя', reply_markup=back_keyboard)

@router.message(UserState.comment)
async def fourth_step(message: types.Message, state: FSMContext) -> None:
    await state.update_data(comment=message.text)
    await state.set_state(UserState.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=num_keyboard)

@router.message(F.contact)
async def fourth_step_2(message: types.Message, state: FSMContext) -> None:
    await state.update_data(number=message.contact)
    await state.set_state(UserState.locate)
    global number
    number = message.contact.phone_number
    await message.answer('Отправьте вашу геопозицию для более точного составления заказа', reply_markup=geo_keyboard)
    
@router.message(F.location)
async def fiveth_step(message: types.Message, state: FSMContext) -> None:
    await state.update_data(locate=message.location)
    data = await state.get_data()
    global latitude
    global longitude
    latitude = message.location.latitude
    longitude = message.location.longitude
    global applic_num
    applic_num += 1
    await message.answer(f'Заказ № {applic_num} Открыт!\n\n<b>Откуда:</b> {data['begin']}\n<b>Куда:</b> {data['finish']}\n<b>Комментарий:</b> {data['comment']}\n<b>Телефон: {number}</b>\n\n<i>Геопозиция будет отправлена водителю</i>\n\n<b>Внимание! После нажатия кнопки создания заказа вы не сможете его отменить. Чтобы отменить заказ вам нужно дождаться принятия этого заказа водителем и в личных сообщениях написать об отказе</b>', reply_markup=applic_keyboard)
    

@router.message(F.text == 'Создать заказ 🏁')
async def create_applic(message: types.Message, state: FSMContext) -> None:
    from handlers.driver.driver import drive_chat_id, user_id_driver
    global applic_num
    global id_user
    id_user = message.from_user.id
    name_user = message.from_user.full_name
    user_name = message.from_user.username
    if user_name == None:
        link = f'https://t.me/{number}'
    else: 
        link = f'https://t.me/{user_name}'
    data = await state.get_data()
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    await cursor.execute('SELECT user_id FROM drivers WHERE isWorking = 1')
    drive_chat_id = await cursor.execute('SELECT user_id FROM drivers WHERE isWorking = 1')
    drivers_ids = await cursor.fetchall()
    for driver_id in drivers_ids:
        try:
            msg_app_1 = await message.bot.send_message(driver_id[0], f"Доступен Заказ № {applic_num}!\n\n<b>Клиент:</b> {name_user}\n\n<b>Откуда:</b> {data['begin']}\n<b>Куда:</b> {data['finish']}\n<b>Комментарий:</b> {data['comment']}\n<b>Телефон:</b> {number}\n\n<a href='{link}'>Написать клиенту</a>\n\n<b>Геопозиция</b>: ")
            msg_app_2 = await message.bot.send_location(driver_id[0], latitude=latitude, longitude=longitude)
            msg_app_3 = await message.bot.send_message(driver_id[0], f'<i>Чтобы принять заказ № {applic_num} нажмите кнопку ниже</i>', reply_markup=work_keyboard)
            sent_messages_1[user_id_driver] = {
        'chat_id': drive_chat_id,
        'message_id': msg_app_1.message_id,
    }
            sent_messages_2[user_id_driver] = {
        'chat_id': drive_chat_id,
        'message_id': msg_app_2.message_id,
    }
            sent_messages_3[user_id_driver] = {
        'chat_id': drive_chat_id,
        'message_id': msg_app_3.message_id,
    }
        except Exception as e:
            print(f"Error sending to driver {driver_id}: {e}")
        await asyncio.sleep(0.3)

    await message.answer('<b>Ваш заказ создан!\nОжидайте отклика водителя!</b>\n\n<i>Вам придет уведомление...</i>', reply_markup=back_keyboard)
    await cursor.close()
    await connect.close()
    await state.clear()

@router.callback_query(F.data == 'work')
async def send_answer(callback: types.CallbackQuery) -> None:
    global id_driver
    id_driver = callback.from_user.id
    global id_chat_driver
    id_chat_driver = callback.message.chat.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    for chat_id, msg_info in sent_messages_1.items():
        if chat_id != id_driver: 
            try:
                await callback.message.bot.delete_message(msg_info['chat_id'], msg_info['message_id'])
            except Exception as e:
                print(f"Не удалось удалить сообщение для {chat_id}: {e}")
    
    for chat_id, msg_info in sent_messages_2.items():
        if chat_id != id_driver: 
            try:
                await callback.message.bot.delete_message(msg_info['chat_id'], msg_info['message_id'])
            except Exception as e:
                print(f"Не удалось удалить сообщение для {chat_id}: {e}")
    
    for chat_id, msg_info in sent_messages_3.items():
        if chat_id != id_driver: 
            try:
                await callback.message.bot.delete_message(msg_info['chat_id'], msg_info['message_id'])
            except Exception as e:
                print(f"Не удалось удалить сообщение для {chat_id}: {e}")

    await callback.answer("Вы приняли этот заказ!")
    about_drive = await cursor.execute(f'SELECT full_name, avto_num, phone_num, about FROM drivers WHERE user_id = ?', (id_driver,))
    about_drive = await about_drive.fetchone()
    full_name, avto_num, phone_num, about = about_drive
    user_id_ = callback.message.from_user.id
    await cursor.execute('UPDATE drivers SET isWorking = 0 WHERE user_id = ?', (user_id_,))
    await connect.commit()
    await callback.message.bot.send_message(id_user, f'<b>Ваш заказ был принят! Водитель уже в пути!\nВаш водитель: </b>\n\n<b>Имя:</b> {full_name}\n<b>Номер автомобиля: </b>{avto_num}\n<b>Номер телефона для связи: </b>{phone_num}\n<b>Описание водителя: </b>{about}\n<i>В скором времени водитель свяжется с вами!</i>')
    await callback.message.answer('<i>Как только вы приедете к клиенту нажмите кнопку ниже</i>', reply_markup=i_drive_keyboard)
    await cursor.close()
    await connect.close()


@router.callback_query(F.data == 'idrive')
async def idrive(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Теперь дождитесь подтверждения от клиента...')
    await callback.message.bot.send_message(id_user, f'Если вы сели в машину нажмите кнопку ниже', reply_markup=sit_keyboard)

@router.callback_query(F.data == 'isit')
async def isit(callback: types.CallbackQuery) -> None:
    await callback.message.bot.send_message(id_user, f'<b>Отлично!</b>\n\nПосле прибытия в точку назначения, нажмите кнопку ниже', reply_markup=stop_app_us_keyboard)


@router.message(F.text == '✅ Прибыл')
async def finish_drive(message: types.Message):
    user_id = message.from_user.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    finish_app_num = await cursor.execute('SELECT finish_applic FROM clients WHERE user_id = ?', (user_id,))
    finish_app_num = await finish_app_num.fetchone()
    finish_app_num = finish_app_num[0] + 1
    await cursor.execute('UPDATE clients SET finish_applic = ? WHERE user_id = ?', (finish_app_num, user_id))
    await connect.commit()
    await cursor.close()
    await connect.close()
    await message.bot.send_message(id_user, f'<i>Теперь дождитесь завершения заказа водителем</i>')
    await message.bot.send_message(id_driver, f'Если вы прибыли в точку назначения, то нажмите <b>✅ Завершить заказ</b>', reply_markup=stop_app_keyboard)

@router.callback_query(F.data == 'finish_app')
async def pay_app(callback: types.CallbackQuery) -> None:
    user_id = callback.message.from_user.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    money_driver = await cursor.execute('SELECT money FROM drivers WHERE user_id = ?', (id_driver,))
    money_driver = await money_driver.fetchone()
    money_driver = money_driver[0] - COMISSION
    await cursor.execute('UPDATE drivers SET money = ? WHERE user_id = ?', (money_driver, id_driver,))
    await connect.commit()
    await cursor.close()
    await connect.close()
    await callback.message.answer('<b>Поздравляем!</b>\n\nС вашего счета в личном кабинете сняты 40 рублей...', reply_markup=driver_keyboard)
    await callback.message.bot.send_message(id_user, f'<i>Заказ завершен!</i>\n\nВы можете вернуться в главное меню', reply_markup=back_keyboard)
    
