from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

znaks = ['♉', '♋', '♐', '♑', '♏', '♒',
         '♓', '♍', '♈', '♌', '♎', '♊']

callbaks_znaks = [f'{i}' for i in znaks]


days = ['Сегодня', 'Завтра', 'Послезавтра']


async def horo_znak_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    [kb.button(text=txt, callback_data='horo_' + cd) for txt, cd in zip(znaks, callbaks_znaks)]
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='horo_cansel'))
    kb.adjust(6, 6, 1)
    return kb.as_markup(resize_keyboard=True)
