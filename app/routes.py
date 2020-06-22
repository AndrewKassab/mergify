from flask import Flask, render_template, request, make_response, redirect, url_for, flash, jsonify
from spotify import *
from spotipy import SpotifyException
from token_util import *
from db.database import db

app = Flask(__name__)


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
        db.update_access_token_for_user(username, access_token)
        db.update_refresh_token_for_user(username, refresh_token)
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
    payload = {}
    try:
        source_playlist_ids = [request.form['source_playlists']]
        destination_playlist_id = request.form['destination_playlist']
        token = request.headers['access_token']
        username = get_username_from_access_token(token)
        if not is_access_token_valid(token, username):
            code = 401
            payload['error_detail'] = 'Invalid Authorization'
        sync_playlists(token, source_playlist_ids, destination_playlist_id)
    except Exception as e:
        if type(e) == SpotifyException:
            code = e.http_status
            payload['error_detail'] = "spotify err"  # TODO: Update to grab detail from exception
        else:
            code = 422
    return jsonify(payload), code


def is_logged_in(user):
    if 'auth_code' in user.cookies:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
