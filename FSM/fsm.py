from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from CONFIG.words_for_the_bot import match
fsm_router = Router()

class AddStates(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()


@fsm_router.message(StateFilter(None), Command("add_product"))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название продукта:")
    await state.set_state(AddStates.name)


@fsm_router.message(AddStates.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text.isalpha and match(message.text):
        await state.update_data(name=message.text)
        await message.answer("Введите описание продукта:")
        await state.set_state(AddStates.description)
    else:
        await message.answer("<b>[NOTE!]</b> Название должно содержать только РУССКИЕ буквы")

@fsm_router.message(AddStates.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    if message.text.isalpha and match(message.text):
        await state.update_data(description=message.text)
        await message.answer("Введите цену продукта:")
        await state.set_state(AddStates.price)
    else:
        await message.answer("<b>[NOTE!]</b> Описание продукта должно содержать только буквы")


@fsm_router.message(AddStates.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=message.text)
        await message.answer("Загрузите изображение продукта:")
        await state.set_state(AddStates.image)
    else:
        await message.answer("<b>[NOTE!]</b> Цена должно содержать только целочисленные значение")


@fsm_router.message(AddStates.image, F.photo)
async def set_image(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        await message.answer("Товар добавлен", reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        await message.answer(str(data))
        await state.clear()
    else:
        await message.answer("<b>[NOTE!]</b> Загрузите изображение")

