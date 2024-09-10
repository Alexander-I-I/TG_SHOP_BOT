from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

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


@fsm_router.message(AddStates.name)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание продукта:")
    await state.set_state(AddStates.description)


@fsm_router.message(AddStates.description)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену продукта:")
    await state.set_state(AddStates.price)


@fsm_router.message(AddStates.price)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение продукта:")
    await state.set_state(AddStates.image)


@fsm_router.message(AddStates.image, F.photo)
async def set_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Товар добавлен", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

