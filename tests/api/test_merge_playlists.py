import unittest
import requests
import os

token = os.environ.get('MERGIFY_SEED_TOKEN')
username = os.environ.get('MERGIFY_SEED_USERNAME')
MERGE_ENDPOINT = "http://localhost:5000/merge"


class MergePlaylistsTest(unittest.TestCase):

    def test(self):
        response = requests.post(url=MERGE_ENDPOINT, data=data)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
