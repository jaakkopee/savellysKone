#!/usr/bin/env python3
"""Test the repeat syntax (items *N) in grammar parser"""

import gengramparser2 as ggp

print("Testing repeat syntax in grammars\n")
print("=" * 50)

# Test 1: Simple repeat
print("\nTest 1: Simple repeat (64 66 65 67 *8)")
grammar_str1 = "$S -> (64 66 65 67 *8)"
grammar1 = ggp.parse_grammar(grammar_str1.strip().split("\n"))
result1 = ggp.generate(grammar1, "$S", 5)  # Use depth > 0 to expand grammar
print(f"Grammar: {grammar_str1}")
print(f"Result: {result1}")
result_list = result1.split()
print(f"Length: {len(result_list)} (expected: 32, which is 4*8)")
expected = ["64", "66", "65", "67"] * 8
if result_list == expected:
    print("✓ Test 1 PASSED")
else:
    print("✗ Test 1 FAILED")
    print(f"Expected: {expected}")

# Test 2: Single item repeat
print("\nTest 2: Single item repeat (60 *4)")
grammar_str2 = "$S -> (60 *4)"
grammar2 = ggp.parse_grammar(grammar_str2.strip().split("\n"))
result2 = ggp.generate(grammar2, "$S", 5)  # Use depth > 0
print(f"Grammar: {grammar_str2}")
print(f"Result: {result2}")
result_list2 = result2.split()
print(f"Length: {len(result_list2)} (expected: 4)")
expected2 = ["60"] * 4
if result_list2 == expected2:
    print("✓ Test 2 PASSED")
else:
    print("✗ Test 2 FAILED")
    print(f"Expected: {expected2}")

# Test 3: Repeat with grammar rules
print("\nTest 3: Repeat with grammar expansion")
grammar_str3 = """$S -> ($NOTES *3)
$NOTES -> 60 62 64"""
grammar3 = ggp.parse_grammar(grammar_str3.strip().split("\n"))
result3 = ggp.generate(grammar3, "$S", 10)
print(f"Grammar:\n{grammar_str3}")
print(f"Result: {result3}")
result_list3 = result3.split()
print(f"Length: {len(result_list3)} (expected: 9, which is 3*3)")
expected3 = ["60", "62", "64"] * 3
if result_list3 == expected3:
    print("✓ Test 3 PASSED")
else:
    print("✗ Test 3 FAILED")
    print(f"Expected: {expected3}")

# Test 4: Multiple repeats in one rule
print("\nTest 4: Multiple repeats (64 65 *2) (66 67 *3)")
grammar_str4 = "$S -> (64 65 *2) (66 67 *3)"
grammar4 = ggp.parse_grammar(grammar_str4.strip().split("\n"))
result4 = ggp.generate(grammar4, "$S", 5)  # Use depth > 0
print(f"Grammar: {grammar_str4}")
print(f"Result: {result4}")
result_list4 = result4.split()
print(f"Length: {len(result_list4)} (expected: 10, which is 2*2 + 2*3)")
expected4 = ["64", "65", "64", "65", "66", "67", "66", "67", "66", "67"]
if result_list4 == expected4:
    print("✓ Test 4 PASSED")
else:
    print("✗ Test 4 FAILED")
    print(f"Expected: {expected4}")

# Test 5: Repeat with floats (for durations/IOI)
print("\nTest 5: Repeat with floats (0.25 0.125 *4)")
grammar_str5 = "$S -> (0.25 0.125 *4)"
grammar5 = ggp.parse_grammar(grammar_str5.strip().split("\n"))
result5 = ggp.generate(grammar5, "$S", 5)  # Use depth > 0
print(f"Grammar: {grammar_str5}")
print(f"Result: {result5}")
result_list5 = result5.split()
print(f"Length: {len(result_list5)} (expected: 8, which is 2*4)")
expected5 = ["0.25", "0.125"] * 4
if result_list5 == expected5:
    print("✓ Test 5 PASSED")
else:
    print("✗ Test 5 FAILED")
    print(f"Expected: {expected5}")

print("\n" + "=" * 50)
print("All tests completed!")
