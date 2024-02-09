import json
from random import randint

import aiohttp
from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline_keyboards.builder import inline_builder

router = Router()


@router.callback_query(F.data == 'start_smart')
async def smart(c: CallbackQuery):
    # noinspection PyBroadException
    author, info = await get_smart()
    s = f'<b>{info}</b>\n\u2014 <i>{author}</i>'
    kb = await inline_builder(text=['Ещё', 'Выход'], callback_data=['smart_more', 'smart_cansel'], sizes=[1, 1])
    await c.answer()
    await c.message.answer(s, parse_mode='html', reply_markup=kb)


async def get_smart() -> (str, str):
    url = f"http://api.forismatic.com/api/1.0/?method=getQuote&format=json&key={randint(1, 999999)}&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.text()
        data = json.loads(r)
    except Exception as ex:
        print(ex)
        a = "что-то пошло не так, попробуйте позже"
        return a, ''
    author = data['quoteAuthor']
    info = data['quoteText']
    if len(data['quoteAuthor']) == 0:
        author = "Автор неизвестен"
    return author, info


@router.callback_query(F.data == 'smart_more')
async def smart_more(c: CallbackQuery):
    author, info = await get_smart()
    await c.answer()
    kb = await inline_builder(text=['Ещё', 'Выход'], callback_data=['smart_more', 'smart_cansel'], sizes=[1, 1])
    await c.message.edit_text(f'<b>{info}</b>\n\u2014 <i>{author}</i>', parse_mode='html', reply_markup=kb)


@router.callback_query(F.data == 'smart_cansel')
async def smart_cansel(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text('Готово', reply_markup=None)
