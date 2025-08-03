import pytest
from cards import Card, Shoe
from game import Dealer

def test_init_defaults():
    dealer = Dealer()
    # hand is a Hand marked as dealer, and hit_soft_17 defaults to True
    assert dealer.hand.is_dealer is True
    assert dealer.hit_soft_17 is True

def test_upcard_empty_raises():
    dealer = Dealer()
    with pytest.raises(ValueError):
        dealer.upcard()

def test_upcard_returns_first_card():
    dealer = Dealer()
    cards = [Card("K", "Spades"), Card("5", "Hearts"), Card("A", "Diamonds")]
    dealer.hand.add_cards(cards)
    assert dealer.upcard() is cards[0]

def test_reset_hand_clears_cards():
    dealer = Dealer()
    dealer.hand.add_cards([Card("2","Hearts"), Card("3","Clubs")])
    assert len(dealer.hand) == 2
    dealer.reset_hand()
    assert dealer.hand.cards == []
    assert len(dealer.hand) == 0

def test_play_hits_until_hard_17():
    # With a fresh shoe (unshuffled), cards come in order: 2♥,3♥,4♥,5♥,6♥,...
    shoe = Shoe(num_decks=1, shuffle_on_init=False)
    dealer = Dealer(hit_soft_17=False)
    # start with empty hand
    dealer.play(shoe)
    # Should have drawn 2,3,4,5,6 (sum=20 >=17)
    drawn = dealer.hand.cards
    values = [c.value for c in drawn]
    assert values == [2, 3, 4, 5, 6]
    total, kind = dealer.hand.value
    assert total == 20 and kind == "Hard"

def test_play_stands_on_soft_17_when_not_hitting_soft_17():
    # Seed the hand with A♣ + 6♦ = Soft 17
    dealer = Dealer(hit_soft_17=False)
    dealer.hand.add_cards([Card("A","Clubs"), Card("6","Diamonds")])
    # Use a shoe that would otherwise deal a card
    shoe = Shoe(num_decks=1, shuffle_on_init=False)
    before = len(dealer.hand)
    dealer.play(shoe)
    # No card should have been added
    assert len(dealer.hand) == before

def test_play_hits_on_soft_17_when_hitting_soft_17():
    # Seed the hand with A♣ + 6♦ = Soft 17
    dealer = Dealer(hit_soft_17=True)
    dealer.hand.add_cards([Card("A","Clubs"), Card("6","Diamonds")])
    shoe = Shoe(num_decks=1, shuffle_on_init=False)
    # Next draw would be 2♥, 3♥, 4♥, 5♥, ...
    dealer.play(shoe)
    # Hand length goes from 2 → 6 and last card is 5♥
    assert len(dealer.hand) == 6
    assert dealer.hand.cards[-1] == Card("5", "Hearts")

def test_repr_shows_hand_and_flag():
    # Seed a known hand so str(hand) is predictable
    dealer = Dealer(hit_soft_17=True)
    dealer.hand.add_cards([Card("10","Spades"), Card("7","Diamonds")])
    # str(dealer.hand) → "10♠, 7♦ (Hard 17)"
    expected_hand_str = "10♠, 7♦ (Hard 17)"
    rep = repr(dealer)
    assert rep == f"Dealer(hand={expected_hand_str}, hit_soft_17=True)"