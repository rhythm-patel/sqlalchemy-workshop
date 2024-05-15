from datetime import datetime

from db.base import Base
from db.customer import Customer
from db.order_items import OrderItems
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    order_time: Mapped[datetime]

    customer: Mapped["Customer"] = relationship(lazy="joined")  # many to one
    order_items: Mapped[list["OrderItems"]] = relationship(
        lazy="joined"
    )  # one to many

    def __repr__(self) -> str:
        return f"Orders(id={self.id!r}, customer_id={self.customer_id!r}, order_time={self.order_time!r}, customer={self.customer})"

    def as_dict(self):
        return {
            "order_id": self.id,
            "customer": {"name": self.customer.name},
            "order_time": self.order_time,
            "items": [
                {
                    "name": order_item.item.name,
                    "price": order_item.item.price,
                    "quantity": order_item.quantity,
                    "total": order_item.item.price * order_item.quantity,
                }
                for order_item in self.order_items
            ],
        }
