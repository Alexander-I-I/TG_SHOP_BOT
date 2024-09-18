import os
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from DATABASE.orm_query import orm_get_products
from FILTERS.filters import ChatTypeFilter, IsAdmin
from aiogram.types import Message, FSInputFile
from KEYBOARDS.keyboard import get_keyboard
from KEYBOARDS.inline import get_callback_btns

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')


handler_router = Router()
handler_router.message.filter(ChatTypeFilter(["private"]))

@handler_router.message(Command('start'))
async def start_cmd(message: types.Message):
    photo_file = FSInputFile(path=os.path.join(all_media_dir, '6.jpg'))
    await message.answer_photo(photo=photo_file,
                               caption=f"Привет👋<b>{message.from_user.first_name}</b>, я 🤖виртуальный помощник магазина <b>Шестёрочка</b>6️⃣\n\n📝Выбери команду для дальнейших действий:\n\n"
                         f"🏬Ассортимен магазина - /assortment\n🆘Помощь - /help")

@handler_router.message(Command('assortment'))
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)} руб.",)

@handler_router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("I can help you with the following commands:\n1. /start - start the chatbot\n2. /help - get help")


# @handler_router.message(F.text | F.sticker | F.audio | F.document | F.photo | F.video | F.voice)
# async def echo(message: types.Message):
#     await message.delete()
#     await message.answer(f"Извините, <b>{message.from_user.first_name}</b>, но я не могу отвечать только на ваши команды!\n"
#                          f"Перечень команд можно узнать с помощью /help или в боковом меню")