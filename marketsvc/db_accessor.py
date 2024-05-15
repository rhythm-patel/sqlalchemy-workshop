import logging
from datetime import datetime

from db.base import async_session_maker
from db.customer import Customer
from db.order_items import OrderItems
from db.orders import Orders
from sqlalchemy import select
from sqlalchemy.sql import func


async def get_customers():
    async with async_session_maker() as session:
        stmt = select(Customer)
        async for customer in await session.stream_scalars(stmt):
            yield customer


async def get_orders_of_customer(customer_id):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Orders).where(Orders.customer_id == customer_id)
        )
        orders = result.scalars().unique().all()

        return orders


async def get_total_cost_of_an_order(order_id):
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.sum(OrderItems.item_total))
            .join(Orders.order_items)
            .join(OrderItems.item)
            .where(Orders.id == order_id)
        )
        return result.scalar()


async def get_orders_between_dates(after, before):
    async with async_session_maker() as session:
        result = await session.stream(
            select(Orders).where(Orders.order_time.between(after, before))
        )
        async for order in result.scalars().unique():
            yield order


async def add_new_order_for_customer(customer_id, items):
    try:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Customer).where(customer_id == customer_id)
            )
            customer = result.scalar()

            new_order = Orders(
                customer_id=customer_id,
                order_time=datetime.now(),
                customer=customer,
            )

            new_order.order_items = [
                OrderItems(
                    item_id=item["id"],
                    quantity=item["quantity"],
                )
                for item in items
            ]

            session.add(new_order)
            await session.commit()
        return True

    except Exception:
        logging.exception("Failed to add new order")
        return False
