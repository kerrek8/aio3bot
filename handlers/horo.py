from aiogram import F
from aiogram.client.session import aiohttp
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bs4 import BeautifulSoup

from keyboards.inline_keyboards.builder import inline_builder
from keyboards.inline_keyboards.horo_keyboards import horo_znak_kb, days
from misk.horo_misks import transcription

router = Router()


@router.message(Command('horoscope'))
async def start(m: Message):
    kb = await horo_znak_kb()
    await m.answer('Выбери знак зодиака', reply_markup=kb)


@router.callback_query(F.data == 'horo_cansel')
async def horoscope(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Отменено", reply_markup=None)


@router.callback_query(F.data.startswith('horo_'))
async def horoscope(query: CallbackQuery):
    data = query.data.split('_')
    if data[1] != 'd':
        await horo_day(data[1], query)
    else:
        await query.answer()
        url = 'https://ignio.com/r/export/utf/xml/daily/com.xml'
        day = data[2]
        choose = data[3]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    r = await response.text()
            soup = BeautifulSoup(r, 'xml')
            await query.message.edit_text(
                text=f'Гороскоп для {choose} на {day}\n' + soup.find(transcription[choose]).find(
                    transcription[day]).text, reply_markup=None)
        except Exception as ex:
            print(ex)
            await query.message.delete()
            await query.message.answer("что-то пошло не так, попробуйте позже")
            return


async def horo_day(c: str, query: CallbackQuery):
    await query.answer()
    callbacks = ['horo_d_' + i + f'_{c}' for i in days]
    callbacks.append('horo_cansel')
    kb = await inline_builder(text=[*days, 'Отмена'], callback_data=callbacks, sizes=[1, 1, 1, 1])
    await query.message.edit_text("Выберите на какой день вы хотите гороскоп", reply_markup=kb)
