import asyncio, logging, os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from HANDLERS.user_private_handler import handler_router
from HANDLERS.user_group_handler import user_group_router
from FSM.fsm import fsm_router
from config import Config, load_config
from DATABASE.engine import create_db, session_maker
from MIDDLEWARS.db import DataBaseSession



config : Config = load_config()

bot = Bot(token=config.tg_bot.token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = []

dp = Dispatcher()
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')
async def main():

    dp.startup.register(create_db)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_router(fsm_router)
    dp.include_router(handler_router)
    dp.include_router(user_group_router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)





if __name__ == '__main__':
    asyncio.run(main())