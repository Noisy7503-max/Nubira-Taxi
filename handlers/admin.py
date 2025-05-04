from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from keyboards.keyboard import * 
from database.db import add_driver
from handlers.user.main_user_handler import back_handler
from states.dispatcher import AdminState
from aiogram.types import TelegramObject
from aiogram.filters import BaseFilter, Command
import aiosqlite, asyncio

admin_ids = [2090971605, 7770756420]

async def get_clients_count():
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    user_count = await cursor.execute('SELECT COUNT(*) FROM clients')
    user_count = await user_count.fetchone()
    await cursor.close()
    await connect.close()
    return user_count[0]

async def get_drivers_count():
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    driver_count = await cursor.execute('SELECT COUNT(*) FROM drivers')
    driver_count = await driver_count.fetchone()
    await cursor.close()
    await connect.close()
    return driver_count[0]

async def get_all_users_id():
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    all_ids = await cursor.execute('SELECT user_id FROM clients')
    all_ids = await all_ids.fetchall()
    await cursor.close()
    await connect.close()
    return all_ids

class IsAdmin(BaseFilter):
    async def __call__(self, obj: TelegramObject) -> bool:
        return obj.from_user.id in admin_ids

async def admin_panel(message: types.Message) -> None:
    await message.answer('Добро пожаловать в Админ-панель!', reply_markup=admin_keyboard)

async def admin_news_1(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminState.news)
    await call.message.edit_text('Рассылка\n\nВведите сообщение, которое будет отправлено пользователем', reply_markup=back_in_keyboard)

async def admin_news_2(message: types.Message, state: FSMContext):
    await state.update_data(news=message.text)
    all_ids = await get_all_users_id()
    for user_id in all_ids:
        try:
            await message.send_copy(user_id[0])
            await asyncio.sleep(0.3)
        except:
            pass
    await state.clear()
    await message.answer('Рассылка завершена!')

async def statistic_handler(call: types.CallbackQuery) -> None:
    clients_count = await get_clients_count()
    drivers_count = await get_drivers_count()
    await call.message.edit_text(f'<b>Статистика</b>\n\nВсего пользователей в боте: {clients_count}\nКлиентов: {clients_count}\nВодителей: {drivers_count}', reply_markup=back_in_keyboard)

def register_admin_messages(dp: Dispatcher):
    dp.message.register(admin_panel, Command('admin'), IsAdmin())
    dp.callback_query.register(admin_news_1, F.data == 'news')
    dp.callback_query.register(admin_news_2, AdminState.news)
    dp.message.register(admin_panel, F.data == 'back', IsAdmin())
    dp.callback_query.register(statistic_handler, F.data == 'stat')