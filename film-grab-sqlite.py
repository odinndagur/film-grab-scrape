import sqlite3
import os

db_path = 'film-grab-db.sqlite3'
os.remove(db_path)

with sqlite3.connect(db_path) as db:
    stmts = [
        'create table lol(id,name);',
        'insert into lol(id,name) values(5,"sponson");'
    ]
    for s in stmts:
        db.execute(s)
    print(db.execute('select * from lol').fetchall())