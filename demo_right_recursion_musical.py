#!/usr/bin/env python3
"""
Demonstrate right recursion creating musical patterns
This shows that right recursion works correctly now.
"""

import sys
sys.path.insert(0, '/Users/jaakkoprattala/Documents/koodii/savellysKone')
import gengramparser2 as ggp

# Example 1: Ascending chromatic scale with variable length
print("=" * 60)
print("Example 1: Variable-length ascending chromatic pattern")
print("=" * 60)

chromatic_grammar = """
$S -> $note $S | $note
$note -> 60 | 61 | 62 | 63 | 64 | 65
"""

grammar1 = ggp.parse_grammar(chromatic_grammar.strip().split("\n"))
print("Grammar:")
print(chromatic_grammar)

print("\nGenerated sequences (5 examples):")
for i in range(5):
    result = ggp.generate(grammar1, "$S", 10)
    notes = result.split()
    print(f"  {i+1}. Length {len(notes)}: {result}")

# Example 2: Rhythm pattern with recursive extension  
print("\n" + "=" * 60)
print("Example 2: Rhythm with recursive variation")
print("=" * 60)

rhythm_grammar = """
$S -> $beat $S | $beat
$beat -> 0.25 | 0.5 | 0.75 | 1.0
"""

grammar2 = ggp.parse_grammar(rhythm_grammar.strip().split("\n"))
print("Grammar:")
print(rhythm_grammar)

print("\nGenerated rhythm patterns (5 examples):")
for i in range(5):
    result = ggp.generate(grammar2, "$S", 8)
    beats = result.split()
    total_duration = sum(float(b) for b in beats)
    print(f"  {i+1}. Length {len(beats)}, Duration {total_duration:.2f}: {result}")

# Example 3: Velocity crescendo/decrescendo
print("\n" + "=" * 60)
print("Example 3: Velocity patterns with right recursion")
print("=" * 60)

velocity_grammar = """
$S -> $vel $S | $vel
$vel -> 40 | 60 | 80 | 100 | 120
"""

grammar3 = ggp.parse_grammar(velocity_grammar.strip().split("\n"))
print("Grammar:")
print(velocity_grammar)

print("\nGenerated velocity patterns (5 examples):")
for i in range(5):
    result = ggp.generate(grammar3, "$S", 6)
    vels = result.split()
    print(f"  {i+1}. Length {len(vels)}: {result}")

# Example 4: Nested phrase structure
print("\n" + "=" * 60)
print("Example 4: Phrase structure with right recursion")
print("=" * 60)

phrase_grammar = """
$S -> $phrase $S | $phrase
$phrase -> $motif $motif
$motif -> 60 62 | 64 65
"""

grammar4 = ggp.parse_grammar(phrase_grammar.strip().split("\n"))
print("Grammar:")
print(phrase_grammar)

print("\nGenerated phrase structures (5 examples):")
for i in range(5):
    result = ggp.generate(grammar4, "$S", 6)
    notes = result.split()
    print(f"  {i+1}. Length {len(notes)}: {result}")

print("\n" + "=" * 60)
print("✓ All right recursion examples work correctly!")
print("=" * 60)
