from flask import Flask, render_template, request, make_response, redirect, url_for
from spotify import get_user_playlists, sync_playlists, get_oauth_url

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    if not is_logged_in(request):
        return redirect(url_for('login'))
    return render_template('homepage.html')


@app.route('/login', methods=['GET'])
def login():
    if is_logged_in(request):
        return redirect(url_for('homepage'))
    else:
        return render_template('loginpage.html')


@app.route('/auth', methods=['GET'])
def spotify_auth():
    return redirect(get_oauth_url())


@app.route('/callback/', methods=['GET'])
def callback():
    if 'error' in request.args:
        return redirect(url_for('login'))
    # TODO: Make sure they can't reach /callback manually
    auth = request.args['code']
    response = make_response()
    response.set_cookie('auth_token', auth)
    response.set_cookie('', auth)
    return redirect('/', 201)


@app.route('/logout', methods=['GET'])
def logout():
    request.delete_cookie('auth_token')
    return redirect(url_for('login'))


def is_logged_in(user):
    if 'auth_token' in user.cookies:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
