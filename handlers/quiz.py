from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot


async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Далее', callback_data='quiz_2')

    keyboard.add(button)

    question = 'В каком году открылся GEEKS?'

    answer = ['2019', '2018', '2021', '2017']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation='Как ты мог не знать этого....',
        open_period=20,
        reply_markup=keyboard
    )

async def quiz_2(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Далее', callback_data='quiz_3')

    keyboard.add(button)

    question = 'Сколько хромосом у человека'
    answer = ['52', '17', '46', '39']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation='Это у тебя столько)',
        open_period=20,
        reply_markup=keyboard
    )

async def quiz_3(call: types.CallbackQuery):
    question = 'Как называется самое большое озеро в мире?'
    answer = ['Байкал', 'Каспийское море', 'Виктория', 'Иссык-куль']
    await bot.send_photo(chat_id=call.from_user.id,
                         photo=open('images/Caspiii.jpg', 'rb'))

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
        explanation='Хотя это и называется море по сути оно является самым большим озером в мире по площади',
        open_period=20
    )

def register_handler_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='quiz_2')
    dp.register_callback_query_handler(quiz_3, text='quiz_3')


