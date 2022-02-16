from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("next", "поиск следующего собеседника"),
            types.BotCommand("stop", "остановить диалог"),
            types.BotCommand("start", "перезапустить бота")
        ]
    )
