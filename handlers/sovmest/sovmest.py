from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from handlers.sovmest.get_sovmest import get_sovmest
from keyboards.inline_keyboards.builder import inline_builder
from keyboards.inline_keyboards.sovmest_keyboards import sovmest_znak_kb
from misk.sovmest_misks import get_znaks, transcription

router = Router()


@router.callback_query(F.data == 'start_sovmest')
@router.message(Command('sovmestimost'))
async def sovmestimost(m: Message):
    kb = await sovmest_znak_kb()
    await m.answer('Выберите знак девушки', reply_markup=kb)


@router.callback_query(F.data == 'sovmest_cansel')
async def sovmest_cansel(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text('Отменено', reply_markup=None)


@router.callback_query(F.data.startswith('sovmest_'))
async def get_women(c: CallbackQuery):
    cnt = len(c.data.split('_'))
    if cnt == 2:
        await c.answer()
        text = await get_znaks()
        cd = ['sovmest_' + i + f'_{c.data.split("_")[1]}' for i in text]
        text.append('Отмена')
        cd.append('sovmest_cansel')
        kb = await inline_builder(text=text, callback_data=cd, sizes=[6, 6, 1])
        await c.message.edit_text('Выберите знак мужчины', reply_markup=kb)
    else:
        await c.answer()
        text = ['Любовь', 'Секс', 'Семья и брак', 'Дружба', 'Работа и бизнес']
        cd = ['type_' + i + f'_{c.data.split("_")[1]}' + f'_{c.data.split("_")[2]}' for i in text]
        text.append("Отмена")
        cd.append('sovmest_cansel')
        kb = await inline_builder(text=text, callback_data=cd, sizes=[3, 2, 2, 1])
        await c.message.edit_text('Выберите тип совместимости', reply_markup=kb)


@router.callback_query(F.data.startswith('type_'))
async def sovmest_final(c: CallbackQuery):
    ent = c.data.split('_')
    type = ent[1]
    znak_m = ent[2]
    znak_w = ent[3]
    answer = await get_sovmest(transcription[znak_m], transcription[znak_w], type)
    if len(answer) == 0:
        await c.answer()
        await c.message.edit_text('Что-то пошло не так, попробуйте ещё раз', reply_markup=None)
        return
    pred = answer[0]
    t = answer[1]
    await c.answer()
    await c.message.edit_text(f'<b>девушка - {znak_w}, мужчина - {znak_m}</b>\n\n' + f'{pred}\n\n<b>{t}</b>\n\n' +
                              '\n'.join(answer[2:]), parse_mode='html', reply_markup=None)
