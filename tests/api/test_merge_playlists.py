import unittest
import requests
import os
import json
import spotipy

MERGE_ENDPOINT = "http://localhost:5000/merge"
REFRESH_ENDPOINT = "http://localhost:5000/refresh"
seed_username = os.environ.get('MERGIFY_SEED_USERNAME')

p_one_song_ids = ['2nelvMgL7LyIUAYwmmRyy1', '17ZcPzaRXy9nbV5wbbpiaO']
p_two_song_ids = ['0u8AnQEMd9W6fDG2UbFjyz', '17ZcPzaRXy9nbV5wbbpiaO']


class MergePlaylistsTest(unittest.TestCase):

    token = os.environ.get('MERGIFY_SEED_TOKEN')

    @classmethod
    def setUpClass(cls):
        super(MergePlaylistsTest, cls).setUpClass()
        headers = {'access_token': cls.token}
        data = {'username': seed_username}
        session = requests.Session()
        response = session.post(url=REFRESH_ENDPOINT, headers=headers, data=data)
        if response.status_code != 201:
            assert False, "Token not refreshed"
        content = json.loads(response.content)
        cls.token = content['access_token']
        cls.sp = spotipy.Spotify(auth=cls.token)
        who = cls.sp.me()
        resp = cls.sp.user_playlist_create(name="Playlist One", public=False)
        resp = cls.sp.user_playlist_create(user=seed_username, name="Playlist Two", public=False)
        cls.sp.user_playlist_add_tracks(user=seed_username, playlist_id=1, tracks=p_one_song_ids)
        cls.sp.user_playlist_add_tracks(user=seed_username, playlist_id=2, tracks=p_two_song_ids)

    def test_missing_playlists(self):
        headers = {'access_token': self.token}
        data = {'username': seed_username}
        session = requests.Session()
        response = session.post(url=MERGE_ENDPOINT, headers=headers, data=data)
        content = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(content['error_detail'], 'Bad Request')
        if content.get('access_token'):
            self.token = content['access_token']

    def test_invalid_playlists(self):
        headers = {'access_token': self.token}
        data = {'source_playlists': 'sff3234', 'destination_playlist': 'asd213', 'username': seed_username}
        session = requests.Session()
        response = session.post(url=MERGE_ENDPOINT, headers=headers, data=data)
        content = json.loads(response.content)
        self.assertEqual(404, response.status_code)
        if content.get('access_token'):
            self.token = content['access_token']





if __name__ == '__main__':
    unittest.main()
