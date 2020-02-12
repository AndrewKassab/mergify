#!/usr/bin/env python

import spotipy
import spotipy.util as auth
import os

# Fill These in yourself
destination_playlist_id = '1F2mahiwXN6lLuf3bpWE6y?si=ZUu0bdTxQMSGAxUG-CVa_A'
source_playlist_ids = ['3nWTj1ZAdLJXNiaLdMUOwj?si=0THwLcT5SDujFJhKt5aYIw']

scope = 'playlist-read-private playlist-modify-private'

# Export these in your environment
username = os.environ['SPOTIFY_USERNAME']
spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']

# In your terminal, export these values as described in the readme.
token = auth.prompt_for_user_token(username, scope, spotify_client_id,
                                   spotify_client_secret, spotify_redirect_uri)

# other_test_source = '6eNpp03c7e3mnT2Otm7mwT?si=hCeXjEgrQuiXTtVeEtqZLA'

sp = spotipy.Spotify(auth=token)

track_ids = set()

for playlist_id in source_playlist_ids:
    response = sp.playlist_tracks(playlist_id, fields='items.track.id, total')
    playlist_tracks = response['tracks']['items']
    while True:
        response = sp.playlist_tracks(playlist_id,
                                           offset=len(playlist_tracks), fields='items.track.id, total')
        playlist_tracks.extend(response['tracks']['items'])
        if (len(response['items']) == 0):
            break
    for item in playlist_tracks:
        track_ids.add(item['track']['id'])

for track_id in track_ids:
    print(track_id)

print(len(track_ids))





