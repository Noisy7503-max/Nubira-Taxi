from aiogram.fsm.state import StatesGroup, State
from aiogram import Dispatcher

dp = Dispatcher()

class UserState(StatesGroup):
    begin_adress = State()
    finish_adress = State()
    comment = State()
    number = State()
    locate = State()

class DriverState(StatesGroup):
    fullname = State()
    phone_num = State()
    avto_num = State()
    card_num = State()

class AdminState(StatesGroup):
    news = State()