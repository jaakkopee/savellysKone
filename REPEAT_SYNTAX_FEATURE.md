# Grammar Syntax Reference: Repeats and Brackets

## Overview
The grammar parser supports powerful features for creating musical patterns:
1. **Repeat Syntax** - `(items *N)` - Repeat patterns multiple times
2. **Bracket Notation** - `[a|b|c]` - Random choice from alternatives
3. **Combined Usage** - Both features work together seamlessly

These features enable you to create complex, varied musical patterns with concise, readable grammars.

## Quick Start

```
# Repeat a pattern
$S -> (60 62 64 65 *8)

# Random choice
$S -> [60|62|64]

# Combined: random choice repeated
$S -> ([60|62|64] 65 *4)

# Multiple brackets with repeat
$S -> ([60|62] [64|65] *8)

# Repeat alternatives
$S -> [(60 62 *4) | (64 65 *6)]
```

## Table of Contents
- [Repeat Syntax](#repeat-syntax)
- [Bracket Notation](#bracket-notation-alternative-selection)
- [Combining Repeats and Brackets](#combining-repeat-and-bracket-notation)
- [Examples Gallery](#examples-gallery)
- [Common Patterns](#common-patterns)
- [Usage in the GUI](#usage-in-the-gui)
- [Quick Reference](#quick-reference)
- [Technical Details](#technical-details)

## Repeat Syntax

### Basic Syntax
```
(items *N)
```
Where:
- `items` is a space-separated list of values (pitches, durations, velocities, or IOI values)
- `*N` indicates the number of times to repeat the pattern
- The `*N` must be inside the parentheses, at the end

## Bracket Notation (Alternative Selection)

### Basic Syntax
```
[option1|option2|option3]
```
Where:
- Options are separated by `|` (pipe character)
- One option is randomly selected each time the grammar is generated
- Can contain single values or multiple values: `[60|62 64|65 67 69]`

### Bracket Examples

**Simple choice:**
```
$S -> [60|62|64]
```
Result: Randomly selects one of 60, 62, or 64

**Multiple values per option:**
```
$S -> [60 62|64 65|67 69]
```
Result: Randomly selects one group (either "60 62", "64 65", or "67 69")

**With non-terminals:**
```
$S -> [$MAJOR|$MINOR]
$MAJOR -> 60 64 67
$MINOR -> 60 63 67
```
Result: Randomly expands to either major or minor chord

## Examples Gallery

### Basic Examples

**Pitch pattern repeat:**
```
$S -> (60 62 64 65 *4)
```
Result: `60 62 64 65 60 62 64 65 60 62 64 65 60 62 64 65` (16 values)

**IOI/rhythm pattern repeat:**
```
$S -> (0.25 0.125 0.125 0.25 *8)
```
Result: The 4-value pattern repeated 8 times (32 values total)

**Single value repeat:**
```
$S -> (60 *10)
```
Result: `60 60 60 60 60 60 60 60 60 60`

**Multiple repeats in one rule:**
```
$S -> (60 62 *2) (64 65 *3) (67 *4)
```
Result: `60 62 60 62 64 65 64 65 64 65 67 67 67 67`

### Bracket Examples

**Simple random choice:**
```
$S -> [60|62|64]
```
Result: One of `60`, `62`, or `64` (randomly selected)

**Multiple brackets:**
```
$S -> [60|62] [64|65] [67|69]
```
Result: Three random selections, e.g., `60 65 69`

**Grouped alternatives:**
```
$S -> [60 62 64|65 67 69|70 72 74]
```
Result: One complete group randomly selected

### Combined Examples

**Brackets inside repeats:**
```
$S -> ([60|62|64] 65 *4)
```
Result: Random pitch (e.g., `62`) then `65`, repeated 4 times: `62 65 62 65 62 65 62 65`

**Multiple brackets in repeat:**
```
$S -> ([60|62] [64|65] *3)
```
Result: Two random choices repeated together: `60 65 60 65 60 65`

**Repeats as alternatives:**
```
$S -> [(60 62 *2) | (64 65 *3)]
```
Result: Either `60 62 60 62` OR `64 65 64 65 64 65`

**Complex combination:**
```
$S -> ([60|62|64] *2) ([65|67] *3)
```
Result: `64 64 65 65 65` (example with random selections)

### Grammar Expansion Examples

**With non-terminals and repeat:**
```
$S -> ($PATTERN *6)
$PATTERN -> 64 66 65 67
```
Result: `64 66 65 67 64 66 65 67 ...` (6 times)

**With non-terminals and brackets:**
```
$S -> ([$MAJOR|$MINOR] *4)
$MAJOR -> 60 64 67
$MINOR -> 60 63 67
```
Result: Either major or minor chord repeated 4 times

**Complex musical structure:**
```
$S -> ($INTRO *2) ($VERSE *4) ($CHORUS *2)
$INTRO -> 60 62 64
$VERSE -> [60|62] 64 65
$CHORUS -> 67 69 71 72
```
Result: Complete song structure with variations

## Combining Repeat and Bracket Notation

The two features work seamlessly together, opening up powerful possibilities for musical variation.

### Brackets Inside Repeats

**Basic combination:**
```
$S -> ([60|62|64] 65 *4)
```
- First, randomly chooses one value from `[60|62|64]`
- Then repeats that choice + 65, four times
- Example output: `62 65 62 65 62 65 62 65`

**Multiple brackets:**
```
$S -> ([60|62] [64|65] *3)
```
- Randomly chooses from each bracket
- Repeats both choices together 3 times
- Example output: `60 65 60 65 60 65`

### Repeats Inside Brackets

**Different repeat patterns as alternatives:**
```
$S -> [(60 62 *2) | (64 65 *3)]
```
- Randomly chooses between two different repeat patterns
- Output is either `60 62 60 62` OR `64 65 64 65 64 65`

**Varying repeat counts:**
```
$S -> [(60 *4) | (62 *6) | (64 *8)]
```
- Selects one pitch and repeats it different amounts

### Complex Combinations

**Multiple groups:**
```
$S -> ([60|62|64] *2) ([65|67] *3)
```
- First group: random choice repeated 2 times
- Second group: random choice repeated 3 times
- Example: `64 64 65 65 65`

**With grammar expansion:**
```
$S -> ([$CHORD1|$CHORD2] *4)
$CHORD1 -> 60 64 67
$CHORD2 -> 62 65 69
```
- Randomly selects a chord, then repeats it 4 times

**Rhythmic variation:**
```
$S -> ([0.25|0.5] 0.125 *8)
```
- Randomly chooses quarter or half note
- Alternates with eighth note, repeated 8 times
- Creates swing or straight rhythm patterns

### Musical Applications

**1. Melodic variation with consistent structure:**
```
$PITCH -> ([60|62|64] 65 67 [69|71] *4)
```
Creates a 4-note pattern with varied endpoints, repeated 4 times.

**2. Rhythmic groove with accents:**
```
$VELOCITY -> ([100|80] 70 70 80 *8)
$IOI -> (0.25 *32)
```
Accent pattern with random strong/medium attack on beat 1.

**3. Chord progression variations:**
```
$S -> ([$I|$Isus4] $IV $V $IV *2) $I
$I -> 60 64 67
$Isus4 -> 60 65 67
$IV -> 65 69 72
$V -> 67 71 74
```
Randomly varies the tonic chord while maintaining progression structure.

**4. Ostinato with variation:**
```
$PITCH -> ([48|50] 55 [52|53] 55 *16)
$IOI -> (0.5 *64)
```
Repeating bass line with subtle pitch variations.

**5. Call and response pattern:**
```
$S -> ([$CALL|$CALL2] $RESPONSE *4)
$CALL -> 60 64 67
$CALL2 -> 62 65 69
$RESPONSE -> 72 67 64 60
```
Varied "call" phrases with consistent "response".

## Processing Order

Understanding how the features are processed helps create effective grammars:

1. **Grammar Rules Expansion** - Non-terminals (like `$S`, `$NOTE`) are expanded first
2. **Bracket Selection** - Random choices from `[a|b|c]` are made
3. **Repeat Expansion** - Patterns with `*N` are repeated last

This order means:
- Brackets inside repeats: Choice is made once, then the chosen value is repeated
- Non-terminals are fully expanded before repeats are processed
- Nested structures work from inside out

## Use Cases

### 1. Creating Rhythmic Patterns
```
$IOI -> (0.25 0.125 0.125 0.5 *16)
```
Creates a 16-bar rhythmic pattern with a consistent groove.

### 2. Building Scales and Arpeggios
```
$PITCH -> (60 62 64 65 67 69 71 72 *4)
```
Repeats a C major scale 4 times for extended melodic material.

### 3. Velocity Patterns
```
$VELOCITY -> (80 90 100 90 *8)
```
Creates a crescendo-decrescendo pattern repeated 8 times.

### 4. Ostinato Patterns
```
$PITCH -> (48 55 52 55 *32)
$IOI -> (0.5 *128)
```
Creates a repeating bass line pattern.

## Usage in the GUI

1. Open the **List Generator** tab
2. Select the parameter type (Pitch, Duration, Velocity, or IOI)
3. Enter a grammar using repeat and/or bracket syntax:
   - Simple repeat: `$S -> (64 66 65 67 *8)`
   - With brackets: `$S -> ([60|62|64] 65 *4)`
   - Complex: `$S -> ([$MAJOR|$MINOR] *4)` with additional rules
4. Click the generate button
5. The pattern will be automatically expanded and can be used to create bars/songs

## Quick Reference

### Repeat Syntax
- `(60 62 64 *4)` - Repeat sequence 4 times
- `(60 *10)` - Repeat single value 10 times
- `((60 62 *2) 64 *3)` - Nested repeats

### Bracket Syntax
- `[60|62|64]` - Choose one value randomly
- `[60 62|64 65]` - Choose one group randomly
- `[$NOTE1|$NOTE2]` - Choose between non-terminals

### Combined Syntax
- `([60|62] 64 *4)` - Random choice, then repeat
- `[(60 *2) | (62 *3)]` - Choose between repeat patterns
- `([60|62] [64|65] *4)` - Multiple random choices repeated together
- `([$CHORD|$SCALE] *8)` - Grammar expansion with repeat

## Technical Details

### Repeat Expansion
- Handled by the `expand_repeats()` function in `gengramparser2.py`
- Expansion happens after all grammar rules are processed
- The `*N` must come at the end of the parenthetical expression
- Whitespace around `*N` is handled automatically
- Works with integers, floats, and any space-separated tokens
- Supports nested repeats (processed inside-out)

### Bracket Expansion
- Handled by the `expand_brackets()` function in `gengramparser2.py`
- Expansion happens during grammar rule generation
- Uses random.choice() to select from alternatives
- Nested brackets are supported
- Can split on `|` while respecting nested structures

### Processing Order
1. Grammar rules are expanded (non-terminals replaced)
2. Brackets are evaluated (random choices made)
3. Repeats are expanded (patterns duplicated)

This ensures that:
- Random choices in brackets are made before repeating
- Non-terminals are fully resolved
- The final output is fully expanded and ready to use

## Implementation Details

### Repeat Syntax Implementation
The `expand_repeats()` function:
1. Searches for parenthesized expressions ending with `*N`
2. Extracts the content before `*N` and the repeat count
3. Repeats the content the specified number of times
4. Handles nested repeats recursively
5. Integrates seamlessly with existing bracket and grammar features

### Bracket Syntax Implementation
The `expand_brackets()` function:
1. Finds bracketed expressions `[...]`
2. Splits content by `|` while respecting nested structures
3. Randomly selects one alternative using `random.choice()`
4. Processes nested brackets from inside out
5. Works before repeat expansion to allow repeating random choices

## Benefits

1. **Conciseness**: Write `(60 62 64 *10)` instead of listing 30 values
2. **Readability**: Easier to see the pattern structure
3. **Flexibility**: Combine with existing grammar features (brackets, non-terminals)
4. **Variation**: Use brackets to create varied but structured patterns
5. **Efficiency**: Generate long sequences quickly
6. **Maintainability**: Change the pattern in one place, affects all repeats
7. **Musical Expression**: Create repetition with variation - fundamental to music

## Common Patterns

### Scales and Arpeggios
```
$SCALE -> (60 62 64 65 67 69 71 72 *4)     # C major scale, 4 octaves
$ARP -> ([60 64 67|60 63 67] *8)           # Major/minor arpeggios alternating
```

### Rhythmic Grooves
```
$IOI -> (0.25 0.25 0.5 *8)                 # Simple 4/4 pattern
$IOI -> ([0.25|0.5] 0.125 0.125 *16)       # Swing variation
```

### Ostinato Patterns
```
$PITCH -> ([48|50|52] 55 52 55 *16)        # Bass ostinato with variation
$DUR -> (0.4 *64)                          # Consistent duration
```

### Chord Progressions
```
$S -> ([$I|$Isus] $V $IV $V *2) $I
$I -> 60 64 67
$Isus -> 60 65 67
$V -> 67 71 74
$IV -> 65 69 72
```

### Dynamic Contours
```
$VEL -> (60 70 80 90 *4) (90 80 70 60 *4)  # Crescendo-decrescendo
$VEL -> ([80|90|100] 70 70 80 *8)          # Accent pattern with variation
```

## Implementation

The repeat expansion is handled by the `expand_repeats()` function in `gengramparser2.py`, which:
1. Searches for parenthesized expressions ending with `*N`
2. Extracts the content before `*N` and the repeat count
3. Repeats the content the specified number of times
4. Handles nested repeats recursively
5. Integrates seamlessly with existing bracket `[a|b|c]` and grammar expansion features
