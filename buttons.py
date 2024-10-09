from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(KeyboardButton('Отмена'))