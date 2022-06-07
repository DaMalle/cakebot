from pickle import NONE
import re

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from discord import FFmpegPCMAudio, PCMVolumeTransformer

from cakebot.utils.general_utils import BotState


class SongNode:
    def __init__(self, song: str) -> None:
        """Nodes used in linked lists"""

        self.song = song
        self.next = None

    def __repr__(self) -> str:
        return self.song


class SongQueue:
    def __init__(self) -> None:
        """Queue for songs to be played"""

        self.head = self.tail = None
    
    def get_song(self) -> str:
        """Gets first song in queue"""

        if self.head:
            return self.head.song

    def add(self, node: SongNode) -> None:
        """Adds a song to the end of the queue"""

        if self.tail:
            self.tail.next = node
            self.tail = self.tail.next
        else:
            self.head = self.tail = node

    def remove_first_song(self) -> None:
        """Removes first song from the queue"""

        if self.head:
            self.head = self.head.next
        if not self.head:
            self.tail = None

    def shuffle(self):
        """shuffles queue with fisher & yates algoritm"""
        pass

    def __repr__(self) -> str:
        node = self.head
        nodes = []

        while node:
            nodes.append(node.song)
            node = node.next

        return " -> ".join(nodes)

class MusicPlayer:
    def __init__(self) -> None:
        """Music Player that play songs from a queue (fifo)"""

        self.song_queue = SongQueue()

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 \
                               -reconnect_streamed 1 \
                               -reconnect_delay_max 5', 
            'options': '-vn'
        }

    def is_link(self, song_query: str) -> bool:
        """Checks if self.song_query is a link or not"""

        regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]\
                            |[$-_@.&+]|[!*\(\),] \|(?:%\
                            [0-9a-fA-F][0-9a-fA-F]))+')

        return (re.match(regex, song_query) is not None)
    
    def get_yt_stream_url(self, song_query: str) -> str:
        """Returns a streaming url for musicplayer"""

        downloader = YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'})
        
        if self.is_link(song_query):
            if "youtube.com/watch?v" in song_query:
                song_info = downloader.extract_info(song_query, download=False)
                stream_url = song_info.get("url")
        else:
            query = f"ytsearch:{song_query}"
            song_info = downloader.extract_info(query, download=False)
            if song_info['entries']:
                stream_url = song_info['entries'][0]['url']
            else:
                stream_url = None

        return stream_url

    def add(self, song_query: str) -> None:
        """Adds song to queue"""

        song_url = self.get_yt_stream_url(song_query)
        
        if song_url is not None:
            self.song_queue.add(SongNode(song_url))

    def remove(self) -> None:
        """Removes first song from queue"""

        self.song_queue.remove_first_song()

    def play(self, voice_client) -> None:
        """Plays songs from queue through voice_client"""

        source = PCMVolumeTransformer(FFmpegPCMAudio(self.song_queue.get_song(),
                                          **self.FFMPEG_OPTIONS), 1)
        voice_client.play(source, after=lambda x: self.play_next(voice_client))


    def play_next(self, voice_client):
        """Removes the first song and plays the next song in queue"""

        self.song_queue.remove_first_song()
        if self.song_queue.head:
            self.play(voice_client)

    def clear_queue(self):
        self.song_queue = SongQueue()