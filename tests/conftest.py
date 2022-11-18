import pytest


@pytest.fixture
def setup_exo_1():
    facts = {"E", "F"}
    rules = [{frozenset({"E", "B"}): {"C"}},
             {frozenset({"F", "D"}): {"A"}},
             {frozenset({"D", "E"}): {"B"}},
             {frozenset({"B", "D"}): {"F"}},
             {frozenset({"E", "F"}): {"D"}}, ]
    return facts, rules

@pytest.fixture
def setup_exo_2():
    facts = {"B", "C"}
    rules = [{frozenset({"D", "B", "E"}): {"F"}},
             {frozenset({"G", "D"}): {"A"}},
             {frozenset({"C", "F"}): {"A"}},
             {frozenset({"B"}): {"X"}},
             {frozenset({"D"}): {"E"}},
             {frozenset({"X", "A"}): {"H"}},
             {frozenset({"C"}): {"D"}},
             {frozenset({"X", "C"}): {"A"}},
             {frozenset({"X", "B"}): {"D"}}, ]
    return facts, rules
