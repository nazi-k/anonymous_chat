from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from db.models import User

from loader import dp


@dp.message_handler(state="*", commands="start")
async def bot_start(message: types.Message, session: AsyncSession):
    await message.answer("Нажмите /next чтобы начать чат с незнакомцем")
    stmt = insert(User).values(telegram_id=message.from_user.id)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=[User.telegram_id])
    await session.execute(stmt)
    await session.commit()
