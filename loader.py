import os
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from handlers import (
    cansel,
    games,
    horo,
    lightning,
    smart,
    weather,
    cubic_game_main,
    start,
)
from handlers.sovmest import sovmest
from misk.commands import set_bot_commands

load_dotenv()
cluster = AsyncIOMotorClient(
    f'mongodb+srv://kerrek8:{str(os.getenv("MDBPASSWORD"))}@aiogrambot.2vjshy0.mongodb.net/''?retryWrites=true&w=majority')
db = cluster.cubic_game

bot = Bot(os.getenv("TOKEN"))
webhook_uri = 'https://aio3bot.onrender.com' + '/' + str(os.getenv('TOKEN'))
dp = Dispatcher(db=db, bot=bot)
dp.include_routers(
    cansel.router, games.router, horo.router, smart.router, lightning.router, weather.router, sovmest.router,
    start.router,  cubic_game_main.router
)


async def start():
    await set_bot_commands(bot)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start()
    print(await bot.set_webhook(url=webhook_uri, allowed_updates=[]), 'webhook was set')
    yield
    print(await bot.delete_webhook(drop_pending_updates=True), 'webhooks was deleted')
    await bot.session.close()


app = FastAPI(docs_url=None, lifespan=lifespan)


@app.post('/' + str(os.getenv("TOKEN")))
async def webhook_response(update: dict):
    return await dp.feed_update(bot=bot, update=Update(**update))


@app.get('/')
async def alive():
    return "Alive"
