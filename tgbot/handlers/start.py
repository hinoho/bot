from aiogram import types, Dispatcher

from tgbot.keyboards.start_route_keyboard import start_route_keyboard
from tgbot.states.route import Route


async def start(message: types.Message):
    user_id = message.chat.id
    #запрос всех ид пользователей из бд
    list_of_ids = [347807375]
    if user_id not in list_of_ids:
        await message.answer("Привет! \nЗарегестрируйся")
        #регистрация
    else:
        # запрос маршрута из бд
        list_of_routs = [1]
        if not list_of_routs:
            await message.answer("Привет! \nМаршрута на сегодня нет")
        else:
            await message.answer("Привет! \nМаршрут на сегодня:", reply_markup=start_route_keyboard)
            await Route.next_point.set()


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])