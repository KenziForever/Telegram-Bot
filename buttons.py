from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = KeyboardButton('Отмена')
cancel.add(cancel_button)

submit = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Нет'))