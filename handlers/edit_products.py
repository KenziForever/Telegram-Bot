import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Edit_product(StatesGroup):
    for_field = State()
    for_new_value = State()
    for_photo = State()


def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM store s 
    INNER JOIN detail_store ds ON s.product_id = ds.product_id 
    INNER JOIN collection c ON c.products_id = c.product_id
    """).fetchall()
    conn.close()
    return products


def update_product_field(product_id, field_name, new_value):
    store_table = ["name_product", "size", "price", "photo"]
    store_detail_table = ["category", "info_product"]

    conn = get_db_connection()

    try:
        if field_name in store_table:
            query = f"UPDATE store SET {field_name} = ? WHERE product_id = ?"
        elif field_name in store_detail_table:
            query = f"UPDATE detail_store SET {field_name} = ? WHERE product_id = ?"
        else:
            raise ValueError(f'Нет такого поля {field_name}')

        conn.execute(query, (new_value, product_id))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'ОШибка - {e}')
    finally:
        conn.close()



async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2,
                                          resize_keyboard=True)

    button_all = types.InlineKeyboardButton('Вывести все товары',
                                            callback_data='all_update')
    button_one = types.InlineKeyboardButton('Вывести по одному',
                                            callback_data='one_update')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как отправятся товары:',
                         reply_markup=keyboard)


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

            delete_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
            delete_button = types.InlineKeyboardButton('Редактировать',
                                                       callback_data=f'edit_{product["product_id"]}')
            delete_keyboard.add(delete_button)
            await callback_query.message.answer_photo(
                photo=product["photo"],
                caption=caption,
                reply_markup=delete_keyboard
            )
    else:
        await callback_query.message.answer('Товар нет!')


async def edit_product(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]

    await state.update_data(product_id=product_id)

    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    name_button = InlineKeyboardButton(text="Название", callback_data="field_name_product")
    category_button = InlineKeyboardButton(text="Категория", callback_data="field_category")
    price_button = InlineKeyboardButton(text="Цена", callback_data="field_price")
    size_button = InlineKeyboardButton(text="Размер", callback_data="field_size")
    photo_button = InlineKeyboardButton(text="Фото", callback_data="field_photo")
    info_button = InlineKeyboardButton(text="Инфо о товаре", callback_data="field_info_product")

    keyboard.add(name_button, category_button, price_button, size_button, photo_button, info_button)

    await  callback_query.message.answer('Выберите поле для редакирования: ',
                                         reply_markup=keyboard)

    await Edit_product.for_field.set()


async def select_field_product(callback_query: types.CallbackQuery, state: FSMContext):
    field_map = {
        "field_name_product": "name_product",
        "field_category": "category",
        "field_price": "price",
        "field_size": "size",
        "field_photo": "photo",
        "field_info_product": "info_product"
    }

    field = field_map.get(callback_query.data)

    if not field:
        await callback_query.message.answer('Недопустимое поле!')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await callback_query.message.answer('Отправьте фото')
        await Edit_product.for_photo.set()
    else:
        await callback_query.message.answer('Отправьте новое значение')
        await Edit_product.for_new_value.set()


async def set_new_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    field = user_data['field']
    new_value = message.text

    update_product_field(product_id, field, new_value)

    await message.answer(f'Поле {field} успешно обновлено!')
    await state.finish()

async def set_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    photo_id = message.photo[-1].file_id

    update_product_field(product_id, 'photo', photo_id)

    await message.answer('Фото успешно обновлено!')
    await state.finish()


def register_update_handler(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['products_update'])
    dp.register_callback_query_handler(sendall_products, Text(equals='all_update'))
    dp.register_callback_query_handler(edit_product, Text(startswith='edit_'), state="*")
    dp.register_callback_query_handler(select_field_product, Text(startswith='field_'), state=Edit_product.for_field)
    dp.register_message_handler(set_new_value,  state=Edit_product.for_new_value)
    dp.register_message_handler(set_new_photo,  state=Edit_product.for_photo, content_types=['photo'])