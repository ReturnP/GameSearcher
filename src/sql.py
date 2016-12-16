import sqlite3

with sqlite3.connect("gameSearch.db") as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE users(username TEXT,password TEXT)")
    c.execute("CREATE TABLE comments(comment TEXT,username TEXT,gameId INTEGER)")

