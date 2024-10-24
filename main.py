from aiogram import executor
import logging
from config import dp, bot, Admins
from handlers import commands, squaring, quiz, FSM_reg, FSM_store, send_products, edit_products
from db import db_main

async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin,
                               text='Бот включен!')
        await db_main.sql_create()

async def on_shutdown(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin,
                               text='Бот выключен!')

quiz.register_handler_quiz(dp)
commands.register_handlers_commands(dp)
FSM_reg.register_handlers_registration(dp)
FSM_store.register_handlers_store(dp)
send_products.register_send_products_handler(dp)
edit_products.register_update_handler(dp)

squaring.register_handler_squaring(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
