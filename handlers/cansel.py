from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command("cansel"))
async def cansel(message: Message):
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
