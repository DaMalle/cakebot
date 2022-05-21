from enum import Enum, auto, unique


@unique
class BotState(Enum):
    """ State of discord bot. """
    IDLE = auto()
    PLAYING_MUSIC = auto()
    PAUSED_MUSIC = auto()
