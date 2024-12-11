import sqlite3
from flask import *

DATABASE = 'database/moneytracker.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        create_users_table()
        create_category_table()
        create_transaction_table()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    cur.row_factory = sqlite3.Row
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id


#Migrations
def create_users_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS user (
        username text PRIMARY KEY UNIQUE,
        password TEXT NOT NULL
    )
    '''
    query_db(create_table_query)

def create_category_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    '''
    query_db(create_table_query)

def create_transaction_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            username TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (category_id) REFERENCES category(category_id),
            FOREIGN KEY (username) REFERENCES user(username)
        )
        '''
    query_db(create_table_query)