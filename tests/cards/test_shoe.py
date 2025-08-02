import pytest
import random
from cards import Card, Shoe

def test_invalid_num_decks_raises():
    with pytest.raises(ValueError):
        Shoe(num_decks=0)
    with pytest.raises(ValueError):
        Shoe(num_decks=9)

@pytest.mark.parametrize("threshold", (-0.1, 0, 1, 1.1))
def test_invalid_penetration_threshold_raises(threshold):
    with pytest.raises(ValueError):
        Shoe(penetration_threshold=threshold)

def test_len_and_remaining_property():
    shoe = Shoe(num_decks=2, shuffle_on_init=False, penetration_threshold=0.5)
    assert len(shoe) == shoe.remaining == 52 * 2

def test_repr_and_str_and_display(capsys):
    shoe = Shoe(num_decks=1, shuffle_on_init=False, penetration_threshold=0.75)
    # repr
    assert repr(shoe) == f"Shoe(num_decks=1, remaining_cards={len(shoe)})"
    # __str__ -> calls display() and prints first 5 cards
    out = str(shoe)
    captured = capsys.readouterr()
    # should print at least the first card label
    assert "1: 2♥" in captured.out
    assert out == "Shoe with 1 decks, 52 cards remaining."

def test_reset_restores_cards():
    shoe = Shoe(num_decks=1, shuffle_on_init=False, penetration_threshold=0.5)
    # draw one, ensure it's the very first card of an unshuffled deck
    first = shoe.draw_card()
    assert first == Card("2", "Hearts")
    assert len(shoe) == 51
    # reset (no shuffle) should restore full deck in original order
    shoe.reset(shuffle=False)
    assert len(shoe) == 52
    assert shoe.draw_card() == Card("2", "Hearts")

def test_shuffle_uses_random_shuffle(monkeypatch):
    shoe = Shoe(num_decks=1, shuffle_on_init=False, penetration_threshold=0.5)
    called = False
    def fake_shuffle(lst):
        nonlocal called
        called = True
    monkeypatch.setattr(random, "shuffle", fake_shuffle)
    shoe.shuffle()
    assert called, "shuffle() should call random.shuffle"

def test_draw_card_reduces_remaining_and_returns_card():
    shoe = Shoe(num_decks=1, shuffle_on_init=False, penetration_threshold=0.5)
    initial = len(shoe)
    card = shoe.draw_card()
    assert isinstance(card, Card)
    assert len(shoe) == initial - 1

def test_draw_card_triggers_reset_when_penetration_threshold_met():
    # choose threshold so that penetration_cut_index == 5
    # 1 - threshold = 5/52 -> threshold = 47/52 ≈ 0.9038
    threshold = 47 / 52
    shoe = Shoe(num_decks=1, shuffle_on_init=False, penetration_threshold=threshold)
    cut = int(52 * (1 - threshold))  # should be 5
    # draw until we reach exactly cut cards remaining
    for _ in range(52 - cut):
        shoe.draw_card()
    assert len(shoe) == cut
    # next draw should reset (to 52) then pop → len=51
    card = shoe.draw_card()
    assert card == Card("2", "Hearts")
    assert len(shoe) == 51