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

    def get_song_source(self, source_link) -> any:
        """Returns source enum based on patternmatching source-input"""
        pass

    def get_yt_link(self, source_link) -> str:
        """Returns yt link for song as a string"""
        pass
    
    def add(self, song_url: str) -> None:
        """Adds song to queue and updates state"""

        self.song_queue.add(SongNode(song_url))

    def remove(self) -> None:
        """Removes first song from queue"""

        self.song_queue.remove()

    def play(self, voice_client) -> None:
        """Plays songs from queue through voice_client"""
        
        try:
            downloader = YoutubeDL({"format": "bestaudio", 'noplaylist':'True'})
            #song_info = downloader.extract_info(self.song_queue.get_song(),
            #                                    download=False)
            query = f"ytsearch:{self.song_queue.get_song()}"
            song_info = downloader.extract_info(query, download=False)
            stream_url = song_info['entries'][0]["url"]
            
            source = PCMVolumeTransformer(FFmpegPCMAudio(stream_url,
                                          **self.FFMPEG_OPTIONS), 1)
            voice_client.play(source,
                              after=lambda x: self.play_next(voice_client))
            
        except DownloadError: 
            self.song_queue.remove_first_song()

    def play_next(self, voice_client):
        """Removes first song and plays next song in queue"""

        self.song_queue.remove_first_song()
        if self.song_queue.head:
            self.play(voice_client)

    def clear_queue(self):
        self.song_queue = SongQueue()
