from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

arrival_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton(text='I have arrived', request_location=True))
