import pytest


@pytest.fixture
def setup_exo_1():
    facts = {"E", "F"}
    rules = [{("E", "B"): {"C"}},
             {("F", "D"): {"A"}},
             {("D", "E"): {"B"}},
             {("B", "D"): {"F"}},
             {("E", "F"): {"D"}}, ]
    return facts, rules


@pytest.fixture
def setup_exo_2():
    facts = {"B", "C"}
    rules = [{("D", "B", "E"): {"F"}},
             {("G", "D"): {"A"}},
             {("C", "F"): {"A"}},
             {("B"): {"X"}},
             {("D"): {"E"}},
             {("X", "A"): {"H"}},
             {("C"): {"D"}},
             {("X", "C"): {"A"}},
             {("X", "B"): {"D"}}, ]
    return facts, rules
