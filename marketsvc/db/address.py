from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    flat_number: Mapped[int]
    post_code: Mapped[int]

    customer: Mapped["Customer"] = relationship(
        back_populates="address",
        lazy="joined",
    )  # one to one

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, flat_number={self.flat_number!r}, post_code={self.post_code!r})"
