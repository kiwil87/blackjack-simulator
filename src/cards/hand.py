from .card import Card

class Hand:
    """
    Represents a blackjack hand, for either a player or the dealer.

    Attributes:
        cards (list[Card]): Cards currently in the hand.
        is_dealer (bool): Whether this hand belongs to the dealer.
    """

    def __init__(self, is_dealer: bool = False, current_bet: float = 1.0):
        self.cards: list[Card] = []
        self.is_dealer: bool = is_dealer
        self.current_bet: float = current_bet

    def add_card(self, card: Card) -> None:
        """
        Add a card to the hand.

        Args:
            card (Card): The card to add.
        """
        self.cards.append(card)

    def add_cards(self, cards: list[Card]) -> None:
        """
        Add multiple cards to the hand.

        Args:
            cards (list[Card]): List of cards to add.
        """
        self.cards.extend(cards)

    def reset(self) -> None:
        """
        Remove all cards from the hand.
        """
        self.cards.clear()

    def win(self, multiplier: float = 1.0) -> float:
        """
        The hand wins, we return the winnings to the player with the multiplier.

        Args:
            multiplier (float): Payout multiplier (e.g., 1.5 for blackjack).

        Returns:
            float: The payout amount.
        """
        payout = self.current_bet * (1 + multiplier)
        self.current_bet = 0.0
        return payout

    def lose(self) -> None:
        """
        Handle a losing hand (bet is already deducted).
        """
        self.current_bet = 0.0

    def push(self) -> float:
        """
        Handle a tie (push): return bet to bankroll.

        Returns:
            float: The bet amount returned to the player.
        """
        payout = self.current_bet
        self.current_bet = 0.0
        return payout

    @property
    def value(self) -> tuple[int, str]:
        """
        Calculate the best hand total and its type ("Hard" or "Soft").

        Uses Card.value() for individual card values (Aces count as 1) and adjusts
        for a single Ace as 11 if it doesn't bust.

        Returns:
            tuple[int, str]: (total, "Hard"/"Soft").
        """
        # Sum all card values, treating Aces as 1
        total = sum(card.value for card in self.cards)
        # Count Aces for potential soft adjustment
        aces = sum(1 for card in self.cards if card.rank == 'A')
        # If there's at least one Ace and treating one as 11 doesn't bust, it's soft
        if aces and total + 10 <= 21:
            return total + 10, "Soft"
        return total, "Hard"

    @property
    def is_soft(self) -> bool:
        """
        True if the hand is soft.
        """
        return self.value[1] == "Soft"

    @property
    def is_blackjack(self) -> bool:
        """
        True if the hand is a natural blackjack (two cards totaling 21).
        """
        return len(self.cards) == 2 and self.value[0] == 21

    @property
    def is_bust(self) -> bool:
        """
        True if the hand value exceeds 21.
        """
        return self.value[0] > 21

    @property
    def can_split(self) -> bool:
        """
        True if the hand can be split (exactly two cards of the same rank).
        """
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def display(self) -> str:
        """
        String representation of the hand

        Returns:
            str: Comma-separated card symbols
        """        
        cards_str = ", ".join(str(c) for c in self.cards)
        total, hand_type = self.value
        return f"{cards_str} ({hand_type} {total})"

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        # Always show all cards when converting to str
        return self.display()