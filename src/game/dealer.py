from src.cards import Card, Hand, Shoe

class Dealer:
    """
    Represents the blackjack dealer, following fixed house rules.

    Attributes:
        hand (Hand): The dealer's current hand.
        hit_soft_17 (bool): Whether dealer hits on soft 17.
    """

    def __init__(self, hit_soft_17: bool = True) -> None:
        self.hand: Hand = Hand(is_dealer=True)
        self.hit_soft_17: bool = hit_soft_17

    def play(self, shoe: Shoe) -> None:
        """
        Play out the dealer's hand according to house rules.

        Args:
            shoe (Shoe): The shoe to draw cards from.
        """
        # Dealer must draw until reaching at least 17
        total, kind = self.hand.value
        while True:
            total, kind = self.hand.value
            # Stop if hard 17 or higher
            if total >= 17 and (kind == "Hard" or not self.hit_soft_17):
                break
            # If soft 17 and house stands, break
            if total == 17 and kind == "Soft" and not self.hit_soft_17:
                break
            # Otherwise, hit
            self.hand.add_card(shoe.draw_card())

    def reset_hand(self) -> None:
        """
        Clear the dealer's hand for the next round.
        """
        self.hand.reset()

    def upcard(self) -> Card:
        """
        Return the dealer's visible upcard.

        Raises:
            ValueError: If dealer has no cards.
        """
        if not self.hand.cards:
            raise ValueError("Dealer has no cards to show as upcard.")
        return self.hand.cards[0]

    def __repr__(self) -> str:
        return f"Dealer(hand={self.hand}, hit_soft_17={self.hit_soft_17})"