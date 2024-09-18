from aiogram import F, Bot, types, Router
from aiogram.filters import Command
from FILTERS.filters import ChatTypeFilter


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    # print(admins_list)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


@user_group_router.message(F.text)
async def censure(message: types.Message, bot: Bot):

    with open('bad-word.text', 'r') as file:
        censored_letters = [line.strip() for line in file]
    for word in censored_letters:
        if word in message.text.lower():
            await message.delete()
            await message.answer(f"Юзер - <b>{message.from_user.first_name}</b>\nБез мата, пожалуйста ⛔")
