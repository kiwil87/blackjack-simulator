from cards import Card, Hand
from game import Action
from .strategy import Strategy

import random

class RandomStrategy(Strategy):
    """
    A strategy that randomly chooses between HIT and STAND.
    """
    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        return random.choice([Action.HIT, Action.STAND])


class AggressiveStrategy(Strategy):
    """
    An aggressive strategy: always hit if hand value is less than 17, otherwise stand.
    """
    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        # aggressive strategy: always hit under 17, otherwise stand
        if hand.value[0] < 17:
            return Action.HIT
        else:
            return Action.STAND


class SafeStrategy(Strategy):
    """
    A safe strategy: always hit if hand value is less than 12, otherwise stand.
    """
    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        # safe strategy: always hit under 12 Hard, otherwise stand
        if hand.value[0] <12 or hand.value[1] == "Soft":
            return Action.HIT
        else:
            return Action.STAND
        
        
class SplitStrategy(Strategy):
    """
    A strategy that splits pairs.
    """
    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        # split if the hand is a pair
        if hand.can_split:
            return Action.SPLIT
        else:
            return Action.STAND
        

class BasicStrategy(Strategy):
    """
    The basic blackjack strategy, being an approximation of the perfect strategy.
    """
    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        hand_value = hand.value[0]
        hand_is_soft = (hand.value[1] == "Soft")
        dealer_upcard_value = dealer_upcard.upcard_value

        # Pair-splitting decision 
        # 8 and A always split, 2, 3, 6, 7, 9 split against weak dealer upcard 2-6
        if hand.can_split:
            if hand.cards[0].value in [1, 8]:
                return Action.SPLIT
            elif hand.cards[0].value in [2, 3, 6, 7, 9] and dealer_upcard_value < 7:
                return Action.SPLIT
        
        # Soft hands
        if hand_is_soft:
            if hand_value <= 15:
                return Action.HIT
            elif 16 <= hand_value <= 18:
                if dealer_upcard_value >= 7 and len(hand.cards) == 2:
                    return Action.DOUBLE_DOWN
                else: # double down not allowed
                    return Action.HIT
            else:  # 19 to 21
                return Action.STAND
            
        # Hard hands
        elif hand_value <= 8:
            return Action.HIT
        elif hand_value == 9:
            if dealer_upcard_value < 7 and len(hand.cards) == 2:
                return Action.DOUBLE_DOWN
            else:
                return Action.HIT
        elif hand_value == 10:
            if dealer_upcard_value < 10 and len(hand.cards) == 2:
                return Action.DOUBLE_DOWN
            else:
                return Action.HIT
        elif hand_value == 11:
            if dealer_upcard_value < 11 and len(hand.cards) == 2:
                return Action.DOUBLE_DOWN
            else:
                return Action.HIT
        elif 12 <= hand_value <= 16:
            if dealer_upcard_value < 7:
                return Action.STAND
            else:
                return Action.HIT
        elif hand_value >= 17:
            return Action.STAND

        # Else raise an error
        raise ValueError("The action cannot be determined for the given hand and dealer upcard.")
    