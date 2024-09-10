from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

handler_router = Router()


@handler_router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Hello, I'm a simple chatbot. I can help you with basic tasks.")


@handler_router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("I can help you with the following commands:\n1. /start - start the chatbot\n2. /help - get help")
