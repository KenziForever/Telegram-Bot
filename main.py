from aiogram import executor
import logging
from config import dp, bot
from handlers import commands, squaring, quiz, FSM_reg, FSM_store


quiz.register_handler_quiz(dp)
commands.register_handlers_commands(dp)
FSM_reg.register_handlers_registration(dp)
FSM_store.store_handler_storing(dp)
squaring.register_handler_squaring(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
