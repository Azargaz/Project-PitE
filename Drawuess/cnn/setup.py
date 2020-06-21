from .database import *
from .model import train, find_all_similar_images

CATEGORIES = ['axe', 'angel', 'alarm clock', 'ant', 'apple', 'bat', 'bucket', 'cannon']

if __name__ == "__main__":
    if input('Are you sure you want to re-initialize and re-train the model? (Y/n) ').lower() == 'y':
        train()
    elif input('Do you want to setup similar images and database? (Y/n) ').lower() == 'y':
        find_all_similar_images()
    
        conn = create_connection('./db.sqlite3')
        with conn:
            create_table(conn, 'CREATE TABLE IF NOT EXISTS Drawuess_category (id integer PRIMARY KEY, name text NOT NULL);')
            create_table(conn, 'CREATE TABLE IF NOT EXISTS Drawuess_similar (id integer PRIMARY KEY, correct_cat_name text NOT NULL, similar_cat_name text NOT NULL, npy_id integer NOT NULL);')

            clear_category(conn)

            for category in CATEGORIES:
                insert_category(conn, [category])

            sql = 'SELECT * FROM Drawuess_similar'
            cur = conn.cursor()
            cur.execute(sql)
            print('Similars')
            for i, row in enumerate(cur.fetchall()):
                if i % 10 == 0:
                    print(row)

            sql = 'SELECT * FROM Drawuess_category'
            cur = conn.cursor()
            cur.execute(sql)
            print('Categories')
            for row in cur.fetchall():
                print(row)