import pytest

from expert_system import backward_chaining, get_backward_chain


def test_empty_facts_base():
    assert backward_chaining(fact="A", facts={}, rules=[]) == (False, [], {})


def test_fact_in_facts_base():
    assert backward_chaining("A", {"A"}, []) == (True, [], {"A"})
    assert backward_chaining("B", {"A"}, []) == (False, [], {"A"})


def test_one_step():
    assert backward_chaining("B", {"A"}, [{("A"): {"B"}}]) == (True, [0], {"A", "B"})
    assert backward_chaining("C", {"A"}, [{("A"): {"B"}}]) == (False, [], {"A"})


def test_two_step():
    facts = {"A", "B"}
    rules = [{("A", "B"): {"D"}},
             {("D"): {"C"}}]
    assert backward_chaining("C", facts, rules) == (True, [0, 1], {'C', 'D', 'A', 'B'})

def test_exo_1():
    facts = {"A", "B"}
    rules = [{("A", "B"): {"D"}},
             {("D"): {"C"}}]
    assert backward_chaining("C", facts, rules) == (True, [0, 1], {'C', 'D', 'A', 'B'})


def test_simple_chaining():
    rules = [{("A"): {"B"}}, ]
    assert get_backward_chain("B", rules) == [0]
    assert get_backward_chain("C", rules) == []


def test_get_2_chaining():
    rules = [{("A"): {"D"}},
             {("D"): {"C"}}]
    assert get_backward_chain("C", rules) == [1, 0]
    assert get_backward_chain("M", rules) == []


def test_get_3_chaining():
    rules = [{("C"): {"E"}},
             {("A"): {"D"}},
             {("D"): {"C"}},
             {("K"): {"M"}},
             {("L"): {"K"}},
             ]
    assert get_backward_chain("E", rules) == [0, 2, 1]
    assert get_backward_chain("M", rules) == [3, 4]


@pytest.mark.skip(reason="i don't know how to implement this yet")
def test_loopy_chaining():
    rules = [{("C"): {"E"}},
             {("E"): {"C"}},
             ]
    assert get_backward_chain("E", rules) == [0, 1]


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
                   {("X", "Y", "Z"): {"E"}},  # 1
                   {("B"): {"Y"}},
                   {("J", "K"): {"X"}},  # 2
                   {("B"): {"K"}},
                   {("C"): {"J"}},  # 3
                   {("J"): {"H"}}
                   ],
             [1, 3, 5, 4, 2, 0, 6]),
    )
)
def test_multiple_facts_in_premise(fact, rules, expected):
    assert get_backward_chain(fact, rules) == expected
