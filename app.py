from flask import Flask, logging, render_template, redirect, request, session, url_for
from db import get_db, close_db, hash_pwd
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
    req = db.cursor().execute(f"SELECT author, title, short_text FROM books ORDER BY RANDOM() LIMIT 1")
    book_data = req.fetchone()
    author = book_data[0]
    title = book_data[1]
    short_text = book_data[2].replace('\n', '<br/>')
    log.error(short_text.count('\n'))
    return render_template("book.html", short_text = short_text, author=author, title=title)

@app.get("/login")
def login_form():
    return render_template("login.html")

@app.post("/login")
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(f'SELECT * FROM users WHERE name = "{username}"').fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif hash_pwd(password) != user[1]:
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user[0]
        return redirect(url_for('index'))
    else:
        return error, 403

@app.get('/')
def index():
    return render_template("index.html")