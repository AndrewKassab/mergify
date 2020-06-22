import sqlite3 as sql
import os
import time

token_life = 3000
db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")

seeded_username = os.environ.get('MERGIFY_SEED_USERNAME')
seeded_token = os.environ.get('MERGIFY_SEED_TOKEN')


class MergifyDataBase:

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            con = sql.connect(path)
            con.execute('CREATE TABLE users (username TEXT PRIMARY_KEY UNIQUE, access_token TEXT, '
                        'expiration_time INTEGER, refresh_token TEXT)')
            if seeded_username and seeded_token:
                cur = con.cursor()
                cur.execute("INSERT INTO users VALUES ('%s','%s','%d','%s')" % (seeded_username,
                                                                                seeded_token, 1, seeded_token))
            con.commit()
            con.close()

    def __get_column_for_user(self, column_name, username):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT %s FROM users WHERE username == '%s'" % (column_name, username))
        rows = cur.fetchall()
        con.close()
        if len(rows) <= 0:
            return -1
        return rows[0][0]

    def get_access_token_for_user(self, username):
        return self.__get_column_for_user('access_token', username)

    def get_refresh_token_for_user(self, username):
        return self.__get_column_for_user('refresh_token', username)

    def get_expiration_time_for_user(self, username):
        return self.__get_column_for_user('expiration_time', username)

    def __update_user_column(self, username, column_name, new_value):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return -1
        cur.execute("UPDATE users SET %s = '%s' WHERE username = '%s'" % (column_name, new_value,
                                                                          username))
        con.commit()
        con.close()

    def update_access_token_for_user(self, username, new_access_token):
        expiration_time = time.time() + token_life
        self.__update_user_column(username, 'access_token', new_access_token)
        self.__update_user_column(username, 'expiration_time', expiration_time)

    def update_refresh_token_for_user(self, username, new_refresh_token):
        self.__update_user_column(username, 'refresh_token', new_refresh_token)

    def does_user_exist(self, username):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        con.close()
        if len(rows) <= 0:
            return False
        return True

    def add_new_entry_to_users(self, username, access_token, refresh_token):
        con = sql.connect(self.path)
        expiration_time = time.time() + token_life
        cur = con.cursor()
        cur.execute("INSERT INTO users VALUES ('%s','%s','%d','%s')" % (username, access_token, expiration_time, refresh_token))
        con.commit()
        con.close()


db = MergifyDataBase(db_path)
