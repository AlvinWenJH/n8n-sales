from fastmcp import FastMCP
from fastapi import HTTPException
from app.modules.sales import Sales

import os
import datetime


mcp = FastMCP("Sales MCP Server")

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")


@mcp.tool
def insert_item(
    operation: str, name: str, description: str, price: int, quantity: int
) -> dict:
    """Insert item into database
    Args:
        operation (str): Operation type BUY|SELL|REFUND
        name (str): Item name
        description (str): Item description
        price (int): Item price in Rupiah
        quantity (int): Item quantity
    Returns:
        Response:
            message: str
            content: dict
    """
    try:
        sales = Sales(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )
        sales.insert_item(operation, name, description, price, quantity)
        return {
            "message": "Item inserted successfully",
            "content": {
                "operation": operation,
                "name": name,
                "description": description,
                "price": price,
                "quantity": quantity,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@mcp.tool
def get_transaction(year=None, month=None, day=None) -> dict:
    """Get on a certain date transaction from database
    Args:
        year (int): Year, if None default to current year
        month (int): Month, if None default to current month
        day (int): Day, if None default to current day
    Returns:
        Response:
            message: str
            content: dict
    """
    try:
        if year is None:
            year = datetime.datetime.now().year
        if month is None:
            month = datetime.datetime.now().month
        if day is None:
            day = datetime.datetime.now().day
        sales = Sales(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )
        data = sales.get_transactions(year, month, day)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000, path="/sales")
