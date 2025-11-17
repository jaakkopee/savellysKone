#!/usr/bin/env python3
"""Test that right recursion is accepted without warnings"""

import grammar_validator

# Test 1: Right recursion should be valid with no warnings
right_recursive_grammar = """
$S -> $A $S | $A
$A -> 60 62 64
"""

print("Test 1: Right recursion grammar (should be valid, no warnings)")
is_valid, message = grammar_validator.validate_grammar(right_recursive_grammar)
print(message)
print(f"Valid: {is_valid}")
print()

# Test 2: Another right recursion pattern
right_recursive_grammar2 = """
$S -> 60 $S | 62 $S | 64
"""

print("Test 2: Another right recursion pattern (should be valid, no warnings)")
is_valid, message = grammar_validator.validate_grammar(right_recursive_grammar2)
print(message)
print(f"Valid: {is_valid}")
print()

# Test 3: Left recursion should still be caught
left_recursive_grammar = """
$S -> $S 60 | 62
"""

print("Test 3: Left recursion (should be rejected)")
is_valid, message = grammar_validator.validate_grammar(left_recursive_grammar)
print(message)
print(f"Valid: {is_valid}")
print()

# Test 4: Indirect left recursion should show warning
indirect_left_recursion = """
$S -> $A 60
$A -> $B 62
$B -> $S 64
"""

print("Test 4: Indirect left recursion cycle (should warn about cycle)")
is_valid, message = grammar_validator.validate_grammar(indirect_left_recursion)
print(message)
print(f"Valid: {is_valid}")
print()

# Test 5: Complex valid right recursion
complex_right = """
$S -> $phrase $S | $phrase
$phrase -> $note01 $note02 $note03
$note01 -> 60
$note02 -> 62
$note03 -> 64
"""

print("Test 5: Complex right recursion (should be valid, no warnings)")
is_valid, message = grammar_validator.validate_grammar(complex_right)
print(message)
print(f"Valid: {is_valid}")
