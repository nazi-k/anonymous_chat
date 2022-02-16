from environs import Env
import os

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов

DB_HOST = env.str("postgres_host")
DB_PORT = env.int("postgres_port")
DB_NAME = env.str("postgres_name")
DB_LOGIN = env.str("postgres_login")
DB_PASSWORD = env.str("postgres_password")
HEROKU_APP_NAME = env.str("app_name")

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = env.str("ip")
WEBAPP_PORT = int(os.environ.get('PORT', 5000))
