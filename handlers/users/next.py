from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

from dialogue import end_dialogue, new_dialogue
from utils import checks_subscription

from loader import dp


@dp.message_handler(state="*", commands="next")
@checks_subscription
async def bot_next(message: types.Message, session: AsyncSession, *args, **kwargs):

    await end_dialogue(dp, message.from_user.id, session)

    await new_dialogue(dp, message.from_user.id, session)

    await session.commit()
