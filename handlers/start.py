from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from contextlib import suppress
from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError
router = Router()


@router.message(CommandStart())
async def start(m: Message, db: MDB):
    s = '<b>Вот список моих команд</b>\n\n' + '/start - ФУНКЦИИ БОТА\n' + '/cubic_game - игра в бросок кубика\n' + \
        '/weather - погода\n' + '/lightning - калькулятор молний\n' + '/game - игры\n' + '/horoscope - гороскоп\n' + \
        '/sovmestimost - совместимость знаков зодиака\n' + '/smart - умная мысль\n' + '/cansel - Отмена\n'
    pattern = {
        '_id': m.from_user.id,
        'stats': {'wins': 0, 'losses': 0, 'tie': 0},
        'game': {'status': 0, 'value': 0, 'rid': 0}
    }
    with suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)
    await m.answer(s, reply_markup=None, parse_mode='html')
