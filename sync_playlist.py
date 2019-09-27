import config
import spotipy
import spotipy.util as auth

token = auth.prompt_for_user_token(config.USERNAME, 'playlist-modify-private',
                                   config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET,
                                   config.SPOTIPY_REDIRECT_URI)

destination_playlist_id = config.DESTINATION_PLAYLIST_ID
source_playlist_ids = config.SOURCE_PLAYLIST_IDS
sp = spotipy.Spotify(auth=token)

tracks = set()

for playlist_id in source_playlist_ids:
    offset = 0
    playlist_tracks = sp.user_playlist_tracks(config.USERNAME, playlist_id, fields=None,
                                              limit=100, offset=offset, market=None)
    while len(playlist_tracks['items']) > 0:
        for j, item in enumerate(tracks['items']):
            tracks.add(item['track']['id'])
        offset += 100
        playlist_tracks = sp.user_playlist_tracks(config.USERNAME, playlist_id, fields=None,
                                                  limit=100, offset=offset, market=None)



