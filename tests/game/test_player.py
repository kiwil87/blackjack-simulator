import pytest
from cards import Card, Hand
from game import Action, Player

class FakeStrategy:
    def __init__(self):
        self.called_with = None
        self.to_return = Action.HIT

    def next_move(self, hand, dealer_upcard):
        self.called_with = (hand, dealer_upcard)
        return self.to_return

def test_init_defaults():
    strat = FakeStrategy()
    p = Player(name="Alice", bankroll=100.0, strategy=strat)
    assert p.name == "Alice"
    assert p.bankroll == 100.0
    assert p.strategy is strat
    assert p.hands == []
    assert p.current_bet == 0.0

@pytest.mark.parametrize("amt", [0, -5.0])
def test_place_bet_invalid_amount_raises(amt):
    p = Player("Bob", bankroll=50.0, strategy=FakeStrategy())
    with pytest.raises(ValueError) as exc:
        p.place_bet(amt)
    assert "Bet must be positive" in str(exc.value)

def test_place_bet_reduces_bankroll_and_sets_current_bet():
    p = Player("Carol", bankroll=200.0, strategy=FakeStrategy())
    p.place_bet(25.5)
    assert p.current_bet == 25.5
    assert p.bankroll == pytest.approx(200.0 - 25.5)

def test_decide_delegates_to_strategy():
    strat = FakeStrategy()
    p = Player("Dan", bankroll=100.0, strategy=strat)
    h = Hand()
    up = Card("K", "Hearts")
    strat.to_return = Action.DOUBLE_DOWN
    result = p.decide(h, up)
    assert result is Action.DOUBLE_DOWN
    assert strat.called_with == (h, up)

def test_win_default_multiplier():
    p = Player("Eve", bankroll=150.0, strategy=FakeStrategy())
    p.place_bet(10.0)
    # bankroll -> 140.0, current_bet -> 10.0
    p.win()
    # payout = 10 * (1 + 1.0) = 20
    assert p.bankroll == pytest.approx(140.0 + 20.0)
    assert p.current_bet == 0.0

def test_win_custom_multiplier():
    p = Player("Frank", bankroll=80.0, strategy=FakeStrategy())
    p.place_bet(16.0)
    # bankroll -> 64.0
    p.win(multiplier=1.5)
    # payout = 16 * (1 + 1.5) = 40
    assert p.bankroll == pytest.approx(64.0 + 40.0)
    assert p.current_bet == 0.0

def test_lose_clears_current_bet_only():
    p = Player("Gina", bankroll=60.0, strategy=FakeStrategy())
    p.place_bet(20.0)
    # bankroll -> 40.0, current_bet -> 20.0
    p.lose()
    assert p.bankroll == pytest.approx(40.0)
    assert p.current_bet == 0.0

def test_push_returns_bet_to_bankroll():
    p = Player("Hank", bankroll=120.0, strategy=FakeStrategy())
    p.place_bet(30.0)
    # bankroll -> 90.0
    p.push()
    assert p.bankroll == pytest.approx(120.0)
    assert p.current_bet == 0.0

def test_reset_hands_clears_all():
    p = Player("Ivy", bankroll=75.0, strategy=FakeStrategy())
    h1, h2 = Hand(), Hand()
    p.hands.append(h1)
    p.hands.append(h2)
    assert p.hands == [h1, h2]
    p.reset_hands()
    assert p.hands == []

def test_repr_shows_name_and_bankroll_two_decimals():
    p = Player("Jane", bankroll=99.987, strategy=FakeStrategy())
    # bankroll formatted to two decimals, rounded
    assert repr(p) == "Player(name='Jane', bankroll=99.99)"