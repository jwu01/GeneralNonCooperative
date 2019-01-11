import sqlite3

def password(username):
    DB_FILE="data/GeneralNonCooperative.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    get_password = 'SELECT password FROM users WHERE users.username = (?)'
    c.execute(get_password,(username,))
    password = c.fetchone()
    return password
