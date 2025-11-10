# Recursion Prevention in Grammar Parser

## Summary

Added validation to `gengramparser2.py` to prevent infinite recursion by rejecting grammar rules where a non-terminal symbol appears as the first symbol on the right-hand side of its own rewrite rule.

## Changes Made

### 1. Modified `gengramparser2.py`

**File**: `/Users/jaakkoprattala/Documents/koodii/savellysKone/gengramparser2.py`

**Change**: Updated `parse_grammar()` function to check for direct left recursion.

**Before**:
```python
def parse_grammar(f):
    grammar = Grammar()
    for line in f:
        line = line.strip()
        if line:
            lhs, rhs_alternatives = line.split("->")
            lhs = lhs.strip()
            alternatives = rhs_alternatives.split("|")
            alternatives = [alt.strip() for alt in alternatives]
            for alternative in alternatives:
                grammar.add_rule(GrammarRule(lhs, alternative))
    if DEBUG:
        print(grammar)
    return grammar
```

**After**:
```python
def parse_grammar(f):
    grammar = Grammar()
    for line in f:
        line = line.strip()
        if line:
            lhs, rhs_alternatives = line.split("->")
            lhs = lhs.strip()
            alternatives = rhs_alternatives.split("|")
            alternatives = [alt.strip() for alt in alternatives]
            for alternative in alternatives:
                # Check for direct left recursion: LHS cannot be the first symbol on RHS
                rhs_first_symbol = alternative.split()[0] if alternative.split() else ""
                if rhs_first_symbol == lhs:
                    raise ValueError(f"Infinite recursion detected: '{lhs} -> {alternative}'. "
                                   f"The non-terminal '{lhs}' cannot appear as the first symbol on the right side of its own rule.")
                grammar.add_rule(GrammarRule(lhs, alternative))
    if DEBUG:
        print(grammar)
    return grammar
```

**Also changed**: Set `DEBUG = False` to reduce console output.

### 2. Updated `testRecursionInGrammar.py`

**File**: `/Users/jaakkoprattala/Documents/koodii/savellysKone/testRecursionInGrammar.py`

**Change**: Fixed the pitch grammar which had left recursion.

**Before**:
```python
pitch_grammar = """
$S -> $phrase0
$phrase0 -> $phrase0 | 55 | 66 | 77
"""
```

**After**:
```python
# Updated: This grammar previously had left recursion ($phrase0 -> $phrase0 ...)
# which would cause infinite loops. Changed to valid right recursion.
pitch_grammar = """
$S -> $phrase0
$phrase0 -> 55 $phrase0 | 66 $phrase0 | 77 $phrase0 | 55 | 66 | 77
"""
```

### 3. Updated Documentation

**File**: `/Users/jaakkoprattala/Documents/koodii/savellysKone/README_GUI.md`

Added comprehensive grammar rules documentation in the "Grammar System" section, including:
- Explanation of left recursion restriction
- Valid and invalid grammar examples
- Clear error message documentation

### 4. Created Test Files

**Files**:
- `test_recursion_check.py` - Unit tests for recursion detection
- `test_grammar_validation.py` - Grammar validation tests
- `test_sk3_recursion.py` - Integration tests with savellysKone3
- `RECURSION_TEST_INSTRUCTIONS.txt` - Manual testing instructions for GUI

## What This Prevents

### Direct Left Recursion (Now Prevented)

These grammar rules will now be **rejected** with a clear error message:

1. **Self-reference**: `$S -> $S`
2. **Self-reference with other symbols**: `$S -> $S $A`
3. **Self-reference in alternatives**: `$S -> 60 | $S`
4. **Multiple rules with recursion**: `$B -> $B 64`

### What Still Works

These grammar patterns remain **valid**:

1. **Right recursion**: `$S -> $A $S | $A`
2. **Simple expansion**: `$S -> 60 62 64 65`
3. **Multiple alternatives**: `$S -> $A | $B`
4. **Nested non-terminals**: `$S -> $A $B $C`

## Error Messages

When a user enters invalid grammar, they will see:

```
Invalid parameter value: Infinite recursion detected: '$S -> $S'. 
The non-terminal '$S' cannot appear as the first symbol on the right side of its own rule.
```

This error is caught by the GUI's exception handler in `generate_single_list()` and displayed in a messagebox.

## Testing

### Unit Tests Pass

Running `test_recursion_check.py`:
```
Test 1: Valid grammar
✓ Valid grammar accepted

Test 2: Direct left recursion - $S -> $S
✓ Correctly rejected

Test 3: Direct left recursion - $S -> $S $A
✓ Correctly rejected

Test 4: Valid recursion - $S -> $A $S
✓ Valid (non-left) recursion accepted

Test 5: Alternative with left recursion - $S -> 60 | $S
✓ Correctly rejected

Test 6: Multiple rules, one with left recursion
✓ Correctly rejected

✓ All tests completed
```

### GUI Integration

The error handling in `savellysKone3_gui.py` already catches `ValueError` exceptions:

```python
def generate_single_list(self, grammar_type):
    try:
        # ... grammar generation code ...
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid parameter value: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating {grammar_type} list: {str(e)}")
```

## Benefits

1. **Prevents Infinite Loops**: Users cannot accidentally create grammars that would run forever
2. **Clear Error Messages**: When invalid grammar is detected, users get helpful feedback
3. **Early Detection**: Errors are caught at parse time, not generation time
4. **Educational**: Error messages teach users about proper grammar construction
5. **No Breaking Changes**: All valid grammars continue to work as before

## Technical Details

### Detection Algorithm

The check examines each grammar rule alternative:
1. Split the right-hand side into tokens (space-separated)
2. Get the first token
3. Compare with the left-hand side non-terminal
4. If they match, raise `ValueError`

This detects **direct left recursion** (the most common infinite recursion case).

### Limitations

This check does **not** detect:
- **Indirect left recursion**: `$A -> $B`, `$B -> $A`
- **Hidden left recursion**: `$A -> $B`, `$B -> $C`, `$C -> $A`

These are more complex to detect and less common in practice. The current implementation handles the most critical cases.

## Future Enhancements (Optional)

If needed, could add:
1. Detection of indirect/mutual recursion
2. Detection of non-terminating grammars
3. Grammar simplification/optimization
4. Maximum recursion depth limits

## Files Modified

1. `gengramparser2.py` - Added recursion check
2. `testRecursionInGrammar.py` - Fixed invalid grammar
3. `README_GUI.md` - Added grammar rules documentation

## Files Created

1. `test_recursion_check.py` - Unit tests
2. `test_grammar_validation.py` - Grammar validation tests
3. `test_sk3_recursion.py` - Integration tests
4. `RECURSION_TEST_INSTRUCTIONS.txt` - Manual test instructions

## Date

November 10, 2025
