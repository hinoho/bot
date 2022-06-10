from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_route_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton(text='Начать маршрут'))
