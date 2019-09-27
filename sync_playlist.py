import config
import spotipy
import spotipy.util as auth

sp = spotipy.Spotify()
auth.prompt_for_user_token('123881475', 'playlist_modify-private', config.SPOTIPY_CLIENT_ID,
                           config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI)

