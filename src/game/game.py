from cards import Card, Shoe, Hand
from .action import Action
from .dealer import Dealer
from .player import Player

class Game:
    """
    Orchestrates the flow of a blackjack game, handling dealing, player decisions,
    dealer play, and bet resolution.
    """
    def __init__(
        self,
        players: list[Player],
        dealer_hits_soft_17: bool = True,
        num_decks: int = 8,
        shuffle_on_init: bool = True,
        penetration_threshold: float = 0.75,
        blackjack_multiplier: float = 1.5,
        bet_amount: float = 1.0,
        verbose: bool = True
    ) -> None:
        self.players = players
        self.dealer = Dealer(hit_soft_17=dealer_hits_soft_17)
        self.shoe = Shoe(
            num_decks=num_decks,
            shuffle_on_init=shuffle_on_init,
            penetration_threshold=penetration_threshold
        )
        self.blackjack_multiplier = blackjack_multiplier
        self.bet_amount = bet_amount
        self.verbose = verbose

    def play_round(self, bet_amount: float = None) -> None:
        """
        Play a single round of blackjack: deal cards, handle player decisions,
        play dealer hand, and settle bets.
        Args:
            bet_amount (float): Amount each player bets; if None, uses default self.bet_amount.
        """
        if bet_amount is None:
            if self.verbose:
                print(f"Beginning of round with default bet amount: {self.bet_amount}")
            bet_amount = self.bet_amount

        self._reset_and_place_bets(bet_amount)
        self.dealer.reset_hand()
        self._deal_initial_cards()

        dealer_upcard = self.dealer.upcard()
        if self.verbose:
            print(f"Dealer's upcard: {dealer_upcard}")

        self._handle_player_turns(dealer_upcard)
        self._handle_dealer_turn()
        if self.verbose:
            print(f"Dealer's hand: {self.dealer.hand}")
        self._settle_bets()

    def _reset_and_place_bets(self, bet_amount: float) -> None:
        for player in self.players:
            if self.verbose:
                print(f"Resetting hands for player {player.name}")
            player.reset_hands()
            try:
                if self.verbose:
                    print(f"Player {player.name} placing bet: {bet_amount}")
                player.place_bet(bet_amount)
            except ValueError as e:
                print(f"Player {player.name} cannot bet: {e}")
                continue
            player.add_hand(Hand(is_dealer=False))

    def _deal_initial_cards(self) -> None:
        for _ in range(2):
            for player in self.players:
                if player.current_bet > 0 and player.hands:
                    if self.verbose:
                        print(f"Dealing card to player {player.name}")
                    player.hands[0].add_card(self.shoe.draw_card())
            if self.verbose:
                print(f"Dealing card to dealer")
            self.dealer.hand.add_card(self.shoe.draw_card())

    def _handle_player_turns(self, dealer_upcard) -> None:
        for player in self.players:
            if self.verbose:
                print(f"Starting turns for player {player.name}")
            i = 0
            while i < len(player.hands):
                hand = player.hands[i]
                if self.verbose:
                    print(f"Player {player.name}'s turn with hand: {hand}")
                has_split = False
                while True:
                    if self.verbose:
                        print(f"Player {player.name} is considering hand: {hand}")
                    # Auto-stand on 21 or higher
                    if hand.value[0] >= 21:
                        if self.verbose:
                            print(f"Player {player.name} auto-stands with hand: {hand}")
                        break

                    action = player.decide(hand, dealer_upcard)
                    if action == Action.HIT:
                        if self.verbose:
                            print(f"Player {player.name} chooses to HIT")
                        hand.add_card(self.shoe.draw_card())

                    elif action == Action.STAND:
                        if self.verbose:
                            print(f"Player {player.name} chooses to STAND")
                        break

                    elif action == Action.DOUBLE_DOWN:
                        if self.verbose:
                            print(f"Player {player.name} chooses to DOUBLE DOWN")
                        if len(hand) == 2:
                            player.place_bet(player.current_bet)
                            hand.add_card(self.shoe.draw_card())
                        else:
                            raise ValueError(f"Cannot double down with hand: {hand}")
                        break

                    elif action == Action.SPLIT:
                        if self.verbose:
                            print(f"Player {player.name} chooses to SPLIT")
                        # Only allow split on two cards of the same rank
                        if len(hand) != 2:
                            raise ValueError(f"Cannot split hand with {len(hand)} cards: {hand}")
                        card1, card2 = hand.cards
                        if card1.rank != card2.rank:
                            raise ValueError(f"Cannot split hand with different ranks: {card1}, {card2}")
                        # Place additional bet for the split hand
                        player.place_bet(player.current_bet)
                        # Create two new hands
                        new_hand1 = Hand(is_dealer=False)
                        new_hand1.add_card(card1)
                        new_hand1.add_card(self.shoe.draw_card())
                        new_hand2 = Hand(is_dealer=False)
                        new_hand2.add_card(card2)
                        new_hand2.add_card(self.shoe.draw_card())
                        # Replace current hand with first new hand and insert second after
                        player.hands[i] = new_hand1
                        player.hands.insert(i + 1, new_hand2)
                        has_split = True
                        break

                    else:
                        raise ValueError(f"Unknown action: {action}")
                # If we didn't split, move to next hand; if we did, process new_hand1 before moving on
                if not has_split:
                    i += 1

    def _handle_dealer_turn(self) -> None:
        self.dealer.play(self.shoe)

    def _settle_bets(self) -> None:
        dealer_total, _ = self.dealer.hand.value
        for player in self.players:
            for hand in player.hands:
                total, _ = hand.value
                if hand.is_bust:
                    if self.verbose:
                        print(f"Player {player.name} busts with hand {hand}")
                    player.lose()
                    if self.verbose:
                        print(f"Player {player.name} bankroll after bust: {player.bankroll}")
                elif hand.is_blackjack and not self.dealer.hand.is_blackjack:
                    if self.verbose:
                        print(f"Player {player.name} has blackjack with hand {hand}")
                    player.win(multiplier=self.blackjack_multiplier)
                    if self.verbose:
                        print(f"Player {player.name} bankroll after blackjack: {player.bankroll}")
                elif self.dealer.hand.is_bust:
                    if self.verbose:
                        print(f"Dealer busts, player {player.name} wins with hand {hand}")
                    player.win()
                    if self.verbose:
                        print(f"Player {player.name} bankroll after win: {player.bankroll}")
                elif total > dealer_total:
                    if self.verbose:
                        print(f"Player {player.name} wins with hand {hand}")
                    player.win()
                    if self.verbose:
                        print(f"Player {player.name} bankroll after win: {player.bankroll}")
                elif total < dealer_total:
                    if self.verbose:
                        print(f"Player {player.name} loses with hand {hand}")
                    player.lose()
                    if self.verbose:
                        print(f"Player {player.name} bankroll after loss: {player.bankroll}")
                else:
                    if self.verbose:
                        print(f"Player {player.name} pushes with hand {hand}")
                    player.push()
                    if self.verbose:
                        print(f"Player {player.name} bankroll after push: {player.bankroll}")

    def __repr__(self) -> str:
        return f"Game(players={self.players}, dealer={self.dealer}, shoe={self.shoe})"