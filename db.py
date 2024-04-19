from flask import current_app, g
import sqlite3
import hashlib

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db

def close_db(e = None):
    db = g.pop('db', None)
    if db:
        db.close()

def hash_pwd(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()