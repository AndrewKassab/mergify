from flask import Flask, render_template, request, make_response, redirect, url_for, flash, jsonify
from spotify import *
from forms import PlaylistForm
from spotipy import SpotifyException
from util import *
from db.database import db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    if not is_logged_in(request):
        return redirect(url_for('login'))
    username = request.cookies['username']
    access_token = db.get_access_token_for_user(username)
    if is_access_token_expired(access_token):
        refresh_token = db.get_refresh_token_for_user(username)
        access_token = get_access_token_from_refresh_token(refresh_token)
        db.update_access_token_for_user(username, access_token)
    playlists = get_user_playlists(access_token)
    playlist_form = PlaylistForm()
    choices = [(v, k) for k, v in playlists.items()]
    playlist_form.source_playlists.choices = choices
    playlist_form.destination_playlist.choices = choices
    response = make_response(render_template('homepage.html', form=playlist_form))
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
    if 'error' in request.args or 'code' not in request.args:
        return redirect(url_for('login'))
    auth_code = request.args['code']
    token_info = get_token_info_from_code(auth_code)
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    username = get_username_from_access_token(access_token)
    response = redirect(url_for('homepage'), 201)
    response.set_cookie('username', username)
    if db.does_user_exist(username):
        db.update_access_token_for_user(access_token)
        db.update_refresh_token_for_user(refresh_token)
    else:
        db.add_new_entry_to_users(username, access_token, refresh_token)
    return response


@app.route('/logout', methods=['GET'])
def logout():
    response = redirect(url_for('login'))
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)
    return response


@app.route('/merge', methods=['POST'])
def merge_playlists():
    code = 201
    try:
        source_playlist_ids = [request.form['source_playlists']]
        destination_playlist_id = request.form['destination_playlist']
        form = request.form
        token = db.get_access_token_for_user(request.cookies['username'])
        sync_playlists(token, source_playlist_ids, destination_playlist_id)
        flash('Playlist merge was successful, please check your spotify!')
    except Exception as e:
        if type(e) == SpotifyException:
            code = e.http_status
        else:
            code = 422
        flash('Playlist merge unsuccessful, please try logging out and logging back in before trying again')
    return make_response(redirect(url_for('homepage')), code)


def is_logged_in(user):
    if 'auth_code' in user.cookies:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
