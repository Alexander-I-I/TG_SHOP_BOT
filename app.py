import asyncio, logging, os
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from dotenv import load_dotenv
from HANDLERS.handler import handler_router
from FSM.fsm import fsm_router
from config import Config, load_config

config : Config = load_config()

bot = Bot(token=config.tg_bot.token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')
async def main():


    dp.include_router(handler_router)
    dp.include_router(fsm_router)



    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)





if __name__ == '__main__':
    asyncio.run(main())