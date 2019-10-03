import spotipy
import spotipy.util as auth
import os

# In your terminal, export these values as described in the readme.
token = auth.prompt_for_user_token(os.environ['SPOTIFY_USERNAME'], 'playlist-modify-private',
                                   os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'],
                                   os.environ['SPOTIFY_REDIRECT_URI'])

destination_playlist_id = '1F2mahiwXN6lLuf3bpWE6y?si=ZUu0bdTxQMSGAxUG-CVa_A'
source_playlist_ids = ['3nWTj1ZAdLJXNiaLdMUOwj?si=0THwLcT5SDujFJhKt5aYIw']
# other_test_source = '6eNpp03c7e3mnT2Otm7mwT?si=hCeXjEgrQuiXTtVeEtqZLA'

sp = spotipy.Spotify(auth=token)

track_ids = set()

for playlist_id in source_playlist_ids:
    response = sp.user_playlist_tracks(config.USERNAME, playlist_id, fields='tracks')
    playlist_tracks = response['tracks']['items']
    while len(playlist_tracks) < response['tracks']['total']:
        response = sp.user_playlist_tracks(config.USERNAME, playlist_id,
                                           offset=len(playlist_tracks), fields='tracks')
        playlist_tracks.extend(response['tracks']['items'])
    for item in playlist_tracks:
        track_ids.add(item['track']['id'])

for track_id in track_ids:
    print(track_id)

print(len(track_ids))





