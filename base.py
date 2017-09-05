import sqlite3 as sqlite
import const


def is_in_base(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = (?)", (user_id,))
    if cur.fetchone():
        return True
    return False


def create_table():
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("CREATE TABLE users (id, user_id)")
        db.commit()
        db.close()
    except Exception as e:
        print("Failed while creating " + str(e))


def drop_table():
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("DROP TABLE IF EXISTS users;")
        db.commit()
        db.close()
    except Exception as e:
        print("Failed while dropping" + str(e))


def add_user(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO users (id, user_id) VALUES (?,?)",
                    (const.counter+1,
                     user_id))
        db.commit()
        db.close()
        const.counter += 1
        return const.counter
    except:
        return -1
