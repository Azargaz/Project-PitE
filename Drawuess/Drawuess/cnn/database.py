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

if __name__ == '__main__':
    conn = create_connection('./db.sqlite3')

    with conn:
        # create_table(conn, 'CREATE TABLE IF NOT EXISTS Drawuess_category (id integer PRIMARY KEY, name text NOT NULL);')
        # create_table(conn, 'CREATE TABLE IF NOT EXISTS Drawuess_similar (id integer PRIMARY KEY, correct_cat_name text NOT NULL, similar_cat_name text NOT NULL, npy_id integer NOT NULL);')

        # print(insert_category(conn, ['test']))
        sql = 'SELECT * FROM Drawuess_similar'
        cur = conn.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            print(row)