from aiogram import F, Bot
from aiogram.dispatcher.router import Router
from aiogram.enums import DiceEmoji
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hcode
from motor.core import AgnosticDatabase as MDB

from keyboards.inline_keyboards.builder import inline_builder
from keyboards.reply_keyboards.builder import reply_builder

router = Router()


@router.callback_query(F.data == 'start_dicegame')
async def start_game(c: CallbackQuery, db: MDB):
    user = await db.users.find_one({'_id': m.from_user.id})
    users_in_search = await db.users.count_documents({'game.status': 1})
    kb = await reply_builder(text='🔎 Поиск')
    await c.answer()
    await c.message.answer('Начинай поиск и играй\n'
                           f'Пользователей в поиске: {hcode(users_in_search)}\n\n'
                           'Статистика: \n'
                           f'Победа: {hcode(user["stats"]["wins"])}\n'
                           f'Поражение: {hcode(user["stats"]["losses"])}\n'
                           f'Ничья: {hcode(user["stats"]["tie"])}', reply_markup=kb, parse_mode='html'
                           )


@router.message(F.text.lower().contains('поиск'))
async def search_game(m: Message, db: MDB, bot: Bot):
    user = await db.users.find_one({'_id': m.from_user.id})
    pattern = {'text': 'У вас уже есть активная игра!'}

    if user['game']['status'] == 0:

        rival = await db.users.find_one({'game.status': 1})
        await db.users.update_one({'_id': user['_id']}, {'$set': {'game.status': 1}})

        if rival is None:
            pattern['text'] = 'Вы успешно начали поиск соперника!'
            pattern['reply_markup'] = await reply_builder(text='❌ Отмена')
        else:
            pattern['text'] = 'Соперник найден!'
            pattern['reply_markup'] = await reply_builder(text=['🎲', '⛔ Завершить'])
            await db.users.update_one(
                {'_id': user['_id']}, {'$set': {'game.status': 2, 'game.rid': rival['_id']}}
            )
            await db.users.update_one(
                {'_id': rival['_id']}, {'$set': {'game.status': 2, 'game.rid': user['_id']}}
            )

            await bot.send_message(rival['_id'], **pattern)
    elif user['game']['status'] == 1:
        pattern['text'] = 'Вы уже находитесь в поиске!'
    await m.answer(**pattern)


@router.message(F.text.lower().contains('отмена'))
async def cansel_game(m: Message, db: MDB):
    user = await db.users.find_one({'_id': m.from_user.id})
    if user['game']['status'] == 1:
        await db.users.update_one({'_id': user['_id']}, {'$set': {'game.status': 0}})
        kb = await reply_builder(text=['🔎 Поиск'])
        await m.answer('Вы отменили поиск соперника!', reply_markup=kb)


@router.callback_query(F.data == 'cubic_cansel')
async def l_g(c: CallbackQuery, db: MDB, bot: Bot):
    user = await db.users.find_one({'_id': c.from_user.id})
    rival = await db.users.find_one({'_id': user['game']['rid']})
    if user['game']['status'] == 2:
        if rival['game']['value'] > 0:
            kb = await reply_builder(text=['🔎 Поиск'])
            await c.message.answer('Вы покинули игру', reply_markup=ReplyKeyboardRemove())
            await bot.send_message(rival['_id'], 'Ваш соперник покинул игру, вы выиграли', reply_markup=kb)
            await db.users.update_many(
                {'_id': {'$in': [user['_id'], rival['_id']]}},
                {'$set': {'game.status': 0, 'game.value': 0, 'game.rid': ''}}
            )
            await db.users.update_one({'_id': user['_id']}, {"$inc": {'stats.losses': 1}})
            await db.users.update_one({'_id': rival['_id']}, {"$inc": {'stats.wins': 1}})
            await c.answer()


@router.message(F.text.lower().contains('завершить'))
async def leave_game(m: Message, db: MDB, bot: Bot):
    user = await db.users.find_one({'_id': m.from_user.id})
    if user['game']['status'] == 2:

        rival = await db.users.find_one({'_id': user['game']['rid']})
        if rival['game']['value'] > 0:
            kb = await inline_builder(text=['Уверен ✅'], callback_data=['cubic_cansel'])
            return await m.answer('Ваш соперник сделал ход, вы уверены что хотите выйти (вы проиграете)!',
                                  reply_markup=kb)
        kb = await reply_builder(text=['🔎 Поиск'])
        await m.answer('Вы покинули игру', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(rival['_id'], 'Ваш соперник покинул игру', reply_markup=kb)

        await db.users.update_many(
            {'_id': {'$in': [user['_id'], rival['_id']]}},
            {'$set': {'game.status': 0, 'game.value': 0, 'game.rid': ''}}
        )


@router.message(F.dice.emoji == DiceEmoji.DICE)
async def game(m: Message, db: MDB, bot: Bot):
    user = await db.users.find_one({'_id': m.from_user.id})
    results = ['Ничья!', 'Ничья!']

    update_data = {'$set': {'game.value': 0}}

    if user['game']['status'] == 2:
        if user['game']['value'] > 0:
            return await m.answer('Вы не можете выкинуть кубик второй раз')
        rival = await db.users.find_one({'_id': user['game']['rid']})

        uvalue = m.dice.value
        rvalue = rival['game']['value']

        await db.users.update_one({'_id': user['_id']}, {'$set': {'game.value': uvalue}})

        if rvalue > 0:
            if rvalue > uvalue:
                await db.users.update_one({'_id': user['_id']}, {"$inc": {'stats.losses': 1}})
                await db.users.update_one({'_id': rival['_id']}, {"$inc": {'stats.wins': 1}})

                results = ['Вы проиграли!', 'Вы выиграли!']
            elif rvalue < uvalue:
                await db.users.update_one({'_id': user['_id']}, {"$inc": {'stats.wins': 1}})
                await db.users.update_one({'_id': rival['_id']}, {"$inc": {'stats.losses': 1}})

                results = ['Вы проиграли!', 'Вы выиграли!'][::-1]
            else:
                update_data['$inc'] = {'stats.tie': 1}

            await m.answer(f'{results[0]} {hcode(uvalue)} | {hcode(rvalue)}', parse_mode='html')
            await bot.send_message(rival['_id'], f'{results[1]} {hcode(uvalue)} | {hcode(rvalue)}', parse_mode='html')

            await db.users.update_many(
                {'_id': {'$in': [user['_id'], rival['_id']]}},
                update_data
            )
