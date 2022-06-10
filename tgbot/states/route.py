from aiogram.dispatcher.filters.state import StatesGroup, State


class Route(StatesGroup):
    next_point = State()
    arrived = State() #прибыл на точку, отправить коорди, время
    photo = State()