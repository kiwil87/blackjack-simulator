from cards import Card, Hand
from game.action import Action
from .strategy import Strategy

import numpy as np

class PerfectStrategy(Strategy):
    """
    The perfect blackjack strategy as known from charts with 4-8 decks and dealer hits on soft 17.
    """
    def __init__(self):
        # SPLIT table: rows index first-card value (1–10), Aces count as 1, cols index dealer upcard value (2–11)
        self.split_table = np.full((11, 12), np.nan, dtype=object)
        # HARD totals table: rows index total 0–20, cols index dealer upcard value 2–11
        self.hard_double_allowed_table = np.full((21, 12), np.nan, dtype=object)
        # HARD totals table: rows index total 0–20, cols index dealer upcard value 2–11
        self.hard_double_forbidden_table = np.full((21, 12), np.nan, dtype=object)
        # SOFT totals table: rows index total 0–20, cols index dealer upcard value 2–11
        self.soft_double_allowed_table = np.full((21, 12), np.nan, dtype=object)
        # SOFT totals table: rows index total 0–20, cols index dealer upcard value 2–11
        self.soft_double_forbidden_table = np.full((21, 12), np.nan, dtype=object)

        self.fill_tables()


    def fill_tables(self):
        """
        Fill the strategy tables with the defined actions.
        """
        ########################
        # SPLIT table
        # Always split A,A (row 1)
        self.split_table[1, 2:] = Action.SPLIT

        # Split 2s and 3s vs dealer 2–7
        self.split_table[2:4, 2:8] = Action.SPLIT
        self.split_table[2:4, 8:] = Action.HIT

        # Split 4s vs dealer 5–6
        self.split_table[4, 2:5] = Action.HIT
        self.split_table[4, 5:7] = Action.SPLIT
        self.split_table[4, 7:] = Action.HIT

        # Pair of 5s: never split and treat as 10
        self.split_table[5, 2:10] = Action.DOUBLE_DOWN
        self.split_table[5, 10:] = Action.HIT
        
        # Split 6s vs dealer 2–6
        self.split_table[6, 2:7] = Action.SPLIT
        self.split_table[6, 7:] = Action.HIT

        # Split 7s vs dealer 2–7
        self.split_table[7, 2:8] = Action.SPLIT
        self.split_table[7, 8:] = Action.HIT

        # Always split 8s (row 8)
        self.split_table[8, 2:] = Action.SPLIT

        # Split 9s vs dealer 2–6,8–9
        self.split_table[9, 2:7] = Action.SPLIT
        self.split_table[9, 7] = Action.STAND
        self.split_table[9, 8:10] = Action.SPLIT
        self.split_table[9, 10:] = Action.STAND

        # Pair of 10s: never split
        self.split_table[10, 2:] = Action.STAND


        ########################
        # HARD totals table
        # Totals 17-21: always stand
        self.hard_double_allowed_table[17:, 2:] = Action.STAND
        self.hard_double_forbidden_table[17:, 2:] = Action.STAND

        # Totals 13–16: stand vs dealer 2–6 and hit vs 7–11
        self.hard_double_allowed_table[13:17, 2:7] = Action.STAND
        self.hard_double_allowed_table[13:17, 7:] = Action.HIT
        self.hard_double_forbidden_table[13:17, 2:7] = Action.STAND
        self.hard_double_forbidden_table[13:17, 7:] = Action.HIT
        
        # Total 12: stand vs dealer 4–6 else hit
        self.hard_double_allowed_table[12, 2:4] = Action.HIT
        self.hard_double_allowed_table[12, 4:7] = Action.STAND
        self.hard_double_allowed_table[12, 7:] = Action.HIT
        self.hard_double_forbidden_table[12, 2:4] = Action.HIT
        self.hard_double_forbidden_table[12, 4:7] = Action.STAND
        self.hard_double_forbidden_table[12, 7:] = Action.HIT

        # Total 11: double when allowed (otherwise hit) vs dealer 2–10 else hit
        self.hard_double_allowed_table[11, 2:11] = Action.DOUBLE_DOWN
        self.hard_double_allowed_table[11, 11] = Action.HIT
        self.hard_double_forbidden_table[11, 2:] = Action.HIT

        # Total 10: double when allowed (otherwise hit) vs dealer 2–9 else hit
        self.hard_double_allowed_table[10, 2:10] = Action.DOUBLE_DOWN
        self.hard_double_allowed_table[10, 10:] = Action.HIT
        self.hard_double_forbidden_table[10, 2:] = Action.HIT

        # Total 9: double when allowed (otherwise hit) vs dealer 3–6 else hit
        self.hard_double_allowed_table[9, 2] = Action.HIT
        self.hard_double_allowed_table[9, 3:7] = Action.DOUBLE_DOWN
        self.hard_double_allowed_table[9, 7:] = Action.HIT
        self.hard_double_forbidden_table[9, 2:] = Action.HIT

        # Totals 2–8: always hit
        self.hard_double_allowed_table[2:9, 2:] = Action.HIT
        self.hard_double_forbidden_table[2:9, 2:] = Action.HIT


        ########################
        # SOFT totals table
        # A,9 (20): always stand
        self.soft_double_allowed_table[20, 2:] = Action.STAND
        self.soft_double_forbidden_table[20, 2:] = Action.STAND

        # A,8 (19): double when allowed (otherwise stand) vs dealer 6 else stand
        self.soft_double_allowed_table[19, 2:6] = Action.STAND
        self.soft_double_allowed_table[19, 6] = Action.DOUBLE_DOWN
        self.soft_double_allowed_table[19, 7:] = Action.STAND
        self.soft_double_forbidden_table[19, 2:] = Action.STAND

        # A,7 (18): double when allowed (otherwise stand) vs dealer 2–6, stand vs 7,8, hit vs 9,10,11
        self.soft_double_allowed_table[18, 2:7] = Action.DOUBLE_DOWN
        self.soft_double_allowed_table[18, 7:9] = Action.STAND
        self.soft_double_allowed_table[18, 9:] = Action.HIT
        self.soft_double_forbidden_table[18, 2:9] = Action.STAND
        self.soft_double_forbidden_table[18, 9:] = Action.HIT

        # A,6 (17): double when allowed (otherwise hit) vs dealer 3–6, hit vs 2,7–11
        self.soft_double_allowed_table[17, 2] = Action.HIT
        self.soft_double_allowed_table[17, 3:7] = Action.DOUBLE_DOWN
        self.soft_double_allowed_table[17, 7:] = Action.HIT
        self.soft_double_forbidden_table[17, 2:] = Action.HIT

        # A,4 (15) & A,5 (16): double when allowed (otherwise hit) vs dealer 4–6, hit vs 2–4,7–11
        self.soft_double_allowed_table[15:17, 2:4] = Action.HIT
        self.soft_double_allowed_table[15:17, 4:7] = Action.DOUBLE_DOWN
        self.soft_double_allowed_table[15:17, 7:] = Action.HIT
        self.soft_double_forbidden_table[15:17, 2:] = Action.HIT

        # A,2 (13) & A,3 (14): double when allowed (otherwise hit) vs dealer 5–6, hit vs 2–4,7–11
        self.soft_double_allowed_table[13:15, 2:5] = Action.HIT
        self.soft_double_allowed_table[13:15, 5:7] = Action.DOUBLE_DOWN
        self.soft_double_allowed_table[13:15, 7:] = Action.HIT
        self.soft_double_forbidden_table[13:15, 2:] = Action.HIT


    def next_move(self, hand: Hand, dealer_upcard: Card) -> Action:
        hand_value = hand.value[0]
        hand_is_soft = (hand.value[1] == "Soft")
        hand_is_hard = (hand.value[1] == "Hard")
        dealer_value = dealer_upcard.upcard_value

        # Pair-splitting decision 
        if hand.can_split:
            row = hand.cards[0].value
            action = self.split_table[row, dealer_value]
        
        # Soft totals (only on two-card soft hands i.e. double down is allowed)
        elif hand_is_soft and len(hand.cards) == 2:
            total = hand_value
            action = self.soft_double_allowed_table[total, dealer_value]
        
        # Soft totals (on soft hands with more than two cards i.e. double down is forbidden)
        elif hand_is_soft and len(hand.cards) > 2:
            total = hand_value
            action = self.soft_double_forbidden_table[total, dealer_value]

        # Hard totals (only on two-card hands i.e. double down is allowed)
        elif hand_is_hard and len(hand.cards) == 2:
            total = hand_value
            action = self.hard_double_allowed_table[total, dealer_value]

        # Hard totals (on hard hands with more than two cards i.e. double down is forbidden)
        elif hand_is_hard and len(hand.cards) > 2:
            total = hand_value
            action = self.hard_double_forbidden_table[total, dealer_value]

        # Else raise an error
        else :
            raise ValueError("Invalid hand type or length for perfect strategy.")

        return action