import sqlite3
import os

db_path = os.path.abspath(os.path.dirname(__file__) + "/database.db")


def create_db():
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE users (username TEXT PRIMARY_KEY UNIQUE, auth_code TEXT)')
    conn.close()
