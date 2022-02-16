from aiogram.utils.executor import start_webhook

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    await dp.bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
