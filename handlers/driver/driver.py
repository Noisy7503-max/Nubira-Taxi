import aiosqlite
from aiogram import types, F, Router
from keyboards.keyboard import * 
from aiogram.types import TelegramObject
#from main import router
from aiogram.filters import BaseFilter

router = Router()

drivers_ids = [2117761461, 2090971605]

class IsDriver(BaseFilter):
    async def __call__(self, obj: TelegramObject) -> bool:
        return obj.from_user.id in drivers_ids

@router.message(F.text == '🚕 Для водителей')
async def for_driver(message: types.Message) -> None:
    await message.answer('Добро пожаловать в панель водителя!\n\nВыберите опцию ниже', reply_markup=driver_keyboard)

@router.message(F.text == '✅ Завершить заказ')
async def stop_app(message: types.Message) -> None:
    await message.answer('Заказ завершен!')
    await application_handler()

@router.message(F.text == '🚀 Работа', IsDriver())
async def application_handler(message: types.Message) -> None:
    global user_id_driver
    global drive_chat_id
    drive_chat_id = message.chat.id
    user_id_driver = message.from_user.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    summa_driver = await cursor.execute('SELECT money FROM drivers WHERE user_id = ?', (user_id_driver,))
    summa_driver = await summa_driver.fetchone()
    if summa_driver and summa_driver[0] > 40:
        await cursor.execute('UPDATE drivers SET isWorking = 1 WHERE user_id = ?', (user_id_driver,))
        await connect.commit()
        await message.answer('Новые заказы будут приходить сюда\n\n<b>Доступные заказы:</b>\n\n', reply_markup=stop_work_keyboard)
    else: 
        await message.answer('У вас недостаточно средств для выполнения заказов!\n\nПополните баланс в личном кабинете...')
        await cursor.close()
        await connect.close()

@router.message(F.text == '⛔ Прекратить работу', IsDriver())
async def stop_work_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    await cursor.execute('UPDATE drivers SET isWorking = 0 WHERE user_id = ?', (user_id,))
    await connect.commit()
    await cursor.close()
    await connect.close()
    await message.answer(f'Работа прекращена\n\n<i>Нажмите вернуться в меню</i>', reply_markup=back_keyboard)

@router.message(F.text == '🚕 Стать водителем')
async def caution_reg(message: types.Message) -> None:
    await message.answer('🚕 <b>Стать водителем</b>\n\nДля заполнения анкеты вы должны:\n➖Быть старше 18 лет\n➖Иметь номер телефона для связи\n➖Сделать фотографию прав и техпаспорта\n➖Сделать фотографию машины спереди с номером\n\n⚠️ Для выполнения заказов вам нужно будет пополнить баланс в личном кабинете!\n\nЕсли вы готовы начать регистрацию, то нажмите копку ниже', reply_markup=reg_keyboard)

