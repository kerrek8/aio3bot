from aiogram import types
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    bot_c = [
        types.BotCommand(command='/start', description='перезапустить бота'),
        # types.BotCommand(command='/cubic_game', description='игра в бросок кубика'),
        # types.BotCommand(command='/weather', description='погода'),
        # types.BotCommand(command='/lightning', description="калькулятор молний"),
        # types.BotCommand(command='/game', description='игры'),
        # types.BotCommand(command='/horoscope', description='гороскоп'),
        # types.BotCommand(command='/sovmestimost', description='совместимость знаков зодиака'),
        # types.BotCommand(command='/smart', description='умная мысль'),
        # types.BotCommand(command='/cansel', description='Отмена')
    ]
    a = await bot.set_my_commands(bot_c)
    print(a, "commands was set")
