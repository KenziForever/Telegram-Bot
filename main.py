import asyncio
from aiogram import Bot, Dispatcher, executor, types
import logging
from decouple import config
import os

token = config('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Добро пожалавать {name} чем могу помочь?')

@dp.message_handler(commands=['star'])
async def picture_send(message: types.Message):
    photo_path = os.path.join('images', '344367ffa26a0bf308806ed9f55613bc.jpg')
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(
        photo = photo,
        caption="СТАР ПЛАТИНУМ")

@dp.message_handler()
async def squaring_send(message: types.Message):
    text = message.text
    if text.isdigit():
        number = int(text)
        squared_number = number ** 2
        await message.answer(str(squared_number))
    else:
        await message.answer(text)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp,)
