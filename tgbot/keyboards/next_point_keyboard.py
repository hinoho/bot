from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

next_point_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton(text='Go to the next point'))
