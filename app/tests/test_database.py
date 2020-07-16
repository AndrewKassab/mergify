import os
import sqlite3 as sql
import time
import unittest

from db.database import MergifyDataBase, token_life

db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")


class DatabaseTest(unittest.TestCase):

    db = MergifyDataBase(db_path)
    username = 'username'
    access_token = 'access_token'
    refresh_token = 'refresh_token'

    @classmethod
    def setUpClass(cls):
        super(DatabaseTest, cls).setUpClass()
        con = sql.connect(db_path)
        cur = con.cursor()
        expiration_time = time.time() + token_life
        cur.execute("INSERT INTO Users (username) VALUES ('%s')" % cls.username)
        cur.execute("INSERT INTO Tokens (access_token, expiration_time, refresh_token) VALUES ('%s','%s','%s')"
                    % (cls.access_token, expiration_time, cls.refresh_token))
        con.commit()
        con.close()

    def test_add_new_user(self):
        test_username = 'test_username_two'
        test_access_token = 'test_access_token_two'
        test_refresh_token = 'test_refresh_token_two'
        self.db.add_new_entry_to_users(test_username, test_access_token, test_refresh_token)
        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE username = '%s'" % test_username)
        rows = cur.fetchall()
        user_id = rows[0][0]
        items = [rows[0][1]]
        cur.execute("SELECT * FROM Tokens WHERE user_id = '%s'" % user_id)
        rows = cur.fetchall()
        items.extend([rows[0][1], rows[0][3]])
        con.close()
        expected_items = [test_username, test_access_token, test_refresh_token]
        self.assertEqual(expected_items, items)

    def test_get_access_token_for_user(self):
        access_token = self.db.get_access_token_for_user(self.username)
        self.assertEqual(self.access_token, access_token)

    def test_get_refresh_token_for_user(self):
        refresh_token = self.db.get_refresh_token_for_user(self.username)
        self.assertEqual(self.refresh_token, refresh_token)

    def test_update_access_token_for_user(self):
        new_access_token = "new_access_token"
        prev_expiration_time = self.db.get_expiration_time_for_user(self.username)
        self.db.update_access_token_for_user(self.username, new_access_token)
        access_token = self.db.get_access_token_for_user(self.username)
        new_expiration_time = self.db.get_expiration_time_for_user(self.username)
        self.assertEqual(new_access_token, access_token)
        self.assertNotEqual(prev_expiration_time, new_expiration_time)

    def test_user_does_exist(self):
        self.assertTrue(self.db.does_user_exist(self.username))

    def test_user_doesnt_exist(self):
        self.assertFalse(self.db.does_user_exist('none'))

    @classmethod
    def tearDownClass(cls):
        super(DatabaseTest, cls).tearDownClass()
        os.remove(db_path)


if __name__ == '__main__':
    unittest.main()
