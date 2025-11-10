#!/usr/bin/env python3
"""Test the recursion prevention in grammar parser"""

import gengramparser2 as ggp

# Test 1: Valid grammar (should work)
print("Test 1: Valid grammar")
try:
    valid_grammar = """$S -> $A $B
$A -> 60 62
$B -> 64 65"""
    grammar = ggp.parse_grammar(valid_grammar.split("\n"))
    print("✓ Valid grammar accepted")
except ValueError as e:
    print(f"✗ Unexpected error: {e}")

# Test 2: Direct left recursion (should fail)
print("\nTest 2: Direct left recursion - $S -> $S")
try:
    invalid_grammar1 = """$S -> $S"""
    grammar = ggp.parse_grammar(invalid_grammar1.split("\n"))
    print("✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected: {e}")

# Test 3: Direct left recursion with other symbols (should fail)
print("\nTest 3: Direct left recursion - $S -> $S $A")
try:
    invalid_grammar2 = """$S -> $S $A
$A -> 60"""
    grammar = ggp.parse_grammar(invalid_grammar2.split("\n"))
    print("✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected: {e}")

# Test 4: Valid recursion (non-terminal not first) - should work
print("\nTest 4: Valid recursion - $S -> $A $S")
try:
    valid_grammar2 = """$S -> $A $S | $A
$A -> 60"""
    grammar = ggp.parse_grammar(valid_grammar2.split("\n"))
    print("✓ Valid (non-left) recursion accepted")
except ValueError as e:
    print(f"✗ Unexpected error: {e}")

# Test 5: Alternative with left recursion (should fail)
print("\nTest 5: Alternative with left recursion - $S -> 60 | $S")
try:
    invalid_grammar3 = """$S -> 60 | $S"""
    grammar = ggp.parse_grammar(invalid_grammar3.split("\n"))
    print("✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected: {e}")

# Test 6: Multiple rules, one with left recursion (should fail)
print("\nTest 6: Multiple rules, one with left recursion")
try:
    invalid_grammar4 = """$S -> $A $B
$A -> 60
$B -> $B 64"""
    grammar = ggp.parse_grammar(invalid_grammar4.split("\n"))
    print("✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected: {e}")

print("\n✓ All tests completed")
