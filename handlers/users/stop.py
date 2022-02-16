from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

from dialogue.end import end_dialogue
from loader import dp


@dp.message_handler(state="*", commands="stop")
async def bot_next(message: types.Message, session: AsyncSession):
    await message.answer("Диалог остановлен. Чтобы начать новый нажмите /next")
    await end_dialogue(dp, message.from_user.id, session)
    await session.commit()
