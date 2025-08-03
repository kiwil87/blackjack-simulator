import pytest
from cards import Card

@pytest.mark.parametrize("rank,suit,expected", [
    ("2", "Hearts", 2),
    ("10", "Spades", 10),
    ("J", "Diamonds", 10),
    ("Q", "Clubs", 10),
    ("K", "Hearts", 10),
    ("A", "Spades", 1),
])
def test_value_property(rank, suit, expected):
    c = Card(rank, suit)
    assert c.value == expected

def test_upcard_value_ace():
    c = Card("A", "Diamonds")
    assert c.upcard_value == 11

@pytest.mark.parametrize("rank,suit", [
    ("3", "Clubs"),
    ("K", "Hearts"),
])
def test_upcard_value_non_ace(rank, suit):
    c = Card(rank, suit)
    assert c.upcard_value == c.value

def test_display_and_str():
    c = Card("A", "Hearts")
    # SYMBOLS maps 'Hearts' to '♥'
    assert c.display() == "A♥"
    assert str(c) == "A♥"

def test_repr():
    c = Card("10", "Spades")
    rep = repr(c)
    assert rep == "Card(rank='10', suit='Spades')"

@pytest.mark.parametrize("rank", ["1", "11", "B", "", None])
def test_invalid_rank_raises(rank):
    with pytest.raises(ValueError) as exc:
        Card(rank, "Hearts")
    assert "Invalid rank" in str(exc.value)

@pytest.mark.parametrize("suit", ["Heart", "Pennies", "", None])
def test_invalid_suit_raises(suit):
    with pytest.raises(ValueError) as exc:
        Card("5", suit)
    assert "Invalid suit" in str(exc.value)

def test_create_deck_length_and_uniqueness():
    deck = Card.create_deck()
    # 4 suits × 13 ranks = 52 cards
    assert len(deck) == 52
    # No duplicates: repr() is unique for each card
    reps = {repr(c) for c in deck}
    assert len(reps) == 52

def test_deck_contents():
    deck = Card.create_deck()
    # make sure each rank-suit pair is present
    for suit in Card.SUITS:
        for rank in Card.RANKS:
            assert Card(rank, suit) in deck