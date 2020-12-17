from unittest import TestCase
from spotify import SpotifyIndex


class SpotifyTest(TestCase):
    def setUp(self):
        self.si = SpotifyIndex()

    def test_add_playlist(self):
        self.assertEqual({}, self.si.get_playlists())
        self.si.add_playlist(
            'toffaha#2022', 'spotify:playlist:2mg5AgzPQmSmozBYCATGwh')
        self.assertEqual(
            {'toffaha#2022': 'https://open.spotify.com/playlist/2mg5AgzPQmSmozBYCATGwh'}, self.si.get_playlists())
