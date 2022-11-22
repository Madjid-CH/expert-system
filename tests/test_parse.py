from parse import *


def test_parse_input():
    fact, facts, rules = parse_input('../input')
    assert fact == 'H'
    assert facts == {'C', 'B'}
    assert rules == [{('D', 'B', 'E'): {'F'}},
                     {('G', 'D'): {'A'}},
                     {('C', 'F'): {'A'}},
                     {'B': {'X'}},
                     {'D': {'E'}},
                     {('X', 'A'): {'H'}},
                     {'C': {'D'}},
                     {('X', 'C'): {'A'}},
                     {('X', 'B'): {'D'}}]
