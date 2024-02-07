from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from misk.sovmest_misks import get_znaks


async def sovmest_znak_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    znaks = await get_znaks()
    callbaks_znaks = [f'{i}' for i in znaks]
    [kb.button(text=txt, callback_data='sovmest_' + cd) for txt, cd in zip(znaks, callbaks_znaks)]
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='sovmest_cansel'))
    kb.adjust(6, 6, 1)
    return kb.as_markup(resize_keyboard=True)
