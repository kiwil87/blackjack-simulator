class Card:
    """
    Represents a playing card in a blackjack simulation.

    Attributes:
        rank (str): Rank of the card, e.g., '2'-'10', 'J', 'Q', 'K', 'A'.
        suit (str): Suit of the card, e.g., 'Hearts', 'Diamonds', 'Clubs', 'Spades'.
    """

    # Class-level constants
    SUITS: list[str] = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    SYMBOLS: dict[str, str] = {'Hearts':'♥', 'Diamonds':'♦', 'Clubs':'♣', 'Spades':'♠'}
    RANKS: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    VALUES: dict[str, int] = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 1 # Aces are counted as 1 by default
    }

    def __init__(self, rank: str, suit: str) -> None:
        """
        Initialize a new Card instance.

        Args:
            rank (str): The rank of the card.
            suit (str): The suit of the card.

        Raises:
            ValueError: If rank or suit is not valid.
        """
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank '{rank}'. Must be one of {self.RANKS}.")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit '{suit}'. Must be one of {self.SUITS}.")
        self.rank: str = rank
        self.suit: str = suit

    @property
    def value(self) -> int:
        """
        Get the blackjack value of this card.

        Note:
            Aces count as 1 by default; adjusting to 11 should be handled in hand logic.
        """
        return self.VALUES[self.rank]
    
    @property
    def upcard_value(self) -> int:
        """
        Return the blackjack value of the dealer's upcard (first card) as an int from 2 to 11.
        Treats Ace as 11.

        Raises:
            ValueError: If the hand has no cards.
        """
        # Ace as 11, others use card.value
        return 11 if self.rank == 'A' else self.value

    def display(self) -> str:
        """
        String representation of the card

        Returns:
            str: card symbols
        """        
        return f"{self.rank}{self.SYMBOLS[self.suit]}"

    def __str__(self) -> str:
        # Always show all cards when converting to str
        return self.display()

    def __repr__(self) -> str:
        """Return an unambiguous representation of the Card."""
        return f"Card(rank='{self.rank}', suit='{self.suit}')"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    @classmethod
    def create_deck(cls) -> list['Card']:
        """
        Create a standard 52-card deck.

        Returns:
            List[Card]: A list of all cards in a fresh deck.
        """
        return [cls(rank, suit) for suit in cls.SUITS for rank in cls.RANKS]