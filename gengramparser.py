import random
import sys

class GrammarRule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return self.lhs + " -> " + self.rhs

    def __repr__(self):
        return self.__str__()

class Grammar:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def __str__(self):
        return "\n".join(map(str, self.rules))

    def __repr__(self):
        return self.__str__()

def parse_grammar(f):
    grammar = Grammar()
    for line in f:
        line = line.strip()
        if line:
            lhs, rhs_alternatives = line.split("->")
            lhs = lhs.strip()
            alternatives = rhs_alternatives.split("|")
            alternatives = [alt.strip() for alt in alternatives]
            for alternative in alternatives:
                grammar.add_rule(GrammarRule(lhs, alternative))
    return grammar

def generate_from_symbol(grammar, symbol):
    options = [rule.rhs for rule in grammar.rules if rule.lhs == symbol]
    if options:
        return random.choice(options)
    return symbol

def generate_from_string(grammar, string):
    output = ""
    for symbol in string:
        output += generate_from_symbol(grammar, symbol)
    return output

def generate(grammar, symbol, depth):
    if depth == 0:
        return symbol
    else:
        return generate(grammar, generate_from_string(grammar, symbol), depth - 1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 gengramparser.py <grammar_file> <depth>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    depth = int(sys.argv[2])

    with open(grammar_file) as f:
        grammar = parse_grammar(f)
        print(grammar)
        print(generate(grammar, "S", depth))
