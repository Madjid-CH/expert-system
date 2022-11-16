from expert_system import forward_chaining


def test_empty_facts_base():
    assert forward_chaining("A", facts={}, rules=[]) == (False, [], {})


def test_fact_in_facts_base():
    assert forward_chaining("A", frozenset({"A"}), []) == (True, [], {"A"})
    assert forward_chaining("B", frozenset(["A"]), []) == (False, [], {"A"})


def test_one_step():
    facts = frozenset(["A", "B"])
    assert forward_chaining("B", frozenset({"A"}), [{frozenset(["A"]): frozenset({"B"})}]) == \
           (True, [0], {"A", "B"})
    assert forward_chaining("C", facts, [{frozenset({"A", "B"}): frozenset({"C"})}]) == \
           (True, [0], {"A", "B", "C"})
    assert forward_chaining("D", facts, [{frozenset({"A", "B"}): frozenset({"C"})}]) == \
           (False, [0], {"A", "B", "C"})


def test_two_forward_steps():
    facts = frozenset(["A", "B"])
    rules = [{frozenset({"A", "B"}): frozenset({"D"})},
             {frozenset({"D"}): frozenset({"C"})}]
    assert forward_chaining("C", facts, rules) == (True, [0, 1], {'C', 'D', 'A', 'B'})
    assert forward_chaining("E", facts, rules) == (False, [0, 1], {'C', 'D', 'A', 'B'})


def test_two_non_forward_steps():
    facts = frozenset(["A", "B"])
    rules = [{frozenset({"C"}): frozenset({"D"})},
             {frozenset({"B"}): frozenset({"C"})}]
    assert forward_chaining("D", facts, rules) == (True, [1, 0], {'D', 'B', 'A', 'C'})
    assert forward_chaining("J", facts, rules) == (False, [1, 0], {'D', 'B', 'A', 'C'})


def test_three_non_forward_steps():
    facts = frozenset(["A", "B"])
    rules = [{frozenset({"C"}): frozenset({"D"})},
             {frozenset({"B"}): frozenset({"C"})},
             {frozenset({"D"}): frozenset({"E"})}]
    assert forward_chaining("E", facts, rules) == (True, [1, 0, 2], {'B', 'D', 'C', 'A', 'E'})
    assert forward_chaining("J", facts, rules) == (False, [1, 0, 2], {'B', 'D', 'C', 'A', 'E'})


def test_four_non_forward_steps():
    facts = frozenset(["A", "B"])
    rules = [{frozenset({"C"}): frozenset({"D"})},
             {frozenset({"H"}): frozenset({"C"})},
             {frozenset({"D"}): frozenset({"E"})},
             {frozenset({"B"}): frozenset({"H"})}, ]
    assert forward_chaining("E", facts, rules) == (True, [3, 1, 0, 2], {'B', 'D', 'H', 'E', 'C', 'A'})
    assert forward_chaining("P", facts, rules) == (False, [3, 1, 0, 2], {'B', 'D', 'H', 'E', 'C', 'A'})

def test_loop_in_rules():
    facts = frozenset(["A", "B"])
    rules = [{frozenset({"C"}): frozenset({"D"})},
             {frozenset({"D"}): frozenset({"C"})},]
    assert forward_chaining("D", facts, rules) == (False, [], {'B', 'A'})

def test_exo_1():
    pass