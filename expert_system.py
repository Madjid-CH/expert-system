def forward_chaining(fact, facts, rules):
    rules_applied = []

    if fact in facts:
        return True, rules_applied, facts
    else:
        rules_stack = []
        facts = apply_rules_if_possible(facts, rules, rules_applied, rules_stack)
        facts = resolve_the_rest_of_rules(fact, facts, rules, rules_applied, rules_stack)

    return fact in facts, rules_applied, facts


def apply_rules_if_possible(facts, rules, rules_applied, rules_stack):
    for rule in rules:
        if is_premise_in_facts(rule, facts):
            facts = apply_rule(facts, rule, rules, rules_applied)
        else:
            rules_stack.append(rule)
    return facts


def resolve_the_rest_of_rules(fact, facts, rules, rules_applied, rules_stack):
    stop = False
    while not stop and (fact not in facts):
        stop = True
        for rule in rules_stack[::-1]:
            if is_premise_in_facts(rule, facts):
                facts = apply_rule(facts, rule, rules, rules_applied)
                rules_stack.pop(rules_stack.index(rule))
                stop = False
    return facts


def apply_rule(facts, rule, rules, rules_applied):
    if not is_consequence_in_facts(rule, facts):
        facts = union_consequence(facts, rule)
        save_rule_index(rule, rules, rules_applied)
    return facts


def is_premise_in_facts(rule, facts):
    return set(list(rule.keys())[0]).issubset(facts)


def is_consequence_in_facts(rule, facts):
    return rule.get(list(rule.keys())[0]).issubset(facts)


def save_rule_index(rule, rules, stack):
    stack.append(rules.index(rule))


def union_consequence(facts, rule):
    return facts.union(rule.get(list(rule.keys())[0]))


def backward_chaining(fact, facts, rules):
    rules_applied = []

    if fact in facts:
        return True, rules_applied, facts
    else:
        rules_stack = get_backward_chain(fact, rules, rules.copy(), facts, already_searched=set())
        remove_unnecessary_rules(rules_stack, rules)
        facts = apply_rules_in_rules_stack(fact, facts, rules, rules_applied, rules_stack)

        return fact in facts, rules_applied, facts


def get_backward_chain(fact, rules, possible_rules, facts, already_searched=set()):
    rules_stack = []
    if fact in already_searched:
        return rules_stack

    rules_of_the_fact = rules_having_fact_in_consequence(fact, possible_rules)
    for rule in rules_of_the_fact:
        while rule in possible_rules and rules.index(rule) not in rules_stack:
            save_rule_index(rule, rules, rules_stack)
            already_searched.add(fact)
            for f in premise_of(rule):
                chain = get_backward_chain(f, rules, possible_rules, facts, already_searched)
                [rules_stack.append(r) for r in chain if r not in rules_stack]

    remove_rules_of_unprovable_fact(already_searched, fact, facts,
                                    possible_rules, rules, rules_of_the_fact,
                                    rules_stack)  # probably an object is hiding screaming to be created :)

    remove_inapplicable_rules(possible_rules, rules, rules_stack)

    return rules_stack


def remove_rules_of_unprovable_fact(already_searched, fact, facts, possible_rules, rules,
                                    rules_of_the_fact,
                                    rules_stack):
    if len(rules_of_the_fact) == 0 and fact not in facts:
        for r in rules_that_have_fact_in_premise(fact, rules):
            for f in premise_of(rules[r]):
                remove_the_rule_of(fact, possible_rules, rules_stack)
                if f in already_searched:
                    already_searched.remove(fact)


def remove_inapplicable_rules(possible_rules, rules, rules_stack):
    for rule in rules:
        i = rules.index(rule)
        if i in rules_stack and rule not in possible_rules:
            rules_stack.remove(i)


def remove_unnecessary_rules(rules_stack, rules):
    count = dict()
    indices_to_remove = []
    for i in rules_stack:
        fact = frozenset(consequence_of(rules[i]))
        if count.get(fact):
            count.update({fact: count.get(fact) + 1})
        else:
            count.update({fact: 1})
        if count.get(fact) > 1:
            indices_to_remove.append(i)

    for i in indices_to_remove:
        rules_stack.remove(i)


def apply_rules_in_rules_stack(fact, facts, rules, rules_applied, rules_stack):
    stop = False
    while not stop and (fact not in facts):
        stop = True
        for i in rules_stack:
            if is_premise_in_facts(rules[i], facts):
                facts = apply_rule(facts, rules[i], rules, rules_applied)
                rules_stack.remove(i)
                stop = False
    return facts


def fact_not_provable(fact, facts, rule):
    return not rule and fact not in facts


def remove_the_rule_of(fact, rules, rules_indices):
    indices = rules_that_have_fact_in_premise(fact, rules)
    [rules_indices.remove(i) for i in indices if i in rules_indices]
    values = [rules[i] for i in indices]
    for v in values:
        rules.remove(v)


def rules_that_have_fact_in_premise(fact, rules):
    result = []
    for i in range(len(rules)):
        if fact in premise_of(rules[i]):
            result.append(i)
    return result


def rules_having_fact_in_consequence(fact, rules):
    result = []
    for rule in rules:
        if fact in consequence_of(rule):
            result.append(rule)
    return result


def premise_of(rule):
    return list(rule.keys())[0]


def consequence_of(rule):
    return rule.get(list(rule.keys())[0])
