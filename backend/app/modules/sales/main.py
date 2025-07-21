from psycopg2 import connect
from .queries import QUERY
import datetime


class Sales:
    def __init__(self, host: str, port: str, dbname: str, user: str, password: str):
        self.init_db(host, port, dbname, user, password)

    def init_db(self, host: str, port: str, dbname: str, user: str, password: str):
        self.conn = connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(QUERY["CREATE_SALES_TABLE"])
        self.conn.commit()

    def insert_item(
        self, operation: str, name: str, description: str, price: int, quantity: int
    ):
        self.cursor.execute(
            QUERY["INSERT_SALES"],
            (operation, name, description, price, quantity),
        )
        self.conn.commit()

    def get_transactions(self, year, month, day):
        start_date = datetime.datetime(year, month, day)
        end_date = start_date + datetime.timedelta(days=1)
        self.cursor.execute(QUERY["GET_TRANSACTIONS"], (start_date, end_date))
        data = self.cursor.fetchall()
        result = []
        for d in data:
            result.append(
                {
                    "id": d[0],
                    "operation": d[1],
                    "name": d[2],
                    "description": d[3],
                    "price": d[4],
                    "quantity": d[5],
                    "created_at": d[6],
                }
            )
        return result
