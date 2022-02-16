from sqlalchemy import Column, ForeignKey, BigInteger, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.base import Base


class User(Base):
    __tablename__ = "user"

    telegram_id = Column(BigInteger, primary_key=True)


class ChannelAd(Base):
    __tablename__ = "channel_ad"

    chat_id = Column(BigInteger, primary_key=True)
    joinchat_url = Column(Text, nullable=False)
    name = Column(Text, nullable=False)

    def get_text_with_url_parse_mode_html(self) -> str:
        return f"<a href='{self.joinchat_url}'>{self.name}</a>"

    @classmethod
    async def get_all_channel_ad(cls,  session: AsyncSession) -> list:
        channels_ad_request = await session.execute(select(cls))
        return channels_ad_request.scalars().all()

    @classmethod
    async def get_channel_ad(cls, session: AsyncSession, chat_id: int):
        channel_ad_request = await session.execute(
            select(cls).where(cls.chat_id == chat_id)
        )
        return channel_ad_request.scalars().first()


class Dialogue(Base):
    __tablename__ = "dialogue"

    user1 = Column(BigInteger, ForeignKey('user.telegram_id'), primary_key=True)
    user2 = Column(BigInteger, ForeignKey('user.telegram_id'), primary_key=True)

    def get_interlocutor(self, telegram_id: int):
        if self.user1 == telegram_id:
            return int(self.user2)
        else:
            return int(self.user1)

    @classmethod
    async def get_dialogue_with_user(cls, session: AsyncSession, telegram_id: int):
        """
        If no dialogue return None

        :return: Dialogue or None
        """
        dialogue_request = await session.execute(
            select(cls).where((cls.user1 == telegram_id) | (cls.user2 == telegram_id))
        )
        return dialogue_request.scalars().first()


class Queue(Base):
    __tablename__ = "queue"

    user = Column(BigInteger, ForeignKey('user.telegram_id'), primary_key=True)

    @classmethod
    async def get_random_queue(cls, session: AsyncSession):
        """
        If the queue is empty it return None

        :return: Queue or None
        """

        queue_request = await session.execute(select(cls).order_by(func.random()))
        return queue_request.scalars().first()
