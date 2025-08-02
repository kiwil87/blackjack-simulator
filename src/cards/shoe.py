from .card import Card
import random

class Shoe:
    """
    Represents a dealer's shoe containing multiple decks of cards for blackjack.

    Attributes:
        num_decks (int): Number of decks in the shoe (4 through 8).
        cards (list[Card]): The current stack of cards in the shoe.
    """

    MIN_DECKS: int = 1
    MAX_DECKS: int = 8

    def __init__(
            self, 
            num_decks: int = 6, 
            shuffle_on_init: bool = True,
            penetration_threshold: float = 0.75
            ) -> None:
        """
        Initialize a new Shoe instance.

        Args:
            num_decks (int, optional): Number of decks to include (between 1 and 8). Defaults to 6.
            shuffle_on_init (bool, optional): Whether to shuffle the shoe upon creation. Defaults to True.
            penetration_threshold (float, optional): The penetration threshold for the shoe. Defaults to 0.75.

        Raises:
            ValueError: If num_decks is outside the allowed range.
        """
        if not (self.MIN_DECKS <= num_decks <= self.MAX_DECKS):
            raise ValueError(f"num_decks must be between {self.MIN_DECKS} and {self.MAX_DECKS}.")
        self.num_decks: int = num_decks
        # Build the shoe by repeating a 52-card deck
        self._original_cards: list[Card] = Card.create_deck() * self.num_decks
        self.cards: list[Card] = list(self._original_cards)

        # Calculate the penetration point
        if not (0 < penetration_threshold < 1):
            raise ValueError("penetration_threshold must be between 0 and 1.")
        
        # Set the penetration point based on the threshold
        self.penetration_threshold: float = penetration_threshold

        # Calculate the number of cards to keep in the shoe based on penetration
        self.penetration_cut_index: int = int(len(self.cards) * (1-penetration_threshold))

        # Shuffle the shoe if required
        self.shuffle_on_init: bool = shuffle_on_init
        if shuffle_on_init:
            self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the cards in the shoe."""
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        """
        Draw a single card from the top of the shoe.

        Returns:
            Card: The drawn card.

        Raises:
            IndexError: If the shoe is empty.
        """
        if len(self.cards) <= self.penetration_cut_index:
            self.reset(shuffle=self.shuffle_on_init)

        return self.cards.pop(0)

    @property
    def remaining(self) -> int:
        """Get the number of remaining cards in the shoe."""
        return len(self.cards)

    def reset(self, shuffle: bool = True) -> None:
        """
        Reset the shoe to its original full state.

        Args:
            shuffle (bool, optional): Whether to shuffle after resetting. Defaults to True.
        """
        self.cards = list(self._original_cards)
        if shuffle:
            self.shuffle()

    def display(self) -> str:
        """
        Display the first few cards in the shoe for debugging.

        Returns:
            str: A string representation of the shoe.
        """
        for i, card in enumerate(self.cards[:5]):
            print(f"{i+1}: {card}")
        return f"Shoe with {self.num_decks} decks, {len(self.cards)} cards remaining."

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"Shoe(num_decks={self.num_decks}, remaining_cards={len(self.cards)})"

    def __str__(self) -> str:
        """Return a user-friendly string for the Shoe."""
        return self.display()