import pathlib

import aiosqlite

DB_PATH = "marketdb"


async def init_db():
    path = pathlib.Path("marketsvc") / "db" / "init_db.sql"
    with path.open() as sql_file:
        sql_script = sql_file.read()

    async with aiosqlite.connect(DB_PATH) as cursor:
        await cursor.executescript(sql_script)
        await cursor.commit()
