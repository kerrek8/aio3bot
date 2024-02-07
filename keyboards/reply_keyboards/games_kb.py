from aiogram.enums import DiceEmoji
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def games_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=DiceEmoji.DICE), KeyboardButton(text=DiceEmoji.DART),
           KeyboardButton(text=DiceEmoji.FOOTBALL))
    kb.row(KeyboardButton(text=DiceEmoji.SLOT_MACHINE), KeyboardButton(text=DiceEmoji.BASKETBALL),
           KeyboardButton(text=DiceEmoji.BOWLING))
    kb.row(KeyboardButton(text="\U00002064Выход\U00002064"))
    return kb.as_markup(resize_keyboard=True)
