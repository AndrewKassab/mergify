import sqlite3
import os

db_path = os.path.relpath('./database.db', os.path.dirname(__file__))


def create_db():
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE users (username TEXT PRIMARY_KEY, auth_code TEXT)')
    conn.close()
