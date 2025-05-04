from aiogram import types, F, Router
from keyboards.keyboard import *

router = Router()

@router.message(F.text == '💻 Тех. поддержка')
async def support_handler(message: types.Message) -> None:
    await message.answer('Если у вас возникли какие-то трудности при использовании нашего бота, или у вас есть предложения как улучшить этого бота то пишите нам в поддержку, мы будем рады вам помочь!\n\n<b>Задайте свой вопрос здесь и мы ответим на него как можно быстрее!</b>', reply_markup=reg_keyboard)
