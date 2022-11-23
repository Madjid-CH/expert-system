from parse import parse_input
from expert_system import forward_chaining, backward_chaining

if __name__ == '__main__':
    fact, facts, rules = parse_input('input2')

    result, rules_applied, new_facts = backward_chaining(fact, facts, rules)

    print("can prove", fact, ": ", result)
    print("facts: ", new_facts)
    rules_applied = [("R" + str(i + 1)) for i in rules_applied]
    print(rules_applied)
