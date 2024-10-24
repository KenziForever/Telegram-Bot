from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db import db_main

cancel_button = types.KeyboardButton('Отмена')
cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel_button)

class fsm_store(StatesGroup):
    name_product = State()
    size = State()
    category = State()
    product_id = State()
    info_product = State()
    collection = State()
    price = State()
    photo = State()
    submit = State()

async def start_store(message: types.Message):
    await message.answer('Введите название товара: ', reply_markup=cancel_keyboard)
    await fsm_store.name_product.set()

async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text
    await message.answer('Введите размер товара: ', reply_markup=cancel_keyboard)
    await fsm_store.next()

async def load_size(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Введите категорию товара: ', reply_markup=cancel_keyboard)
    await fsm_store.next()

async def load_category(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.answer('Введите артикул товара: ', reply_markup=cancel_keyboard)
    await fsm_store.next()

async def load_product_id(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text
    await message.answer('Введите инфо о товара: ', reply_markup=cancel_keyboard)
    await fsm_store.next()

async def load_info_product(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text
    await message.answer('Введите коллекцию: ', reply_markup=cancel_keyboard)
    await fsm_store.next()


async def load_collection(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text
    await message.answer('Ввведите цену товара : ', reply_markup=cancel_keyboard)
    await fsm_store.next()


async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фото товара: ', reply_markup=cancel_keyboard)
    await fsm_store.next()

async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Верные ли данные: \n'
                f'Название - {data["name_product"]}\n'
                f'Размер - {data["size"]}\n'
                f'Категория - {data["category"]}\n'
                f'Цена - {data["price"]}\n'
                f'Цена - {data["collection"]}\n',
        reply_markup=buttons.submit
    )
    await fsm_store.next()

async def submit(message: types.Message, state=FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await db_main.sql_insert_store(
                name_product=data['name_product'],
                size=data['size'],
                product_id=data['product_id'],
                price=data['price'],
                photo=data['photo']
            )
            await db_main.sql_insert_store_detail(
                product_id=data['product_id'],
                category=data['category'],
                info_product=data['info_product']
            )
            await db_main.sql_insert_store_collection(
                product_id=data['product_id'],
                collection=data['collection']
            )
        await message.answer('Товар в базе!')
        await state.finish()
    elif message.text == 'Нет':
        await message.answer('Отменено!')
        await state.finish()
    else:
        await message.answer('Для дальнейщего действия, нажмите на кнопки ниже')

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=types.ReplyKeyboardRemove())

def register_handlers_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_store, commands=['store'])
    dp.register_message_handler(load_name, state=fsm_store.name_product)
    dp.register_message_handler(load_size, state=fsm_store.size)
    dp.register_message_handler(load_category, state=fsm_store.category)
    dp.register_message_handler(load_product_id, state=fsm_store.product_id)
    dp.register_message_handler(load_info_product, state=fsm_store.info_product)
    dp.register_message_handler(load_collection, state=fsm_store.collection)
    dp.register_message_handler(load_photo, state=fsm_store.photo, content_types=['photo'])
    dp.register_message_handler(load_price, state=fsm_store.price)
    dp.register_message_handler(submit, state=fsm_store.submit)
