from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = config('BOT_TOKEN')
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

