import os
from routes import app
from db.database import *

# TODO: Update later
app.secret_key = 'dev key'

if __name__ == '__main__':
    app.run(debug=True)
