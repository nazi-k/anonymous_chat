from aiogram import Dispatcher, Bot

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Dialogue, Queue
from states.dialogue import DialogueState


async def new_dialogue(dp: Dispatcher, telegram_id: int, session: AsyncSession) -> None:
    queue = await Queue.get_random_queue(session)

    if queue and queue.user != telegram_id:

        await DialogueState.set_on_dialogue_state(dp, telegram_id)
        await DialogueState.set_on_dialogue_state(dp, queue.user)

        await notify_start_dialogue(dp.bot, telegram_id)
        await notify_start_dialogue(dp.bot, queue.user)

        dialogue = Dialogue(user1=telegram_id, user2=queue.user)

        session.add(dialogue)

        await session.delete(queue)

    else:
        queue = Queue(user=telegram_id)
        session.add(queue)


async def notify_start_dialogue(bot: Bot, telegram_id: int) -> None:
    await bot.send_message(telegram_id, "Собеседник найден!\nНапишите что-нибудь. "
                                        "Чтобы остановить чат напишите /stop, чтобы начать новый напишите /next")
