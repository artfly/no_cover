from flask import Flask, logging, render_template
from db import get_db, close_db
import sqlite3
import random

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='no_cover.db'
)
app.teardown_appcontext(close_db)
log = logging.create_logger(app)

@app.get('/book')
def show_book():
    db = get_db()
    cur: sqlite3.Cursor = db.cursor()
    req = cur.execute("SELECT COUNT(*) FROM books")
    n_rows = req.fetchone()[0]
    n_row = random.randint(0, n_rows)
    req = db.cursor().execute(f"SELECT short_text FROM books ORDER BY RANDOM() LIMIT 1")
    short_text = req.fetchone()[0].replace('\n', '<br/>')
    log.error(short_text.count('\n'))
    return render_template("book.html", short_text = short_text)