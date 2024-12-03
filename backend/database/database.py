import sqlite3
from flask import *

DATABASE = 'moneytracker.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        create_users_table()

    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv


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
        category_id INT PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    '''
    query_db(create_table_query)

def create_transaction_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS transaction (
        transaction_id INT PRIMARY KEY AUTOINCREMENT,
        category_id INT NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        username TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES category(category_id)
    )
    '''
    query_db(create_table_query)