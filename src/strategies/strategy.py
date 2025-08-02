from src.cards import Card, Hand
from src.game.action import Action
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        pass