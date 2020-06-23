from flask import Flask
from routes import app as routes

app = Flask(__name__)
app.register_blueprint(routes)

# TODO: Update later
app.secret_key = 'dev key'

if __name__ == '__main__':
    app.run(debug=True)

