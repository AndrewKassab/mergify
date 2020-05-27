from flask import Flask, render_template, request, make_response, redirect, url_for, flash, get_flashed_messages
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
    response = render_template('homepage.html', playlist_form=playlist_form)
    response.set_cookie('playlists', playlists)
    return response


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
    response.set_cookie()
    return response


@app.route('/merge', methods=['POST'])
def merge_playlists():
    source_playlist_names = request.form['sources']
    destination_playlist_name = request.form['dest']
    source_playlist_ids = []
    for name in source_playlist_names:
        source_playlist_ids.append(request.cookies['playlists'][name])
    destination_playlist_id = request.cookies['playlists'][destination_playlist_name]
    token = get_access_token(request.cookies['auth_code'])
    if sync_playlists(token, source_playlist_ids, destination_playlist_id) == -1:
        flash('Error merging playlists')
        return make_response(redirect('/', 422))
    flash('Playlist created successfully')
    return make_response(redirect('/', 201))


def is_logged_in(user):
    if 'auth_code' in user.cookies:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
