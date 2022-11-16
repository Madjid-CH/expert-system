def forward_chaining(fact, facts, rules):
    rules_stack = rules.copy()
    rules_stack_2 = []
    rules_applied = []

    if fact in facts:
        return True, rules_applied, facts
    else:
        for rule in rules_stack:
            if is_premise_in_facts(rule, facts):
                if not is_consequence_in_facts(rule, facts):
                    facts = union_consequence(facts, rule)
                    save_rule_index(rule, rules, rules_applied)
                    # rules_stack.pop(rules_stack.index(rule))
            else:
                rules_stack_2.append(rule)

        stop = False
        while not stop and (fact not in facts):
            stop = True
            for rule in rules_stack_2[::-1]:
                if is_premise_in_facts(rule, facts):
                    if not is_consequence_in_facts(rule, facts):
                        facts = union_consequence(facts, rule)
                        save_rule_index(rule, rules, rules_applied)
                        rules_stack_2.pop(rules_stack_2.index(rule))
                        stop = False

    print(rules_stack_2)
    return fact in facts, rules_applied, facts


def is_premise_in_facts(rule, facts):
    return list(rule.keys())[0].issubset(facts)


def is_consequence_in_facts(rule, facts):
    return rule.get(list(rule.keys())[0]).issubset(facts)


def save_rule_index(rule, rules, rules_applied):
    rules_applied.append(rules.index(rule))


def union_consequence(facts, rule):
    return facts.union(rule.get(list(rule.keys())[0]))
