from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///marketdb", echo=True)

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks
# The AsyncSession object is a mutable, stateful object which represents a single, stateful database transaction in progress.
# Using concurrent tasks with asyncio, with APIs such as asyncio.gather() for example, should use a separate AsyncSession per individual task.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass
