from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


class fcm_storing(StatesGroup):
    name = State()
    category = State()
    price = State()
    size = State()
    photo = State()

async def start_store(message: types.Message):
    await message.answer(text='Введите названия одежды:', reply_markup=buttons.cancel)
    await fcm_storing.name.set()

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message.answer('Введите категорию одежды:')
        await fcm_storing.next()

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
        await message.answer('Введите цену:')
        await fcm_storing.next()

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('S', 'L', 'M', 'XL')
        await message.answer('Введите размер:', reply_markup=markup)
        await fcm_storing.next()

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
        await message.answer('Отправьте фото одежды:')
        await fcm_storing.next()

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

        await message.answer_photo(photo=data['photo'],
                                   caption=f'Данные:\n'
                                   f'Название - {data["name"]}\n'
                                   f'Категория - {data["category"]}\n'
                                   f'Цена - {data["price"]}\n'
                                   f'Размер - {data["size"]}\n')

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Да'), KeyboardButton('Нет'))
        await message.answer('Верны ли данные?', reply_markup=markup)

async def Yes_Not_fsm(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer('Данные сохранены.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Данные не сохранены', reply_markup=ReplyKeyboardRemove())

    await state.finish()

def store_handler_storing(dp: Dispatcher):
    dp.register_message_handler(start_store, commands="store", state=None)
    dp.register_message_handler(load_name, state=fcm_storing.name)
    dp.register_message_handler(load_category, state=fcm_storing.category)
    dp.register_message_handler(load_price, state=fcm_storing.price)
    dp.register_message_handler(load_size, state=fcm_storing.size)
    dp.register_message_handler(load_photo, content_types=['photo'], state=fcm_storing.photo)
    dp.register_message_handler(Yes_Not_fsm, Text(equals=["Да", "Нет"]), state=fcm_storing.photo)

