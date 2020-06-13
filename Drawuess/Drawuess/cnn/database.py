import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_category(conn, category):
    """
    Insert a new category into the categories table
    :param conn:
    :param category:
    :return: category id
    """
    sql = ''' INSERT INTO Drawuess_category(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, category)
    return cur.lastrowid

def insert_similar(conn, similar):
    """
    Insert a new similar into the similars table
    :param conn:
    :param similar:
    :return: similar id
    """
    sql = ''' INSERT INTO Drawuess_similar(correct_cat_name,similar_cat_name,npy_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, similar)
    return cur.lastrowid

def clear_category(conn):
    """
    Delete everything from categories table
    :param conn:
    """
    sql = ''' DELETE FROM Drawuess_category '''
    cur = conn.cursor()
    cur.execute(sql)

def clear_similar(conn):
    """
    Delete everything from similars table
    :param conn:
    """
    sql = ''' DELETE FROM Drawuess_similar '''
    cur = conn.cursor()
    cur.execute(sql)

def get_categories(conn):
    """
    Select all from categories table
    :param conn:
    :return: categories
    """
    sql = ''' SELECT * FROM Drawuess_category '''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_category_names(conn):
    return [category[1] for category in get_categories(conn)]