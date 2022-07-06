from typing import List

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram_media_group import media_group_handler

from tgbot.states.route import Route

from tgbot.keyboards.next_point_keyboard import next_point_keyboard
from tgbot.keyboards.arrival_keyboard import arrival_keyboard
from tgbot.keyboards.photo_keyboard import photo_keyboard

from tgbot.utils.db.schemas.quick_commands import update_point, get_next_point, select_user


async def arrival_handler(message: types.Message, state: FSMContext):
    await state.update_data(longitude=message.location.longitude,
                            latitude=message.location.latitude,
                            time=str(message.date),
                            photos='')
    await message.answer(f"Send photo", reply_markup=photo_keyboard)
    await Route.next()


async def photo_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos')
    photo_id = message.photo[0].file_id
    await message.photo[-1].download(f"{photo_id}.jpg")
    if photos == '':
        photos = photo_id
    else:
        photos = photos + '\n' + photo_id
    await state.update_data(photos=photos)


@media_group_handler
async def album_handler(messages: List[types.Message], state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos')
    for message in messages:
        photo_id = message.photo[0].file_id
        await message.photo[-1].download(f"{photo_id}.jpg")
        if photos == '':
            photos = photo_id
        else:
            photos = photos + '\n' + photo_id
    await state.update_data(photos=photos)


async def photo_done_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    longitude = data.get("longitude")
    latitude = data.get('latitude')
    time = data.get('time')
    photos = data.get('photos')
    await message.answer(f"longitude: {longitude}")
    await message.answer(f"latitude: {latitude}")
    await message.answer(f"time: {time}")
    lenght = len(photos.split('\n'))
    await message.answer(f"photos: {lenght}")
    await message.answer(f"photos: {photos}")
    user = await select_user(message.chat.id)
    await update_point(user.id)
    await message.answer('Go to the next point', reply_markup=next_point_keyboard)
    await Route.next_point.set()


async def next_point_handler(message: types.Message, state: FSMContext):
    user = await select_user(message.chat.id)
    point = await get_next_point(user.id)
    if point:
        await message.answer(f"Next point: {point.address}", reply_markup=arrival_keyboard)
        await Route.next()
    else:
        await message.answer("end of route")
        await state.finish()


def register_route(dp: Dispatcher):
    dp.register_message_handler(arrival_handler, state=Route.arrived, content_types=['location'])
    dp.register_message_handler(next_point_handler, state=Route.next_point)
    dp.register_message_handler(album_handler, MediaGroupFilter(is_media_group=True), state=Route.photo,
                                content_types=['photo'])
    dp.register_message_handler(photo_handler, state=Route.photo, content_types=['photo'])
    dp.register_message_handler(photo_done_handler, state=Route.photo, content_types=types.ContentTypes.TEXT,
                                regexp='Done')
