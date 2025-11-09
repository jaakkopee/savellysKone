"""
Example usage of the MIDI parser module.

This script demonstrates how to use the midi_parser module to validate
MIDI files. It creates simple test files using mido to demonstrate validation.
"""

from midi_parser import MIDIParser, validate_midi_file
import mido


def create_simple_midi_file(filepath, notes):
    """
    Helper function to create a MIDI file with specified notes.
    
    Args:
        filepath: Path where to save the MIDI file
        notes: List of (note, start_time, duration) tuples
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Sort notes by start time
    sorted_notes = sorted(notes, key=lambda x: x[1])
    
    # Convert to MIDI messages with delta times
    events = []
    for note, start, duration in sorted_notes:
        events.append((start, 'note_on', note))
        events.append((start + duration, 'note_off', note))
    
    events.sort(key=lambda x: x[0])
    
    # Convert to delta times
    current_time = 0
    for time, msg_type, note in events:
        delta = int((time - current_time) * 480)  # Convert to ticks
        if msg_type == 'note_on':
            track.append(mido.Message('note_on', note=note, velocity=64, time=delta))
        else:
            track.append(mido.Message('note_off', note=note, velocity=0, time=delta))
        current_time = time
    
    mid.save(filepath)


def example_basic_validation():
    """
    Example 1: Basic validation of a MIDI file
    """
    print("\n" + "="*70)
    print("Example 1: Basic MIDI File Validation")
    print("="*70)
    
    # Create a simple MIDI file with a C major chord
    notes = [
        (60, 0.0, 1.0),   # C (middle C)
        (64, 0.0, 1.0),   # E
        (67, 0.0, 1.0),   # G
        (72, 1.0, 1.0),   # C (octave higher)
    ]
    
    create_simple_midi_file("example_song.mid", notes)
    print("Generated MIDI file: example_song.mid")
    
    # Validate the generated file
    is_valid = validate_midi_file("example_song.mid", verbose=True)
    
    if is_valid:
        print("\n✓ The MIDI file is valid!")
    else:
        print("\n✗ The MIDI file has validation errors!")
    
    return is_valid


def example_detailed_validation():
    """
    Example 2: Detailed validation with programmatic access to errors
    """
    print("\n" + "="*70)
    print("Example 2: Detailed MIDI File Validation")
    print("="*70)
    
    # Create a melodic sequence
    notes = [
        (60, 0.0, 0.5),   # C
        (62, 0.5, 0.5),   # D
        (64, 1.0, 0.5),   # E
        (65, 1.5, 0.5),   # F
        (67, 2.0, 0.5),   # G
        (69, 2.5, 0.5),   # A
        (71, 3.0, 0.5),   # B
        (72, 3.5, 1.0),   # C
    ]
    
    create_simple_midi_file("detailed_example.mid", notes)
    print("Generated MIDI file: detailed_example.mid")
    
    # Create parser and validate
    parser = MIDIParser("detailed_example.mid")
    
    # Parse the file
    events = parser.parse()
    print(f"\nFound {len(events)} note events in the MIDI file")
    
    # Validate
    is_valid, errors = parser.validate()
    
    if is_valid:
        print("\n✓ Validation successful - no errors found!")
    else:
        print(f"\n✗ Validation failed - found {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error.error_type}: {error.message}")
    
    # Show detailed note information
    print("\nNote events (first 10):")
    for i, event in enumerate(events[:10]):
        print(f"  {i+1}. {event.event_type:8s} | Note: {event.note:3d} | "
              f"Channel: {event.channel} | Time: {event.time:6.2f}")
    
    return is_valid


def example_command_line_usage():
    """
    Example 3: Command-line usage demonstration
    """
    print("\n" + "="*70)
    print("Example 3: Command-Line Usage")
    print("="*70)
    
    print("\nTo use the MIDI parser from the command line:")
    print("\n  python3 midi_parser.py <midi_file_path>")
    print("\nExample:")
    print("  python3 midi_parser.py example_song.mid")
    print("\nThe script will:")
    print("  - Parse the MIDI file")
    print("  - Validate note timing")
    print("  - Print a detailed report")
    print("  - Exit with code 0 if valid, 1 if invalid")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("MIDI Parser Usage Examples")
    print("="*70)
    
    # Run examples
    try:
        example_basic_validation()
        example_detailed_validation()
        example_command_line_usage()
        
        print("\n" + "="*70)
        print("Examples completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
