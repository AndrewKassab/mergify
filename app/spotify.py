import spotipy
import os

scope = 'playlist-read-private playlist-modify-private'
client_id = os.environ['PSYNC_CLIENT_ID']
client_secret = os.environ['PSYNC_CLIENT_SECRET']
redirect_uri = os.environ['PSYNC_REDIRECT_URI']


def get_oauth_url():
    return "https://accounts.spotify.com/authorize?client_id=%s" \
           "&response_type=code&redirect_uri=%s&scope=%s"


def get_user_playlists(token, username):
    sp = spotipy.spotify(auth=token)
    user_playlists_list = []
    offset = 0
    while True:
        response = sp.user_playlists(username, offset=offset)['items']
        if len(response) == 0:
            break
        user_playlists_list.extend(response)
        offset = offset + 50
    playlists = {}
    for item in user_playlists_list:
        playlists[item['name']] = item['uri'][17:]
    return sp.user_playlists(username)
