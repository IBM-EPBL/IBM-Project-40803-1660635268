import sqlite3

conn = sqlite3.connect('user.db')

conn.execute('CREATE TABLE students (name TEXT,mobile TEXT)')
print("Table created successfully")
conn.close()
