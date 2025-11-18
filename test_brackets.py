#!/usr/bin/env python3
"""Test bracket functionality in gengramparser2"""

import gengramparser2 as ggp

# Test 1: Simple bracketed alternatives
print("=" * 60)
print("Test 1: Simple bracketed alternatives")
print("=" * 60)
grammar_str1 = """
$S -> $phrase $phrase $phrase $phrase
$phrase -> [60 | 62 | 64 | 65]
"""
grammar1 = ggp.parse_grammar(grammar_str1.strip().split("\n"))
result1 = ggp.generate(grammar1, "$S", 128)
print(f"Grammar:\n{grammar_str1}")
print(f"Result: {result1}")
print()

# Test 2: Bracketed alternatives with non-terminals
print("=" * 60)
print("Test 2: Bracketed alternatives with non-terminals")
print("=" * 60)
grammar_str2 = """
$S -> $phrase $phrase $phrase $phrase
$phrase -> [$low | $mid | $high]
$low -> 60
$mid -> 67
$high -> 72
"""
grammar2 = ggp.parse_grammar(grammar_str2.strip().split("\n"))
result2 = ggp.generate(grammar2, "$S", 128)
print(f"Grammar:\n{grammar_str2}")
print(f"Result: {result2}")
print()

# Test 3: Mixed brackets and regular alternatives
print("=" * 60)
print("Test 3: Mixed brackets in sequence")
print("=" * 60)
grammar_str3 = """
$S -> $phrase $phrase
$phrase -> [60 | 62] [64 | 65] [67 | 69]
"""
grammar3 = ggp.parse_grammar(grammar_str3.strip().split("\n"))
result3 = ggp.generate(grammar3, "$S", 128)
print(f"Grammar:\n{grammar_str3}")
print(f"Result: {result3}")
print()

# Test 4: Nested brackets
print("=" * 60)
print("Test 4: Nested brackets")
print("=" * 60)
grammar_str4 = """
$S -> $phrase $phrase
$phrase -> [[60 | 62] | [64 | 65]]
"""
grammar4 = ggp.parse_grammar(grammar_str4.strip().split("\n"))
result4 = ggp.generate(grammar4, "$S", 128)
print(f"Grammar:\n{grammar_str4}")
print(f"Result: {result4}")
print()

# Test 5: Complex example with brackets and non-terminals
print("=" * 60)
print("Test 5: Complex example - melody with rhythm variations")
print("=" * 60)
grammar_str5 = """
$S -> $melody $melody
$melody -> $note [1.0 | 0.5 | 0.25] $note [1.0 | 0.5] $note [1.0 | 2.0]
$note -> [60 | 62 | 64 | 65 | 67]
"""
grammar5 = ggp.parse_grammar(grammar_str5.strip().split("\n"))
result5 = ggp.generate(grammar5, "$S", 128)
print(f"Grammar:\n{grammar_str5}")
print(f"Result: {result5}")
print()

print("=" * 60)
print("All tests completed successfully!")
print("=" * 60)
