import pytest
from cards import Card, Hand

def test_init_defaults():
    hand = Hand()
    assert hand.cards == []
    assert hand.is_dealer is False
    assert hand.current_bet == 1.0 

    dealer_hand = Hand(is_dealer=True)
    assert dealer_hand.is_dealer is True

def test_add_card_and_len():
    hand = Hand()
    card = Card("5", "Diamonds")
    hand.add_card(card)
    assert len(hand) == 1
    assert hand.cards == [card]

def test_add_cards():
    hand = Hand()
    cards = [Card("2", "Hearts"), Card("3", "Spades")]
    hand.add_cards(cards)
    assert len(hand) == 2
    assert hand.cards == cards

def test_win_normal_payout():
    hand = Hand(current_bet=10.0)
    payout = hand.win()
    assert payout == 20.0  # 10 bet + 10 win
    assert hand.current_bet == 0.0

def test_win_blackjack_payout():
    hand = Hand(current_bet=10.0)
    payout = hand.win(multiplier=1.5)
    assert payout == 25.0  # 10 bet + 15 win
    assert hand.current_bet == 0.0

def test_lose():
    hand = Hand(current_bet=10.0)
    hand.lose()
    assert hand.current_bet == 0.0

def test_push():
    hand = Hand(current_bet=10.0)
    returned_bet = hand.push()
    assert returned_bet == 10.0
    assert hand.current_bet == 0.0

def test_reset_clears_cards():
    hand = Hand()
    hand.add_cards([Card("2", "Hearts"), Card("3", "Spades")])
    hand.reset()
    assert hand.cards == []
    assert len(hand) == 0

@pytest.mark.parametrize("cards, expected", [
    ([], (0, "Hard")),
    ([Card("2", "Hearts"), Card("3", "Clubs")], (5, "Hard")),
    ([Card("A", "Spades")], (11, "Soft")),
    ([Card("A", "Spades"), Card("9", "Hearts")], (20, "Soft")),
    ([Card("A", "Spades"), Card("K", "Clubs")], (21, "Soft")),
    ([Card("A", "Spades"), Card("A", "Hearts")], (12, "Soft")),
    ([Card("A", "Spades"), Card("A", "Hearts"), Card("9", "Clubs")], (21, "Soft")),
    ([Card("A", "Spades"), Card("A", "Hearts"), Card("K", "Diamonds")], (12, "Hard")),
])
def test_value_property(cards, expected):
    hand = Hand()
    hand.add_cards(cards)
    assert hand.value == expected

def test_is_soft_blackjack_bust_and_split():
    # Soft but not blackjack or bust
    hand1 = Hand()
    hand1.add_cards([Card("A", "Hearts"), Card("5", "Clubs")])
    assert hand1.is_soft is True
    assert hand1.is_blackjack is False
    assert hand1.is_bust is False
    assert hand1.can_split is False

    # Natural blackjack
    hand2 = Hand()
    hand2.add_cards([Card("A", "Hearts"), Card("K", "Clubs")])
    assert hand2.is_blackjack is True
    assert hand2.is_bust is False

    # Bust
    hand3 = Hand()
    hand3.add_cards([Card("K", "Hearts"), Card("Q", "Diamonds"), Card("2", "Clubs")])
    assert hand3.is_bust is True
    assert hand3.is_soft is False

    # Can split
    hand4 = Hand()
    hand4.add_cards([Card("8", "Hearts"), Card("8", "Diamonds")])
    assert hand4.can_split is True
    assert hand4.is_blackjack is False

def test_display_and_str():
    hand = Hand()
    hand.add_cards([Card("10", "Spades"), Card("7", "Diamonds")])
    # Card.display()/__str__ use ♠ and ♦
    expected = "10♠, 7♦ (Hard 17)"
    assert hand.display() == expected
    assert str(hand) == expected

