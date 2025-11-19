#!/usr/bin/env python3
"""
Demo of the new repeat syntax (items *N) in grammars

This script demonstrates how you can use parentheses with *N
to repeat patterns in your grammars.

Syntax: (items *N) repeats the items N times

Examples:
    (60 62 64 *4)           → 60 62 64 60 62 64 60 62 64 60 62 64
    (0.25 0.125 *8)         → 0.25 0.125 0.25 0.125 ... (8 times)
    (64 66 65 67 *8)        → repeats the pattern 8 times
"""

import gengramparser2 as ggp

print("=" * 60)
print("DEMO: Repeat Syntax in Grammars")
print("=" * 60)

# Example 1: Simple pitch pattern with repeat
print("\n1. Pitch pattern with repeat:")
print("   Grammar: $S -> (60 62 64 65 *4)")
print("   This creates: 60 62 64 65 (repeated 4 times)")

pitch_grammar = """$S -> (60 62 64 65 *4)"""
grammar1 = ggp.parse_grammar(pitch_grammar.strip().split("\n"))
result1 = ggp.generate(grammar1, "$S", 10)
print(f"   Result: {result1}")
print(f"   Length: {len(result1.split())}")

# Example 2: IOI pattern with repeat
print("\n2. IOI (rhythm) pattern with repeat:")
print("   Grammar: $S -> (0.25 0.125 0.125 0.25 *8)")
print("   This creates a rhythmic pattern repeated 8 times")

ioi_grammar = """$S -> (0.25 0.125 0.125 0.25 *8)"""
grammar2 = ggp.parse_grammar(ioi_grammar.strip().split("\n"))
result2 = ggp.generate(grammar2, "$S", 10)
print(f"   Result: {result2}")
print(f"   Length: {len(result2.split())}")

# Example 3: Combined with grammar rules
print("\n3. Repeat with grammar expansion:")
print("   Grammar:")
print("   $S -> ($PATTERN *6)")
print("   $PATTERN -> 64 66 65 67")

combined_grammar = """$S -> ($PATTERN *6)
$PATTERN -> 64 66 65 67"""
grammar3 = ggp.parse_grammar(combined_grammar.strip().split("\n"))
result3 = ggp.generate(grammar3, "$S", 10)
print(f"   Result: {result3}")
print(f"   Length: {len(result3.split())}")

# Example 4: Multiple repeats in one rule
print("\n4. Multiple repeats in one line:")
print("   Grammar: $S -> (60 62 *2) (64 65 *3) (67 *4)")

multi_grammar = """$S -> (60 62 *2) (64 65 *3) (67 *4)"""
grammar4 = ggp.parse_grammar(multi_grammar.strip().split("\n"))
result4 = ggp.generate(grammar4, "$S", 10)
print(f"   Result: {result4}")
print(f"   Length: {len(result4.split())}")

print("\n" + "=" * 60)
print("How to use in the GUI:")
print("=" * 60)
print("""
1. Go to the List Generator tab
2. Enter a grammar like: $S -> (64 66 65 67 *8)
3. Click 'Generate Pitch/Duration/Velocity/IOI List'
4. The pattern will be repeated 8 times automatically!

This works for:
- Pitch lists: (60 62 64 *4)
- Duration lists: (0.5 0.25 *8)
- Velocity lists: (80 90 100 *4)
- IOI lists: (0.25 0.125 *16)
""")

print("=" * 60)
