# Grammar Guide for savellysKone3

## Table of Contents
- [Introduction](#introduction)
- [Basic Grammar Syntax](#basic-grammar-syntax)
- [Non-Terminals](#non-terminals)
- [Repeat Syntax](#repeat-syntax)
- [Bracket Notation](#bracket-notation-random-alternatives)
- [Combining Features](#combining-features)
- [Musical Parameters](#musical-parameters)
- [Complete Examples](#complete-examples)
- [Tips and Best Practices](#tips-and-best-practices)
- [Troubleshooting](#troubleshooting)

## Introduction

savellysKone3 uses **context-free grammars** to generate musical parameters (pitch, duration, velocity, IOI). Grammars provide a powerful, flexible way to create structured yet varied musical patterns.

### What are Grammars?

Grammars consist of **rules** that define how to expand **non-terminals** (symbols starting with `$`) into **terminals** (actual values like pitches or durations).

### Why Use Grammars?

- **Structured Variation**: Create patterns with controlled randomness
- **Hierarchical Organization**: Build complex patterns from simple building blocks
- **Reusability**: Define patterns once, use them multiple times
- **Expressiveness**: Combine repetition, variation, and structure naturally

## Basic Grammar Syntax

### Grammar Rules

A grammar rule has the form:
```
$NonTerminal -> expansion
```

**Example:**
```
$S -> 60 62 64 65
```

This rule says: "When you see `$S`, replace it with `60 62 64 65`"

### Starting Symbol

By convention, `$S` is the **start symbol** - the root of your grammar.

```
$S -> 60 62 64
```

When you generate from this grammar, it produces: `60 62 64`

### Multiple Rules

You can have multiple rules for the same non-terminal. One will be chosen randomly:

```
$S -> 60 62 64
$S -> 65 67 69
```

Each time you generate, it randomly picks one rule. Result is either `60 62 64` OR `65 67 69`.

### Alternative Notation

Instead of multiple rules, you can use `|` to separate alternatives on one line:

```
$S -> 60 62 64 | 65 67 69
```

This is equivalent to having two separate rules.

## Non-Terminals

### Defining Non-Terminals

Non-terminals are symbols that start with `$`. They act as placeholders that get expanded into other symbols.

```
$S -> $INTRO $VERSE
$INTRO -> 60 62
$VERSE -> 64 65 67
```

Result: `60 62 64 65 67`

### Recursive Rules

Non-terminals can reference themselves (recursion), but **only on the right side** to avoid infinite left recursion:

```
$S -> 60 $S    # ✗ Left recursion - NOT ALLOWED
$S -> $S 60    # ✓ Right recursion - OK
```

**Valid recursive example:**
```
$S -> 60 $REST | 60
$REST -> 62 $REST | 62
```

This can generate sequences like: `60 62 62` or `60 62 62 62 62` (length varies)

### Naming Conventions

- Start with `$` followed by uppercase letters
- Use descriptive names: `$PITCH`, `$CHORUS`, `$SCALE`, `$CHORD1`
- Common names: `$S` (start), `$NOTE`, `$PATTERN`, `$INTRO`, `$VERSE`

## Repeat Syntax

### Basic Repeat

Repeat a pattern N times using parentheses and `*N`:

```
(items *N)
```

**Examples:**
```
$S -> (60 62 64 *4)
```
Result: `60 62 64 60 62 64 60 62 64 60 62 64` (pattern repeated 4 times)

```
$S -> (60 *10)
```
Result: `60 60 60 60 60 60 60 60 60 60`

### Multiple Repeats

You can use multiple repeat groups in one rule:

```
$S -> (60 62 *2) (64 65 *3)
```
Result: `60 62 60 62 64 65 64 65 64 65`

### Nested Repeats

Repeats can be nested:

```
$S -> ((60 62 *2) 64 *3)
```
First expands inner: `(60 62 60 62 64 *3)`
Then outer: `60 62 60 62 64 60 62 60 62 64 60 62 60 62 64`

### Repeats with Non-Terminals

Combine repeats with grammar expansion:

```
$S -> ($PATTERN *8)
$PATTERN -> 60 62 64 65
```
Result: The pattern expanded 8 times

## Bracket Notation (Random Alternatives)

### Basic Brackets

Choose randomly from alternatives using brackets and `|`:

```
[option1|option2|option3]
```

**Example:**
```
$S -> [60|62|64]
```
Result: One of `60`, `62`, or `64` (randomly selected each time)

### Multiple Brackets

Use multiple brackets for independent random choices:

```
$S -> [60|62] [64|65] [67|69]
```
Result: Three random selections, e.g., `62 64 69` or `60 65 67`

### Multi-Value Options

Each bracket alternative can contain multiple values:

```
$S -> [60 62|64 65|67 69]
```
Result: One complete group, e.g., `60 62` OR `64 65` OR `67 69`

### Brackets with Non-Terminals

Brackets can contain non-terminals:

```
$S -> [$MAJOR|$MINOR]
$MAJOR -> 60 64 67
$MINOR -> 60 63 67
```
Result: Expands to either major or minor chord

## Combining Features

The real power comes from combining grammars, repeats, and brackets together.

### Brackets Inside Repeats

Random choice made once, then the result is repeated:

```
$S -> ([60|62|64] 65 *4)
```
- First: randomly choose from `[60|62|64]`, say `62`
- Then: repeat `62 65` four times
- Result: `62 65 62 65 62 65 62 65`

### Multiple Brackets in Repeats

Multiple independent choices, all repeated together:

```
$S -> ([60|62] [64|65] *3)
```
- First: choose from each bracket, say `60` and `65`
- Then: repeat `60 65` three times
- Result: `60 65 60 65 60 65`

### Repeats as Bracket Alternatives

Choose between different repeat patterns:

```
$S -> [(60 62 *2) | (64 65 *3)]
```
Result: Either `60 62 60 62` OR `64 65 64 65 64 65`

### Complex Combinations

```
$S -> ([$CHORD1|$CHORD2] *4) $ENDING
$CHORD1 -> 60 64 67
$CHORD2 -> 62 65 69
$ENDING -> 72
```
- Randomly selects a chord
- Repeats it 4 times
- Adds ending note
- Result example: `60 64 67 60 64 67 60 64 67 60 64 67 72`

### Processing Order

Understanding the order helps create effective grammars:

1. **Grammar Expansion** - Non-terminals like `$S`, `$PATTERN` are expanded
2. **Bracket Selection** - Random choices from `[a|b|c]` are made
3. **Repeat Expansion** - Patterns with `*N` are repeated

This means:
- Brackets inside repeats: Choice made once, then repeated
- Non-terminals expanded before brackets evaluated
- Repeats happen last, after everything else is resolved

## Musical Parameters

### Pitch

Pitch values are MIDI note numbers (0-127):

```
$S -> 60 62 64 65 67    # C major scale (middle C = 60)
$S -> 48 50 52          # Lower bass notes
```

**Common MIDI notes:**
- Middle C (C4): 60
- A440: 69
- One octave = 12 semitones

**Example grammars:**
```
# Random melody
$S -> [60|62|64|65|67] [64|65|67|69] [67|69|71|72]

# Scale pattern
$S -> (60 62 64 65 67 69 71 72 *4)

# Chord progression
$S -> ($Cmaj *2) ($Fmaj *2) ($Gmaj *2) ($Cmaj *1)
$Cmaj -> 60 64 67
$Fmaj -> 65 69 72
$Gmaj -> 67 71 74
```

### Duration

Duration in seconds (floating point):

```
$S -> 0.5 0.25 0.25 0.5    # Quarter, eighth, eighth, quarter
```

**Common durations (at 120 BPM):**
- Whole note: 2.0
- Half note: 1.0
- Quarter note: 0.5
- Eighth note: 0.25
- Sixteenth note: 0.125

**Example grammars:**
```
# Consistent quarter notes
$S -> (0.5 *32)

# Rhythmic pattern
$S -> (0.5 0.25 0.25 *8)

# Random durations
$S -> [0.5|0.25|0.125] [0.5|0.25|0.125] [0.5|0.25]
```

### Velocity

Velocity is note intensity (0-127):
- 0 = silent
- 64 = medium
- 127 = maximum

```
$S -> 80 90 100 90    # Crescendo then decrescendo
```

**Typical ranges:**
- pp (pianissimo): 20-35
- mp (mezzo-piano): 40-55
- mf (mezzo-forte): 60-75
- ff (fortissimo): 96-127

**Example grammars:**
```
# Accent pattern
$S -> ([100|80] 70 70 80 *8)

# Dynamic curve
$S -> (60 70 80 90 100 *2) (100 90 80 70 60 *2)

# Random dynamics
$S -> [60|70|80|90|100]
```

### IOI (Inter-Onset Interval)

IOI is the time between note onsets (in seconds). Controls rhythm independently from duration.

```
$S -> 0.5 0.5 0.25 0.25    # Quarter, quarter, eighth, eighth spacing
```

**Key difference from duration:**
- Duration = how long a note sounds
- IOI = when the next note starts

**Example grammars:**
```
# Steady eighth notes
$S -> (0.25 *32)

# Swing rhythm
$S -> ([0.33|0.25] 0.17 *16)

# Varied rhythm
$S -> (0.5 0.25 0.125 0.125 *8)

# Polyrhythm
$S -> [0.33|0.5|0.25]
```

## Complete Examples

### Example 1: Simple Melody

```
$S -> (60 62 64 65 *2) (67 65 64 62 *2) 60
```
- Ascending pattern twice
- Descending pattern twice  
- Ends on root

### Example 2: Bassline with Variation

```
$S -> ([48|50] 55 [52|53] 55 *16)
$DURATION -> (0.4 *64)
$VELOCITY -> (80 *64)
```
- Bass note varies between 48 and 50
- Third note varies between 52 and 53
- Pattern repeats 16 times
- Consistent duration and velocity

### Example 3: Chord Progression

```
# Pitch
$S -> ($I *4) ($IV *4) ($V *4) ($I *2)
$I -> 60 64 67
$IV -> 65 69 72
$V -> 67 71 74

# Duration
$DUR -> (1.0 *14)

# Velocity
$VEL -> (80 *42)
```
- I-IV-V-I progression
- Each chord is 3 notes
- Whole note durations
- Consistent velocity

### Example 4: Rhythmic Pattern with Accents

```
# Pitch (repeated note)
$PITCH -> (60 *32)

# IOI (steady eighth notes)
$IOI -> (0.25 *32)

# Duration (staccato)
$DUR -> (0.1 *32)

# Velocity (accent on beats 1 and 3)
$VEL -> (100 70 70 70 90 70 70 70 *4)
```
- Single pitch (60)
- Steady rhythm
- Short notes (staccato)
- Accented pattern creates groove

### Example 5: Generative Melody

```
$S -> $INTRO $VERSE $VERSE $CHORUS $VERSE $OUTRO

$INTRO -> ([$LOW|$MID] *2)
$VERSE -> ([$MOTIF1|$MOTIF2] *4)
$CHORUS -> ($HIGH *4)
$OUTRO -> ($LOW *2) 60

$LOW -> [48|50|52]
$MID -> [60|62|64]
$HIGH -> [72|74|76]
$MOTIF1 -> 60 62 64 65
$MOTIF2 -> 60 64 67 65
```
- Song structure: Intro-Verse-Verse-Chorus-Verse-Outro
- Each section uses different pitch material
- Motifs provide variation in verses
- Random elements create unique results each time

### Example 6: Polyrhythmic Pattern

```
# Voice 1: Pitch
$PITCH1 -> (60 64 67 *16)
$IOI1 -> (0.5 *48)
$DUR1 -> (0.4 *48)

# Voice 2: Pitch (separate pattern)
$PITCH2 -> (72 76 79 *21)
$IOI2 -> (0.375 *63)
$DUR2 -> (0.3 *63)
```
- Two independent rhythmic layers
- Voice 1: triplet feel (0.5s)
- Voice 2: different subdivision (0.375s)
- Create as separate songs/tracks

### Example 7: Call and Response

```
$S -> ($CALL $RESPONSE *4) $CALL

$CALL -> [$CALL1|$CALL2|$CALL3]
$RESPONSE -> 72 71 69 67 65 64 62 60

$CALL1 -> 60 64 67 72
$CALL2 -> 60 65 69 72
$CALL3 -> 60 62 65 69

$DUR -> (0.25 *36)
$VEL -> (90 *36)
```
- Varied "call" phrases
- Consistent "response" phrase
- Pattern repeats 4 times
- Ends with final call

## Tips and Best Practices

### Start Simple

Begin with basic patterns and add complexity gradually:

```
# Start here
$S -> 60 62 64

# Then add variation
$S -> [60|62] [62|64] [64|65]

# Then add repetition
$S -> ([60|62] [62|64] [64|65] *4)

# Then add structure
$S -> ($INTRO *2) ($MAIN *4)
$INTRO -> [60|62] [62|64]
$MAIN -> [64|65] [65|67]
```

### Test Incrementally

Generate and listen after each change to ensure it sounds as expected.

### Use Descriptive Names

```
# Good
$VERSE -> ...
$CHORUS -> ...
$Cmaj -> 60 64 67

# Less clear
$A -> ...
$B -> ...
$X -> 60 64 67
```

### Balance Randomness and Structure

Too much randomness = chaos
Too much structure = boring

```
# Good balance
$S -> ($STABLE *2) ($VARIED *2)
$STABLE -> 60 62 64
$VARIED -> [60|62|64] [65|67]
```

### Consider Parameter Relationships

Pitch, duration, velocity, and IOI interact:

```
# High notes softer, low notes louder
$PITCH -> [72|74|76]
$VEL -> [60|70|80]

# vs

$PITCH -> [48|50|52]
$VEL -> [90|100|110]
```

### Mind the Length

Ensure lists have compatible lengths or use Generate Every Bar (GEB):

```
# OK - same length
$PITCH -> (60 62 64 65 *4)    # 16 notes
$DUR -> (0.5 *16)              # 16 durations

# OK - circular buffer will wrap
$PITCH -> (60 62 64 65 *4)    # 16 notes
$DUR -> (0.5 0.25 *8)          # 16 durations

# Problematic - very different lengths
$PITCH -> (60 62 64 65 *100)  # 400 notes
$DUR -> (0.5 *5)               # 5 durations (will wrap, maybe not intended)
```

### Use Comments

Comments help remember your intent:

```
# Verse section - mysterious feel
$VERSE -> ([60|62] 63 *4)

# Chorus - bright and energetic
$CHORUS -> (72 74 76 77 *4)
```

Note: The grammar parser doesn't actually support `#` comments in the grammar itself, but you can keep notes separately or in variable names.

## Troubleshooting

### Grammar Won't Generate

**Problem**: Getting `$S` as output instead of expanded values

**Solution**: Make sure depth is high enough (try 10 or higher)

```python
result = ggp.generate(grammar, "$S", 10)  # Not 0
```

### Left Recursion Error

**Problem**: Error says "Direct left recursion detected"

```
$S -> $S 60    # ✗ Not allowed
```

**Solution**: Use right recursion instead:

```
$S -> 60 $S    # ✓ OK
$S -> 60       # ✓ Base case
```

### Unexpanded Non-Terminals

**Problem**: Output contains `$PATTERN` or other non-terminals

**Solution**: 
1. Check that all non-terminals are defined
2. Increase generation depth
3. Check for typos in non-terminal names

```
$S -> $PATERN    # ✗ Typo
$PATTERN -> 60   # Defined but name doesn't match
```

### Pattern Not Repeating

**Problem**: Using `*N` but pattern not repeating

**Solution**: Make sure `*N` is inside the parentheses at the end:

```
(60 62 *4)    # ✓ Correct
60 62 *4      # ✗ Won't work
(60 62) *4    # ✗ Won't work
```

### Brackets Not Working

**Problem**: Getting literal `[60|62]` in output

**Solution**: Ensure:
1. Using `|` (pipe) not other characters
2. Brackets are properly matched
3. No spaces around `|` inside brackets (or consistent spacing)

### Lists Different Lengths

**Problem**: Pitch has 100 notes but duration has 10

**Solution**:
- Use circular buffer mode (lists wrap)
- Make lists same length
- Or use Generate Every Bar (GEB) mode

### Too Much Repetition

**Problem**: Pattern repeats too many times

**Solution**: Reduce the `*N` value or use brackets for variation:

```
# Instead of
$S -> (60 62 64 *100)

# Try
$S -> ([60|62|64] [62|64|65] *50)
```

### Not Enough Variation

**Problem**: Pattern too predictable

**Solution**: Add more brackets and alternatives:

```
# Add variation
$S -> ([$MOTIF1|$MOTIF2|$MOTIF3] *8)
$MOTIF1 -> 60 62 64
$MOTIF2 -> 60 64 67
$MOTIF3 -> 60 65 69
```

## Advanced Topics

### Generate Every Bar (GEB)

In the GUI, you can enable GEB mode, which generates new values for each bar from the grammar. This creates continuous variation.

**Without GEB**: Grammar generates once, values used for all bars
**With GEB**: Grammar generates separately for each bar

### Combining Multiple Parameters

Create coherent musical material by coordinating grammars across parameters:

```
# All parameters use related structure
$PITCH_S -> ($INTRO *2) ($MAIN *4)
$DUR_S -> (0.5 *18)
$VEL_S -> ([$SOFT|$LOUD] *3)

$INTRO -> 60 62
$MAIN -> [64|65] [67|69]
$SOFT -> 60 60 70
$LOUD -> 90 90 100
```

### Markov-Like Behavior

Use non-terminals to create state-like transitions:

```
$S -> $STATE1
$STATE1 -> 60 $STATE2 | 60 $STATE1
$STATE2 -> 64 $STATE3 | 64 $STATE1  
$STATE3 -> 67 $STATE1 | 67 $STATE2
```

This creates patterns where the "next note" depends on the "current state."

### Limiting Recursion

Control pattern length by having base cases:

```
$S -> 60 $REST | 60
$REST -> 62 $REST | 62 $REST | 62

# This will generate 2-4 values typically
```

## Summary

### Key Concepts

- **Non-terminals** (`$NAME`): Placeholders that get expanded
- **Terminals**: Actual values (pitches, durations, etc.)
- **Rules**: Define how to expand non-terminals
- **Alternatives**: Use `|` or multiple rules
- **Repeats**: `(pattern *N)` repeats pattern N times
- **Brackets**: `[a|b|c]` randomly chooses one option

### Syntax Summary

```
# Basic rule
$S -> 60 62 64

# Multiple rules (alternatives)
$S -> 60 62
$S -> 64 65

# Alternatives on one line
$S -> 60 62 | 64 65

# Non-terminal expansion
$S -> $INTRO $VERSE
$INTRO -> 60 62
$VERSE -> 64 65 67

# Repeats
$S -> (60 62 64 *8)
$S -> ((60 *2) 64 *4)

# Brackets
$S -> [60|62|64]
$S -> [60 62|64 65]
$S -> [$A|$B]

# Combined
$S -> ([60|62|64] 65 *4)
$S -> ([$CHORD1|$CHORD2] *8)
```

### Next Steps

1. Start with simple pitch patterns
2. Add brackets for variation
3. Use repeats for structure
4. Combine parameters (pitch, duration, velocity, IOI)
5. Create song structures with non-terminals
6. Experiment with GEB mode for continuous variation

Happy composing! 🎵
