from aiogram import Router, types, F

router = Router()

@router.message(F.text == '🚀 Работа')
async def error_drive_handler(message: types.Message) -> None:
    await message.answer('Вы не можете работать так как вы не водитель!')

@router.message()
async def error_handler(message: types.Message) -> None:
    await message.answer('Такой команды нет :(\n\nПопробуйте еще раз...')