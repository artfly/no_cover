import sqlite3
import csv

def create_db(cur: sqlite3.Cursor):
    cur.execute('CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, title, author, short_text)')

def add_books(cur: sqlite3.Cursor):
    with open('books.csv', encoding='utf-8') as f:
        content = csv.DictReader(f)
        for book in content:
            title = book['title'].strip()
            author = book['author'].strip()
            short_text = book['short_text'].strip()
            vals = ", ".join([f'"{x}"' for x in (title, author, short_text)])
            cur.execute(f'INSERT INTO books(title, author, short_text) VALUES ({vals});')

if __name__ == '__main__':
    con = sqlite3.connect("no_cover.db")
    cur = con.cursor()
    create_db(cur)
    add_books(cur)
    con.commit()
    cur.close()


