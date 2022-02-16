from aiogram import types
from aiogram.dispatcher.filters import IDFilter, RegexpCommandsFilter

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ChannelAd

from data.config import ADMINS

from loader import dp


@dp.message_handler(IDFilter(ADMINS), RegexpCommandsFilter(regexp_commands=['add([\s?.+])']), state="*")
async def add_channel(message: types.Message, session: AsyncSession):
    try:
        chat_id = message.reply_to_message.forward_from_chat.id
        url = message.text.split(' ')[1]
        text = normalization_quotes(message.text).split('"')[1]
        channel_ad = ChannelAd(chat_id=chat_id, joinchat_url=url, name=text)
        session.add(channel_ad)
        await session.commit()
        await message.answer(f"Добавлено: {channel_ad.get_text_with_url_parse_mode_html()}",
                             disable_web_page_preview=True)
    except AttributeError:
        await message.answer(get_wrong_format_text(), disable_web_page_preview=True)


@dp.message_handler(IDFilter(ADMINS), RegexpCommandsFilter(regexp_commands=['del([_\d*|\d*])']), state="*")
async def del_channel(message: types.Message, session: AsyncSession):
    chat_id = int(message.text.split(' ')[0].replace('/del', '').replace('_', '-'))
    channel_ad = await ChannelAd.get_channel_ad(session, chat_id)
    await session.delete(channel_ad)
    await session.commit()
    await message.answer("Успішно видалено!")


@dp.message_handler(IDFilter(ADMINS), commands="add", state="*")
async def add_info(message: types.Message):
    await message.answer(get_wrong_format_text(), disable_web_page_preview=True)


@dp.message_handler(IDFilter(ADMINS), commands="del", state="*")
async def del_info(message: types.Message, session: AsyncSession):
    await message.answer(get_commands_del_text(await ChannelAd.get_all_channel_ad(session)),
                         disable_web_page_preview=True)


def get_wrong_format_text() -> str:
    return "Чекаю повідомлення формату:\n" \
           "(відповідь на переслане повідомлення з потрібного каналу/групи)\n" \
           "url[приклад:https://t.me/joinchat/T1jUGhLBKjE2MzBi або https://t.me/+T1jUGhLBKjE2MzBi]\n" \
           'text[приклад:"Новини про спорт⚽"]\n' \
           '/add url "text"'


def get_commands_del_text(channels_ad: list[ChannelAd]) -> str:
    commands_del = "Виберіть канали/групи для видалення\n\n"
    for channel_ad in channels_ad:
        commands_del += f"/del{str(channel_ad.chat_id).replace('-', '_')} " \
                      f"{channel_ad.get_text_with_url_parse_mode_html()}\n"
    return commands_del


def normalization_quotes(text: str) -> str:
    for quotes in ('«', '»', '“', '”', '„'):
        text.replace(quotes, '"')
    return text
