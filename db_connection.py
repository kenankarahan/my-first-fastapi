import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, age INTEGER NOT NULL, email TEXT NOT NULL UNIQUE, created_time DATE DEFAULT CURRENT_DATE)')
cur.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL, category TEXT NOT NULL, quantity INTEGER NOT NULL, created_time DATE DEFAULT CURRENT_DATE)')
