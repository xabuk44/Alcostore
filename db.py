import sqlite3


def open_db(db_url):
    db = sqlite3.connect(db_url)
    db.row_factory = sqlite3.Row
    return db

def get_list(db_url, page=1):
    db = open_db(db_url)
    limit = 5
    offset = limit * (page - 1)
    shops = db.cursor().execute(
        'SELECT id, name, adress, coordinate, rating FROM alcoshops LIMIT  :limit OFFSET  :offset',
    {'limit': limit, 'offset': offset}
    ).fetchall()
    db.close()
    return shops


def search_shop(db_url, search):
    db = open_db(db_url)
    shop_searched = db.cursor().execute('''SELECT id, name, adress, coordinate, rating FROM alcoshops WHERE name LIKE :search or adress like :search''',
                                        {'search': '%' + search + '%'}
                                        )
    alcoshops = shop_searched.fetchall()
    db.close()
    return alcoshops


def add_alcoshop(db_url, name, adress, coordinate, rating):
    db = open_db(db_url)
    sql = '''INSERT INTO alcoshops(name, adress, coordinate, rating) VALUES (?, ?, ?, ?)'''
    db.cursor().execute(sql, (name, adress, coordinate, rating))
    db.commit()
    alcoshop_id = db.cursor().execute('SELECT MAX(id) from alcoshops;').fetchall()
    db.close()
    return alcoshop_id[0][0]



def update_alcoshop(db_url, shop_id, name, adress, coordinate, rating):
    db = open_db(db_url)
    sql_data = '''UPDATE alcoshops SET name = ?, adress = ?, coordinate = ?, rating = ? WHERE id = ?'''
    db.cursor().execute(sql_data, (name, adress, coordinate, rating, shop_id))
    db.commit()
    db.close()
    return shop_id

def search_shop_by_id(db_url, shop_id):
    db = open_db(db_url)
    alcoshop = db.cursor().execute(
        'SELECT id,  name, adress, coordinate, rating FROM alcoshops WHERE id = :id',
        {'id': shop_id}).fetchone()
    db.close()
    return alcoshop


def delete_by_id(db_url, shop_id):
    db = open_db(db_url)
    db.cursor().execute(
        'DELETE FROM alcoshops WHERE id = :id',
        {'id': shop_id}
                        )
    db.commit()
    db.close()