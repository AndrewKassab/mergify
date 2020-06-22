import os
import sqlite3 as sql
import time
import unittest

from db.database import MergifyDataBase, token_life

db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")


class DatabaseTest(unittest.TestCase):

    db = MergifyDataBase(db_path)
    username = 'test_username'
    access_token = 'test_access_token'
    refresh_token = 'test_refresh_token'

    @classmethod
    def setUpClass(cls):
        super(DatabaseTest, cls).setUpClass()
        con = sql.connect(db_path)
        cur = con.cursor()
        expiration_time = time.time() + token_life
        cur.execute("INSERT INTO users VALUES ('%s','%s','%d','%s')" % (cls.username, cls.access_token, expiration_time, cls.refresh_token))
        con.close()

    def test_add_new_user(self):
        new_username = 'test_username_two'
        new_access_token = 'test_access_token_two'
        new_refresh_token = 'test_refresh_token_two'
        self.db.add_new_entry_to_users(new_username, new_access_token, new_refresh_token)
        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        self.assertEqual(len(rows), 1)
        exected_row = [new_username, new_access_token, new_refresh_token]
        actual_row = [rows[0][0], rows[0][1], rows[0][3]]
        self.assertEqual(actual_row, exected_row)
        con.close()

    @classmethod
    def tearDownClass(cls):
        super(DatabaseTest, cls).tearDownClass()
        os.remove(db_path)


if __name__ == '__main__':
    unittest.main()
