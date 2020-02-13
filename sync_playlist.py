#!/usr/bin/env python

import spotipy
import spotipy.util as auth
import os

# Fill These in yourself
destination_playlist_id = ''
source_playlist_ids = []

scope = 'playlist-read-private playlist-modify-private'

# Export these in your environment
username = os.environ['SPOTIFY_USERNAME']
spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']

# In your terminal, export these values as described in the readme.
token = auth.prompt_for_user_token(username, scope, spotify_client_id,
                                   spotify_client_secret, spotify_redirect_uri)

sp = spotipy.Spotify(auth=token)

source_track_ids = set()
destination_track_ids = set()

# get track ids from source playlists
for playlist_id in source_playlist_ids:
    playlist_tracks = []
    while True:
        response = sp.playlist_tracks(playlist_id,
                                           offset=len(playlist_tracks), fields='items.track.id, total')
        playlist_tracks.extend(response['items'])
        if (len(response['items']) == 0):
            break
    for item in playlist_tracks:
        source_track_ids.add(item['track']['id'])

# get track ids from destination playlist
destination_playlist_tracks = []
while True:
    response = sp.playlist_tracks(destination_playlist_id,
                                           offset=len(destination_playlist_tracks), fields='items.track.id, total')
    destination_playlist_tracks.extend(response['items'])
    if (len(response['items']) == 0):
        break
for item in destination_playlist_tracks:
    destination_track_ids.add(item['track']['id'])

exceptset = source_track_ids - destination_track_ids

track_ids_to_add = list(source_track_ids - destination_track_ids)

# add 100 tracks at a time
start = 0
while True:
    track_ids_to_add_shrunk = track_ids_to_add[start:start+100]
    if (len(track_ids_to_add_shrunk) == 0):
        break
    sp.user_playlist_add_tracks(username, destination_playlist_id, track_ids_to_add_shrunk)
    start = start + 100
