import spotipy
from spotify import *
import os
import unittest

# all values are stuff I've seeded onto the spotify test account akassabtester
refresh_token = os.environ.get('MERGIFY_TEST_REFRESH_TOKEN')
token = ''
playlist_one_name = 'test_one'
playlist_two_name = 'test_two'
playlist_one_id = '3Y8wge7Ler8F9PJ2cyBm7S'
playlist_two_id = '7JdlXBRIdGCi8oOPZGuAeJ'
playlist_ids = {playlist_one_id, playlist_two_id}
playlist_one_track_ids = {'2b4SSorCTQ2VzmllaeWuuT', '1JY6B9ILvmRla2IKKRZvnH'}
playlist_two_track_ids = {'2b4SSorCTQ2VzmllaeWuuT', '41SwdQIX8Hy2u6fuEDgvWr'}
expected_merge_tracks = {'2b4SSorCTQ2VzmllaeWuuT', '41SwdQIX8Hy2u6fuEDgvWr', '1JY6B9ILvmRla2IKKRZvnH'}

try:
    token = refresh_access_token(refresh_token)['access_token']
    sp = spotipy.Spotify(auth=token)
except:
    print('Missing or invalid refresh token in environment')


class SpotifyTest(unittest.TestCase):

    def test_get_user_playlists(self):
        playlist_dict = get_user_playlists(token)
        returned_playlist_ids = set(playlist_dict.keys())
        self.assertEqual(playlist_ids, returned_playlist_ids.intersection(playlist_ids))

    def test_get_track_ids_from_playlist(self):
        track_ids = get_track_ids_from_playlist(playlist_one_id, token)
        self.assertEqual(playlist_one_track_ids, track_ids)

    def test_merge_to_new_playlist(self):
        merged_playlist_id = merge_to_new_playlist(token, playlist_ids, 'Merge 1/2 Test')
        track_ids = get_track_ids_from_playlist(merged_playlist_id, token)
        self.assertEqual(expected_merge_tracks, track_ids)


if __name__ == '__main__':
    unittest.main()
