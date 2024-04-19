import sqlite3
import csv
from db import hash_pwd

def create_db(cur: sqlite3.Cursor):
    cur.execute('CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, title, author, short_text)')
    cur.execute('CREATE TABLE IF NOT EXISTS users(name PRIMIARY KEY, password)')

def add_books(cur: sqlite3.Cursor):
    with open('books.csv', encoding='utf-8') as f:
        content = csv.DictReader(f)
        for book in content:
            title = book['title'].strip()
            author = book['author'].strip()
            short_text = book['short_text'].strip()
            vals = ", ".join([f'"{x}"' for x in (title, author, short_text)])
            cur.execute(f'INSERT INTO books(title, author, short_text) VALUES ({vals});')

def add_user(cur: sqlite3.Cursor):
    pwd = hash_pwd("1234")
    cur.execute(f'INSERT INTO users VALUES ("artfly", "{pwd}")')

if __name__ == '__main__':
    con = sqlite3.connect("no_cover.db")
    cur = con.cursor()
    create_db(cur)
    add_books(cur)
    add_user(cur)
    con.commit()
    cur.close()


