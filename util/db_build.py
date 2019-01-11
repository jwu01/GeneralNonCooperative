import sqlite3

def users():
    DB_FILE="./data/GeneralNonCooperative.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE users(username TEXT, password TEXT)"
    c.execute(command)

def main():
    try:
        users()
    except:
        pass
