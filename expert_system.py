def forward_chaining(fact, facts, rules):
    rules_stack = rules.copy()
    rules_applied = []
    if fact in facts:
        return True, rules_applied, facts
    else:
        for rule in rules_stack:
            if premise_in_facts(rule, facts):
                facts = union_consequence(facts, rule)
                save_rule_index(rule, rules, rules_applied)
                rules_stack.pop(rules_stack.index(rule))

        stop = False
        while not stop:
            stop = True
            for rule in rules_stack[::-1]:
                if premise_in_facts(rule, facts):
                    facts = union_consequence(facts, rule)
                    save_rule_index(rule, rules, rules_applied)
                    rules_stack.pop(rules_stack.index(rule))
                    stop = False


    return fact in facts, rules_applied, facts


def save_rule_index(rule, rules, rules_applied):
    rules_applied.append(rules.index(rule))


def union_consequence(facts, rule):
    return facts.union(rule.get(list(rule.keys())[0]))


def premise_in_facts(rule, facts):
    return list(rule.keys())[0].issubset(facts)
