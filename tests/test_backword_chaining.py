import pytest

from expert_system import backward_chaining, get_backward_chain


def test_empty_facts_base():
    assert backward_chaining(fact="A", facts={}, rules=[]) == (False, [], {})


def test_fact_in_facts_base():
    assert backward_chaining("A", {"A"}, []) == (True, [], {"A"})
    assert backward_chaining("B", {"A"}, []) == (False, [], {"A"})


def test_one_step():
    assert backward_chaining("B", {"A"}, [{"A": {"B"}}]) == (True, [0], {"A", "B"})
    assert backward_chaining("C", {"A"}, [{("A"): {"B"}}]) == (False, [], {"A"})


def test_two_step():
    facts = {"A", "B"}
    rules = [{("A", "B"): {"D"}},
             {("D"): {"C"}}]
    assert backward_chaining("C", facts, rules) == (True, [0, 1], {'C', 'D', 'A', 'B'})


def test_exo_1(setup_exo_1):
    fact, facts, rules = setup_exo_1
    assert backward_chaining(fact, facts, rules) == (True, [4, 2, 0], {'F', 'D', 'C', 'E', 'B'})


def test_exo_2(setup_exo_2):
    fact, facts, rules = setup_exo_2
    assert backward_chaining(fact, facts, rules) == (    )


def test_simple_chaining():
    rules = [{("A"): {"B"}}, ]
    assert get_backward_chain("B", rules, set()) == [0]
    assert get_backward_chain("C", rules, set()) == []


def test_get_2_chaining():
    rules = [{("A"): {"D"}},
             {("D"): {"C"}}]
    assert get_backward_chain("C", rules, set()) == [1, 0]
    assert get_backward_chain("M", rules, set()) == []


def test_get_3_chaining():
    rules = [{("C"): {"E"}},
             {("A"): {"D"}},
             {("D"): {"C"}},
             {("K"): {"M"}},
             {("L"): {"K"}},
             ]
    assert get_backward_chain("E", rules, set()) == [0, 2, 1]
    assert get_backward_chain("M", rules, set()) == [3, 4]


@pytest.mark.parametrize(
    'fact, rules, expected',
    (
            ("E", [{("C"): {"E"}},
                   {("E"): {"C"}}, ],
             [0, 1]),

            ("E", [{("C"): {"E"}},
                   {("E"): {"F"}},
                   {("F"): {"C"}}, ],
             [0, 2, 1]),
    )
)
def test_loopy_chaining(fact, rules, expected):
    assert get_backward_chain(fact, rules, set()) == expected


@pytest.mark.parametrize(
    'fact, rules, expected',
    (
            ("F", [{("A"): {"E"}},
                   {("C", "E"): {"F"}},
                   {("B"): {"C"}}],
             [1, 2, 0]),

            ("E", [{("X", "Y", "Z"): {"E"}},
                   {("A"): {"Z"}},
                   {("B"): {"Y"}},
                   {("C", "B"): {"X"}},
                   ],
             [0, 3, 2, 1]),

            ("E", [{("A", "H"): {"Z"}},
                   {("X", "Y", "Z"): {"E"}},
                   {("B"): {"Y"}},
                   {("J", "K"): {"X"}},
                   {("B"): {"K"}},
                   {("C"): {"J"}},
                   {("J"): {"H"}}
                   ],
             [1, 3, 5, 4, 2, 0, 6]),
    )
)
def test_multiple_facts_in_premise(fact, rules, expected):
    assert get_backward_chain(fact, rules, set()) == expected
