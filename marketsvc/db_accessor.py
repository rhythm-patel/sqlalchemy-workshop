import logging
from datetime import datetime

from db.base import engine
from db.customer import Customer
from db.order_items import OrderItems
from db.orders import Orders
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_customers():
    with Session(engine) as session:
        stmt = select(Customer)
        result = session.execute(stmt)
        customers = result.scalars().all()

        return customers


def get_orders_of_customer(customer_id):
    with Session(engine) as session:
        result = session.execute(
            select(Orders).where(Orders.customer_id == customer_id)
        )
        orders = result.scalars().unique().all()

        return orders


def get_total_cost_of_an_order(order_id):
    with Session(engine) as session:
        result = session.execute(
            select(func.sum(OrderItems.item_total))
            .join(Orders.order_items)
            .join(OrderItems.item)
            .where(Orders.id == order_id)
        )
        total_cost = result.scalar()

        return total_cost


def get_orders_between_dates(after, before):
    with Session(engine) as session:
        result = session.execute(
            select(Orders).where(Orders.order_time.between(after, before))
        )
        orders = result.scalars().unique().all()

        return orders


def add_new_order_for_customer(customer_id, items):
    try:
        with Session(engine) as session:
            result = session.execute(
                select(Customer).where(Customer.id == customer_id)
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
            session.commit()

        return True

    except Exception:
        logging.exception("Failed to add new order")
        return False
