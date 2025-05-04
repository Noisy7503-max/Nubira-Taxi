from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from yoomoney import Quickpay, Client
from states.dispatcher import DriverState
from keyboards.keyboard import * 
from database.db import add_user
from config.config import *
import html, aiosqlite

router = Router()
client = Client(YOO_TOKEN)

@router.message(F.text == '🏠 Личный кабинет')
async def main_cabinet(message: types.Message) -> None:
    user_id = message.from_user.id
    connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
    cursor = await connect.cursor()
    global check_user
    check_user = await cursor.execute('SELECT * FROM drivers WHERE user_id = ?', (user_id,))
    check_user = await check_user.fetchone()
    if check_user is None:
        await message.answer(f'<b>Добро пожаловать в личный кабинет!</b>\n\n<b>Статус: </b>🚘Клиент🚘\n\n<b>Количество успешных поездок: </b>\n<b>Количество отмененных заказов: </b>\n')
        await connect.commit()
    else:
        summa = await cursor.execute('SELECT money FROM drivers WHERE user_id = ?', (user_id,))
        summa = await summa.fetchone()
        await message.answer(f'<b>Добро пожаловать в личный кабинет!</b>\n\n<b>Статус: </b>🚖Водитель🚖\n<b>Сумма на аккаунте: {summa[0]} рублей</b>\n<b>Количество успешных поездок: </b>\n<b>Количество отмененных заказов: </b>\n', reply_markup=cabinet_keyboard)
    await cursor.close()
    await connect.close()

@router.callback_query(F.data == 'pay')
async def pay_cabinet(callback: types.CallbackQuery) -> None:
    label = callback.from_user.id
    quickpay = Quickpay(
            receiver="4100118970052190", # Номер вашего аккаунта
            quickpay_form="shop", # Это я хз зачем, но я это не трогаю
            targets="Pay cabinet", # Цели, я их не изменяю, потому что особой нужды в этом нет.
            paymentType="SB", # Это лучше не трогать
            sum=400, # Это сумма
            label=label # Это комментарий для проверки на наличие оплаты
            )
    link_for_pay = quickpay.base_url
    await callback.message.answer(f'Внимание!\n\n<b>Фиксированная сумма пополнения личного кабинета:</b> 400 рос. рублей.\n\nПОСЛЕ ВНЕСЕНИЯ ОПЛАТЫ ДЕНЬГИ ВЫВЕСТИ ОБРАТНО НЕЛЬЗЯ\n\n<i>Если вы готовы пополнить личный кабинет, нажмите кнопку ниже</i>\n\n<a href="{link_for_pay}">Пополнить баланс</a>\n\nПосле внесения оплаты нажмите <b>💳 Оплатил</b>', reply_markup=check_pay_keyboard)

@router.callback_query(F.data == 'check_pay')
async def pay_check(callback: types.CallbackQuery) -> None:
    label = callback.from_user.id
    history = client.operation_history(label=label)
    if history.operations == []:
        await callback.answer('Оплата не найдена!')

    for operation in history.operations:
        if operation.status == 'success':
            await callback.answer('Оплата найдена! Ваш кошелек в личном кабинете пополнен на 400 рос. рублей!')
            connect = await aiosqlite.connect(r'C:\PYTHONP\NubiraTaxi\database\database.db')
            cursor = await connect.cursor()
            summa_driver = await cursor.execute('SELECT money FROM drivers WHERE user_id = ?', (label,))
            summa_driver = await summa_driver.fetchone()
            summa_driver = summa_driver[0] + 400
            await cursor.execute('UPDATE driver SET money = ? WHERE user_id = ?', (summa_driver, label,))
            await connect.commit()
            await cursor.close()
            await connect.close()


    
            
            
 