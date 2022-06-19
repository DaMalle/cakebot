import re
import asyncio
from dataclasses import dataclass

from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from cakebot.utils.general_utils import send_message


@dataclass(init=True)
class YoutubeSong:
    name: str = None
    stream_url: str = None
    is_valid: bool = False


class SongNode:
    def __init__(self, song: YoutubeSong) -> None:
        """Nodes used in linked lists"""

        self.song: YoutubeSong = song
        self.next = None

    def __repr__(self) -> str:
        return self.song


class SongQueue:
    def __init__(self) -> None:
        """Queue for songs to be played"""

        self.head = self.tail = None
    
    def get_song(self) -> YoutubeSong:
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
            nodes.append(node.song.name)
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

    def get_song_from_link(self, downloader, song_query) -> YoutubeSong:
        """Returns YoutubeSong-class """

        song = YoutubeSong()

        if "youtube.com/watch?v" in song_query or "youtu.be" in song_query:
            song_info = downloader.extract_info(song_query, download=False)

            song.name = song_info.get('title')
            song.stream_url = song_info.get('url')
            song.is_valid = True

        return song
        
    def get_song_from_search(self, downloader, song_query) -> YoutubeSong:
        """Searches YouTube with ytsearch and returns YoutubeSong-class"""

        query = f"ytsearch:{song_query}"
        song_info = downloader.extract_info(query, download=False)
        song = YoutubeSong()

        if song_info['entries']:
            song.name = song_info['entries'][0]['title']
            song.stream_url = song_info['entries'][0]['url']
            song.is_valid = True

        return song

    def get_yt_stream_url(self, song_query: str) -> YoutubeSong:
        """Returns YoutubeSong-class with name and streamlink to song"""
        
        downloader = YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'})

        if self.is_link(song_query):
            song = self.get_song_from_link(downloader, song_query)
        else:
            song = self.get_song_from_search(downloader, song_query)
        return song

    async def add(self, ctx, song_query: str) -> None:
        """Adds song to queue"""
        youtube_song = self.get_yt_stream_url(song_query)
        
        if youtube_song.is_valid:
            
            self.song_queue.add(SongNode(youtube_song))
            title = "You have a terrible taste in music, but it has been added to the queue"
            await send_message(ctx, title, f"{youtube_song.name}")

    def remove(self) -> None:
        """Removes first song from queue"""

        self.song_queue.remove_first_song()

    async def play(self, ctx) -> None:
        """Plays songs from queue through voice_client"""
        
        while self.song_queue.head:
        
            song = self.song_queue.get_song()
        
            source = PCMVolumeTransformer(FFmpegPCMAudio(song.stream_url,
                                          **self.FFMPEG_OPTIONS), 1)
            
            await send_message(ctx, "Now playing :cake:", song.name)

            ctx.voice_client.play(source)

            self.song_queue.remove_first_song()

    def get_queue(self):
        node = self.song_queue.head
        nodes = []

        while node:
            nodes.append(node.song.name)
            node = node.next

        return "\n".join(nodes)

    def clear_queue(self):
        self.song_queue = SongQueue()
