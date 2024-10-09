from aiogram import types, Dispatcher
from random import choice
import os

async def commands_start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Добро пожалавать {name} чем могу помочь?')

async def picture_send(message: types.Message):
    photo_path = os.path.join('images', '344367ffa26a0bf308806ed9f55613bc.jpg')
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(
            photo=photo,
            caption="СТАР ПЛАТИНУМ")

def game_dice(games: list) -> str:
    return choice(games)
async def random_game_handler(message: types.Message):
    games = ['⚽️', '🎰', '🏀', '🎯', '🎳', '🎲']
    await message.answer(game_dice(games))

def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(picture_send, commands=['pic'])
    dp.register_message_handler(random_game_handler, commands=['game'])
