from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_builder(text: str | list[str], callback_data: str | list[str],
                         sizes: int | list[int] = 2) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    text = [text] if isinstance(text, str) else text
    callback_data = [callback_data] if isinstance(callback_data, str) else callback_data
    sizes = [sizes] if isinstance(sizes, int) else sizes
    [builder.button(text=txt, callback_data=cd) for txt, cd in zip(text, callback_data)]
    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True)


