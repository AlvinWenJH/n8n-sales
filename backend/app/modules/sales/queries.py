QUERY = {}

QUERY["CREATE_SALES_TABLE"] = """
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    operation TEXT,
    name TEXT,
    description TEXT,
    price INTEGER,
    quantity FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

QUERY["INSERT_SALES"] = """
INSERT INTO sales (operation, name, description, price, quantity)
VALUES (%s, %s, %s, %s, %s)
"""

QUERY["GET_TRANSACTIONS"] = """
SELECT * FROM sales
WHERE created_at >= %s AND created_at < %s
"""
