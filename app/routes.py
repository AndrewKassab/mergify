from flask import Flask, render_template, request, make_response, redirect, url_for, flash, jsonify
from spotify import *
from forms import PlaylistForm
from spotipy import SpotifyException
import sqlite3 as sql
from db.database import db_path

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    if not is_logged_in(request):
        return redirect(url_for('login'))
    token = get_access_token(request.cookies['auth_code'])
    playlists = get_user_playlists(token)
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
    username = get_username_from_authcode(auth_code)
    response = redirect(url_for('homepage'), 201)
    response.set_cookie('auth_code', auth_code)
    response.set_cookie('username', username)
    with sql.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
        rows = cur.fetchall()
        if len(rows) <= 0:
            cur.execute("INSERT INTO users (username, auth_code) VALUES(?, ?)", (username, auth_code))
        else:
            cur.execute("UPDATE users SET auth_code = '%s' WHERE username = '%s'" % (auth_code, username))
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
        token = get_access_token(request.cookies['auth_code'])
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
