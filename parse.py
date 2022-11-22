def parse_input(input_file):
    with open(input_file, 'r') as file:
        lines = file.read().split('\n')
        facts = parse_facts(lines[1])
        i = lines.index('DEMONTRER:')
        rules = parse_rules(lines[3:i])
        fact = lines[-1]
        return fact, facts, rules


def parse_facts(header):
    return {c for c in header if c.isalpha()}


def parse_rules(rules_lines):
    return [parse_rule(line) for line in rules_lines]


def parse_rule(line):
    line = line.split(" ")
    premise = parse_premise(line)
    consequence = parse_consequence(line)
    return {tuple(premise) if len(premise) > 1 else premise[0] : consequence}


def parse_consequence(line):
    return {c for c in line[line.index('ALORS'):] if c.isalpha() and len(c) == 1}


def parse_premise(line):
    return [c  for c in line[: line.index('ALORS')] if c.isalpha() and len(c) == 1]