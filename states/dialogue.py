from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher


class DialogueState(StatesGroup):
    on_dialogue = State()

    @staticmethod
    async def finish_on_dialogue_state(dp: Dispatcher, telegram_id: int) -> None:
        await dp.get_current().current_state(chat=telegram_id, user=telegram_id).finish()

    @staticmethod
    async def set_on_dialogue_state(dp: Dispatcher, telegram_id: int) -> None:
        await dp.get_current().current_state(chat=telegram_id, user=telegram_id).set_state(
            DialogueState.on_dialogue.state)
