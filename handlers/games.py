from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards.reply_keyboards.games_kb import games_kb

router = Router()


@router.callback_query(F.data == 'start_games')
async def game(c: CallbackQuery):
    kb = await games_kb()
    await c.answer()
    await c.message.answer('Выберите игру', reply_markup=kb)


@router.message(F.text == "\U00002064Выход\U00002064")
async def dice(m: Message):
    await m.answer("Хорошего настроения", reply_markup=ReplyKeyboardRemove())
