import random
import sys

DEBUG = False
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

def split_alternatives(text):
    """Split by | but only outside of brackets"""
    alternatives = []
    current = ""
    bracket_depth = 0
    
    for char in text:
        if char == "[":
            bracket_depth += 1
            current += char
        elif char == "]":
            bracket_depth -= 1
            current += char
            if bracket_depth < 0:
                raise ValueError(f"Unmatched closing bracket ] in: {text}")
        elif char == "|" and bracket_depth == 0:
            # This | is outside brackets, so it's a rule alternative separator
            alternatives.append(current.strip())
            current = ""
        else:
            current += char
    
    # Check for unmatched opening brackets
    if bracket_depth > 0:
        raise ValueError(f"Unmatched opening bracket [ in: {text}")
    
    # Don't forget the last alternative
    if current.strip():
        alternatives.append(current.strip())
    
    return alternatives

def expand_brackets(string):
    """Expand bracketed alternatives [a | b | c] by choosing one randomly.
    Processes brackets from outermost to innermost, one level at a time."""
    
    # Keep expanding until no brackets remain
    while "[" in string:
        result = ""
        i = 0
        
        while i < len(string):
            if string[i] == "[":
                # Find the matching closing bracket
                bracket_depth = 1
                j = i + 1
                while j < len(string) and bracket_depth > 0:
                    if string[j] == "[":
                        bracket_depth += 1
                    elif string[j] == "]":
                        bracket_depth -= 1
                    j += 1
                
                if bracket_depth != 0:
                    raise ValueError(f"Unmatched brackets in: {string}")
                
                # Extract content between brackets (excluding [ and ])
                bracketed_content = string[i+1:j-1]
                
                # Split by | to get alternatives at THIS level only
                # We need to respect nested brackets when splitting
                alternatives = split_bracket_alternatives(bracketed_content)
                
                # Choose one alternative randomly
                chosen = random.choice(alternatives)
                
                result += chosen
                i = j
            else:
                result += string[i]
                i += 1
        
        string = result
    
    return string

def split_bracket_alternatives(text):
    """Split by | but only at the top level (not inside nested brackets)"""
    alternatives = []
    current = ""
    bracket_depth = 0
    
    for char in text:
        if char == "[":
            bracket_depth += 1
            current += char
        elif char == "]":
            bracket_depth -= 1
            current += char
        elif char == "|" and bracket_depth == 0:
            # This | is at the top level
            alternatives.append(current.strip())
            current = ""
        else:
            current += char
    
    # Don't forget the last alternative
    if current.strip():
        alternatives.append(current.strip())
    
    return alternatives

def parse_grammar(f):
    grammar = Grammar()
    for line in f:
        line = line.strip()
        if line:
            lhs, rhs_alternatives = line.split("->")
            lhs = lhs.strip()
            # Use smart splitting that respects brackets
            alternatives = split_alternatives(rhs_alternatives)
            for alternative in alternatives:
                # Check for direct left recursion: LHS cannot be the first symbol on RHS
                # Note: Right recursion (LHS at end) is valid and allowed
                rhs_first_symbol = alternative.split()[0] if alternative.split() else ""
                if rhs_first_symbol == lhs:
                    raise ValueError(f"Direct left recursion detected: '{lhs} -> {alternative}'. "
                                   f"The non-terminal '{lhs}' cannot appear as the first symbol on the right side of its own rule. "
                                   f"(Note: Right recursion like '{lhs} -> other_symbols {lhs}' is allowed)")
                grammar.add_rule(GrammarRule(lhs, alternative))
    if DEBUG:
        print(grammar)
    return grammar

def generate_from_symbol(grammar, symbol):
    options = [rule.rhs for rule in grammar.rules if rule.lhs == symbol]
    if options:
        chosen = random.choice(options)
        # Expand brackets in the chosen rule before returning
        return expand_brackets(chosen)
    return symbol

def generate_from_string(grammar, string):
    output = ""
    i = 0
    while i < len(string):
        if string[i] == "$":
            j = i + 1
            while j < len(string) and string[j] != " ":
                j += 1
            nonterminal = string[i:j]
            output += generate_from_symbol(grammar, nonterminal)
            i = j
        else:
            output += string[i]
            i += 1
    return output

def generate(grammar, symbol, depth):
    if depth == 0:
        return symbol
    else:
        return generate(grammar, generate_from_string(grammar, symbol), depth - 1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 gengramparser2.py <grammar_file> <depth>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    depth = int(sys.argv[2])

    with open(grammar_file) as f:
        grammar = parse_grammar(f)
        print(grammar)
        print(generate(grammar, "$S", depth))

