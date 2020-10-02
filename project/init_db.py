import sqlite3
from sqlite3 import Error

connection = None

try:
    connection = sqlite3.connect('hockey.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    print(sqlite3.version)
except Error as e:
    print(e)
finally:
    if connection:
        connection.close()
