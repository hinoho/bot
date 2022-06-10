from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

arrival_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton(text='Я прибыл', request_location=True))
