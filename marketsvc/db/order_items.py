from db.base import Base
from db.item import Item
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItems(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id"), primary_key=True
    )
    quantity: Mapped[int]

    item: Mapped["Item"] = relationship(lazy="joined")  # many to one

    @hybrid_property
    def item_total(self):
        return self.item.price * self.quantity

    @item_total.expression
    @classmethod
    def item_total(cls):
        return Item.price * cls.quantity

    def __repr__(self) -> str:
        return f"OrderItems(order_id={self.order_id!r}, item_id={self.item_id!r}, quantity={self.quantity!r}, item={self.item})"
