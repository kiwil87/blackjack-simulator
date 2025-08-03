from cards import Card, Hand 
from .action import Action
from strategies import Strategy

class Player:
    """
    Represents a blackjack player, including bankroll management and decision making.

    Attributes:
        name (str): The player's name or identifier.
        bankroll (float): The amount of money the player has available.
        strategy (Strategy): The strategy object that dictates betting and play decisions.
        hands (List[Hand]): Current list of active hands (supporting splits).
        current_bet (float): The amount wagered on the current hand.
    """
    def __init__(self, name: str, bankroll: float, strategy: Strategy) -> None:
        self.name: str = name
        self.bankroll: float = bankroll
        self.strategy: Strategy = strategy
        self.hands: list[Hand] = []
        self.current_bet: float = 0.0

    def place_bet(self, amount: float) -> None:
        """
        Place a wager for the upcoming round.

        Args:
            amount (float): Amount to bet

        Raises:
            ValueError: If amount is non-positive or exceeds bankroll.
        """
        if amount <= 0:
            raise ValueError(f"Bet must be positive; got {amount}.")

        self.current_bet = amount
        self.bankroll -= amount
    
    def add_hand(self, hand: Hand) -> None:
        """
        Add a new hand to the player's active hands.

        Args:
            hand (Hand): The hand to add.
        """
        self.hands.append(hand)

    def decide(self, hand: Hand, dealer_upcard: Card) -> Action:
        """
        Choose the next action for a given hand based on the player's strategy.

        Args:
            hand (Hand): The player's hand to act on.
            dealer_upcard (Card): The dealer's visible card.

        Returns:
            Action: The chosen move (HIT, STAND, DOUBLE_DOWN, SPLIT, etc.).
        """
        return self.strategy.next_move(hand, dealer_upcard)

    def win(self, multiplier: float = 1.0) -> None:
        """
        Award winnings to the player's bankroll.

        Args:
            multiplier (float): Payout multiplier (e.g., 1.5 for blackjack).
        """
        payout = self.current_bet * (1 + multiplier)
        self.bankroll += payout
        self.current_bet = 0.0

    def lose(self) -> None:
        """
        Handle a losing hand (bet is already deducted).
        """
        self.current_bet = 0.0

    def push(self) -> None:
        """
        Handle a tie (push): return bet to bankroll.
        """
        self.bankroll += self.current_bet
        self.current_bet = 0.0

    def reset_hands(self) -> None:
        """
        Clear all hands in preparation for a new round.
        """
        self.hands.clear()
        self.current_bet = 0.0

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, bankroll={self.bankroll:.2f})"