import sqlite3
from flask import session, request


def addUser(username, password)
    DB_FILE = "data/GeneralNonCooperative.db"
    db = sqlite.connect(DB_FILE)
    c = db.cursor()
    insert = "INSERT INTO users VALUES(?,?)"
    parameters=(username, password)
    c.execute(insert, parameters)
    db.commit()
    db.close()
