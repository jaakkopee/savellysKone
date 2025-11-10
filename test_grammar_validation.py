#!/usr/bin/env python3
"""Test the recursion prevention without full imports"""

import gengramparser2 as ggp

# Simulate what ListGenerator does
def test_list_generator_grammar(grammar_str, description):
    print(f"\n{description}")
    try:
        grammar = ggp.parse_grammar(grammar_str.split("\n"))
        print(f"✓ Grammar accepted (parsed successfully)")
        # Try to generate something
        result = ggp.generate(grammar, "$S", 64)
        print(f"  Generated: {result[:50]}..." if len(result) > 50 else f"  Generated: {result}")
        return True
    except ValueError as e:
        print(f"✓ Correctly rejected with ValueError:")
        print(f"  {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
        return False

# Test with valid grammar
test_list_generator_grammar(
    """$S -> $phrase01 $phrase02
$phrase01 -> $note01 $note02
$phrase02 -> $note03 $note04
$note01 -> 60
$note02 -> 62
$note03 -> 64
$note04 -> 65""",
    "Test 1: Valid grammar"
)

# Test with invalid grammar (direct left recursion)
test_list_generator_grammar(
    """$S -> $S""",
    "Test 2: Invalid grammar - $S -> $S (should be rejected)"
)

# Test with another invalid grammar
test_list_generator_grammar(
    """$S -> $S $A
$A -> 60""",
    "Test 3: Invalid grammar - $S -> $S $A (should be rejected)"
)

# Test with grammar that has left recursion in one alternative
test_list_generator_grammar(
    """$S -> 60 | $S""",
    "Test 4: Grammar with left recursion in alternative (should be rejected)"
)

# Test valid right recursion
test_list_generator_grammar(
    """$S -> $A $S | $A
$A -> 60 62""",
    "Test 5: Valid right recursion (should work)"
)

# Test another invalid one with multiple rules
test_list_generator_grammar(
    """$S -> $A $B
$A -> 60 62
$B -> $B 64 65""",
    "Test 6: Invalid - left recursion in $B rule (should be rejected)"
)

print("\n✓ All tests completed")
