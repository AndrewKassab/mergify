import sqlite3 as sql
import os

db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")

con = sql.connect(db_path)


def create_db():
    con.execute('CREATE TABLE users (username TEXT PRIMARY_KEY UNIQUE, access_token TEXT, expiration_time INTEGER, refresh_token TEXT)')
    print('Database created.')
    con.close()


def get_access_token_for_user(username):
    cur = con.cursor();
    cur.execute("SELECT access_token FROM users WHERE username = '%s'" % username)
    rows = cur.fetchall()
    if len(rows) <= 0:
        return -1
    return rows[0]


def get_refresh_token_for_user(username):
    cur = con.cursor()
    cur.execute("SELECT refresh_token FROM users WHERE username = '%s'" % username)
    rows = cur.fetchall()
    if len(rows) <= 0:
        return -1
    return rows[0]


def update_access_token_for_user(username, new_access_token):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
    rows = cur.fetchall()
    if len(rows) <= 0:
        return -1
    cur.execute("UPDATE users SET access_token = '%s' WHERE username = '%s'" % (new_access_token, username))


def does_user_exist(username):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
    rows = cur.fetchall()
    if len(rows) <= 0:
        return False
    return True


def add_new_entry_to_users(username, access_token, refresh_token):
    cur = con.cursor()
    cur.execute("UPDATE users SET auth_token = '%s', refresh_token = '%s' WHERE username = '%s'" % (access_token, refresh_token, username))

