import sqlite3 as sqlite3

connection =sqlite3.connect("donar.db")
print("Database Created Successfully")

connection.execute(""" CREATE TABLE DONARS (
    id TEXT PRIMARY KEY,
    name TEXT,
    phone TEXT ,
    email TEXT NOT NULL UNIQUE,
    password TEXT)  """)

print("Table Donars Successfully")


connection.close()