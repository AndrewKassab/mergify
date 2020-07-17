from flask import request, redirect, url_for, jsonify, Blueprint
from spotify import *
from spotipy import SpotifyException
from token_util import *
from db.database import db

app = Blueprint('routes', __name__)


@app.route('/auth', methods=['GET'])
def spotify_auth():
    return redirect(get_oauth_url())


# TODO: Rewrite and make to /login
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


@app.route('/merge', methods=['POST'])
def merge_playlists():
    code = 201
    payload = {}
    auth_token = request.headers.get('auth_token')
    if not is_auth_token_valid(auth_token):
        code = 401
        payload['error_detail'] = 'Invalid Authorization'
        return jsonify(payload), code
    user_id = db.get_user_id_from_auth_token(auth_token)
    if is_users_access_token_expired(user_id):
        token = refresh_and_update_access_token_for_user(user_id)
    else:
        token = db.get_access_token_for_user(user_id)
    try:
        source_playlist_ids = [request.form['source_playlists']]
        destination_playlist = request.form['destination_playlist']
        to_new = request.form['to_new']
        if to_new:
            merge_to_new_playlist(token, source_playlist_ids, destination_playlist)
        else:
            sync_playlists(token, source_playlist_ids, destination_playlist)
    except Exception as e:
        if type(e) == SpotifyException:
            code = e.http_status
            payload['error_detail'] = e.msg
        else:
            code = e.code
            payload['error_detail'] = 'Bad Request'
    return payload, code


@app.route('/playlists', methods=['GET'])
def get_playlists():
    auth_token = request.headers.get('auth_token')
    if not is_auth_token_valid(auth_token):
        code = 401
        payload = {'error_detail': 'Invalid Authorization'}
        return jsonify(payload), code
    user_id = db.get_user_id_from_auth_token(auth_token)
    if is_users_access_token_expired(user_id):
        token = refresh_and_update_access_token_for_user(user_id)
    else:
        token = db.get_access_token_for_user(user_id)
    playlists = get_user_playlists(token)
    return jsonify(playlists), 200
