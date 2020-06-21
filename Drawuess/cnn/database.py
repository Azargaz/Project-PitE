import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_category(conn, category):
    sql = ''' INSERT INTO Drawuess_category(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, category)
    return cur.lastrowid

def insert_similar(conn, similar):
    sql = ''' INSERT INTO Drawuess_similar(correct_cat_name,similar_cat_name,npy_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, similar)
    return cur.lastrowid

def clear_category(conn):
    sql = ''' DELETE FROM Drawuess_category '''
    cur = conn.cursor()
    cur.execute(sql)

def clear_similar(conn):
    sql = ''' DELETE FROM Drawuess_similar '''
    cur = conn.cursor()
    cur.execute(sql)

def get_categories(conn):
    sql = ''' SELECT * FROM Drawuess_category '''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_category_names(conn):
    return [category[1] for category in get_categories(conn)]