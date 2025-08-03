import pytest
from game import Action

def test_enum_members_and_order():
    # Enum preserves definition order
    expected = ["HIT", "STAND", "DOUBLE_DOWN", "SPLIT"]
    members = [member.name for member in Action]
    assert members == expected

def test_values_are_int_and_unique_and_sequential():
    values = [member.value for member in Action]
    # all auto() values are ints
    assert all(isinstance(v, int) for v in values)
    # no duplicates
    assert len(values) == len(set(values))
    # sequential starting at 1
    assert values == list(range(1, len(values) + 1))

@pytest.mark.parametrize("name", ["HIT", "STAND", "DOUBLE_DOWN", "SPLIT"])
def test_lookup_by_name(name):
    # Action['HIT'] → Action.HIT, etc.
    member = Action[name]
    assert member.name == name
    assert isinstance(member, Action)

@pytest.mark.parametrize("member,repr_str,str_str", [
    (Action.HIT,         "<Action.HIT: 1>",     "Action.HIT"),
    (Action.STAND,       "<Action.STAND: 2>",   "Action.STAND"),
    (Action.DOUBLE_DOWN, "<Action.DOUBLE_DOWN: 3>", "Action.DOUBLE_DOWN"),
    (Action.SPLIT,       "<Action.SPLIT: 4>",   "Action.SPLIT"),
])
def test_str_and_repr(member, repr_str, str_str):
    assert repr(member) == repr_str
    assert str(member) == str_str

def test_invalid_lookup_raises():
    with pytest.raises(KeyError):
        _ = Action["SURRENDER"]

def test_int_casting_back_to_enum():
    # ensure you can do Action(1) → Action.HIT, etc.
    for member in Action:
        assert Action(member.value) is member