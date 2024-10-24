import sqlite3
from db import queries

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def sql_create():
    if db:
        print('База данных подключена')
    cursor.execute(queries.CREATE_TABLE_STORE)
    cursor.execute(queries.CREATE_TABLE_STORE_DETAIL)
    cursor.execute(queries.CREATE_TABLE_COLLECTION_PRODUCTS)


async def sql_insert_store(name_product, product_id, size, price, photo):
    cursor.execute(queries.INSERT_STORE_QUERY, (
        name_product, product_id, size, price, photo
    ))
    db.commit()


async def sql_insert_store_detail(product_id, category, info_product):
    cursor.execute(queries.INSERT_STORE_DETAIL_QUERY, (
        product_id, category, info_product
    ))
    db.commit()

async def sql_insert_store_collection(product_id, collection):
    cursor.execute(queries.INSERT_STORE_COLLECTION_QUERY, (
        product_id, collection
    ))
    db.commit()