"""
Grammar Validator for Generative Grammars
Supports BNF-like syntax with $ prefix for non-terminals
"""

import re
from typing import Dict, List, Set, Tuple


class GrammarValidationError(Exception):
    """Exception raised for grammar validation errors"""
    pass


class GrammarValidator:
    """
    Validates generative grammars in BNF-like format.
    
    Expected format:
        $NonTerminal -> symbol1 symbol2 ... | alternative1 alternative2
        
    Rules:
        - Non-terminals must start with $
        - Each production must have exactly one ->
        - LHS must be a single non-terminal
        - No direct left recursion (A -> A ...)
        - All non-terminals on RHS must be defined
        - Start symbol $S should exist
    """
    
    def __init__(self):
        self.rules: Dict[str, List[List[str]]] = {}  # {lhs: [[rhs1], [rhs2], ...]}
        self.non_terminals: Set[str] = set()
        self.terminals: Set[str] = set()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def parse_and_validate(self, grammar_text: str) -> Tuple[bool, List[str], List[str]]:
        """
        Parse and validate grammar text.
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.reset()
        lines = grammar_text.strip().split('\n')
        
        # Phase 1: Parse rules
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):  # Skip empty lines and comments
                continue
                
            try:
                self._parse_rule(line, line_num)
            except GrammarValidationError as e:
                self.errors.append(f"Line {line_num}: {str(e)}")
        
        # Phase 2: Semantic validation (only if parsing succeeded)
        if not self.errors:
            self._validate_semantics()
        
        return (len(self.errors) == 0, self.errors, self.warnings)
    
    def reset(self):
        """Reset validator state"""
        self.rules.clear()
        self.non_terminals.clear()
        self.terminals.clear()
        self.errors.clear()
        self.warnings.clear()
    
    def _parse_rule(self, line: str, line_num: int):
        """Parse a single grammar rule"""
        # Check for -> separator
        if '->' not in line:
            raise GrammarValidationError("Missing '->' separator in production rule")
        
        parts = line.split('->')
        if len(parts) != 2:
            raise GrammarValidationError("Multiple '->' found in production rule")
        
        lhs = parts[0].strip()
        rhs = parts[1].strip()
        
        # Validate LHS
        if not lhs:
            raise GrammarValidationError("Left-hand side is empty")
        
        if not lhs.startswith('$'):
            raise GrammarValidationError(f"Non-terminal '{lhs}' must start with '$'")
        
        if ' ' in lhs:
            raise GrammarValidationError(f"Left-hand side must be a single non-terminal, found: '{lhs}'")
        
        if not re.match(r'^\$[a-zA-Z_][a-zA-Z0-9_]*$', lhs):
            raise GrammarValidationError(f"Invalid non-terminal name: '{lhs}'. Must be $identifier")
        
        self.non_terminals.add(lhs)
        
        # Parse RHS alternatives (separated by |)
        alternatives = [alt.strip() for alt in rhs.split('|')]
        
        for alt in alternatives:
            if not alt:
                raise GrammarValidationError("Empty alternative found")
            
            # Parse symbols in alternative
            symbols = alt.split()
            
            # Check for direct left recursion
            if symbols and symbols[0] == lhs:
                raise GrammarValidationError(
                    f"Direct left recursion: '{lhs}' cannot be first symbol in its own production '{alt}'"
                )
            
            # Categorize symbols
            for symbol in symbols:
                if symbol.startswith('$'):
                    # Validate non-terminal format
                    if not re.match(r'^\$[a-zA-Z_][a-zA-Z0-9_]*$', symbol):
                        raise GrammarValidationError(f"Invalid non-terminal: '{symbol}'")
                else:
                    self.terminals.add(symbol)
            
            # Add to rules
            if lhs not in self.rules:
                self.rules[lhs] = []
            self.rules[lhs].append(symbols)
    
    def _validate_semantics(self):
        """Perform semantic validation checks"""
        # Check for start symbol
        if '$S' not in self.non_terminals:
            self.errors.append("Missing start symbol '$S'")
        
        # Check for undefined non-terminals
        for lhs, alternatives in self.rules.items():
            for symbols in alternatives:
                for symbol in symbols:
                    if symbol.startswith('$') and symbol not in self.rules:
                        self.errors.append(
                            f"Undefined non-terminal '{symbol}' used in production for '{lhs}'"
                        )
        
        # Check for unreachable non-terminals (not reachable from $S)
        if '$S' in self.rules:
            reachable = self._find_reachable('$S')
            unreachable = self.non_terminals - reachable
            for nt in unreachable:
                self.warnings.append(f"Non-terminal '{nt}' is unreachable from start symbol '$S'")
        
        # Check for non-productive non-terminals (can't derive any terminals)
        non_productive = self._find_non_productive()
        for nt in non_productive:
            self.warnings.append(
                f"Non-terminal '{nt}' is non-productive (cannot derive terminal strings)"
            )
        
        # Detect potential indirect left recursion (only left recursion is problematic)
        left_recursive_cycles = self._detect_left_recursive_cycles()
        if left_recursive_cycles:
            for cycle in left_recursive_cycles:
                cycle_str = ' -> '.join(cycle + [cycle[0]])
                self.warnings.append(f"Potential indirect left recursion detected: {cycle_str}")
    
    def _find_reachable(self, start: str) -> Set[str]:
        """Find all non-terminals reachable from start symbol"""
        reachable = {start}
        changed = True
        
        while changed:
            changed = False
            for nt in list(reachable):
                if nt in self.rules:
                    for symbols in self.rules[nt]:
                        for symbol in symbols:
                            if symbol.startswith('$') and symbol not in reachable:
                                reachable.add(symbol)
                                changed = True
        
        return reachable
    
    def _find_non_productive(self) -> Set[str]:
        """Find non-terminals that cannot derive any terminal strings"""
        productive = set()
        changed = True
        
        # A non-terminal is productive if it has a production with only terminals
        # or only productive non-terminals
        while changed:
            changed = False
            for lhs, alternatives in self.rules.items():
                if lhs not in productive:
                    for symbols in alternatives:
                        if all(not s.startswith('$') or s in productive for s in symbols):
                            productive.add(lhs)
                            changed = True
                            break
        
        return self.non_terminals - productive
    
    def _detect_left_recursive_cycles(self) -> List[List[str]]:
        """
        Detect cycles that involve left recursion (problematic).
        Only reports cycles where the non-terminal appears as the FIRST symbol.
        Right recursion (non-terminal at end) is valid and not reported.
        """
        cycles = []
        
        def dfs(current: str, path: List[str], visited: Set[str]):
            if current in path:
                # Found a cycle - check if it's left-recursive
                cycle_start = path.index(current)
                cycle = path[cycle_start:]
                
                # Only report if not already found
                if cycle not in cycles:
                    cycles.append(cycle)
                return
            
            if current in visited or current not in self.rules:
                return
            
            path.append(current)
            
            # ONLY follow FIRST symbols in productions (left recursion check)
            # Right recursion (symbol appears later) is fine and won't be followed
            for symbols in self.rules[current]:
                if symbols and symbols[0].startswith('$'):
                    dfs(symbols[0], path.copy(), visited)
            
            visited.add(current)
        
        for nt in self.non_terminals:
            dfs(nt, [], set())
        
        return cycles
    
    def format_errors_and_warnings(self) -> str:
        """Format validation results as a readable string"""
        output = []
        
        if self.errors:
            output.append("=== ERRORS ===")
            for error in self.errors:
                output.append(f"  ✗ {error}")
            output.append("")
        
        if self.warnings:
            output.append("=== WARNINGS ===")
            for warning in self.warnings:
                output.append(f"  ⚠ {warning}")
            output.append("")
        
        if not self.errors and not self.warnings:
            output.append("✓ Grammar is valid!")
            output.append(f"  Non-terminals: {len(self.non_terminals)}")
            output.append(f"  Terminals: {len(self.terminals)}")
            output.append(f"  Productions: {sum(len(alts) for alts in self.rules.values())}")
        
        return "\n".join(output)


def validate_grammar(grammar_text: str) -> Tuple[bool, str]:
    """
    Convenience function to validate grammar text.
    
    Args:
        grammar_text: Grammar in BNF-like format
        
    Returns:
        (is_valid, formatted_message)
    """
    validator = GrammarValidator()
    is_valid, errors, warnings = validator.parse_and_validate(grammar_text)
    message = validator.format_errors_and_warnings()
    return is_valid, message


if __name__ == "__main__":
    # Test with example grammars
    
    # Valid grammar
    valid_grammar = """
    $S -> $phrase01 $phrase02
    $phrase01 -> 60 62 64 65
    $phrase02 -> 67 69 71 72
    """
    
    print("Testing valid grammar:")
    is_valid, msg = validate_grammar(valid_grammar)
    print(msg)
    print()
    
    # Grammar with left recursion
    left_recursive = """
    $S -> $S 60 | 62
    """
    
    print("Testing left-recursive grammar:")
    is_valid, msg = validate_grammar(left_recursive)
    print(msg)
    print()
    
    # Grammar with undefined non-terminal
    undefined_nt = """
    $S -> $phrase01 $phrase02
    $phrase01 -> 60 62
    """
    
    print("Testing grammar with undefined non-terminal:")
    is_valid, msg = validate_grammar(undefined_nt)
    print(msg)
