# Grammar Validation System

## Overview

The grammar validation system provides comprehensive validation for generative grammars used in savellysKone. It follows a BNF-like (Backus-Naur Form) standard with custom extensions.

## Grammar Format Standard

### Syntax Rules

1. **Non-terminals**: Must start with `$` followed by a valid identifier
   - Format: `$[a-zA-Z_][a-zA-Z0-9_]*`
   - Examples: `$S`, `$phrase01`, `$note_C`

2. **Productions**: Use `->` to separate left-hand side from right-hand side
   - Format: `$LHS -> RHS`
   - Example: `$S -> $phrase01 $phrase02`

3. **Alternatives**: Use `|` to separate alternative productions
   - Format: `$LHS -> alt1 | alt2 | alt3`
   - Example: `$note -> 60 | 62 | 64`

4. **Terminals**: Any symbol not starting with `$`
   - Examples: `60`, `1.0`, `100`

5. **Comments**: Lines starting with `#` are ignored

### Example Valid Grammar

```
# Pitch grammar for C major scale
$S -> $phrase01 $phrase02
$phrase01 -> $note01 $note02 $note03 $note04
$phrase02 -> $note05 $note06 $note07 $note08
$note01 -> 60
$note02 -> 62
$note03 -> 64
$note04 -> 65
$note05 -> 67
$note06 -> 69
$note07 -> 71
$note08 -> 72
```

## Validation Checks

### Syntax Validation

- **Missing separator**: Each production must have exactly one `->`
- **Invalid non-terminal names**: Non-terminals must follow identifier rules
- **Empty productions**: Productions cannot be empty
- **Malformed rules**: LHS must be a single non-terminal

### Semantic Validation

1. **Start Symbol**: Grammar must define `$S` (the start symbol)
2. **Undefined Non-terminals**: All non-terminals used must be defined
3. **Direct Left Recursion**: Detects rules like `$A -> $A ...` which cause infinite loops
4. **Reachability**: Warns about non-terminals unreachable from `$S`
5. **Productivity**: Warns about non-terminals that cannot derive terminal strings
6. **Indirect Recursion**: Detects potential cycles in the grammar

## Using the Validator

### In the GUI

1. Enter your grammar in any of the three grammar text boxes (Pitch, Duration, or Velocity)
2. Click the "Validate Grammar" button below the text box
3. Review the validation results:
   - ✓ Success message shows grammar statistics
   - ✗ Error messages explain what needs to be fixed
   - ⚠ Warning messages suggest potential improvements

### Programmatically

```python
from grammar_validator import validate_grammar

grammar_text = """
$S -> $phrase01 $phrase02
$phrase01 -> 60 62 64
$phrase02 -> 67 69 71
"""

is_valid, message = validate_grammar(grammar_text)
print(message)
```

## Common Errors and Solutions

### Error: "Direct left recursion"

**Problem**: A non-terminal appears as the first symbol in its own production
```
$S -> $S 60  # WRONG: infinite recursion
```

**Solution**: Rewrite the grammar to avoid left recursion
```
$S -> 60 $S_tail
$S_tail -> 60 $S_tail | 62
```

### Error: "Undefined non-terminal"

**Problem**: A non-terminal is used but not defined
```
$S -> $phrase01
# $phrase01 is not defined
```

**Solution**: Define all non-terminals you use
```
$S -> $phrase01
$phrase01 -> 60 62 64
```

### Error: "Missing start symbol '$S'"

**Problem**: No rule defines `$S`
```
$phrase -> 60 62
```

**Solution**: Always define `$S` as your grammar's entry point
```
$S -> $phrase
$phrase -> 60 62
```

### Warning: "Non-terminal is unreachable"

**Problem**: A non-terminal cannot be reached from `$S`
```
$S -> $phrase01
$phrase01 -> 60 62
$phrase02 -> 64 65  # Unreachable!
```

**Solution**: Either use the non-terminal or remove it
```
$S -> $phrase01 $phrase02
$phrase01 -> 60 62
$phrase02 -> 64 65
```

## Grammar Best Practices

1. **Start with $S**: Always use `$S` as your top-level non-terminal
2. **Clear naming**: Use descriptive names like `$phrase`, `$note`, `$duration`
3. **Avoid deep nesting**: Keep grammar relatively flat for better readability
4. **Use alternatives**: Leverage `|` for variations instead of multiple rules
5. **Test incrementally**: Validate your grammar as you build it
6. **Document complex rules**: Use comments to explain non-obvious patterns

## Technical Details

### Validation Algorithm

1. **Parse Phase**: 
   - Tokenize each line
   - Extract LHS and RHS
   - Check syntax rules
   - Build internal representation

2. **Semantic Phase**:
   - Verify start symbol exists
   - Check all non-terminals are defined
   - Detect direct left recursion
   - Compute reachable set from `$S`
   - Compute productive set
   - Detect cycles (indirect recursion)

3. **Report Phase**:
   - Format errors with line numbers
   - Provide actionable suggestions
   - Include grammar statistics

### Comparison to Standards

| Feature | BNF | EBNF | savellysKone |
|---------|-----|------|--------------|
| Non-terminal marker | `<>` | `<>` or plain | `$` prefix |
| Alternative separator | `\|` | `\|` | `\|` |
| Production operator | `::=` | `=` or `::=` | `->` |
| Repetition | Multiple rules | `{}` or `[]` | Multiple rules |
| Optional | Multiple rules | `[]` | `\|` with empty |
| Comments | N/A | `(*  *)` | `#` |

### Future Enhancements

Possible future additions to the validation system:

- **EBNF syntax support**: Add `[]` for optional, `{}` for repetition
- **Ambiguity detection**: Warn about potentially ambiguous grammars
- **Grammar optimization**: Suggest simplifications
- **Export formats**: Generate grammars in standard formats (BNF, EBNF, ABNF)
- **Interactive repair**: Suggest fixes for common errors
- **Grammar metrics**: Complexity analysis, coverage estimation

## References

- **Backus-Naur Form (BNF)**: [Wikipedia](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)
- **Extended BNF (EBNF)**: [ISO/IEC 14977](https://www.iso.org/standard/26153.html)
- **Context-Free Grammars**: [Theory of Computation](https://en.wikipedia.org/wiki/Context-free_grammar)
- **Left Recursion Elimination**: [Compilers: Principles, Techniques, and Tools](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
