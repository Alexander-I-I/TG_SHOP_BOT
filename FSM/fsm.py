from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from KEYBOARDS.inline import get_callback_btns
from CONFIG.words_for_the_bot import match
from FILTERS.filters import ChatTypeFilter, IsAdmin
from DATABASE.orm_query import get_add_product, orm_get_products, orm_get_product, orm_add_user, orm_update_product, orm_delete_product

fsm_router = Router()
fsm_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

class AddStates(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None


@fsm_router.message(StateFilter(None), Command("add_product"))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название продукта:")
    await state.set_state(AddStates.name)

@fsm_router.message(Command('assortment'))
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)} руб.",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_{product.id}",
                    "Изменить": f"change_{product.id}",
                }
            ),
        )

@fsm_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар удален")
    await callback.message.answer("Товар удален!")


@fsm_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddStates.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара"
    )
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


@fsm_router.message(AddStates.image, or_f(F.photo, F.text == "."))
async def set_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(image=AddStates.product_for_change.image)

    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddStates.product_for_change:
            await orm_update_product(session, AddStates.product_for_change.id, data)
        else:
            await get_add_product(session, data)
        await message.answer("Товар добавлен/изменен")
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
        )
        await state.clear()

    AddStates.product_for_change = None
    #
    # else:
    #     await message.answer("<b>[NOTE!]</b> Загрузите изображение")

