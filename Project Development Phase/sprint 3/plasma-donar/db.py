import sqlite3 as sqlite3

connection =sqlite3.connect("donar.db")
print("Database Created Successfully")

connection.execute(""" CREATE TABLE DONARS (
    id TEXT PRIMARY KEY,
    name TEXT,
    phone TEXT ,
    email TEXT  UNIQUE,
    password TEXT,
    age TEXT,
    blood_group TEXT,
    weight TEXT,
    parasitic TEXT,
    hiv TEXT,
    blood_disease TEXT,
    drugs TEXT,
    vaccine TEXT,
    overall_health TEXT,
    donated_plasma TEXT,
    date TEXT)  """)

print("Table Donars Successfully")


connection.close()