from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

import re

from db.models import Dialogue
from states.dialogue import DialogueState
from utils import checks_subscription
from dialogue import end_dialogue
from dialogue.end import notify_you_skip

from loader import dp


@dp.message_handler(content_types=types.ContentTypes.all(), state=DialogueState.on_dialogue)
@checks_subscription
async def bot_dialogue(message: types.Message, session: AsyncSession, *args, **kwargs):
    dialogue = await Dialogue.get_dialogue_with_user(session, message.from_user.id)
    if dialogue:
        if not is_message_with_url(message):
            await message.send_copy(dialogue.get_interlocutor(message.from_user.id))
        else:
            await notify_forbidden_message(message)
    else:
        await end_dialogue(dp, message.from_user.id, session, dialogue)
        await notify_you_skip(dp.bot, message.from_user.id)


def is_message_with_url(message: types.Message) -> bool:
    if message["entities"]:
        for message_entity in message["entities"]:
            if message_entity["type"] == "url":
                return True

    if message["caption_entities"]:
        for message_caption_entity in message["caption_entities"]:
            if message_caption_entity["type"] == "url":
                return True

    return False


async def notify_forbidden_message(message: types.Message) -> None:
    await message.answer("Такое сообщение нельзя отправлять!")
