from enum import Enum, auto

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

class State(Enum):
    IDLE = auto()
    PLAYING = auto()
    PAUSED = auto()

class MusicPlayer:
    def __init__(self) -> None:
        """Music Player that control the audio state"""
        self.song_queue = SongQueue()
        self.current_song = None
        seld.state = State.IDLE
    
    def add(self, song_url: str) -> None:
        """Adds song to queue and updates state"""
        self.song_queue.add(SongNode(song_url))

    def remove(self) -> None:
        self.song_queue.remove()
