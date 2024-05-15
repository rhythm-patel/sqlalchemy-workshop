import logging

import aiosqlite
from db.init_db import DB_PATH


async def execute_query(query, params):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return rows


async def stream_query(query, *params):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(query, *params) as cursor:
            async for row in cursor:
                yield row


async def execute_insert_query(query, params):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(query, params)
        result = await cursor.fetchone()
        await db.commit()
        return result


async def execute_insert_queries(query, params_tuple):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(query, params_tuple)
        await db.commit()


def get_customers():
    return stream_query("SELECT * FROM customer", {})


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
    rows = await execute_query(
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
    return rows[0][0]


def get_orders_between_dates(after, before):
    return stream_query(
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


async def add_new_order_for_customer(customer_id, items):
    try:
        result = await execute_insert_query(
            """
            INSERT INTO orders
                (customer_id, order_time)
            VALUES
                (:customer_id, Date('now'))
            RETURNING id
            """,
            {"customer_id": customer_id},
        )
        new_order_id = result[0]

        await execute_insert_queries(
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
