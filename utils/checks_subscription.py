from aiogram.types import Message, ChatMemberLeft
from aiogram.utils.exceptions import Unauthorized, BadRequest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models import ChannelAd

from utils.notify_admins import bot_not_member_channel
from dialogue.end import end_dialogue

from loader import dp


def get_need_subscribe_text(channels: list[ChannelAd]) -> str:
    text = "Наш чат абсолютно бесплатный, но вам нужно быть подписанными на каналы наших спонсоров:\n"
    for channel in channels:
        text += f"👉 {channel.get_text_with_url_parse_mode_html()}\n"
    text += "\nПодпишитесь на ВСЕ каналы и нажмите /next для поиска собеседника"

    return text


def checks_subscription(func):

    async def wrapper(*args, **kwargs):

        message: Message = None
        session: AsyncSession = dp.middleware.applications[0].session_pool()
        for arg in args:
            if isinstance(arg, Message):
                message = arg
                break

        if not message:
            raise ValueError("no argument Message")

        channels_ad_request = await session.execute(select(ChannelAd))

        channels_ad = channels_ad_request.scalars().all()

        channels_without_subscription = []

        for channel_ad in channels_ad:
            try:
                chat_member = \
                    (await message.bot.get_chat_member(chat_id=channel_ad.chat_id, user_id=message.from_user.id))
                if isinstance(chat_member, ChatMemberLeft):
                    channels_without_subscription.append(channel_ad)
            except Unauthorized:
                await bot_not_member_channel(message.bot, channel_ad)
            except BadRequest:
                await bot_not_member_channel(message.bot, channel_ad)

        if channels_without_subscription:
            await message.answer(get_need_subscribe_text(channels_without_subscription), disable_web_page_preview=True)
            await end_dialogue(dp, message.from_user.id, session)

        else:
            return await func(*args, **kwargs)

    return wrapper


