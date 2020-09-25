import spotipy
from spotipy import oauth2
import os
import requests
import json

SCOPE = 'playlist-modify-public playlist-read-private playlist-modify-private'

CLIENT_ID = os.environ['MERGIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['MERGIFY_CLIENT_SECRET']
REDIRECT_URI = os.environ['MERGIFY_REDIRECT_URI']

SPOTIFY_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

spoauth = oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                              redirect_uri=REDIRECT_URI, scope=SCOPE)


def get_oauth_url():
    return spoauth.get_authorize_url()


# { access_token: "", refresh_token: "" }
def get_token_info_from_code(auth_code):
    body = {
        "grant_type": 'authorization_code',
        "code": str(auth_code),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(SPOTIFY_TOKEN_ENDPOINT, data=body)
    text = json.loads(response.text)

    token_info = {'access_token': text['access_token'], 'refresh_token': text['refresh_token']}
    return token_info


def refresh_access_token(refresh_token):
    return spoauth.refresh_access_token(refresh_token)


def get_user_playlists(token):
    sp = spotipy.Spotify(auth=token)
    username = sp.me()['id']
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
        if item['owner']['id'] == username:
            playlists[item['id']] = item['name']
    return playlists


def get_track_ids_from_playlist(playlist_id, token):
    sp = spotipy.Spotify(auth=token)
    track_ids = set()
    playlist_tracks = []
    while True:
        response = sp.playlist_tracks(playlist_id, offset=len(playlist_tracks),
                                      fields='items.track.id, total')
        playlist_tracks.extend(response['items'])
        if len(response['items']) == 0:
            break
    for item in playlist_tracks:
        track_ids.add(item['track']['id'])
    return track_ids


def sync_playlists(token, source_playlist_ids, destination_playlist_id):
    sp = spotipy.Spotify(auth=token)
    username = sp.me()['id']
    source_track_ids = set()
    for playlist_id in source_playlist_ids:
        source_track_ids = source_track_ids.union(get_track_ids_from_playlist(playlist_id, token))
    dest_track_ids = get_track_ids_from_playlist(destination_playlist_id, token)
    ids_to_add = list(source_track_ids - dest_track_ids)
    offset = 0
    while True:
        curr_ids = ids_to_add[offset:offset + 100]
        if len(curr_ids) == 0:
            break
        sp.user_playlist_add_tracks(username, destination_playlist_id, curr_ids)
        offset = offset + 100


def merge_to_new_playlist(token, source_playlist_ids, new_playlist_name):
    sp = spotipy.Spotify(auth=token)
    username = sp.me()['id']
    dest_playlist = sp.user_playlist_create(user=username, name=new_playlist_name)
    destination_playlist_id = dest_playlist['id']  # TODO: Make this actually work
    sync_playlists(token, source_playlist_ids, destination_playlist_id)
    return destination_playlist_id


def get_username_from_access_token(access_token):
    sp = spotipy.Spotify(auth=access_token)
    return sp.me()['id']
