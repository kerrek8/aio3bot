from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline_keyboards.builder import inline_builder

router = Router()


@router.message(Command("lightning"))
async def lightning(message: Message):
    t = ['-5', '-1', '+1', '+5']
    cd = ['lightnumber_' + i + '_0' for i in t]
    t.append('Готово')
    t.append('Отмена')
    cd.append('light_done')
    cd.append('light_cansel')
    kb = await inline_builder(text=t, callback_data=cd, sizes=[4, 1])
    await message.answer(f'Введите количество секунд, прошедшее с момента вспышки до грома: 0', reply_markup=kb)


@router.callback_query(F.data.startswith('lightnumber_'))
async def light(c: CallbackQuery):
    await c.answer()
    t = ['-5', '-1', '+1', '+5']
    time = int(c.data.split('_')[2])
    delta = int(c.data.split('_')[1])
    answer = time + delta
    cd = ['lightnumber_' + i + f'_{answer}' for i in t]
    t.append('Готово')
    t.append('Отмена')
    cd.append('light_done' + f'_{answer}')
    cd.append('light_cansel')
    kb = await inline_builder(text=t, callback_data=cd, sizes=[4, 1, 1])
    await c.message.edit_text(f'Введите количество секунд, прошедшее с момента вспышки до грома: {answer}',
                              reply_markup=kb)


@router.callback_query(F.data == 'light_cansel')
async def light_cansel(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text('Отменено', reply_markup=None)


@router.callback_query(F.data.startswith('light_done'))
async def light_done(c: CallbackQuery):
    await c.answer()
    t = int(c.data.split('_')[2])
    t *= 340
    await c.message.edit_text(f'Молния ударила на расстоянии {t} метров', reply_markup=None)
