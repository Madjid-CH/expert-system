import pytest

from expert_system import forward_chaining


def test_empty_facts_base():
    assert forward_chaining("A", facts={}, rules=[]) == (False, [], {})


@pytest.mark.parametrize(
    'fact, facts, rules, expected',
    (
            ("A", {"A"}, [], (True, [], {"A"})),
            ("B", {"A"}, [], (False, [], {"A"})),
    )
)
def test_fact_in_facts_base(fact, facts, rules, expected):
    assert forward_chaining(fact, facts, rules) == expected


@pytest.mark.parametrize(
    'fact, facts, rules, expected',
    (
            ("B", {"A"}, [{frozenset(["A"]): {"B"}}], (True, [0], {"A", "B"})),
            ("C", {"A", "B"}, [{frozenset({"A", "B"}): {"C"}}], (True, [0], {"A", "B", "C"})),
            ("D", {"A", "B"}, [{frozenset({"A", "B"}): {"C"}}], (False, [0], {"A", "B", "C"})),
    )
)
def test_one_step(fact, facts, rules, expected):
    assert forward_chaining(fact, facts, rules) == expected


def test_two_forward_steps():
    facts = {"A", "B"}
    rules = [{frozenset({"A", "B"}): {"D"}},
             {frozenset({"D"}): {"C"}}]
    assert forward_chaining("C", facts, rules) == (True, [0, 1], {'C', 'D', 'A', 'B'})
    assert forward_chaining("E", facts, rules) == (False, [0, 1], {'C', 'D', 'A', 'B'})


def test_two_non_forward_steps():
    facts = {"A", "B"}
    rules = [{frozenset({"C"}): {"D"}},
             {frozenset({"B"}): {"C"}}]
    assert forward_chaining("D", facts, rules) == (True, [1, 0], {'D', 'B', 'A', 'C'})
    assert forward_chaining("J", facts, rules) == (False, [1, 0], {'D', 'B', 'A', 'C'})


def test_three_non_forward_steps():
    facts = {"A", "B"}
    rules = [{frozenset({"C"}): {"D"}},
             {frozenset({"B"}): {"C"}},
             {frozenset({"D"}): {"E"}}]
    assert forward_chaining("E", facts, rules) == (True, [1, 0, 2], {'B', 'D', 'C', 'A', 'E'})
    assert forward_chaining("J", facts, rules) == (False, [1, 0, 2], {'B', 'D', 'C', 'A', 'E'})


def test_four_non_forward_steps():
    facts = {"A", "B"}
    rules = [{frozenset({"C"}): {"D"}},
             {frozenset({"H"}): {"C"}},
             {frozenset({"D"}): {"E"}},
             {frozenset({"B"}): {"H"}}, ]
    assert forward_chaining("E", facts, rules) == (True, [3, 1, 0, 2], {'B', 'D', 'H', 'E', 'C', 'A'})
    assert forward_chaining("P", facts, rules) == (False, [3, 1, 0, 2], {'B', 'D', 'H', 'E', 'C', 'A'})


def test_loop_in_rules():
    facts = {"A", "B"}
    rules = [{frozenset({"C"}): {"D"}},
             {frozenset({"D"}): {"C"}}, ]
    assert forward_chaining("D", facts, rules) == (False, [], {'B', 'A'})


def test_exo_1(setup_exo_1):
    facts, rules = setup_exo_1
    assert forward_chaining("C", facts, rules) == \
           (True, [4, 2, 1, 0], {'E', 'F', 'D', 'A', 'C', 'B'})


def test_exo_2(setup_exo_2):
    facts , rules = setup_exo_2
    assert forward_chaining("H", facts, rules) == \
           (True, [3, 6, 7, 5, 4, 0], {'E', 'C', 'B', 'F', 'D', 'X', 'A', 'H'})
