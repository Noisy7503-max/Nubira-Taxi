from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.keyboard import * 
from database.db import add_user
import html, aiosqlite

router = Router()

@router.message(CommandStart())
async def menu_handler(message: types.Message) -> None:
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(f'<b>Приветствую {html.escape(message.from_user.full_name)}!</b>\n\n<i>Прежде чем начать сотрудничество с нами, ознакомьтесь с нашими правилами и советами для комфортного использования👇</i>\n\n- Заказы по городу стоят 250 рублей\n- Рекомендуется пользоваться нашим ботом исключительно с телефона\n- Чтобы выполнять заказы необходимо пополнить баланс в личном кабинете.', reply_markup=keyboard)    

@router.message(F.text == '🔙 Вернуться в меню')
async def back_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await menu_handler(message)

@router.message(F.text == '🚫 Отменить заказ')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    cancel_app_num = await cursor.execute('SELECT cancel_applic FROM clients WHERE user_id = ?', (user_id,))
    cancel_app_num = await cursor.fetchone()
    cancel_app_num = cancel_app_num[0] + 1
    await cursor.execute('UPDATE clients SET cancel_applic = ? WHERE user_id = ?', (cancel_app_num, user_id))
    await connect.commit()
    await state.clear()
    await message.answer('Заказ отменен...')
    await cursor.close()
    await connect.close()
    await menu_handler(message)

@router.message(F.text == '📱 О нас')
async def about_handler(message: types.Message) -> None:
    await message.answer('Мы создали такси для вас прямо в телеграмме! Теперь вам будет не только удобно ездить в вашие любимые места, но и выгодно! У нас, цены намного ниже чем у других такси-компаний.Следите за нами в нашем телеграмм канале!\n\n<b>Приятных поездок!</b>', reply_markup=canal_keyboard)

