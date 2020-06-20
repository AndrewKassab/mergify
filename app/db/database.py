import sqlite3 as sql
import os
import time

token_life = 3000
db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")


class MergifyDataBase:

    def __init__(self):
        self.con = sql.self.con.ect(db_path)

    def create_db(self):
        self.con.execute('CREATE TABLE users (username TEXT PRIMARY_KEY UNIQUE, access_token TEXT, expiration_time INTEGER refresh_token TEXT)')
        print('Database created.')
        self.con.close()

    def __get_column_for_user(self, column_name, username):
        cur = self.con.cursor()
        cur.execute("SELECT '%s' FROM users WHERE username = '%s'" % (column_name,username))
        rows = cur.fetchall()
        if len(rows) <= 0:
            return -1
        return rows[0]

    def get_access_token_for_user(self, username):
        return self.__get_column_for_user('access_token', username)

    def get_refresh_token_for_user(self, username):
        return self.__get_column_for_user('refresh_token', username)

    def get_expiration_time_for_user(self, username):
        return self.__get_column_for_user('expiration_time', username)

    def __update_user_column(self, username, column_name, new_value):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return -1
        cur.execute("UPDATE users SET '%s' = '%s'' WHERE username = '%s'" % (column_name, new_value, username))

    def update_access_token_for_user(self, username, new_access_token):
        expiration_time = time.time() + token_life
        self.__update_user_column(username, 'access_token', new_access_token)
        self.__update_user_column(username, 'expiration_time', expiration_time)

    def update_refresh_token_for_user(self, username, new_refresh_token):
        self.__update_user_column(username, 'refresh_token', new_refresh_token)

    def does_user_exist(self, username):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return False
        return True

    def add_new_entry_to_users(self, username, access_token, refresh_token):
        expiration_time = time.time() + token_life
        cur = self.con.cursor()
        cur.execute("INSERT INTO users VALUES ('%s','%s','%d','%s')" % (access_token, expiration_time, refresh_token, username))


db = MergifyDataBase()

