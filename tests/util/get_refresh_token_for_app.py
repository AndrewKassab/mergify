import spotipy
import os
import json


SCOPE = 'playlist-modify-public playlist-read-private playlist-modify-private'

CLIENT_ID = os.environ['MERGIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['MERGIFY_CLIENT_SECRET']
REDIRECT_URI = os.environ['MERGIFY_REDIRECT_URI']
USERNAME = os.environ['MERGIFY_SEED_USERNAME']

cache_path = os.path.abspath(os.path.dirname(__file__) + ("./.cache-%s" % USERNAME))


spotipy.prompt_for_user_token(USERNAME, scope=SCOPE, client_secret=CLIENT_SECRET, client_id=CLIENT_ID, redirect_uri=REDIRECT_URI)

with open(cache_path) as token_data:
    data = json.load(token_data)
    print(data['refresh_token'])
