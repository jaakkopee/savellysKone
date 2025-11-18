# Bracket Notation in gengramparser2

## Overview

gengramparser2 now supports bracket notation `[ ]` as scope definers for inline alternatives within grammar rules. This allows you to create more compact and expressive grammars.

## Syntax

Brackets `[ ]` enclose alternatives separated by `|`:

```
[option1 | option2 | option3]
```

When the grammar is expanded, one option is randomly chosen from the bracketed alternatives.

## Features

### 1. Simple Alternatives

Instead of writing multiple rules:
```
$phrase -> $opt1
$phrase -> $opt2
$phrase -> $opt3
$opt1 -> 60
$opt2 -> 62
$opt3 -> 64
```

You can write:
```
$phrase -> [60 | 62 | 64]
```

### 2. Multiple Brackets in Sequence

You can use multiple bracket groups in a single rule:
```
$phrase -> [60 | 62] [64 | 65] [67 | 69]
```

This generates a sequence where each bracket independently chooses one alternative.

### 3. Mixing Brackets with Non-terminals

Brackets can contain non-terminal symbols:
```
$phrase -> [$low | $mid | $high]
$low -> 60
$mid -> 67
$high -> 72
```

### 4. Nested Brackets

Brackets can be nested for complex alternatives:
```
$phrase -> [[60 | 62] | [64 | 65]]
```

This first chooses between `[60 | 62]` OR `[64 | 65]`, then expands the chosen bracket.

### 5. Complex Combinations

Combine brackets with regular grammar elements:
```
$melody -> $note [1.0 | 0.5 | 0.25] $note [1.0 | 0.5] $note [1.0 | 2.0]
$note -> [60 | 62 | 64 | 65 | 67]
```

## Traditional Rule Alternatives vs Brackets

### Traditional `|` (Rule-level alternatives)
```
$phrase -> 60 64 | 62 65 | 64 67
```
This creates **three separate rules** for $phrase. Each expansion chooses one complete alternative.

### Brackets `[ ]` (Inline alternatives)
```
$phrase -> [60 | 62 | 64] [64 | 65 | 67]
```
This is **one rule** with inline choices. Each bracket independently chooses an alternative.

Result:
- Traditional: Always pairs (60 64), (62 65), or (64 67)
- Brackets: Any combination of first bracket (60/62/64) with second bracket (64/65/67)

## Expansion Order

Brackets are expanded **from outermost to innermost**, one level at a time. When a rule is selected:

1. The rule's RHS (right-hand side) is retrieved
2. All bracketed alternatives in that RHS are expanded
3. Each `[ ]` group randomly chooses one alternative
4. Non-terminals (like `$note`) are then expanded in subsequent steps

## Whitespace

Whitespace around alternatives is automatically trimmed:
```
[60 | 62 | 64]     # spaces are OK
[60|62|64]         # no spaces is also OK
[ 60 | 62 | 64 ]   # spaces everywhere is OK
```

## Error Handling

### Unmatched Brackets
```
$phrase -> [60 | 62
```
Error: `Unmatched opening bracket [ in: [60 | 62`

```
$phrase -> 60 | 62]
```
Error: `Unmatched closing bracket ] in: 60 | 62]`

### Nested Unmatched Brackets
The parser tracks bracket depth and reports errors if brackets don't match.

## Examples

### Example 1: Pitch Variations
```
$S -> $melody $melody
$melody -> [60 | 62 | 64 | 65 | 67]
```

### Example 2: Rhythm Patterns
```
$S -> $pattern $pattern
$pattern -> [0.25 | 0.5 | 1.0 | 2.0]
```

### Example 3: Combined Parameters
```
$S -> $note
$note -> [60 | 62 | 64] [0.5 | 1.0] [80 | 100 | 120]
```
Generates: pitch, duration, velocity combinations

### Example 4: Musical Scales
```
$S -> $scale $scale $scale $scale
$scale -> [60 | 62 | 64 | 65 | 67 | 69 | 71 | 72]
```
C major scale

### Example 5: Complex Melody
```
$S -> $phrase $phrase
$phrase -> $note $rhythm $note $rhythm $note $rhythm
$note -> [60 | 62 | 64 | 65 | 67]
$rhythm -> [0.25 | 0.5 | 1.0]
```

## Comparison with Other Features

### Brackets vs Pipe Alternatives

**Pipe `|` at rule level:**
```
$phrase -> 60 62
$phrase -> 64 65
```
Creates multiple rules. Each time $phrase is expanded, one rule is chosen.

**Brackets `[ ]` within rule:**
```
$phrase -> [60 | 64] [62 | 65]
```
Single rule with inline choices. More combinations possible.

### Brackets vs Multiple Non-terminals

**Without brackets:**
```
$phrase -> $note1 $note2
$note1 -> 60 | 62 | 64
$note2 -> 65 | 67 | 69
```

**With brackets:**
```
$phrase -> [60 | 62 | 64] [65 | 67 | 69]
```
More concise, same functionality.

## Best Practices

1. **Use brackets for simple inline choices**: Perfect for values that don't need separate rules
2. **Use traditional rules for complex structures**: When alternatives have different structures
3. **Combine both**: Use brackets within rules that have traditional alternatives
4. **Nest carefully**: Deep nesting can be hard to read - consider splitting into multiple rules

## Limitations

- Brackets work with space-separated tokens
- The `|` separator inside brackets must not be confused with rule-level `|`
- Very deep nesting may reduce readability

## Technical Notes

- Brackets are expanded when a rule is selected (before non-terminal expansion)
- Random choice is made for each bracket group independently
- Expansion happens iteratively from outside to inside
- Parser correctly handles bracket depth when splitting rule alternatives

