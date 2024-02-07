from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def weather_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text="\U00002063Сейчас\U00002063"))
    kb.row(KeyboardButton(text="\U00002063Сегодня\U00002063"), KeyboardButton(text="\U00002063Завтра\U00002063"),
           KeyboardButton(text="\U00002063Послезавтра\U00002063"))
    kb.row(KeyboardButton(text="\U00002063На 5 дней\U00002063"))
    return kb.as_markup(resize_keyboard=True)


async def weather_sity_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text="\U00002063Стрежевой\U00002063"), KeyboardButton(text="\U00002063Тюмень\U00002063"))
    return kb.as_markup(resize_keyboard=True)
