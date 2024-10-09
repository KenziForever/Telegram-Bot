from aiogram import types, Dispatcher

async def squaring_send(message: types.Message):
    text = message.text
    if text.isdigit():
        number = int(text)
        squared_number = number ** 2
        await message.answer(str(squared_number))
    else:
        await message.answer(text)


def register_handler_squaring(dp: Dispatcher):
    dp.register_message_handler(squaring_send)
