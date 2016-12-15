import sqlite3

with sqlite3.connect("users.db") as connection:
    c = connection.cursor()
    
    c.execute("CREATE TABLE users(username TEXT,password TEXT)")

