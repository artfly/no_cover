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
    username = session.get("user_id", "")
    req = db.cursor().execute(f'''
    SELECT author, title, short_text FROM books WHERE 
    author NOT IN (SELECT author FROM disliked_authors WHERE username = "{username}")
    ORDER BY RANDOM() LIMIT 1
    ''')
    book_data = req.fetchone()
    author = book_data[0]
    title = book_data[1]
    short_text = book_data[2].replace('\n', '<br/>')
    log.error(short_text.count('\n'))
    return render_template("book.html", short_text = short_text, author=author, title=title)

@app.post('/dislike/<author>')
def dislike_author(author):
    user_id = session.get("user_id", None)
    if not user_id:
        return 403, "Not logged in"
    db = get_db()
    cur: sqlite3.Cursor = db.cursor()
    cur.execute(f'INSERT INTO disliked_authors(username, author) VALUES ("{user_id}", "{author}")')
    db.commit()
    return redirect(url_for('show_book'))

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