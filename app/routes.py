from flask import Flask, render_template, request, make_response, redirect, url_for
from spotify import get_user_playlists, sync_playlists, get_oauth_url, get_access_token
from forms import PlaylistForm

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    if not is_logged_in(request):
        return redirect(url_for('login'))
    token = get_access_token(request.cookies['auth_code'])
    playlists = get_user_playlists(token)
    playlist_names = playlists.keys()
    playlist_form = PlaylistForm(playlist_names)
    return render_template('homepage.html', playlist_form=playlist_form)


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
    print(request.args)
    if 'error' in request.args or 'code' not in request.args:
        return redirect(url_for('login'))
    # TODO: Make sure they can't reach /callback manually
    auth_code = request.args['code']
    response = redirect('/', 201)
    response.set_cookie('auth_code', auth_code)
    return response


@app.route('/logout', methods=['GET'])
def logout():
    response = redirect(url_for('login'))
    response.set_cookie('auth_code', '', expires=0)
    return response


def is_logged_in(user):
    if 'auth_code' in user.cookies:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
