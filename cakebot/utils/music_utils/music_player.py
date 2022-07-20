# built-in
import random
import re
import os
import asyncio
from collections import deque
from dataclasses import dataclass

# Third-party
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio

# local
from cakebot.utils.general_utils import send_message


@dataclass(init=True)
class YouTubeSong:
    title: str = None
    stream_url: str = None


class SpotifyHandler:
    def __init__(self) -> None:
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
        try:
            playlist = result["items"]
            return [f'{track["track"]["album"]["artists"][0]["name"]} {track["track"]["name"]}' for track in playlist]
        except KeyError:
            playlist = result["tracks"]["items"]
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


def get_song_query_from_link(song_query) -> list[str]:
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
        songs = SpotifyHandler().get_track(song_query)
    elif "open.spotify.com/playlist" in song_query:
        songs = SpotifyHandler().get_playlist(song_query)
    elif "open.spotify.com/album" in song_query:
        songs = SpotifyHandler().get_album(song_query)
    else:
        songs = [song_query]
    return songs


def is_link(song_query: str) -> bool:
    """Checks if self.song_query is a link or not"""

    regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
                       r"[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    return (re.match(regex, song_query) is not None)


def get_youtube_song_from_search(downloader, youtube_query) -> YouTubeSong:
    """Searches YouTube with ytsearch and returns stream-url and song title"""

    song = YouTubeSong()
    query = f"ytsearch:{youtube_query}"
    song_info = downloader.extract_info(query, download=False)

    if song_info['entries']:
        song.title = song_info['entries'][0]['title']
        song.stream_url = song_info['entries'][0]['url']

    return song


def get_song_from_youtube(youtube_query) -> YouTubeSong:
    """gets stream-url and song title from either link or search query"""

    downloader = YoutubeDL({'format': 'bestaudio', 
                            'noplaylist': 'True'})

    song = YouTubeSong()
    if is_link(youtube_query):
        song_info = downloader.extract_info(youtube_query, download=False)

        song.title = song_info.get('title')
        song.stream_url = song_info.get('url')
    else:
        song = get_youtube_song_from_search(downloader, youtube_query)
    return song

class MusicPlayer:
    def __init__(self) -> None:
        """Music Player that play songs from a queue"""

        self.song_queue = deque()
        # self.song_history = deque()
        # self.loop = False

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 \
                               -reconnect_streamed 1 \
                               -reconnect_delay_max 5',
            'options': '-vn'
        }

    async def add(self, ctx, song_query: str) -> None:
        """Adds songs to queue"""
        
        song_queries = get_song_query_from_link(song_query)
        self.song_queue.extend(reversed(song_queries))
        title = "You have a terrible music taste, "\
                "but it has been added to the queue"
        await send_message(ctx, title)

    async def play(self, ctx) -> None:
        """Plays songs from queue through voice_client"""

        if self.song_queue:
            song_query = self.song_queue.pop()
            song = get_song_from_youtube(song_query)
            if song.stream_url is not None:
                source = FFmpegPCMAudio(song.stream_url, **self.FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda _: ctx.voice_client.loop.create_task(self.play(ctx)))
                await send_message(ctx, "Now playing :cake:", song.title)

    def get_queue(self):
        return "\n".join([song.title for song in self.song_queue])

    def clear_queue(self):
        self.song_queue.clear()

    def shuffle(self):
        random.shuffle(self.song_queue)
