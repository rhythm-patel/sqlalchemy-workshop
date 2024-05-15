import logging

from db.base import engine
from sqlalchemy import text


async def execute_query(query, params=None):
    async with engine.begin() as conn:
        return await conn.execute(text(query), params)


async def stream_query(query, params=None):
    async with engine.begin() as conn:
        # https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/basic.html
        # for a streaming result that buffers only segments of the
        # result at time, the AsyncConnection.stream() method is used.
        # this returns a sqlalchemy.ext.asyncio.AsyncResult object.
        result = await conn.stream(text(query), params)
        async for row in result:
            yield row


async def execute_insert_query(query, params=None):
    async with engine.begin() as conn:
        result = await conn.execute(text(query), params)
        await conn.commit()
        return result


def get_customers():
    rows = stream_query("SELECT * FROM customer")
    return rows


async def get_orders_of_customer(customer_id):
    rows = await execute_query(
        """
        SELECT 
            item.name, 
            item.description, 
            item.price, 
            item.price*order_items.quantity AS total
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.customer_id=:customer_id
        """,
        {"customer_id": customer_id},
    )
    return rows


async def get_total_cost_of_an_order(order_id):
    result = await execute_insert_query(
        """
        SELECT 
            SUM(item.price*order_items.quantity) AS total
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.id=:order_id
        """,
        {"order_id": order_id},
    )
    return result.one().total


def get_orders_between_dates(after, before):
    rows = stream_query(
        """
        SELECT
            customer.name,
            item.name, 
            item.price, 
            item.price*order_items.quantity AS total
        FROM orders 
        JOIN customer
        ON
            customer.id = orders.customer_id
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.order_time >= :after
        AND
            orders.order_time <= :before
        """,
        {"after": after, "before": before},
    )
    return rows


async def add_new_order_for_customer(customer_id, items):
    try:
        result = await execute_query(
            """
            INSERT INTO orders
                (customer_id, order_time)
            VALUES
                (:customer_id, Date('now'))
            RETURNING id
            """,
            {"customer_id": customer_id},
        )
        new_order_id = result.one().id

        await execute_insert_query(
            """
        INSERT INTO order_items
            (order_id, item_id, quantity)
        VALUES
            (:order_id, :item_id, :quantity)
        """,
            [
                {
                    "order_id": new_order_id,
                    "item_id": item["id"],
                    "quantity": item["quantity"],
                }
                for item in items
            ],
        )

        return True

    except Exception:
        logging.exception("Failed to add new order")
        return False
