from aiogram import Dispatcher, Bot

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Dialogue
from states.dialogue import DialogueState


async def end_dialogue(dp: Dispatcher, telegram_id_who_skip: int, session: AsyncSession, dialogue: Dialogue = None):
    if not dialogue:
        dialogue = await Dialogue.get_dialogue_with_user(session, telegram_id_who_skip)

    await DialogueState.finish_on_dialogue_state(dp, telegram_id_who_skip)

    if dialogue:
        telegram_id_which_skip = dialogue.get_interlocutor(telegram_id_who_skip)

        await DialogueState.finish_on_dialogue_state(dp, telegram_id_which_skip)

        await notify_you_skip(dp.bot, telegram_id_which_skip)

        await session.delete(dialogue)


async def notify_you_skip(bot: Bot, telegram_id: int):
    await bot.send_message(telegram_id, "Ваш собеседник прервал диалог, нажмите /next чтобы найти нового")
