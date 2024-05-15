import pathlib
import sqlite3

DB_PATH = 'marketdb'

def init_db(): 
    path = pathlib.Path('marketsvc') / 'db' / 'init_db.sql'
    with path.open() as sql_file:
        sql_script = sql_file.read()

    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.executescript(sql_script)

    db.commit()
    db.close()
