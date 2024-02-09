from contextlib import suppress

from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

from keyboards.inline_keyboards.builder import inline_builder

router = Router()


@router.message(CommandStart())
async def start(m: Message, db: MDB):
    s = ('<b>Привет!! Я простой бот который умеет много разного</b>\n' +
         '<b>К примеру я могу помочь тебе узнать погоду или скоротать время</b>\n' +
         '<b>Но так же у меня есть и другие возможности с которыми ты можешь ознакомиться по кнопкам ниже</b>')
    # '/weather - погода\n' +
    # '/lightning - калькулятор молний\n' +
    # '/game - игры\n' +
    # '/horoscope - гороскоп\n' +
    # '/sovmestimost - совместимость знаков зодиака\n' +
    # '/smart - умная мысль\n' + '/cansel - Отмена\n')
    kb = await inline_builder(
        text=['🎲Игра в бросок кубика🎲', '☀️Погода☀️', '⚡Калькулятор молний⚡', '🎳Игры🎰', '♑Гороскоп♈',
              '💘Совместимость знаков зодиака💘', '🤔Умная мысль🤔'],
        callback_data=['start_dicegame', 'start_weather', 'start_lightning', 'start_games', 'start_horo',
                       'start_sovmest', 'start_smart'],
        sizes=[1, 2, 2, 1, 1])
    pattern = {
        '_id': m.from_user.id,
        'first_name': m.from_user.first_name,
        'username': m.from_user.username,
        'stats': {'wins': 0, 'losses': 0, 'tie': 0},
        'game': {'status': 0, 'value': 0, 'rid': 0}
    }
    with suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)
    await m.answer(s, reply_markup=kb, parse_mode='html')
