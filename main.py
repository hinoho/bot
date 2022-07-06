import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.handlers.route_handler import register_route
from tgbot.handlers.start import register_start

from tgbot.utils.db.db_helper import create_db

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    #dp.setup_middleware(DbMiddleware())
    pass


def register_all_filters(dp):
    #dp.filters_factory.bind(AdminFilter)
    pass


def register_all_handlers(dp):
    #register_admin(dp)
    #register_user(dp)
    register_start(dp)
    register_route(dp)

    pass


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2(password=config.tg_bot.redis_pass) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    #register_all_middlewares(dp)
    #register_all_filters(dp)
    register_all_handlers(dp)

    await create_db(f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}")

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")