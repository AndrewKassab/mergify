import config
import spotipy
import spotipy.util as auth

token = auth.prompt_for_user_token(config.USERNAME, 'playlist-modify-private',
                                   config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET,
                                   config.SPOTIPY_REDIRECT_URI)

destination_playlist_id = config.DESTINATION_PLAYLIST_ID
source_playlist_ids = config.SOURCE_PLAYLIST_IDS
sp = spotipy.Spotify(auth=token)

track_ids = set()

for playlist_id in source_playlist_ids:
    response = sp.user_playlist_tracks(config.USERNAME, playlist_id, fields=None,
                                       limit=100, market=None)
    playlist_tracks = response['tracks']['items']
    while len(playlist_tracks) < response['tracks']['total']:
        offset = len(playlist_tracks)
        response = sp.user_playlist_tracks(config.USERNAME, playlist_id, fields=None,
                                           limit=100, offset=offset, market=None)
        playlist_tracks.extend(response['tracks']['items'])
    for item in playlist_tracks:
        track_ids.add(item['track']['id'])

for track_id in track_ids:
    print(track_id)

print(len(track_ids))





