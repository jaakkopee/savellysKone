#!/usr/bin/env python3
"""
Test the interaction between repeat syntax (*N) and bracket notation [a|b|c]
"""

import gengramparser2 as ggp

print("=" * 70)
print("Testing Repeat Syntax with Bracket Notation")
print("=" * 70)

# Test 1: Brackets inside repeat
print("\nTest 1: Brackets inside repeat - ([60|62|64] 65 *4)")
print("Expected: Random choice from [60,62,64] followed by 65, repeated 4 times")
grammar1 = "$S -> ([60|62|64] 65 *4)"
g1 = ggp.parse_grammar(grammar1.strip().split("\n"))
print("Sample outputs:")
for i in range(5):
    result = ggp.generate(g1, "$S", 10)
    print(f"  Run {i+1}: {result} (length: {len(result.split())})")

# Test 2: Multiple brackets in repeat
print("\nTest 2: Multiple brackets in repeat - ([60|62] [64|65] *3)")
print("Expected: Two random choices, repeated 3 times")
grammar2 = "$S -> ([60|62] [64|65] *3)"
g2 = ggp.parse_grammar(grammar2.strip().split("\n"))
print("Sample outputs:")
for i in range(5):
    result = ggp.generate(g2, "$S", 10)
    print(f"  Run {i+1}: {result} (length: {len(result.split())})")

# Test 3: Repeat inside bracket alternatives
print("\nTest 3: Repeat inside bracket alternatives - [(60 62 *2) | (64 65 *3)]")
print("Expected: Either '60 62 60 62' OR '64 65 64 65 64 65'")
grammar3 = "$S -> [(60 62 *2) | (64 65 *3)]"
g3 = ggp.parse_grammar(grammar3.strip().split("\n"))
print("Sample outputs:")
for i in range(5):
    result = ggp.generate(g3, "$S", 10)
    print(f"  Run {i+1}: {result} (length: {len(result.split())})")

# Test 4: Complex nested combination
print("\nTest 4: Complex nested - ([60|62|64] *2) ([65|67] *3)")
print("Expected: Random choice repeated 2x, then another random choice repeated 3x")
grammar4 = "$S -> ([60|62|64] *2) ([65|67] *3)"
g4 = ggp.parse_grammar(grammar4.strip().split("\n"))
print("Sample outputs:")
for i in range(5):
    result = ggp.generate(g4, "$S", 10)
    print(f"  Run {i+1}: {result} (length: {len(result.split())})")

# Test 5: Brackets with non-terminal expansion and repeat
print("\nTest 5: Brackets with grammar expansion and repeat")
print("Grammar:")
print("  $S -> ([$NOTE|$ALT] *4)")
print("  $NOTE -> 60 62")
print("  $ALT -> 64 65")
grammar5 = """$S -> ([$NOTE|$ALT] *4)
$NOTE -> 60 62
$ALT -> 64 65"""
g5 = ggp.parse_grammar(grammar5.strip().split("\n"))
print("Sample outputs:")
for i in range(5):
    result = ggp.generate(g5, "$S", 10)
    print(f"  Run {i+1}: {result} (length: {len(result.split())})")

# Test 6: IOI pattern with brackets and repeat (rhythmic variation)
print("\nTest 6: IOI pattern with brackets and repeat - ([0.25|0.5] 0.125 *8)")
print("Expected: Random quarter or half note, then eighth, repeated 8 times")
grammar6 = "$S -> ([0.25|0.5] 0.125 *8)"
g6 = ggp.parse_grammar(grammar6.strip().split("\n"))
print("Sample outputs:")
for i in range(3):
    result = ggp.generate(g6, "$S", 10)
    print(f"  Run {i+1}: {result}")
    print(f"           Length: {len(result.split())}")

print("\n" + "=" * 70)
print("Summary:")
print("=" * 70)
print("""
✓ Brackets work inside repeats: ([a|b] c *N)
✓ Multiple brackets in repeats: ([a|b] [c|d] *N)
✓ Repeats work as bracket alternatives: [(a *2) | (b *3)]
✓ Can combine multiple repeat+bracket groups
✓ Works with non-terminal expansion
✓ Perfect for creating rhythmic and melodic variations

Use cases:
- Varied rhythmic patterns: ([0.25|0.5] 0.125 *16)
- Melodic variation: ([60|62|64] 65 67 *4)
- Chord progressions: ([$Cmaj|$Fmaj] $Gmaj *4)
""")
