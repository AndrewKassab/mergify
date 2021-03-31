import sqlite3 as sql
import os
import time

token_life = 3000
db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")


class MergifyDataBase:

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            con = sql.connect(path)
            con.execute('CREATE TABLE Users (user_id INTEGER NOT NULL PRIMARY KEY, '
                        'username TEXT UNIQUE, auth_token TEXT)')
            con.execute('CREATE TABLE Tokens (user_id INTEGER NOT NULL, access_token TEXT, expiration_time INTEGER, '
                        'refresh_token TEXT, PRIMARY KEY(user_id), FOREIGN KEY (user_id) REFERENCES Users(user_id))')
            con.commit()
            con.close()

    def __get_tokens_column(self, column_name, user_id):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT %s FROM Tokens WHERE user_id == '%s'" % (column_name, user_id))
        rows = cur.fetchall()
        con.close()
        if len(rows) <= 0:
            return -1
        return rows[0][0]

    def get_user_id_from_auth_token(self, auth_token):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT user_id FROM Users WHERE auth_token = '%s'" % auth_token)
        rows = cur.fetchall()
        con.close()
        if len(rows) <= 0:
            return -1
        return rows[0][0]

    def get_user_id_from_username(self, username):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT user_id FROM Users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        con.close()
        if len(rows) <= 0:
            return -1
        return rows[0][0]

    def update_auth_token_for_user(self, user_id, new_auth_token):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE user_id = '%s'" % user_id)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return -1
        cur.execute("UPDATE Users SET auth_token = '%s' WHERE user_id = '%s'" % (new_auth_token, user_id))
        con.commit()
        con.close()

    def get_access_token_for_user(self, user_id):
        return self.__get_tokens_column('access_token', user_id)

    def get_refresh_token_for_user(self, user_id):
        return self.__get_tokens_column('refresh_token', user_id)

    def get_expiration_time_for_user(self, user_id):
        return self.__get_tokens_column('expiration_time', user_id)

    def __update_tokens_column(self, user_id, column_name, new_value):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT * FROM Tokens WHERE user_id = '%s'" % user_id)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return -1
        cur.execute("UPDATE Tokens SET %s = '%s' WHERE user_id = '%s'" % (column_name, new_value,
                                                                          user_id))
        con.commit()
        con.close()

    def update_access_token_for_user(self, user_id, new_access_token):
        expiration_time = time.time() + token_life
        self.__update_tokens_column(user_id, 'access_token', new_access_token)
        self.__update_tokens_column(user_id, 'expiration_time', expiration_time)

    def update_refresh_token_for_user(self, user_id, new_refresh_token):
        self.__update_tokens_column(user_id, 'refresh_token', new_refresh_token)

    def does_user_exist(self, username):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        con.close()
        return len(rows) > 0

    def does_auth_token_exist(self, auth_token):
        con = sql.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE auth_token = '%s'" % auth_token)
        rows = cur.fetchall()
        con.close()
        return len(rows) > 0

    def add_new_entry_to_users(self, username, auth_token, access_token, refresh_token):
        con = sql.connect(self.path)
        expiration_time = time.time() + token_life
        cur = con.cursor()
        cur.execute("INSERT INTO Users (username, auth_token) VALUES ('%s','%s')" % (username, auth_token))
        cur.execute("INSERT INTO Tokens (access_token, expiration_time, refresh_token) VALUES "
                    "('%s','%s','%s')" % (access_token, expiration_time, refresh_token))
        con.commit()
        con.close()


db = MergifyDataBase(db_path)
