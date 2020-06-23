import unittest
import requests
import os
import json

token = os.environ.get('MERGIFY_SEED_TOKEN')
seed_username = os.environ.get('MERGIFY_SEED_USERNAME')
MERGE_ENDPOINT = "http://localhost:5000/merge"


class MergePlaylistsTest(unittest.TestCase):

    def test_missing_playlists(self):
        headers = {'access_token': token}
        data = {'username': seed_username}
        session = requests.Session()
        response = session.post(url=MERGE_ENDPOINT, headers=headers, data=data)
        content = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(content['error_detail'], 'Bad Request')

    def test_invalid_playlists(self):
        headers = {'access_token': token}
        data = {'source_playlists': 'sff3234', 'destination_playlist': 'asd213', 'username': seed_username}
        session = requests.Session()
        response = session.post(url=MERGE_ENDPOINT, headers=headers, data=data)
        self.assertEqual(404, response.status_code)



if __name__ == '__main__':
    unittest.main()
