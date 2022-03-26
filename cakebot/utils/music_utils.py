from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from discord import FFmpegPCMAudio, PCMVolumeTransformer

class SongNode:
    def __init__(self, data) -> None:
        """Nodes used in linked lists"""
        self.data = data
        self.next = None

    def __repr__(self) -> str:
        return self.data

class SongQueue:
    def __init__(self) -> None:
        """Queue for songs to be played"""
        self.head = self.tail = None
    
    def get_song(self) -> str:
        if self.head:
            return self.head.data

    def add(self, node) -> None:
        """Adds a song to the end of the queue"""
        if self.tail:
            self.tail.next = node
            self.tail = self.tail.next
        else:
            self.head = self.tail = node

    def remove(self) -> None:
        """Removes first item from the queue"""
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
            nodes.append(node.data)
            node = node.next

        return " -> ".join(nodes)


class MusicPlayer:
    def __init__(self) -> None:
        """Music Player that control the audio state"""
        self.song_queue = SongQueue()

        self.ffmpeg_options = {
            'before_options': '-reconnect 1 \
                               -reconnect_streamed 1 \
                               -reconnect_delay_max 5', 
            'options': '-vn'
        }
        self.YTDL_options = {"format": "bestaudio"}
    
    def add(self, song_url: str) -> None:
        """Adds song to queue and updates state"""
        self.song_queue.add(SongNode(song_url))

    def remove(self) -> None:
        self.song_queue.remove()

    def play(self, voice_client) -> None: # todo finish
        """Plays song from song_url through voice_client"""
        
        try:
            info = YoutubeDL(self.YTDL_options).extract_info(self.song_queue.get_song(), download=False)
            stream_url = info.get("url")
            source = PCMVolumeTransformer(FFmpegPCMAudio(stream_url,
                                          **self.ffmpeg_options), 1)
            voice_client.play(source,
                              after=lambda x: self.play_next(voice_client))
        except DownloadError as e:
            self.song_queue.remove()
            

    def play_next(self, voice_client) -> None:
        self.song_queue.remove()
        if self.song_queue.head:
            self.play(voice_client)
