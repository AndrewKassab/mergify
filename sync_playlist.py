import spotipy
import spotipy.util as auth
import os
import sys
import json

scope = 'playlist-read-private playlist-modify-private'

# Export these in your environment
username = os.environ['SPOTIFY_USERNAME']
spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']

data_file_path = '.playlist_sync.json'

# In your terminal, export these values as described in the readme.
token = auth.prompt_for_user_token(username, scope, spotify_client_id,
                                   spotify_client_secret, spotify_redirect_uri)

sp = spotipy.Spotify(auth=token)


# First time use or after a reset
def setup():
    user_playlists_list = []
    offset = 0
    while True:
        response = sp.user_playlists(username, offset=offset)['items']
        if len(response) == 0:
            break
        user_playlists_list.extend(response)
        offset = offset + 50
    user_playlists = {}
    for item in user_playlists_list:
        user_playlists[item['name']] = item['uri'][17:]

    playlist_name = ""
    json_data = {}
    while True:
        playlist_name = input('Enter the name of the destination playlist you would like to sync to: ')
        if playlist_name in user_playlists:
            break
        print('Playlist does not exist, please try again.')
    json_data["destination_playlist"] = {"name": playlist_name, "id": user_playlists[playlist_name]}
    json_data["source_playlists"] = []
    while True:
        playlist_name = input('Enter name of a source playlist you would like to sync from, or blank when finished: ')
        if playlist_name == "":
            break
        if playlist_name not in user_playlists:
            print('Playlist does not exist, please try again.')
            continue
        json_data["source_playlists"].append({"name": playlist_name, "id": user_playlists[playlist_name]})
    if len(json_data["source_playlists"]) == 0:
        print('Error, no source playlists specified, restarting setup...')
        setup()
        return
    with open(data_file_path, 'w') as json_file:
        json.dump(json_data, json_file)


# script begins
if not os.path.isfile(data_file_path):
    setup()

with open(data_file_path, 'r') as data_file:
    data = json.load(data_file)

source_track_ids = set()
destination_track_ids = set()
source_playlist_names = []
source_playlist_ids = []
for playlist in data['source_playlists']:
    source_playlist_ids.append(playlist['id'])
    source_playlist_names.append(playlist['name'])
destination_playlist_name = data['destination_playlist']['name']
destination_playlist_id = data['destination_playlist']['id']

print('Welcome to Playlist-Sync. If you would like to reset, delete the .playlist_sync.json file in your home directory')
print('Source playlists: ', source_playlist_names)
print('Destination playlist: ', destination_playlist_name)

print("Retrieving songs...")
# get track ids from source playlists
for playlist_id in source_playlist_ids:
    playlist_tracks = []
    while True:
        response = sp.playlist_tracks(playlist_id, offset=len(playlist_tracks),
                                      fields='items.track.id, total')
        playlist_tracks.extend(response['items'])
        if len(response['items']) == 0:
            break
    for item in playlist_tracks:
        source_track_ids.add(item['track']['id'])

# get track ids from destination playlist
destination_playlist_tracks = []
while True:
    response = sp.playlist_tracks(destination_playlist_id,
                                           offset=len(destination_playlist_tracks), fields='items.track.id, total')
    destination_playlist_tracks.extend(response['items'])
    if len(response['items']) == 0:
        break
for item in destination_playlist_tracks:
    destination_track_ids.add(item['track']['id'])

except_set = source_track_ids - destination_track_ids

track_ids_to_add = list(source_track_ids - destination_track_ids)

print('Syncing songs to destination...')
# add 100 tracks at a time
offset = 0
while True:
    track_ids_to_add_shrunk = track_ids_to_add[offset:offset+100]
    if (len(track_ids_to_add_shrunk) == 0):
        break
    sp.user_playlist_add_tracks(username, destination_playlist_id, track_ids_to_add_shrunk)
    offset = offset + 100

print('Sync Complete.')
