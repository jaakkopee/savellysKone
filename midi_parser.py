"""
MIDI Parser module for validating note timing in generated MIDI sequences.
This module provides validation functions to ensure notes have valid timing
(i.e., notes start before they end).
"""


def validate_note_timing(note):
    """
    Validate that a single note has valid timing.
    
    Args:
        note: A Note object with onset and duration attributes
        
    Returns:
        bool: True if the note is valid (duration > 0), False otherwise
    """
    return note.duration > 0


def validate_song_timing(song):
    """
    Validate that all notes in a song have valid timing.
    
    Args:
        song: A Song object containing bar_list with notes
        
    Returns:
        tuple: (is_valid, message) where is_valid is bool and message is str
    """
    if not hasattr(song, 'bar_list') or not song.bar_list:
        return False, "No bars found in song"
    
    invalid_notes = []
    total_notes = 0
    
    for bar_idx, bar in enumerate(song.bar_list):
        if not hasattr(bar, 'note_list'):
            continue
            
        for note_idx, note in enumerate(bar.note_list):
            total_notes += 1
            if not validate_note_timing(note):
                invalid_notes.append((bar_idx, note_idx, note.onset, note.duration))
    
    if invalid_notes:
        error_msg = f"Found {len(invalid_notes)} invalid notes out of {total_notes}:\n"
        for bar_idx, note_idx, onset, duration in invalid_notes[:5]:  # Show first 5
            error_msg += f"  Bar {bar_idx}, Note {note_idx}: onset={onset:.3f}, duration={duration:.3f}\n"
        if len(invalid_notes) > 5:
            error_msg += f"  ... and {len(invalid_notes) - 5} more"
        return False, error_msg
    
    return True, f"All {total_notes} notes are valid"


def get_validation_status(song):
    """
    Get a simple validation status for display.
    
    Args:
        song: A Song object containing bar_list with notes
        
    Returns:
        str: "Valid" if all notes are valid, "Invalid" otherwise
    """
    is_valid, _ = validate_song_timing(song)
    return "Valid" if is_valid else "Invalid"
