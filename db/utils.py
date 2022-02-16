from data import config


def make_connection_string(async_fallback: bool = False) -> str:
    result = f"postgresql+asyncpg://" \
             f"{config.DB_LOGIN}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    if async_fallback:
        result += "?async_fallback=True"
    return result
