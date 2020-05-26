from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    if not is_logged_in(request):
        redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if is_logged_in(request):
        redirect(url_for('homepage'))
    else:
        render_template('loginpage.html')


def is_logged_in(user):
    if 'auth_token' in user.cookies and 'username' in user.cookies:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
