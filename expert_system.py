def forward_chaining(fact, facts, rules):
    rules_applied = []

    if fact in facts:
        return True, rules_applied, facts
    else:
        rules_stack = []
        for rule in rules:
            if is_premise_in_facts(rule, facts):
                facts = apply_rule(facts, rule, rules, rules_applied)
            else:
                rules_stack.append(rule)

        stop = False
        while not stop and (fact not in facts):
            stop = True
            for rule in rules_stack[::-1]:
                if is_premise_in_facts(rule, facts):
                    facts = apply_rule(facts, rule, rules, rules_applied)
                    rules_stack.pop(rules_stack.index(rule))
                    stop = False

    return fact in facts, rules_applied, facts


def apply_rule(facts, rule, rules, rules_applied):
    if not is_consequence_in_facts(rule, facts):
        facts = union_consequence(facts, rule)
        save_rule_index(rule, rules, rules_applied)
    return facts


def is_premise_in_facts(rule, facts):
    return set(list(rule.keys())[0]).issubset(facts)


def is_consequence_in_facts(rule, facts):
    return rule.get(list(rule.keys())[0]).issubset(facts)


def save_rule_index(rule, rules, rules_applied):
    rules_applied.append(rules.index(rule))


def union_consequence(facts, rule):
    return facts.union(rule.get(list(rule.keys())[0]))


def backward_chaining(fact, facts, rules):
    rules_applied = []

    if fact in facts:
        return True, rules_applied, facts
    else:
        rules_stack = get_backward_chain(fact, rules)
        for rule in rules_stack[::-1]:
            facts = apply_rule(facts, rules[rule], rules, rules_applied)

        return fact in facts, rules_applied, facts


def rule_having_fact_in_consequence(fact, rules):
    for rule in rules:
        if fact in consequence_of(rule):
            return rule
    return None


def premise_of(rule):
    return list(rule.keys())[0]


def consequence_of(rule):
    return rule.get(list(rule.keys())[0])


def get_backward_chain(fact, rules):
    rules_stack = []
    rule = rule_having_fact_in_consequence(fact, rules)
    while rule and rules.index(rule) not in rules_stack:
        rule1 = rules.index(rule)
        rules_stack.append(rule1)
        for f in premise_of(rule):
            chain = get_backward_chain(f, rules)
            [rules_stack.append(r) for r in chain if r not in rules_stack]

    return rules_stack
