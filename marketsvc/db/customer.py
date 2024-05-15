from db.address import Address
from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))

    address: Mapped["Address"] = relationship(
        back_populates="customer", lazy="joined"
    )  # one to one

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, name={self.name!r}, address_id={self.address_id!r}, address={self.address})"

    def as_dict(self):
        return {
            "name": self.name,
            "address": {
                "flat_number": self.address.flat_number,
                "post_code": self.address.post_code,
            },
        }
