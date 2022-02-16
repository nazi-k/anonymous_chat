from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

from loader import dp


@dp.message_handler(state="*", commands="start")
async def bot_start(message: types.Message, session: AsyncSession):
    await message.answer("Нажмите /next чтобы начать чат с незнакомцем")
    user = User(telegram_id=message.from_user.id)
    session.add(user)
    await session.commit()
