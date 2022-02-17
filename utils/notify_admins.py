import logging

from aiogram import Bot

from data.config import ADMINS

from db.models import ChannelAd


async def bot_not_member_channel(bot: Bot, channel: ChannelAd):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"Бот не є адміністратором каналу "
                                          f"{channel.get_text_with_url_parse_mode_html()}",
                                   disable_web_page_preview=True)

        except Exception as err:
            logging.exception(err)
