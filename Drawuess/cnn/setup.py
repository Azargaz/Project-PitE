import urllib.request
from .database import *
from .model import train, find_all_similar_images

CATEGORIES = ['axe', 'angel', 'alarm clock', 'ant', 'apple', 'bat', 'bucket', 'cannon']

def download_images():
    url = 'https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{}.npy'
    for category in CATEGORIES:
        print('Downloading {}...'.format(category))
        urllib.request.urlretrieve(url.format(category).replace(' ', '%20'), './Drawuess/cnn/{}.npy'.format(category))

if __name__ == "__main__":
    setup_type = input('''\nWhat would you like to setup?
    1. Download images.
    2. Re-initialize and re-train the model.
    3. Clear and setup the database.
(type 1/2/3 to choose option or any other key to do nothing) ''')

    if setup_type.lower() == '1':
        print('\n-Downloading images...')
        download_images()
    elif setup_type.lower() == '2':
        train()
    elif setup_type.lower() == '2':
        print('\n-Setting up the database...')
        conn = create_connection('./db.sqlite3')
        with conn:
            create_table(conn, 'CREATE TABLE IF NOT EXISTS Drawuess_category (id integer PRIMARY KEY, name text NOT NULL);')
            create_table(conn, 'CREATE TABLE IF NOT EXISTS Drawuess_similar (id integer PRIMARY KEY, correct_cat_name text NOT NULL, similar_cat_name text NOT NULL, npy_id integer NOT NULL);')
            clear_category(conn)
            print('\n-Filling up the database...')        
            for category in CATEGORIES:
                insert_category(conn, [category])
        
        print('\n-Finding similar images...')
        find_all_similar_images()
    
        with conn:
            sql = 'SELECT * FROM Drawuess_similar'
            cur = conn.cursor()
            cur.execute(sql)
            print('\nSimilars table (top 10 rows)')
            for i, row in enumerate(cur.fetchall()):
                if i >= 10:
                    break
                print(row)

            sql = 'SELECT * FROM Drawuess_category'
            cur = conn.cursor()
            cur.execute(sql)
            print('\nCategories table')
            for row in cur.fetchall():
                print(row)