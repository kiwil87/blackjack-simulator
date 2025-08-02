from enum import Enum, auto

class Action(Enum):
    """
    Possible player actions in a blackjack game.
    """
    HIT = auto()
    STAND = auto()
    DOUBLE_DOWN = auto()
    SPLIT = auto()
    #SURRENDER = auto()