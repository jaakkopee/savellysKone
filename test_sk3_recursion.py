#!/usr/bin/env python3
"""Test the recursion prevention in the context of savellysKone3"""

import savellysKone3 as sk3

# Test with valid grammar
print("Test 1: Creating ListGenerator with valid grammar")
try:
    valid_grammar = """$S -> $phrase01 $phrase02
$phrase01 -> $note01 $note02
$phrase02 -> $note03 $note04
$note01 -> 60
$note02 -> 62
$note03 -> 64
$note04 -> 65"""
    
    gen = sk3.ListGenerator(valid_grammar, 8, "pitch")
    result = gen.generate_list()
    print(f"✓ Valid grammar works. Generated list: {result}")
except Exception as e:
    print(f"✗ Unexpected error with valid grammar: {e}")

# Test with invalid grammar (direct left recursion)
print("\nTest 2: Creating ListGenerator with invalid grammar ($S -> $S)")
try:
    invalid_grammar = """$S -> $S"""
    gen = sk3.ListGenerator(invalid_grammar, 8, "pitch")
    result = gen.generate_list()
    print(f"✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected with ValueError: {e}")
except Exception as e:
    print(f"✗ Wrong exception type: {type(e).__name__}: {e}")

# Test with another invalid grammar
print("\nTest 3: Creating ListGenerator with invalid grammar ($S -> $S $A)")
try:
    invalid_grammar2 = """$S -> $S $A
$A -> 60"""
    gen = sk3.ListGenerator(invalid_grammar2, 8, "pitch")
    result = gen.generate_list()
    print(f"✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected with ValueError: {e}")
except Exception as e:
    print(f"✗ Wrong exception type: {type(e).__name__}: {e}")

# Test with grammar that has left recursion in one alternative
print("\nTest 4: Grammar with left recursion in alternative ($S -> 60 | $S)")
try:
    invalid_grammar3 = """$S -> 60 | $S"""
    gen = sk3.ListGenerator(invalid_grammar3, 8, "pitch")
    result = gen.generate_list()
    print(f"✗ Invalid grammar was accepted (should have been rejected)")
except ValueError as e:
    print(f"✓ Correctly rejected with ValueError: {e}")
except Exception as e:
    print(f"✗ Wrong exception type: {type(e).__name__}: {e}")

print("\n✓ All savellysKone3 integration tests completed")
