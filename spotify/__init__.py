import os
import random
import requests
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from utils import NotEnoughSongsError

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')


class SpotifyIndex:
    def __init__(self):
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
        self.playlists = {'ChilledCow': self.sp.playlist(
            'spotify:playlist:31FWVQBp3WQydWLNhO0ACi')}

     # 'Static' functions (don't rely on app state aka self.playlists)
    def get_tracklink_by_id(self, tid: str):
        track = self.sp.track(tid)
        return track['external_urls']['spotify']

    def check_playlist_structure(self):
        return self.sp.playlist('spotify:playlist:1CHdgx6xv0rIW74aMFT2IJ')

     # Setters
    def add_playlist(self, dUser: str, playlist: str):
        self.playlists[dUser] = self.sp.playlist(playlist)
        return self.get_playlist(dUser)

    # Getters

    def get_playlists(self):
        minified = {}
        for dUser in self.playlists:
            minified[dUser] = self.playlists.get(
                dUser)['external_urls']['spotify']
        return minified

    def get_playlist(self, dUser: str):
        pl = self.playlists.get(dUser)
        if(pl == None):
            return None
        return pl['external_urls']['spotify']

    # for !suggest command
    def get_track_from_collective_playlist(self, count=1):
        gigalist = []
        lengthOfAll = 0
        for dUser in self.playlists:
            curList = self.playlists.get(dUser)['tracks']['items']
            lengthOfAll += len(curList)
            gigalist.append(curList)
        if(lengthOfAll < count):
            raise NotEnoughSongsError(
                f'All playlists collectively hold but {lengthOfAll} songs.')
        tracks = []
        for i in range(count):
            wacky_list = random.randint(0, len(gigalist)-1)
            wacky_choice = random.randint(0, len(gigalist[wacky_list])-1)
            track = gigalist[wacky_list][wacky_choice]['track']['external_urls']['spotify']
            tracks.append(track)

        return tracks

    def get_track_from_user_playlist(self, dUser: str, count=1):
        playlist_tracks = self.playlists.get(dUser)['tracks']['items']
        if(playlist_tracks == None):
            raise TypeError
        if(count > len(playlist_tracks)):
            raise IndexError
        tracks = []
        for i in range(count):
            wacky_choice = random.randint(1, len(playlist_tracks))
            track = playlist_tracks[wacky_choice]['track']['external_urls']['spotify']
            tracks.append(track)

        return tracks
