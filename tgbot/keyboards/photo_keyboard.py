from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

photo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton(text='Done'))
