from aiogram import types, Dispatcher

from tgbot.keyboards.start_route_keyboard import start_route_keyboard
from tgbot.states.route import Route

from tgbot.utils.db.schemas.quick_commands import select_all_users, add_points, get_points, add_user, select_user


async def start(message: types.Message):
    telegram_id = message.chat.id
    list_of_ids = await select_all_users()
    if telegram_id not in list_of_ids:
        id = await add_user(telegram_id)
        await message.answer(f"New user: {telegram_id}")
        await add_points(id, ['first point', 'second point'])
    user = await select_user(telegram_id)
    list_of_points = await get_points(user.id)
    if not list_of_points:
        await message.answer("No route")
    else:
        answer = "Route: "
        for point in list_of_points:
            answer += f"\n {point.id}: {point.address}"
        await message.answer(answer, reply_markup=start_route_keyboard)
        await Route.next_point.set()


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])