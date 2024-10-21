import sqlite3
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

# Глобальный индекс текущего товара
current_product_index = 0

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM store s 
    INNER JOIN detail_store ds 
    ON s.product_id = ds.product_id 
    """).fetchall()
    conn.close()
    return products

def fetch_product_by_index(index):
    products = fetch_all_products()
    if 0 <= index < len(products):
        return products[index]
    return None

async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all')
    button_one = types.InlineKeyboardButton('Вывести по одному', callback_data='one')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как отправятся товары:', reply_markup=keyboard)

async def sendall_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    if products:
        for product in products:
            caption = (f'Название - {product["name_product"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Цена - {product["price"]}\n'
                       f'Артикул - {product["product_id"]}\n\n'
                       f'Информация о товаре - {product["info_product"]}')

            await callback_query.message.answer_photo(
                photo=product["photo"],
                caption=caption
            )
    else:
        await callback_query.message.answer('Товаров нет!')

async def send_one_product(callback_query: types.CallbackQuery):
    global current_product_index
    product = fetch_product_by_index(current_product_index)

    if product:
        caption = (f'Название - {product["name_product"]}\n'
                   f'Размер - {product["size"]}\n'
                   f'Категория - {product["category"]}\n'
                   f'Цена - {product["price"]}\n'
                   f'Артикул - {product["product_id"]}\n\n'
                   f'Информация о товаре - {product["info_product"]}')

        delete_keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
        next_button = types.InlineKeyboardButton('Следующий', callback_data='next_product')
        delete_keyboard.add(delete_button, next_button)

        await callback_query.message.answer_photo(
            photo=product["photo"],
            caption=caption,
            reply_markup=delete_keyboard
        )
    else:
        await callback_query.message.answer('Товар жок!')

async def show_next_product(callback_query: types.CallbackQuery):
    global current_product_index
    current_product_index += 1
    product = fetch_product_by_index(current_product_index)

    if product:
        await send_one_product(callback_query)
    else:
        await callback_query.message.answer('Больше товаров нет!')

def register_send_products_handler(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['products'])
    dp.register_callback_query_handler(sendall_products, Text(equals='all'))
    dp.register_callback_query_handler(send_one_product, Text(equals='one'))
    dp.register_callback_query_handler(show_next_product, Text(equals='next_product'))

