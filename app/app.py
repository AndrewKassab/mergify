import os
from routes import app
from db.database import create_db, db_path

# TODO: Update later
app.secret_key = 'dev key'

if __name__ == '__main__':
    if not os.path.exists(db_path):
        create_db()
    app.run(debug=True)
