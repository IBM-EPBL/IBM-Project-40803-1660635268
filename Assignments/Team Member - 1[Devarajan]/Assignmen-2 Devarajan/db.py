import sqlite3

con=sqlite3.connect("lists.db")
print("successfullly connected");

con.execute("CREATE TABLE lists (name TEXT,email TEXT,phone TEXT ,password TEXT)")

print("table created")
con.close()