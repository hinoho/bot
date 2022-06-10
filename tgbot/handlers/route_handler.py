from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.next_point_keyboard import next_point_keyboard
from tgbot.states.route import Route
from tgbot.keyboards.arrival_keyboard import arrival_keyboard


async def arrival_handler(message: types.Message, state: FSMContext):
    await state.update_data(longitude=message.location.longitude,
                            latitude=message.location.latitude,
                            time=message.date)
    await message.answer(f"Отправь фотографию")
    await Route.next()


async def photo_handler(message: types.Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    data = await state.get_data()
    longitude = data.get("longitude")
    latitude = data.get('latitude')
    time = data.get('time')
    await message.photo[-1].download('test.jpg')
    await message.answer('Отправиться на следующую точку', reply_markup=next_point_keyboard)
    await Route.next_point.set()


async def next_point_handler(message: types.Message, state: FSMContext):
    await message.answer(f"Следующая точка:", reply_markup=arrival_keyboard)
    await Route.next()


def register_route(dp: Dispatcher):
    dp.register_message_handler(arrival_handler, state=Route.arrived, content_types=['location'])
    dp.register_message_handler(photo_handler, state=Route.photo, content_types=['photo'])
    dp.register_message_handler(next_point_handler, state=Route.next_point)

