#!/usr/bin/env python3
"""
Quick demonstration of recursion prevention.
Run this to see how the grammar parser now prevents infinite recursion.
"""

import gengramparser2 as ggp

print("=" * 70)
print("RECURSION PREVENTION DEMONSTRATION")
print("=" * 70)
print()

# Example 1: Valid grammar
print("Example 1: VALID GRAMMAR")
print("-" * 70)
valid_grammar = """$S -> $A $B
$A -> 60 62
$B -> 64 65"""
print("Grammar:")
print(valid_grammar)
print()
try:
    grammar = ggp.parse_grammar(valid_grammar.split("\n"))
    result = ggp.generate(grammar, "$S", 10)
    print(f"✓ SUCCESS: Generated: {result}")
except ValueError as e:
    print(f"✗ ERROR: {e}")
print()

# Example 2: Invalid grammar - direct self-reference
print("Example 2: INVALID GRAMMAR (Direct Self-Reference)")
print("-" * 70)
invalid_grammar1 = """$S -> $S"""
print("Grammar:")
print(invalid_grammar1)
print()
try:
    grammar = ggp.parse_grammar(invalid_grammar1.split("\n"))
    result = ggp.generate(grammar, "$S", 10)
    print(f"✗ SHOULD HAVE FAILED: Generated: {result}")
except ValueError as e:
    print(f"✓ CORRECTLY REJECTED:")
    print(f"   {e}")
print()

# Example 3: Invalid grammar - self-reference with other symbols
print("Example 3: INVALID GRAMMAR (Self-Reference with Other Symbols)")
print("-" * 70)
invalid_grammar2 = """$S -> $S $A
$A -> 60"""
print("Grammar:")
print(invalid_grammar2)
print()
try:
    grammar = ggp.parse_grammar(invalid_grammar2.split("\n"))
    result = ggp.generate(grammar, "$S", 10)
    print(f"✗ SHOULD HAVE FAILED: Generated: {result}")
except ValueError as e:
    print(f"✓ CORRECTLY REJECTED:")
    print(f"   {e}")
print()

# Example 4: Valid grammar - right recursion
print("Example 4: VALID GRAMMAR (Right Recursion)")
print("-" * 70)
valid_grammar2 = """$S -> $A $S | $A
$A -> 60 62"""
print("Grammar:")
print(valid_grammar2)
print()
try:
    grammar = ggp.parse_grammar(valid_grammar2.split("\n"))
    result = ggp.generate(grammar, "$S", 10)
    print(f"✓ SUCCESS: Generated: {result}")
except ValueError as e:
    print(f"✗ ERROR: {e}")
print()

# Example 5: Invalid grammar - self-reference in alternative
print("Example 5: INVALID GRAMMAR (Self-Reference in Alternative)")
print("-" * 70)
invalid_grammar3 = """$S -> 60 | $S"""
print("Grammar:")
print(invalid_grammar3)
print()
try:
    grammar = ggp.parse_grammar(invalid_grammar3.split("\n"))
    result = ggp.generate(grammar, "$S", 10)
    print(f"✗ SHOULD HAVE FAILED: Generated: {result}")
except ValueError as e:
    print(f"✓ CORRECTLY REJECTED:")
    print(f"   {e}")
print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()
print("The grammar parser now prevents infinite recursion by rejecting")
print("rules where a non-terminal appears as the first symbol on the")
print("right-hand side of its own rewrite rule.")
print()
print("Valid:   $S -> $A $S | $A  (right recursion)")
print("Invalid: $S -> $S          (left recursion)")
print("Invalid: $S -> $S $A       (left recursion)")
print()
