import spotipy
import os

scope = 'playlist-read-private playlist-modify-private'
client_id = os.environ['PSYNC_CLIENT_ID']
client_secret = os.environ['PSYNC_CLIENT_SECRET']
redirect_uri = os.environ['PSYNC_REDIRECT_URI']


def get_oauth_url():
    return "https://accounts.spotify.com/authorize?client_id=%s" \
           "&response_type=code&redirect_uri=%s&scope=%s" % (client_id, redirect_uri, scope)


def get_user_playlists(token):
    try:
        sp = spotipy.Spotify(auth=token)
    except:
        return -1
    # TODO: Extract username from this call
    username = sp.me()
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


def sync_playlists(username, token, source_playlists_ids, destination_playlist_id):
    try:
        sp = spotipy.Spotify(auth=token)
    except:
        return -1
    source_track_ids = set()
    for playlist_id in source_playlists_ids:
        source_track_ids.union(get_track_ids_from_playlist(playlist_id,token))
    dest_track_ids = get_track_ids_from_playlist(destination_playlist_id, token)
    ids_to_add = list(source_track_ids - dest_track_ids)

    offset = 0
    while True:
        curr_ids = ids_to_add[offset:offset+100]
        if len(curr_ids) == 0:
            break
        sp.user_playlist_add_tracks(username, destination_playlist_id, curr_ids)
        offset = offset + 100
    return 1


def get_username_from_token(token):
    try:
        sp = spotipy.Spotify(auth=token)
    except:
        return -1
    # TODO: Extract username from here
    return sp.me()['']
