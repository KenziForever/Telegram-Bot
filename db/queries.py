CREATE_TABLE_STORE = """
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product VARCHAR(255),
    product_id VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255),
    photo TEXT
    )
"""

INSERT_STORE_QUERY = """
    INSERT INTO store (name_product, product_id, size, price, photo)
    VALUES (?, ?, ?, ?, ?)
"""


CREATE_TABLE_STORE_DETAIL = """
CREATE TABLE IF NOT EXISTS detail_store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(255),
    category VARCHAR(255),
    info_product VARCHAR(255)
    )
"""

INSERT_STORE_DETAIL_QUERY = """
    INSERT INTO detail_store (product_id, category, info_product)
    VALUES (?, ?, ?)
"""

