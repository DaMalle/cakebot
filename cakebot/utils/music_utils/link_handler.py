import re
import os
import spotipy
from dataclasses import dataclass
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from yt_dlp import YoutubeDL


@dataclass(init=True)
class YouTubeSong:
    title: str = None
    stream_url: str = None


class SpotifyHandler:
    def __init__(self, downloader) -> None:
        self.downloader = downloader
        load_dotenv()  # Get access to .env
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
            )
        )
    
    def get_track(self, query) -> list[str]:
        """returns artist and title of a track"""

        spotify_query = query.split("/")[-1]
        print(spotify_query)
        result = self.api.track(
            track_id=spotify_query,
            market="DK"
        )
        artists = result["artists"][0]["name"]
        song_name = result["album"]["name"]
        return [f"{artists} {song_name}"]
    
    def get_playlist(self, query) -> list[str]:
        """returns artist and title of a playlist"""

        spotify_query = query.split("/")[-1]
        result = self.api.playlist_tracks(
            playlist_id=spotify_query,
            market="DK"
        )
        
        playlist = result["items"] # ["tracks"]
        return [f'{track["track"]["album"]["artists"][0]["name"]} {track["track"]["name"]}' for track in playlist]
    
    def get_album(self, query) -> list[str]:
        """returns artist and title of a album"""

        spotify_query = query.split("/")[-1]
        self.api.album_tracks(
            album_id=spotify_query,
            market="DK"
        )
        album = result["tracks"]
        return [f'{track["artists"][0]["name"]} {track["name"]}' for track in result["tracks"]["items"]]


def is_link(song_query: str) -> bool:
    """Checks if self.song_query is a link or not"""

    regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
                       r"[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    return (re.match(regex, song_query) is not None)


def get_song_query_from_search(downloader, song_query) -> YouTubeSong:
    """Searches YouTube with ytsearch and returns stream-url and song title"""

    song = YouTubeSong()
    query = f"ytsearch:{song_query}"
    song_info = downloader.extract_info(query, download=False)

    if song_info['entries']:
        song.title = song_info['entries'][0]['title']
        song.stream_url = song_info['entries'][0]['url']

    return song


def get_song_query_from_link(downloader, song_query) -> list[str]:
    """Returns list of song queries, either as link or search text
    Supports:
    youtube standard videos
    spotify track
    spotify playlist
    spotify albums
    """

    if "www.youtube.com/playlist?list" in song_query:
        pass
    elif "youtube.com/watch?" in song_query or "youtu.be" in song_query:
        songs = [song]
    elif "open.spotify.com/track" in song_query:
        songs = SpotifyHandler(downloader).get_track(song_query)
    elif "open.spotify.com/playlist" in song_query:
        songs = SpotifyHandler(downloader).get_playlist(song_query)
    elif "open.spotify.com/album" in song_query:
        songs = SpotifyHandler(downloader).get_album(song_query)
    else:
        songs = [song_query]
    return songs