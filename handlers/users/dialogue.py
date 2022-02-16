from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

import re

from db.models import Dialogue
from states.dialogue import DialogueState
from utils import checks_subscription
from dialogue import end_dialogue
from dialogue.end import notify_you_skip

from loader import dp


@dp.message_handler(state=DialogueState.on_dialogue)
@checks_subscription
async def bot_dialogue(message: types.Message, session: AsyncSession, *args, **kwargs):
    dialogue = await Dialogue.get_dialogue_with_user(session, message.from_user.id)
    if dialogue:
        if not message.text or not is_text_with_url(message.text):
            await message.send_copy(dialogue.get_interlocutor(message.from_user.id))
        else:
            await notify_forbidden_message(message)
    else:
        await end_dialogue(dp, message.from_user.id, session, dialogue)
        await notify_you_skip(dp.bot, message.from_user.id)


def is_text_with_url(text: str) -> bool:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+" \
            r"|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)
    return bool(url)


async def notify_forbidden_message(message: types.Message) -> None:
    await message.answer("Такое сообщение нельзя отправлять!")
